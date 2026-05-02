from sqlalchemy.orm import Session

from backend.models.question import Question

QUESTION_BANK = {
    ("electrician", "en"): [
        "Tell us about a recent electrical installation or repair you handled.",
        "How do you stay safe while working with live systems or power tools?",
        "What steps do you follow when diagnosing a wiring fault?",
    ],
    ("electrician", "hi"): [
        "Haal hi mein aapne kis electrical kaam ya repair par kaam kiya tha?",
        "Live systems ya power tools ke saath kaam karte waqt aap suraksha kaise sunishchit karte hain?",
        "Wiring fault diagnose karne ke liye aap kaun se steps follow karte hain?",
    ],
    ("electrician", "kn"): [
        "ಇತ್ತೀಚೆಗೆ ನೀವು ಮಾಡಿದ ವಿದ್ಯುತ್ ಅಳವಡಿಕೆ ಅಥವಾ ದುರಸ್ತಿ ಕೆಲಸದ ಬಗ್ಗೆ ಹೇಳಿ.",
        "ಲೈವ್ ಸಿಸ್ಟಮ್ ಅಥವಾ ಪವರ್ ಟೂಲ್‌ಗಳೊಂದಿಗೆ ಕೆಲಸ ಮಾಡುವಾಗ ಸುರಕ್ಷತೆಯನ್ನು ನೀವು ಹೇಗೆ ಕಾಪಾಡುತ್ತೀರಿ?",
        "ವೈರಿಂಗ್ ದೋಷವನ್ನು ಪತ್ತೆಹಚ್ಚಲು ನೀವು ಯಾವ ಕ್ರಮಗಳನ್ನು ಅನುಸರಿಸುತ್ತೀರಿ?",
    ],
    ("delivery_associate", "en"): [
        "Tell us about a time you handled multiple deliveries under time pressure.",
        "How do you deal with an incorrect address or an unavailable customer?",
        "What checks do you make before completing a delivery handoff?",
    ],
    ("delivery_associate", "hi"): [
        "Batayein jab aapne time pressure mein multiple deliveries handle ki thi.",
        "Galat address ya customer unavailable hone par aap kya karte hain?",
        "Delivery handoff complete karne se pehle aap kaun se checks karte hain?",
    ],
    ("delivery_associate", "kn"): [
        "ಸಮಯದ ಒತ್ತಡದಲ್ಲಿ ಅನೇಕ ಡೆಲಿವರಿಗಳನ್ನು ನಿರ್ವಹಿಸಿದ ಸಂದರ್ಭವನ್ನು ವಿವರಿಸಿ.",
        "ತಪ್ಪಾದ ವಿಳಾಸ ಅಥವಾ ಲಭ್ಯವಿಲ್ಲದ ಗ್ರಾಹಕರ ಪರಿಸ್ಥಿತಿಯನ್ನು ನೀವು ಹೇಗೆ ನಿಭಾಯಿಸುತ್ತೀರಿ?",
        "ಡೆಲಿವರಿ ಹಸ್ತಾಂತರಿಸುವ ಮೊದಲು ನೀವು ಯಾವ ಪರಿಶೀಲನೆಗಳನ್ನು ಮಾಡುತ್ತೀರಿ?",
    ],
}


def normalize_role(role: str) -> str:
    return role.strip().lower().replace(" ", "_")


def get_fallback_questions(role: str, language: str) -> list[dict]:
    normalized_role = normalize_role(role)
    questions = QUESTION_BANK.get((normalized_role, language)) or QUESTION_BANK.get(("electrician", language))
    return [
        {"id": f"q{index + 1}", "text": question, "order_index": index + 1}
        for index, question in enumerate(questions)
    ]


def get_questions(role: str, language: str, db: Session | None = None) -> list[dict]:
    normalized_role = normalize_role(role)

    if db is not None:
        rows = (
            db.query(Question)
            .filter_by(role=normalized_role, language=language)
            .order_by(Question.order_index.asc(), Question.id.asc())
            .all()
        )
        if rows:
            return [
                {
                    "id": f"q{row.order_index}",
                    "text": row.question_text,
                    "order_index": row.order_index,
                }
                for row in rows
            ]

    return get_fallback_questions(normalized_role, language)


def get_question_seed_rows() -> list[dict]:
    rows = []
    for (role, language), questions in QUESTION_BANK.items():
        for index, question in enumerate(questions, start=1):
            rows.append(
                {
                    "role": role,
                    "language": language,
                    "question_text": question,
                    "question_audio_url": None,
                    "order_index": index,
                }
            )
    return rows


def infer_workforce_category(role: str) -> str:
    role_lower = role.lower()
    if any(keyword in role_lower for keyword in ["electrician", "plumber", "welder", "mason"]):
        return "BLUE_COLLAR_TRADE"
    if any(keyword in role_lower for keyword in ["iti", "diploma", "lab", "technician"]):
        return "POLYTECHNIC_SKILLED"
    return "SEMI_SKILLED"
