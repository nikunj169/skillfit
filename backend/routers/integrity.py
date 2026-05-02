from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.dependencies import get_db
from backend.services.integrity.audio_validator import validate_audio_quality
from backend.services.integrity.duplicate_detector import detect_duplicate
from backend.services.integrity.face_validator import validate_face_presence

router = APIRouter(prefix="/integrity", tags=["Integrity"])


@router.get("/validate-face")
def validate_face(video_path: str = Query("", description="Path to the video file")):
    if not video_path:
        return {"passed": False, "error": "video_path query parameter is required"}
    return validate_face_presence(video_path)


@router.get("/validate-audio")
def validate_audio(video_path: str = Query("", description="Path to the video file")):
    if not video_path:
        return {"passed": False, "error": "video_path query parameter is required"}
    return validate_audio_quality(video_path)


@router.get("/check-duplicate")
def check_duplicate(candidate_id: int = Query(0, description="Candidate ID to check"), db: Session = Depends(get_db)):
    if candidate_id == 0:
        return {"duplicate_detected": False, "error": "candidate_id query parameter is required"}
    return detect_duplicate(candidate_id, db=db)

