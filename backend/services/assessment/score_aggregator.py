def aggregate_scores(clarity_score: float, confidence_score: float, relevance_score: float) -> float:
    return round((clarity_score + confidence_score + relevance_score) / 3, 2)
