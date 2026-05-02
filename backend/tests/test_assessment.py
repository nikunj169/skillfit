def test_assessment_endpoint(client):
    response = client.post(
        "/api/v1/assessment/assess",
        json={
            "candidate_id": 1,
            "transcript": "I have worked on installation, troubleshooting, and customer support tasks.",
            "role_applied": "Field Technician",
            "language": "en",
        },
    )
    assert response.status_code == 200
    assert response.json()["overall_score"] > 0
