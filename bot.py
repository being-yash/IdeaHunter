import os
import re
import telebot
from dotenv import load_dotenv
from engine import IdeaEngine

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ALLOWED_USER_ID = int(os.getenv("ALLOWED_USER_ID", "0"))

if not BOT_TOKEN:
    raise ValueError("Missing TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
engine = IdeaEngine()

def extract_url(text: str) -> str | None:
    match = re.search(r'(https?://[^\s]+)', text)
    return match.group(0) if match else None

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id != ALLOWED_USER_ID:
        return
    bot.reply_to(message, "⚡ Idea Hunter Bot Active.\n\nShare or paste any Reddit/forum link to run the extraction and scoring matrix.")

@bot.message_handler(func=lambda msg: True)
def handle_incoming_link(message):
    if message.from_user.id != ALLOWED_USER_ID:
        bot.reply_to(message, "⛔ Unauthorized. This bot is private.")
        return

    url = extract_url(message.text)
    if not url:
        bot.reply_to(message, "Please share a message containing a valid URL.")
        return

    status_msg = bot.reply_to(message, f"🔍 Scraping page and extracting pain points...\n{url}")

    try:
        markdown = engine.scrape(url)
        if not markdown:
            bot.edit_message_text("❌ Failed to scrape content from that URL.", chat_id=message.chat.id, message_id=status_msg.message_id)
            return

        bot.edit_message_text("🧠 Synthesizing ideas & running Kill Matrix...", chat_id=message.chat.id, message_id=status_msg.message_id)
        observations = engine.extract_problems(markdown)

        if not observations:
            bot.edit_message_text("ℹ️ No distinct operational pain points found on this page.", chat_id=message.chat.id, message_id=status_msg.message_id)
            return

        bot.delete_message(chat_id=message.chat.id, message_id=status_msg.message_id)

        pass_count = 0
        for obs in observations:
            result = engine.evaluate_idea(obs)
            if result.verdict == "PASS":
                pass_count += 1
                card = (
                    f"🎯 *PASSED MATRIX* ({result.total_score}/25)\n\n"
                    f"*Concept:* {result.concept_title}\n"
                    f"*User:* {result.target_user}\n"
                    f"*Problem:* {result.problem_addressed}\n"
                    f"*Hypothesis:* {result.proposed_solution_hypothesis}\n\n"
                    f"📊 *Scores:*\n"
                    f"• Frequency: {result.frequency_score}/5\n"
                    f"• Budget/Pain: {result.budget_desperation_score}/5\n"
                    f"• Distribution: {result.distribution_access_score}/5\n"
                    f"• Leverage: {result.technical_leverage_score}/5\n"
                    f"• Friction: {result.switching_friction_score}/5"
                )
                bot.send_message(message.chat.id, card, parse_mode="Markdown")

        if pass_count == 0:
            bot.send_message(message.chat.id, f"❌ Processed {len(observations)} observations, but all failed the Kill Matrix (Budget<3, Dist<3, or Total<18 rule).")

    except Exception as e:
        print(f"Error: {e}")
        bot.send_message(message.chat.id, f"⚠️ Error processing request: {str(e)}")

if __name__ == "__main__":
    print("Bot polling started...")
    bot.infinity_polling()
