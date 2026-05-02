from typing import Optional

from pydantic import BaseModel, Field


class InterviewSessionStartRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=120)
    district: str = Field(..., min_length=2, max_length=80)
    role_applied: str = Field(..., min_length=2, max_length=120)
    language: str = Field(default="en", pattern="^(en|hi|kn)$")
    phone_number: Optional[str] = Field(default=None, max_length=30)


class InterviewSessionStartResponse(BaseModel):
    candidate_id: int
    session_id: int
    session_token: str
    message: str
    first_question: str
    total_questions: int




class InterviewChunkSubmitResponse(BaseModel):
    prompt_id: str
    transcript: str
    status: str
    next_question: Optional[str] = None


class InterviewFinalizeRequest(BaseModel):
    session_token: str
    role_applied: str
    language: str = Field(default="en", pattern="^(en|hi|kn)$")


class InterviewFinalizeResponse(BaseModel):
    candidate_id: int
    session_id: int
    status: str
    message: str


class InterviewStatusResponse(BaseModel):
    candidate_id: int
    session_id: int
    status: str
    fitment_label: str
    overall_score: float
    confidence_score: float
    next_step_message: Optional[str] = None


class InterviewQuestion(BaseModel):
    id: str
    text: str
    order_index: int


class InterviewQuestionSetResponse(BaseModel):
    role: str
    language: str
    questions: list[InterviewQuestion]
