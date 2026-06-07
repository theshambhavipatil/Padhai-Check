from src.agents.base_agent import BaseAgent
from src.utils.json_parser import parse_json_response


class TrendAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are a Trend Analysis Agent for Padhai Check, an Indian exam misinformation detection system.

Your job is to:
1. Categorize claims into trending topics
2. Identify if this claim is part of a known misinformation pattern
3. Suggest related claims that students should be aware of

Common misinformation patterns in Indian education:
- Exam postponement rumors (especially before JEE/NEET)
- Paper leak claims (often appear right before or after exams)
- Fake circulars with official-looking letterheads
- Result manipulation claims
- New rule/regulation fake news
- Admission scams and fake seat allotment
- Scholarship fraud messages
- Fake website links mimicking official sites

IMPORTANT: Respond ONLY with valid JSON, no markdown formatting or code blocks.

Output format:
{"trend_category": "The broader category this falls into", "is_known_pattern": true, "pattern_description": "Description of the misinformation pattern if known", "related_claims": ["List of related claims students should watch out for"], "seasonal_relevance": "Is this claim typical for current exam season?", "spread_risk": "low/medium/high"}
"""
        super().__init__("TrendAgent", system_prompt)
    
    def analyze_trend(self, claim_data: dict, verdict_data: dict) -> dict:
        content = f"""
Claim: {claim_data.get('main_claim', '')}
Category: {claim_data.get('category', '')}
Verdict: {verdict_data.get('verdict', '')}
Related Body: {claim_data.get('related_body', '')}
"""
        result = self.process(content)
        parsed = parse_json_response(result)
        if parsed:
            return parsed
        return {
            "trend_category": claim_data.get('category', 'OTHER'),
            "is_known_pattern": False,
            "pattern_description": None,
            "related_claims": [],
            "seasonal_relevance": "Unknown",
            "spread_risk": "medium"
        }
