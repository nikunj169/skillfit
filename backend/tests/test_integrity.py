def test_integrity_endpoints_require_params(client):
    """Endpoints return a graceful error when called without required params."""
    face_response = client.get("/api/v1/integrity/validate-face")
    assert face_response.status_code == 200
    assert face_response.json()["passed"] is False

    duplicate_response = client.get("/api/v1/integrity/check-duplicate")
    assert duplicate_response.status_code == 200
    assert duplicate_response.json()["duplicate_detected"] is False


def test_integrity_duplicate_with_candidate_id(client):
    """Duplicate check returns clean result for a candidate with no prior embedding."""
    start_response = client.post(
        "/api/v1/interview/session/start",
        json={
            "full_name": "Integrity Test User",
            "district": "Hubli",
            "role_applied": "Electrician",
            "language": "en",
        },
    )
    candidate_id = start_response.json()["candidate_id"]

    dup_response = client.get(f"/api/v1/integrity/check-duplicate?candidate_id={candidate_id}")
    assert dup_response.status_code == 200
    assert dup_response.json()["duplicate_detected"] is False

