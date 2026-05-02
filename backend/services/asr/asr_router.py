import os
from backend.services.asr.sarvam_client import transcribe_kannada_or_hindi
from backend.services.asr.whisper_client import transcribe_english


def transcribe(language: str, file_path: str | None = None) -> str:
    if language in {"hi", "kn"}:
        return transcribe_kannada_or_hindi(file_path, language)
    return transcribe_english(file_path)
