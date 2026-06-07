from src.agents.base_agent import BaseAgent
from src.utils.json_parser import parse_json_response


class IngestionAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are an Ingestion Agent for Padhai Check, an Indian exam misinformation detection system.

Your job is to:
1. Clean and normalize the input text (remove extra spaces, fix encoding issues)
2. Identify the language (Hindi, English, Hinglish, or mixed)
3. Translate any Hindi content to English while preserving the original meaning
4. Extract key entities (exam names like JEE, NEET, CBSE, NCERT, NTA, UGC, etc.)
5. Identify dates, deadlines, or time references
6. Summarize the main topic in 1-2 sentences

IMPORTANT: Respond ONLY with valid JSON, no markdown formatting or code blocks.

Output format:
{"cleaned_text": "the cleaned and normalized text", "language": "English/Hindi/Hinglish", "translated_text": "English translation if original was Hindi/Hinglish", "entities": ["list", "of", "key", "entities"], "dates_mentioned": ["any dates or deadlines mentioned"], "summary": "1-2 sentence summary of the content"}

Focus on Indian education-related content: board exams (CBSE, ICSE), competitive exams (JEE, NEET, UPSC, SSC), universities (DU, JNU, IITs, NITs), and regulatory bodies (UGC, AICTE, NTA, NCERT).
"""
        super().__init__("IngestionAgent", system_prompt)
    
    def prepare_text(self, raw_text: str) -> dict:
        result = self.process(raw_text)
        parsed = parse_json_response(result)
        if parsed:
            return parsed
        return {
            "cleaned_text": raw_text,
            "language": "Unknown",
            "translated_text": raw_text,
            "entities": [],
            "dates_mentioned": [],
            "summary": raw_text[:200]
        }
