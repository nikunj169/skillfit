import httpx
from backend.config import get_settings

def transcribe_kannada_or_hindi(file_path: str | None, language: str) -> str:
    mock_response_kn = "ನನಗೆ ವಿದ್ಯುತ್ ಕಾಮಗಾರಿಯಲ್ಲಿ ಅನುಭವ ಇದೆ."
    mock_response_hi = "Mujhe field operations aur customer support ka anubhav hai."
    mock_response = mock_response_kn if language == "kn" else mock_response_hi
    
    if not file_path:
        return mock_response
        
    settings = get_settings()
    if not settings.sarvam_api_key:
        return mock_response
        
    lang_code = "hi-IN" if language == "hi" else "kn-IN"
    
    try:
        with open(file_path, "rb") as f:
            response = httpx.post(
                "https://api.sarvam.ai/speech-to-text",
                headers={"api-subscription-key": settings.sarvam_api_key},
                files={"file": (file_path, f, "audio/webm")},
                data={"language_code": lang_code, "model": "saaras:v1"}
            )
            response.raise_for_status()
            return response.json().get("transcript", mock_response)
    except Exception as e:
        print(f"Sarvam ASR error: {e}")
        return mock_response
