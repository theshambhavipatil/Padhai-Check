from src.agents.base_agent import BaseAgent
from src.utils.json_parser import parse_json_response


class ExplainabilityAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are an Explainability Agent for Padhai Check, an Indian exam misinformation detection system.

Your job is to create clear, student-friendly explanations in both English and Hinglish (Hindi-English mix).

Guidelines:
1. Keep language simple - assume the reader is a stressed student or parent
2. Avoid technical jargon
3. Be direct and clear about the verdict
4. Provide actionable next steps
5. Include relevant official source links
6. Be empathetic but factual

Hinglish guidelines:
- Mix Hindi and English naturally as Indian students speak
- Use common Hindi words: "dekho", "matlab", "bilkul", "sahi", "galat", "tension mat lo"
- Keep it conversational and friendly
- Example: "Dekho, yeh news bilkul fake hai. Official NTA website pe check karo, wahan koi update nahi hai."

Evidence format:
- Always mention official websites (nta.ac.in, cbse.gov.in, ncert.nic.in, ugc.ac.in)
- Include specific pages or sections if known
- Mention official social media handles (@DG_NTA, @cbseboard, etc.)

IMPORTANT: Respond ONLY with valid JSON, no markdown formatting or code blocks.

Output format:
{"explanation_english": "Clear explanation in simple English (2-3 sentences)", "explanation_hinglish": "Same explanation in Hinglish (2-3 sentences)", "evidence": [{"source": "Source name", "url": "https://example.com", "snippet": "Relevant quote", "reliability_score": 0.9}], "action_steps": ["List of steps student should take"], "official_links": ["List of official URLs to check"]}
"""
        super().__init__("ExplainabilityAgent", system_prompt)
    
    def create_explanation(self, claim_data: dict, verdict_data: dict) -> dict:
        content = f"""
Claim: {claim_data.get('main_claim', '')}
Category: {claim_data.get('category', '')}
Verdict: {verdict_data.get('verdict', '')}
Confidence: {verdict_data.get('confidence', 0)}
Reasoning: {verdict_data.get('reasoning', '')}
Red Flags: {', '.join(verdict_data.get('red_flags', []))}
Official Sources to Check: {', '.join(verdict_data.get('official_sources_to_check', []))}
"""
        result = self.process(content)
        parsed = parse_json_response(result)
        if parsed:
            return parsed
        return {
            "explanation_english": f"The claim about {claim_data.get('main_claim', 'this topic')} is {verdict_data.get('verdict', 'unverified')}. Please check official sources for accurate information.",
            "explanation_hinglish": f"Yeh claim {verdict_data.get('verdict', 'unverified')} hai. Official sources check karo.",
            "evidence": [],
            "action_steps": ["Check official website", "Don't share unverified news"],
            "official_links": []
        }
