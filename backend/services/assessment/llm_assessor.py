from backend.schemas.assessment import AssessmentResponse
from backend.services.assessment.prompt_templates import build_assessment_prompt
from backend.services.assessment.score_aggregator import aggregate_scores


def assess_transcript(candidate_id: int, transcript: str, role_applied: str, language: str) -> AssessmentResponse:
    build_assessment_prompt(role_applied, language)

    word_count = len(transcript.split())
    clarity = min(10.0, round(4.5 + word_count / 8, 2))
    confidence = min(10.0, round(4.0 + word_count / 10, 2))
    relevance = min(10.0, round(4.8 + word_count / 9, 2))
    overall = aggregate_scores(clarity, confidence, relevance)

    return AssessmentResponse(
        candidate_id=candidate_id,
        clarity_score=clarity,
        confidence_score=confidence,
        relevance_score=relevance,
        overall_score=overall,
        strengths=["Structured response", "Good role alignment"],
        improvement_areas=["Add more concrete examples", "Quantify past outcomes"],
    )


def assess_question_response(transcript: str, question_text: str, role_applied: str, language: str) -> dict:
    build_assessment_prompt(role_applied, language)
    word_count = len(transcript.split())
    if word_count < 3:
        return {
            "relevance_score": 0.0,
            "completeness_score": 0.0,
            "clarity_score": 0.0,
            "skill_confidence_score": 0.0,
            "llm_notes": "Transcript too short to evaluate.",
        }

    clarity = min(10.0, round(4.5 + word_count / 8, 2))
    confidence = min(10.0, round(4.0 + word_count / 10, 2))
    relevance = min(10.0, round(4.8 + word_count / 9, 2))
    completeness = min(10.0, round(4.2 + word_count / 11, 2))

    return {
        "relevance_score": relevance,
        "completeness_score": completeness,
        "clarity_score": clarity,
        "skill_confidence_score": confidence,
        "llm_notes": "Good attempt, could use more specific examples.",
    }
