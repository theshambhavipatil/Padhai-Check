from src.agents.ingestion_agent import IngestionAgent
from src.agents.claim_agent import ClaimAgent
from src.agents.factcheck_agent import FactCheckAgent
from src.agents.explainability_agent import ExplainabilityAgent
from src.agents.wellbeing_agent import WellbeingAgent
from src.agents.trend_agent import TrendAgent
from src.models.schemas import ClaimResult, Verdict, Evidence
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentOrchestrator:
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if AgentOrchestrator._initialized:
            return
        self._ingestion_agent = None
        self._claim_agent = None
        self._factcheck_agent = None
        self._explainability_agent = None
        self._wellbeing_agent = None
        self._trend_agent = None
        AgentOrchestrator._initialized = True
    
    @property
    def ingestion_agent(self):
        if self._ingestion_agent is None:
            self._ingestion_agent = IngestionAgent()
        return self._ingestion_agent
    
    @property
    def claim_agent(self):
        if self._claim_agent is None:
            self._claim_agent = ClaimAgent()
        return self._claim_agent
    
    @property
    def factcheck_agent(self):
        if self._factcheck_agent is None:
            self._factcheck_agent = FactCheckAgent()
        return self._factcheck_agent
    
    @property
    def explainability_agent(self):
        if self._explainability_agent is None:
            self._explainability_agent = ExplainabilityAgent()
        return self._explainability_agent
    
    @property
    def wellbeing_agent(self):
        if self._wellbeing_agent is None:
            self._wellbeing_agent = WellbeingAgent()
        return self._wellbeing_agent
    
    @property
    def trend_agent(self):
        if self._trend_agent is None:
            self._trend_agent = TrendAgent()
        return self._trend_agent
    
    def process_claim(self, content: str, extracted_text: Optional[str] = None) -> ClaimResult:
        text_to_process = extracted_text if extracted_text else content
        
        logger.info("Step 1: Ingestion Agent - Preparing text")
        prepared_text = self.ingestion_agent.prepare_text(text_to_process)
        
        logger.info("Step 2: Claim Agent - Identifying claim")
        claim_data = self.claim_agent.identify_claim(prepared_text)
        
        logger.info("Step 3: Fact-Check Agent - Verifying claim")
        verdict_data = self.factcheck_agent.verify_claim(claim_data, prepared_text)
        
        logger.info("Step 4: Explainability Agent - Creating explanation")
        explanation_data = self.explainability_agent.create_explanation(claim_data, verdict_data)
        
        logger.info("Step 5: Wellbeing Agent - Assessing student wellbeing")
        wellbeing_data = self.wellbeing_agent.assess_wellbeing(content, claim_data.get('category', 'OTHER'))
        
        logger.info("Step 6: Trend Agent - Analyzing trends")
        trend_data = self.trend_agent.analyze_trend(claim_data, verdict_data)
        
        verdict_map = {
            "True": Verdict.TRUE,
            "False": Verdict.FALSE,
            "Misleading": Verdict.MISLEADING,
            "Unverified": Verdict.UNVERIFIED
        }
        verdict = verdict_map.get(verdict_data.get('verdict', 'Unverified'), Verdict.UNVERIFIED)
        
        evidence_list = []
        for ev in explanation_data.get('evidence', []):
            evidence_list.append(Evidence(
                source=ev.get('source', 'Unknown'),
                url=ev.get('url'),
                snippet=ev.get('snippet', ''),
                reliability_score=ev.get('reliability_score', 0.8)
            ))
        
        result = ClaimResult(
            original_content=content,
            extracted_text=extracted_text,
            claim=claim_data.get('main_claim', text_to_process[:200]),
            verdict=verdict,
            confidence=verdict_data.get('confidence', 0.5),
            explanation_english=explanation_data.get('explanation_english', ''),
            explanation_hinglish=explanation_data.get('explanation_hinglish', ''),
            evidence=evidence_list,
            wellbeing_message=wellbeing_data.get('wellbeing_message'),
            stress_detected=wellbeing_data.get('stress_detected', False),
            category=trend_data.get('trend_category', claim_data.get('category'))
        )
        
        return result


orchestrator = AgentOrchestrator()
