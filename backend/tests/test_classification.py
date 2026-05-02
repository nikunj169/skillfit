def test_classification_endpoint(client):
    response = client.post(
        "/api/v1/classification/classify",
        json={
            "candidate_id": 1,
            "overall_score": 8.4,
            "integrity_flags": [],
        },
    )
    assert response.status_code == 200
    assert response.json()["fitment_label"] == "JOB_READY"
