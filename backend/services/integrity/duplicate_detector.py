import math

from sqlalchemy.orm import Session

from backend.models.embedding import CandidateEmbedding

SIMILARITY_THRESHOLD = 0.85


def _cosine_similarity(vec_a: list[float], vec_b: list[float]) -> float:
    if len(vec_a) != len(vec_b) or not vec_a:
        return 0.0
    dot = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)


def detect_duplicate(candidate_id: int, embedding: list[float] | None = None, db: Session | None = None) -> dict:
    if not embedding or not db:
        return {"duplicate_detected": False, "similarity_score": 0.0}

    existing = (
        db.query(CandidateEmbedding)
        .filter(CandidateEmbedding.candidate_id != candidate_id)
        .all()
    )

    best_score = 0.0
    matched_candidate_id = None

    for record in existing:
        score = _cosine_similarity(embedding, record.vector)
        if score > best_score:
            best_score = score
            matched_candidate_id = record.candidate_id

    return {
        "duplicate_detected": best_score >= SIMILARITY_THRESHOLD,
        "similarity_score": round(best_score, 4),
        "matched_candidate_id": matched_candidate_id if best_score >= SIMILARITY_THRESHOLD else None,
    }
