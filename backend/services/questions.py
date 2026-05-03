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
    ("plumber", "en"): [
        "Describe a recent plumbing repair or installation you completed — what was the fault and how did you fix it?",
        "How do you locate a water leak that is hidden behind a wall or under the floor?",
        "What safety steps do you take when working on pressurised water supply lines or drainage pipes?",
    ],
    ("plumber", "hi"): [
        "Haal hi mein aapne jo plumbing ka kaam kiya, uske baare mein batayein — kya kharabi thi aur aapne use kaise theek kiya?",
        "Aap diwar ke peeche ya zameen ke neeche chhupe paani ke leak ko kaise dhundhte hain?",
        "Pressure water supply line ya drainage pipe par kaam karte waqt aap kaun se safety kadam uthate hain?",
    ],
    ("plumber", "kn"): [
        "ನೀವು ಇತ್ತೀಚೆಗೆ ಮಾಡಿದ ಪ್ಲಂಬಿಂಗ್ ದುರಸ್ತಿ ಅಥವಾ ಅಳವಡಿಕೆ ಬಗ್ಗೆ ಹೇಳಿ — ಸಮಸ್ಯೆ ಏನಿತ್ತು ಮತ್ತು ನೀವು ಅದನ್ನು ಹೇಗೆ ಸರಿಪಡಿಸಿದಿರಿ?",
        "ಗೋಡೆಯ ಹಿಂದೆ ಅಥವಾ ನೆಲದ ಅಡಿ ಮರೆಮಾಡಿದ ನೀರಿನ ಸೋರಿಕೆಯನ್ನು ನೀವು ಹೇಗೆ ಪತ್ತೆ ಮಾಡುತ್ತೀರಿ?",
        "ಒತ್ತಡದ ನೀರಿನ ಕೊಳವೆ ಅಥವಾ ಒಳಚರಂಡಿ ಪೈಪ್‌ಗಳ ಮೇಲೆ ಕೆಲಸ ಮಾಡುವಾಗ ನೀವು ಯಾವ ಸುರಕ್ಷತಾ ಕ್ರಮಗಳನ್ನು ತೆಗೆದುಕೊಳ್ಳುತ್ತೀರಿ?",
    ],
    ("welder", "en"): [
        "Tell us about a welding job you recently completed — what material were you working with and which technique did you use?",
        "How do you inspect a finished weld to confirm it meets quality and safety standards?",
        "What protective equipment do you wear while welding and why is each item important?",
    ],
    ("welder", "hi"): [
        "Haal hi mein aapne jo welding kaam kiya, uske baare mein batayein — aapne kaunsa material use kiya aur kaunsi technique apnayi?",
        "Aap ek poori ho chuki weld ko kaise inspect karte hain taaki woh quality aur safety standards ko poora kare?",
        "Welding ke dauran aap kaun se protective equipment pahante hain aur har ek kyon zaroori hai?",
    ],
    ("welder", "kn"): [
        "ನೀವು ಇತ್ತೀಚೆಗೆ ಮಾಡಿದ ವೆಲ್ಡಿಂಗ್ ಕೆಲಸದ ಬಗ್ಗೆ ಹೇಳಿ — ನೀವು ಯಾವ ಲೋಹ ಬಳಸಿದಿರಿ ಮತ್ತು ಯಾವ ತಂತ್ರ ಅನುಸರಿಸಿದಿರಿ?",
        "ವೆಲ್ಡ್ ಗುಣಮಟ್ಟ ಮತ್ತು ಸುರಕ್ಷತಾ ಮಾನದಂಡಗಳನ್ನು ಪೂರೈಸುತ್ತದೆ ಎಂದು ಖಚಿತಪಡಿಸಲು ನೀವು ಪೂರ್ಣಗೊಂಡ ವೆಲ್ಡ್ ಅನ್ನು ಹೇಗೆ ಪರಿಶೀಲಿಸುತ್ತೀರಿ?",
        "ವೆಲ್ಡಿಂಗ್ ಮಾಡುವಾಗ ನೀವು ಯಾವ ರಕ್ಷಣಾ ಉಪಕರಣಗಳನ್ನು ಧರಿಸುತ್ತೀರಿ ಮತ್ತು ಪ್ರತಿಯೊಂದು ಏಕೆ ಮುಖ್ಯ?",
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
