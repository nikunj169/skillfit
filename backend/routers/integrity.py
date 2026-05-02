from fastapi import APIRouter

from backend.services.integrity.audio_validator import validate_audio_quality
from backend.services.integrity.duplicate_detector import detect_duplicate
from backend.services.integrity.face_validator import validate_face_presence

router = APIRouter(prefix="/integrity", tags=["Integrity"])


@router.get("/validate-face")
def validate_face():
    return validate_face_presence()


@router.get("/validate-audio")
def validate_audio():
    return validate_audio_quality()


@router.get("/check-duplicate")
def check_duplicate():
    return detect_duplicate()
