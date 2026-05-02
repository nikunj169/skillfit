from typing import List, Optional

from pydantic import BaseModel


class QuestionResponseItem(BaseModel):
    question_key: str
    question_text: str
    transcript: str
    order_index: int


class CandidateSummary(BaseModel):
    id: int
    full_name: str
    district: str
    role_applied: str
    language: str
    status: str
    workforce_category: str
    fitment_label: str
    overall_score: float
    confidence_score: float
    shortlisted: bool


class CandidateDetail(CandidateSummary):
    phone_number: Optional[str] = None
    integrity_flags: List[str] = []
    latest_transcript: str = ""
    latest_session_status: str = "PENDING"
    latest_assessment: Optional[dict] = None
    response_history: List[QuestionResponseItem] = []


class CandidateListResponse(BaseModel):
    items: List[CandidateSummary]
    total: int


class ShortlistRequest(BaseModel):
    shortlisted: bool


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class AdminLoginResponse(BaseModel):
    token: str
    message: str


class AdminStatsResponse(BaseModel):
    total_candidates: int
    shortlisted_candidates: int
    pending_review: int
    job_ready: int
