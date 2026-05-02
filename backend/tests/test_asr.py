def test_start_session_and_submit_chunk(client):
    start_response = client.post(
        "/api/v1/interview/session/start",
        json={
            "full_name": "Asha Kumar",
            "district": "Bengaluru Urban",
            "role_applied": "Electrician",
            "language": "en",
        },
    )
    assert start_response.status_code == 200
    session_data = start_response.json()
    session_token = session_data["session_token"]
    assert session_data["total_questions"] >= 1
    assert session_data["first_question"]

    chunk_response = client.post(
        "/api/v1/interview/session/submit-chunk",
        json={
            "session_token": session_token,
            "prompt_id": "intro-1",
            "language": "en",
        },
    )
    assert chunk_response.status_code == 200
    assert "experience" in chunk_response.json()["transcript"].lower()

    finalize_response = client.post(
        "/api/v1/interview/session/finalize",
        json={
            "session_token": session_token,
            "role_applied": "Electrician",
            "language": "en",
        },
    )
    assert finalize_response.status_code == 200
    assert finalize_response.json()["status"] == "PROCESSING"

    status_response = client.get(f"/api/v1/interview/session/{session_data['session_id']}/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "COMPLETED"


def test_fetch_questions(client):
    response = client.get("/api/v1/interview/questions/delivery_associate/hi")
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "delivery_associate"
    assert len(payload["questions"]) >= 1
    assert payload["questions"][0]["text"]
