import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.db.base import Base
from backend.db.session import SessionLocal, engine
from backend.models.question import Question
from backend.services.questions import get_question_seed_rows


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        rows = get_question_seed_rows()
        inserted = 0
        updated = 0

        for row in rows:
            existing = (
                db.query(Question)
                .filter_by(
                    role=row["role"],
                    language=row["language"],
                    order_index=row["order_index"],
                )
                .first()
            )

            if existing:
                existing.question_text = row["question_text"]
                existing.question_audio_url = row["question_audio_url"]
                updated += 1
            else:
                db.add(Question(**row))
                inserted += 1

        db.commit()
        print(
            f"Question seed complete. Inserted: {inserted}, updated: {updated}, total definitions: {len(rows)}."
        )
    finally:
        db.close()


if __name__ == "__main__":
    main()
