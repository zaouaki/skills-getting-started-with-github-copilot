def test_signup_succeeds_for_valid_activity_and_new_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "alice.student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in activities[activity_name]["participants"]


def test_signup_rejects_duplicate_student_for_same_activity(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_returns_not_found_for_unknown_activity(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}
