import json

from openai import OpenAI

from backend.config import get_settings
from backend.schemas.assessment import AssessmentResponse
from backend.services.assessment.prompt_templates import get_language_note, get_role_context
from backend.services.assessment.score_aggregator import aggregate_scores


def _build_prompts(transcript: str, question_text: str, role_applied: str, language: str) -> tuple[str, str]:
    role_context = get_role_context(role_applied)
    language_note = get_language_note(language)
    system_prompt = (
        f"You are an expert technical interviewer assessing a candidate for the role of '{role_applied}'.\n"
        f"{role_context}\n"
        f"{language_note}\n"
        "Evaluate their answer based on relevance, completeness, clarity, and confidence.\n"
        "Respond with a JSON object containing exactly these fields:\n"
        "- 'relevance_score' (float 0.0 to 10.0)\n"
        "- 'completeness_score' (float 0.0 to 10.0)\n"
        "- 'clarity_score' (float 0.0 to 10.0)\n"
        "- 'skill_confidence_score' (float 0.0 to 10.0)\n"
        "- 'llm_notes' (short 1-2 sentence constructive feedback string)\n"
        "Output only the JSON object with no additional text."
    )
    user_prompt = f"Question: {question_text}\nCandidate Answer: {transcript}"
    return system_prompt, user_prompt


def _parse_scores(result: dict) -> dict:
    return {
        "relevance_score": float(result.get("relevance_score", 0.0)),
        "completeness_score": float(result.get("completeness_score", 0.0)),
        "clarity_score": float(result.get("clarity_score", 0.0)),
        "skill_confidence_score": float(result.get("skill_confidence_score", 0.0)),
        "llm_notes": str(result.get("llm_notes", "Evaluation complete.")),
    }


def _heuristic_scores(word_count: int) -> dict:
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


def _assess_with_claude(api_key: str, system_prompt: str, user_prompt: str) -> dict | None:
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=512,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )
        result = json.loads(response.content[0].text)
        return _parse_scores(result)
    except Exception as e:
        print(f"Claude Assessor Error: {e}")
        return None


def _assess_with_openai(api_key: str, system_prompt: str, user_prompt: str) -> dict | None:
    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
            temperature=0.3,
        )
        result = json.loads(response.choices[0].message.content)
        return _parse_scores(result)
    except Exception as e:
        print(f"OpenAI Assessor Error: {e}")
        return None


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
    system_prompt, user_prompt = _build_prompts(transcript, question_text, role_applied, language)

    if settings.llm_provider == "claude" and settings.anthropic_api_key:
        result = _assess_with_claude(settings.anthropic_api_key, system_prompt, user_prompt)
        if result:
            return result

    if settings.openai_api_key:
        result = _assess_with_openai(settings.openai_api_key, system_prompt, user_prompt)
        if result:
            return result

    return _heuristic_scores(word_count)


def assess_transcript(candidate_id: int, transcript: str, role_applied: str, language: str) -> AssessmentResponse:
    scores = assess_question_response(
        transcript,
        "Describe your overall experience and suitability for this role.",
        role_applied,
        language,
    )
    overall = aggregate_scores(scores["clarity_score"], scores["skill_confidence_score"], scores["relevance_score"])
    note = scores["llm_notes"]
    is_real_note = note and "(Mock response)" not in note
    strengths = [note] if is_real_note and overall > 5 else []
    improvement_areas = [note] if is_real_note and overall <= 5 else []
    return AssessmentResponse(
        candidate_id=candidate_id,
        clarity_score=scores["clarity_score"],
        confidence_score=scores["skill_confidence_score"],
        relevance_score=scores["relevance_score"],
        overall_score=overall,
        strengths=strengths,
        improvement_areas=improvement_areas,
    )
