from src.agents.base_agent import BaseAgent
from src.utils.json_parser import parse_json_response


class ClaimAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are a Claim Identification Agent for Padhai Check, an Indian exam misinformation detection system.

Your job is to:
1. Identify the main claim or question being asked about Indian exams/education
2. Categorize the claim type (exam date change, paper leak, rule change, admission update, result issue, fee change, etc.)
3. Assess the urgency level (low, medium, high, critical)
4. Identify which official body this claim relates to (NTA, CBSE, NCERT, UGC, AICTE, specific university, etc.)

Common claim categories:
- EXAM_POSTPONEMENT: Claims about exam dates being changed or postponed
- PAPER_LEAK: Claims about question paper leaks
- RESULT_ISSUE: Claims about results, re-evaluation, or grace marks
- RULE_CHANGE: Claims about new rules, eligibility criteria changes
- ADMISSION_UPDATE: Claims about admission processes, cutoffs, seat allocation
- FEE_CHANGE: Claims about fee increases or reductions
- SYLLABUS_CHANGE: Claims about curriculum or syllabus modifications
- SCHOLARSHIP: Claims about scholarships or financial aid
- FAKE_CIRCULAR: Potentially fake official-looking documents
- OTHER: Any other education-related claims

IMPORTANT: Respond ONLY with valid JSON, no markdown formatting or code blocks.

Output format:
{"main_claim": "the specific claim being made in clear English", "category": "one of the categories listed above", "urgency": "low/medium/high/critical", "related_body": "NTA/CBSE/NCERT/UGC/AICTE/specific body name", "affected_exams": ["list of exams this might affect"], "requires_immediate_verification": true}
"""
        super().__init__("ClaimAgent", system_prompt)
    
    def identify_claim(self, prepared_text: dict) -> dict:
        content = f"""
Cleaned Text: {prepared_text.get('cleaned_text', '')}
Summary: {prepared_text.get('summary', '')}
Entities: {', '.join(prepared_text.get('entities', []))}
Dates Mentioned: {', '.join(prepared_text.get('dates_mentioned', []))}
"""
        result = self.process(content)
        parsed = parse_json_response(result)
        if parsed:
            return parsed
        return {
            "main_claim": prepared_text.get('summary', 'Unable to identify claim'),
            "category": "OTHER",
            "urgency": "medium",
            "related_body": "Unknown",
            "affected_exams": [],
            "requires_immediate_verification": False
        }
