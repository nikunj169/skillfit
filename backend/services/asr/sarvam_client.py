def transcribe_kannada_or_hindi(transcript_hint: str | None, language: str) -> str:
    if transcript_hint:
        return transcript_hint
    if language == "kn":
        return "ನನಗೆ ವಿದ್ಯುತ್ ಕಾಮಗಾರಿಯಲ್ಲಿ ಅನುಭವ ಇದೆ."
    return "Mujhe field operations aur customer support ka anubhav hai."
