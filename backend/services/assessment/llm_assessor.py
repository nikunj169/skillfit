import json
from openai import OpenAI

from backend.config import get_settings
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
    word_count = len(transcript.split())
    if word_count < 3:
        return {
            "relevance_score": 0.0,
            "completeness_score": 0.0,
            "clarity_score": 0.0,
            "skill_confidence_score": 0.0,
            "llm_notes": "Transcript too short to evaluate.",
        }

    settings = get_settings()
    if not settings.openai_api_key:
        clarity = min(10.0, round(4.5 + word_count / 8, 2))
        confidence = min(10.0, round(4.0 + word_count / 10, 2))
        relevance = min(10.0, round(4.8 + word_count / 9, 2))
        completeness = min(10.0, round(4.2 + word_count / 11, 2))

        return {
            "relevance_score": relevance,
            "completeness_score": completeness,
            "clarity_score": clarity,
            "skill_confidence_score": confidence,
            "llm_notes": "Good attempt, could use more specific examples. (Mock response)",
        }

    try:
        client = OpenAI(api_key=settings.openai_api_key)
        
        system_prompt = (
            f"You are an expert technical interviewer assessing a candidate for the role of '{role_applied}'.\n"
            f"The candidate is speaking in '{language}'.\n"
            "Evaluate their answer based on relevance, completeness, clarity, and confidence.\n"
            "Respond in JSON format with exactly the following fields:\n"
            "- 'relevance_score' (float 0.0 to 10.0)\n"
            "- 'completeness_score' (float 0.0 to 10.0)\n"
            "- 'clarity_score' (float 0.0 to 10.0)\n"
            "- 'skill_confidence_score' (float 0.0 to 10.0)\n"
            "- 'llm_notes' (short 1-2 sentence constructive feedback string)\n"
            "Important: Do not penalize for informal or dialectal speech patterns."
        )
        
        user_prompt = f"Question: {question_text}\nCandidate Answer: {transcript}"
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        
        result_json = response.choices[0].message.content
        result = json.loads(result_json)
        
        return {
            "relevance_score": float(result.get("relevance_score", 0.0)),
            "completeness_score": float(result.get("completeness_score", 0.0)),
            "clarity_score": float(result.get("clarity_score", 0.0)),
            "skill_confidence_score": float(result.get("skill_confidence_score", 0.0)),
            "llm_notes": str(result.get("llm_notes", "Evaluation complete.")),
        }
    except Exception as e:
        print(f"OpenAI Assessor Error: {e}")
        return {
            "relevance_score": 5.0,
            "completeness_score": 5.0,
            "clarity_score": 5.0,
            "skill_confidence_score": 5.0,
            "llm_notes": f"Evaluation failed due to API error: {e}",
        }
