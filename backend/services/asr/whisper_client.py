import httpx
from backend.config import get_settings

def transcribe_english(file_path: str | None) -> str:
    mock_response = "I have hands-on experience in troubleshooting and customer support."
    if not file_path:
        return mock_response
        
    settings = get_settings()
    if not settings.openai_api_key:
        return mock_response
        
    try:
        with open(file_path, "rb") as f:
            response = httpx.post(
                "https://api.openai.com/v1/audio/transcriptions",
                headers={"Authorization": f"Bearer {settings.openai_api_key}"},
                files={"file": (file_path, f, "audio/webm")},
                data={"model": "whisper-1", "language": "en"}
            )
            response.raise_for_status()
            return response.json().get("text", mock_response)
    except Exception as e:
        print(f"Whisper ASR error: {e}")
        return mock_response
