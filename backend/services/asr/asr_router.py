from backend.services.asr.sarvam_client import transcribe_kannada_or_hindi
from backend.services.asr.whisper_client import transcribe_english


def transcribe(language: str, transcript_hint: str | None = None) -> str:
    if language in {"hi", "kn"}:
        return transcribe_kannada_or_hindi(transcript_hint, language)
    return transcribe_english(transcript_hint)
