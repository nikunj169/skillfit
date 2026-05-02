from backend.schemas.classification import ClassificationResponse


def classify_candidate(candidate_id: int, overall_score: float, integrity_flags: list[str]) -> ClassificationResponse:
    reasons = []

    if "SUSPECTED_DUPLICATE" in integrity_flags:
        reasons.append("Potential duplicate submission detected")
        label = "SUSPECTED_DUPLICATE"
    elif "LOW_QUALITY" in integrity_flags:
        reasons.append("Media quality was below the acceptable threshold")
        label = "LOW_QUALITY_SUBMISSION"
    elif integrity_flags:
        reasons.extend(integrity_flags)
        label = "REQUIRES_MANUAL_VERIFICATION"
    elif overall_score >= 8:
        label = "JOB_READY"
        reasons.append("Strong interview performance")
    elif overall_score >= 6:
        label = "REQUIRES_UPSKILLING"
        reasons.append("Promising candidate with moderate skill gaps")
    else:
        label = "LOW_QUALITY_SUBMISSION"
        reasons.append("Response quality below baseline")

    return ClassificationResponse(
        candidate_id=candidate_id,
        fitment_label=label,
        confidence_score=round(min(0.99, overall_score / 10), 2),
        reasons=reasons,
    )
