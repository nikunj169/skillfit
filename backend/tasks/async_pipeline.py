from backend.db.session import SessionLocal
from backend.models.assessment import Assessment
from backend.models.candidate import Candidate
from backend.models.session import InterviewSession
from backend.services.assessment.llm_assessor import assess_transcript
from backend.services.classification.fitment_classifier import classify_candidate


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

        assessment = assess_transcript(candidate.id, session.transcript, role_applied, language)
        classification = classify_candidate(candidate.id, assessment.overall_score, [])

        db.add(
            Assessment(
                candidate_id=candidate.id,
                clarity_score=assessment.clarity_score,
                confidence_score=assessment.confidence_score,
                relevance_score=assessment.relevance_score,
                overall_score=assessment.overall_score,
                strengths=assessment.strengths,
                improvement_areas=assessment.improvement_areas,
            )
        )

        session.status = "COMPLETED"
        session.completed = True
        candidate.fitment_label = classification.fitment_label
        candidate.overall_score = assessment.overall_score
        candidate.confidence_score = classification.confidence_score
        candidate.status = "shortlisted" if classification.fitment_label == "JOB_READY" else "manual_review"
        db.add(session)
        db.add(candidate)
        db.commit()

        return {
            "status": "completed",
            "assessment": assessment.model_dump(),
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
