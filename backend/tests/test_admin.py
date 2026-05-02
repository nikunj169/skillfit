def test_admin_login_and_stats(client):
    login_response = client.post(
        "/api/v1/admin/login",
        json={
            "username": "admin@skillfit.in",
            "password": "skillfit2024",
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["token"]

    stats_response = client.get("/api/v1/admin/stats", headers={"X-Admin-Token": token})
    assert stats_response.status_code == 200
    assert "total_candidates" in stats_response.json()


def test_admin_candidate_detail_includes_transcript_and_assessment(client):
    start_response = client.post(
        "/api/v1/interview/session/start",
        json={
            "full_name": "Ravi Driver",
            "district": "Mysuru",
            "role_applied": "Delivery Associate",
            "language": "en",
        },
    )
    session_data = start_response.json()

    client.post(
        "/api/v1/interview/session/submit-chunk",
        json={
            "session_token": session_data["session_token"],
            "prompt_id": "q1",
            "language": "en",
            "transcript_hint": "I handled urgent delivery routes and customer handoffs carefully.",
        },
    )
    client.post(
        "/api/v1/interview/session/finalize",
        json={
            "session_token": session_data["session_token"],
            "role_applied": "Delivery Associate",
            "language": "en",
        },
    )

    login_response = client.post(
        "/api/v1/admin/login",
        json={
            "username": "admin@skillfit.in",
            "password": "skillfit2024",
        },
    )
    token = login_response.json()["token"]

    detail_response = client.get(
        f"/api/v1/admin/candidates/{session_data['candidate_id']}",
        headers={"X-Admin-Token": token},
    )
    assert detail_response.status_code == 200
    payload = detail_response.json()
    assert payload["latest_transcript"]
    assert payload["latest_session_status"] == "COMPLETED"
    assert payload["latest_assessment"] is not None
    assert len(payload["response_history"]) >= 1
    assert payload["response_history"][0]["question_text"]
