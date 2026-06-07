from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from datetime import datetime
import uuid


class Verdict(str, Enum):
    TRUE = "True"
    FALSE = "False"
    MISLEADING = "Misleading"
    UNVERIFIED = "Unverified"


class ContentType(str, Enum):
    TEXT = "text"
    IMAGE = "image"
    PDF = "pdf"


class VerifyRequest(BaseModel):
    content: str = Field(..., description="Text content or claim to verify")
    content_type: ContentType = Field(default=ContentType.TEXT, description="Type of content")
    file_id: Optional[str] = Field(None, description="ID of uploaded file if any")


class Evidence(BaseModel):
    source: str = Field(..., description="Name of the source (e.g., NTA, CBSE, NCERT)")
    url: Optional[str] = Field(None, description="URL to the official source")
    snippet: str = Field(..., description="Relevant text snippet from the source")
    reliability_score: float = Field(default=0.0, ge=0.0, le=1.0)


class ClaimResult(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    original_content: str
    extracted_text: Optional[str] = None
    claim: str
    verdict: Verdict
    confidence: float = Field(ge=0.0, le=1.0)
    explanation_english: str
    explanation_hinglish: str
    evidence: List[Evidence]
    wellbeing_message: Optional[str] = None
    stress_detected: bool = False
    category: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    content_type: ContentType
    extracted_text: str
    message: str


class TrendingClaim(BaseModel):
    claim: str
    verdict: Verdict
    count: int
    first_seen: datetime
    last_seen: datetime
    category: Optional[str] = None


class TrendsResponse(BaseModel):
    trending_claims: List[TrendingClaim]
    total_claims_checked: int
    most_common_category: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
