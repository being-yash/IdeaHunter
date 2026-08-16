# Telegram Idea Hunting Bot

End-to-end bot that scrapes any Reddit/forum link you share and runs it through a 5-point Kill Matrix.

## Setup

1.  **Get Keys:**
    *   Telegram: @BotFather -> /newbot -> save `TELEGRAM_BOT_TOKEN`
    *   Chat ID: @userinfobot -> save as `ALLOWED_USER_ID`
    *   Gemini: aistudio.google.com -> Get API Key
    *   Firecrawl: firecrawl.dev -> API Key

2.  **Local Run:**
    ```bash
    pip install -r requirements.txt
    cp .env.example .env # fill keys
    python bot.py
    ```

3.  **Deploy on Render.com (Free):**
    *   Push this folder to a private GitHub repo
    *   Render -> New + -> Background Worker
    *   Connect Repo
    *   Build Command: `pip install -r requirements.txt`
    *   Start Command: `python bot.py`
    *   Add Env Vars: GEMINI_API_KEY, FIRECRAWL_API_KEY, TELEGRAM_BOT_TOKEN, ALLOWED_USER_ID

## Usage on Android
Reddit App -> Share -> Telegram -> Select your bot. You'll get PASS cards only.

Matrix Rules: KILL if Budget<3 OR Distribution<3 OR Total<18.
