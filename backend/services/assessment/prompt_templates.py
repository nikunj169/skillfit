_ROLE_CONTEXTS = {
    "electrician": (
        "Focus on: knowledge of electrical installation and repair techniques, safe working "
        "practices with live systems and power tools, systematic fault diagnosis and wiring "
        "troubleshooting, and compliance with electrical safety standards."
    ),
    "delivery_associate": (
        "Focus on: time management and route efficiency under pressure, handling of incorrect "
        "addresses or unavailable customers, pre-delivery and handoff verification checks, "
        "and professional customer communication."
    ),
    "plumber": (
        "Focus on: practical plumbing repair and installation skills, methods for locating "
        "hidden leaks, safe handling of pressurised water supply and drainage systems, "
        "and correct use of plumbing tools and fittings."
    ),
    "welder": (
        "Focus on: welding techniques and material knowledge, methods for inspecting weld "
        "quality and confirming it meets safety standards, correct use of personal protective "
        "equipment (PPE), and general workplace safety awareness."
    ),
}

_DEFAULT_ROLE_CONTEXT = (
    "Focus on: relevant domain knowledge, practical problem-solving ability, "
    "and prior hands-on experience in the role."
)

_LANGUAGE_NOTES = {
    "kn": (
        "The candidate is answering in Kannada. Do not penalise code-switching between "
        "Kannada and English (Kanglish), dialectal variation across Karnataka districts, "
        "or informal register. Assess the substance and technical accuracy of the answer, "
        "not linguistic formality."
    ),
    "hi": (
        "The candidate is answering in Hindi. Do not penalise Hinglish (Hindi-English "
        "mixing), regional dialect variation, or informal register. Assess the substance "
        "and technical accuracy of the answer, not linguistic formality."
    ),
    "en": (
        "The candidate is answering in English. Do not penalise non-native pronunciation, "
        "accented English, or minor grammatical imperfection. Assess the substance and "
        "clarity of the answer."
    ),
}

_DEFAULT_LANGUAGE_NOTE = _LANGUAGE_NOTES["en"]


def get_role_context(role_applied: str) -> str:
    normalized = role_applied.strip().lower().replace(" ", "_").replace("-", "_")
    return _ROLE_CONTEXTS.get(normalized, _DEFAULT_ROLE_CONTEXT)


def get_language_note(language: str) -> str:
    return _LANGUAGE_NOTES.get(language.lower(), _DEFAULT_LANGUAGE_NOTE)
