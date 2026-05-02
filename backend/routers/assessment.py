from fastapi import APIRouter

from backend.schemas.assessment import AssessmentRequest, AssessmentResponse
from backend.services.assessment.llm_assessor import assess_transcript

router = APIRouter(prefix="/assessment", tags=["Assessment"])


@router.post("/assess", response_model=AssessmentResponse)
def assess_candidate(payload: AssessmentRequest):
    return assess_transcript(
        candidate_id=payload.candidate_id,
        transcript=payload.transcript,
        role_applied=payload.role_applied,
        language=payload.language,
    )
