from fastapi import APIRouter

from backend.schemas.classification import ClassificationRequest, ClassificationResponse
from backend.services.classification.fitment_classifier import classify_candidate

router = APIRouter(prefix="/classification", tags=["Classification"])


@router.post("/classify", response_model=ClassificationResponse)
def classify(payload: ClassificationRequest):
    return classify_candidate(
        candidate_id=payload.candidate_id,
        overall_score=payload.overall_score,
        integrity_flags=payload.integrity_flags,
    )
