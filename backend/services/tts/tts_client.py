def generate_prompt_audio(question: str, language: str) -> dict:
    return {
        "question": question,
        "language": language,
        "audio_url": f"/static/prompts/{language}/question.mp3",
    }
