import os
from firecrawl import Firecrawl
from google import genai
from google.genai import types
from schemas import ObservationList, IdeaMatrixEvaluation, RawObservation

class IdeaEngine:
    def __init__(self):
        gemini_key = os.getenv("GEMINI_API_KEY")
        firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        
        if not gemini_key or not firecrawl_key:
            raise ValueError("Missing GEMINI_API_KEY or FIRECRAWL_API_KEY in environment")

        self.gemini_client = genai.Client(api_key=gemini_key)
        self.firecrawl = Firecrawl(api_key=firecrawl_key)

    def scrape(self, url: str) -> str:
        try:
            res = self.firecrawl.scrape(url=url, formats=['markdown'])
            return res.markdown or ""
        except Exception as e:
            print(f"Scrape error: {e}")
            return ""

    def extract_problems(self, markdown_text: str) -> list[RawObservation]:
        prompt = f"""
        Extract specific workflow bottlenecks, repeated manual steps, software limitations, 
        or awkward workarounds from this scraped content. Ignore generic complaints.
        
        Content:
        {markdown_text[:18000]}
        """
        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ObservationList,
                temperature=0.2,
            ),
        )
        parsed: ObservationList = response.parsed
        return parsed.observations

    def evaluate_idea(self, obs: RawObservation, tech_domain: str = "AI Agents & Modern Automation") -> IdeaMatrixEvaluation:
        system_instruction = f"""
        You are a ruthless product evaluator.
        1. Synthesize a solution hypothesis attacking the problem using: '{tech_domain}'.
        2. Score the hypothesis (1-5 each): Frequency, Budget/Desperation, Distribution Access, Technical Leverage, Switching Friction.
        3. Hard rules: If Budget < 3 OR Distribution < 3 OR Total < 18, verdict MUST be 'KILL'. Otherwise 'PASS'.
        """
        user_content = f"User: {obs.target_persona}\nProblem: {obs.problem_summary}\nWorkaround: {obs.current_workaround}\nUrgency: {obs.urgency_level}/5"

        response = self.gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_content,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                response_mime_type="application/json",
                response_schema=IdeaMatrixEvaluation,
                temperature=0.3,
            ),
        )
        return response.parsed
