def test_integrity_endpoints(client):
    face_response = client.get("/api/v1/integrity/validate-face")
    duplicate_response = client.get("/api/v1/integrity/check-duplicate")

    assert face_response.status_code == 200
    assert duplicate_response.status_code == 200
    assert duplicate_response.json()["duplicate_detected"] is False
