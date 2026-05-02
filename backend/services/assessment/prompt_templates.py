def build_assessment_prompt(role_applied: str, language: str) -> str:
    return (
        f"Assess the candidate for the role '{role_applied}' in language '{language}' "
        "for clarity, confidence, and relevance."
    )
