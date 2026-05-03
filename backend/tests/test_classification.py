import pytest


def _classify(client, score, flags=None):
    response = client.post(
        "/api/v1/classification/classify",
        json={"candidate_id": 1, "overall_score": score, "integrity_flags": flags or []},
    )
    assert response.status_code == 200
    return response.json()["fitment_label"]


def test_job_ready_at_threshold(client):
    assert _classify(client, 7.5) == "JOB_READY"


def test_job_ready_above_threshold(client):
    assert _classify(client, 8.4) == "JOB_READY"


def test_requires_upskilling_at_threshold(client):
    assert _classify(client, 4.5) == "REQUIRES_UPSKILLING"


def test_requires_upskilling_mid_range(client):
    assert _classify(client, 6.0) == "REQUIRES_UPSKILLING"


def test_requires_manual_verification_below_baseline(client):
    # Weak answers with no integrity issues → manual review, NOT low quality submission
    assert _classify(client, 3.0) == "REQUIRES_MANUAL_VERIFICATION"


def test_low_quality_submission_from_integrity_flag(client):
    assert _classify(client, 8.0, flags=["LOW_QUALITY"]) == "LOW_QUALITY_SUBMISSION"


def test_suspected_duplicate_overrides_high_score(client):
    assert _classify(client, 9.0, flags=["SUSPECTED_DUPLICATE"]) == "SUSPECTED_DUPLICATE"


def test_boundary_below_job_ready(client):
    # 7.4 is just under the JOB_READY threshold
    assert _classify(client, 7.4) == "REQUIRES_UPSKILLING"


def test_boundary_below_upskilling(client):
    # 4.4 is just under the REQUIRES_UPSKILLING threshold
    assert _classify(client, 4.4) == "REQUIRES_MANUAL_VERIFICATION"
