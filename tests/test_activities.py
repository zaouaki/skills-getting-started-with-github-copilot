def test_root_redirects_to_static_index(client):
    # Arrange

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_catalog_with_expected_shape(client):
    # Arrange

    # Act
    response = client.get("/activities")
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert len(payload) == 9
    assert "Chess Club" in payload

    chess = payload["Chess Club"]
    assert set(chess.keys()) == {"description", "schedule", "max_participants", "participants"}
    assert isinstance(chess["participants"], list)


def test_get_activities_reflects_latest_state_after_signup(client):
    # Arrange
    activity_name = "Science Club"
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities_response = client.get("/activities")
    payload = activities_response.json()

    # Assert
    assert signup_response.status_code == 200
    assert activities_response.status_code == 200
    assert email in payload[activity_name]["participants"]
