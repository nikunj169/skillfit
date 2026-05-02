import hashlib
import os

from backend.db.session import SessionLocal
from backend.models.assessment import Assessment
from backend.models.candidate import Candidate
from backend.models.embedding import CandidateEmbedding
from backend.models.session import InterviewSession
from backend.models.question_response import QuestionResponse
from backend.services.assessment.llm_assessor import assess_question_response, assess_transcript
from backend.services.classification.fitment_classifier import classify_candidate
from backend.services.integrity.audio_validator import validate_audio_quality
from backend.services.integrity.duplicate_detector import detect_duplicate
from backend.services.integrity.face_validator import validate_face_presence


def _generate_mock_embedding(candidate_name: str, dims: int = 128) -> list[float]:
    """Generate a deterministic mock embedding from the candidate name.

    In production this would be replaced by DeepFace face-embedding
    extraction. For local/SQLite development, we derive a reproducible
    128-dim vector from a SHA-256 hash so that identical names always
    produce identical vectors (enabling duplicate-detection testing).
    """
    digest = hashlib.sha256(candidate_name.strip().lower().encode()).digest()
    # Expand the 32-byte digest to fill `dims` floats in [-1, 1]
    values: list[float] = []
    for i in range(dims):
        byte_val = digest[i % len(digest)]
        values.append((byte_val / 127.5) - 1.0)
    return values


def run_interview_pipeline(session_id: int, role_applied: str, language: str) -> dict:
    db = SessionLocal()
    try:
        session = db.query(InterviewSession).filter_by(id=session_id).first()
        if not session:
            return {"status": "missing_session"}

        candidate = db.query(Candidate).filter_by(id=session.candidate_id).first()
        if not candidate:
            session.status = "FAILED"
            db.add(session)
            db.commit()
            return {"status": "missing_candidate"}

        responses = db.query(QuestionResponse).filter_by(session_id=session.id).all()
        overall_scores = []
        clarity_scores = []
        confidence_scores = []
        relevance_scores = []

        integrity_flags = []
        ratios = []

        for response in responses:
            video_path = f"uploads/{session.session_token}_{response.question_key}.webm"
            if os.path.exists(video_path):
                face_res = validate_face_presence(video_path)
                ratios.append(face_res.get("face_presence_ratio", 1.0))
                if not face_res["passed"] and "LOW_QUALITY" not in integrity_flags:
                    integrity_flags.append("LOW_QUALITY")

                audio_res = validate_audio_quality(video_path)
                if not audio_res["passed"] and "LOW_QUALITY" not in integrity_flags:
                    integrity_flags.append("LOW_QUALITY")

            q_scores = assess_question_response(response.transcript, response.question_text, role_applied, language)
            response.relevance_score = q_scores["relevance_score"]
            response.completeness_score = q_scores["completeness_score"]
            response.clarity_score = q_scores["clarity_score"]
            response.skill_confidence_score = q_scores["skill_confidence_score"]
            response.llm_notes = q_scores["llm_notes"]
            db.add(response)

            avg_q_score = (q_scores["relevance_score"] + q_scores["completeness_score"] + q_scores["clarity_score"] + q_scores["skill_confidence_score"]) / 4
            overall_scores.append(avg_q_score)
            clarity_scores.append(q_scores["clarity_score"])
            confidence_scores.append(q_scores["skill_confidence_score"])
            relevance_scores.append(q_scores["relevance_score"])

        avg_overall = sum(overall_scores) / len(overall_scores) if overall_scores else 0.0
        avg_clarity = sum(clarity_scores) / len(clarity_scores) if clarity_scores else 0.0
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
        avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0.0
        avg_face_presence = sum(ratios) / len(ratios) if ratios else 1.0

        embedding = _generate_mock_embedding(candidate.full_name)
        db.add(CandidateEmbedding(candidate_id=candidate.id, vector=embedding))
        db.flush()

        dup_res = detect_duplicate(candidate.id, embedding=embedding, db=db)
        if dup_res.get("duplicate_detected") and "SUSPECTED_DUPLICATE" not in integrity_flags:
            integrity_flags.append("SUSPECTED_DUPLICATE")

        candidate.integrity_flags = integrity_flags
        candidate.face_presence_ratio = avg_face_presence

        db.add(
            Assessment(
                candidate_id=candidate.id,
                clarity_score=avg_clarity,
                confidence_score=avg_confidence,
                relevance_score=avg_relevance,
                overall_score=avg_overall,
                strengths=["Structured response", "Good role alignment"] if avg_overall > 5 else [],
                improvement_areas=["Add more concrete examples", "Quantify past outcomes"] if avg_overall <= 8 else [],
            )
        )
        
        classification = classify_candidate(candidate.id, avg_overall, integrity_flags)

        session.status = "COMPLETED"
        session.completed = True
        candidate.fitment_label = classification.fitment_label
        candidate.overall_score = avg_overall
        candidate.confidence_score = classification.confidence_score
        candidate.status = "shortlisted" if classification.fitment_label == "JOB_READY" else "manual_review"
        db.add(session)
        db.add(candidate)
        db.commit()

        return {
            "status": "completed",
            "classification": classification.model_dump(),
        }
    except Exception:
        session = db.query(InterviewSession).filter_by(id=session_id).first()
        if session:
            session.status = "FAILED"
            db.add(session)
            db.commit()
        raise
    finally:
        db.close()
