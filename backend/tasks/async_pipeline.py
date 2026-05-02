from backend.db.session import SessionLocal
from backend.models.assessment import Assessment
from backend.models.candidate import Candidate
from backend.models.question_response import QuestionResponse
from backend.models.session import InterviewSession
from backend.services.assessment.llm_assessor import assess_question_response, assess_transcript
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

        responses = db.query(QuestionResponse).filter_by(session_id=session.id).all()
        overall_scores = []
        clarity_scores = []
        confidence_scores = []
        relevance_scores = []

        for response in responses:
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
        
        classification = classify_candidate(candidate.id, avg_overall, [])

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
