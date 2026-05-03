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
        data={
            "session_token": session_token,
            "prompt_id": "q1",
            "language": "en",
        },
        files={"video": ("answer.webm", b"mock video content", "video/webm")},
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


def test_fetch_plumber_questions_english(client):
    response = client.get("/api/v1/interview/questions/plumber/en")
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "plumber"
    assert len(payload["questions"]) == 3
    # Confirm the questions are plumber-specific, not the electrician fallback
    texts = [q["text"] for q in payload["questions"]]
    assert any("plumb" in t.lower() or "leak" in t.lower() or "pipe" in t.lower() for t in texts)


def test_fetch_welder_questions_kannada(client):
    response = client.get("/api/v1/interview/questions/welder/kn")
    assert response.status_code == 200
    payload = response.json()
    assert payload["role"] == "welder"
    assert len(payload["questions"]) == 3
    # Confirm the questions are welder-specific — all should contain Kannada script
    texts = [q["text"] for q in payload["questions"]]
    assert all(any(ord(c) > 0x0C7F for c in t) for t in texts)


def test_plumber_session_receives_plumber_questions(client):
    response = client.post(
        "/api/v1/interview/session/start",
        json={
            "full_name": "Ravi Nayak",
            "district": "Mysuru",
            "role_applied": "Plumber",
            "language": "en",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["total_questions"] >= 1
    # The first question must be plumber-specific, not an electrician question
    first_q = data["first_question"].lower()
    assert "electrical" not in first_q and "wiring" not in first_q
