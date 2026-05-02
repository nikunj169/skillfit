from typing import List

from pydantic import BaseModel, Field


class AssessmentRequest(BaseModel):
    candidate_id: int
    transcript: str = Field(..., min_length=5)
    role_applied: str
    language: str = Field(default="en", pattern="^(en|hi|kn)$")


class AssessmentResponse(BaseModel):
    candidate_id: int
    clarity_score: float
    confidence_score: float
    relevance_score: float
    overall_score: float
    strengths: List[str]
    improvement_areas: List[str]
