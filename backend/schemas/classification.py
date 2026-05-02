from typing import List

from pydantic import BaseModel


class ClassificationRequest(BaseModel):
    candidate_id: int
    overall_score: float
    integrity_flags: List[str] = []


class ClassificationResponse(BaseModel):
    candidate_id: int
    fitment_label: str
    confidence_score: float
    reasons: List[str]
