def test_get_activities_returns_all_activities(client):
    # Arrange
    # (No setup required beyond the fixture.)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_for_activity_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Signed up {email} for {activity_name}" in response.json()["message"]

    # Verify participant was added
    response = client.get("/activities")
    assert email in response.json()[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up"


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent"
    email = "somebody@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_remove_participant_removes_existing(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert f"Removed {email} from {activity_name}" in response.json()["message"]

    # Verify participant was removed
    response = client.get("/activities")
    assert email not in response.json()[activity_name]["participants"]


def test_remove_nonexistent_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "ghost@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up"


def test_remove_from_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "DoesNotExist"
    email = "someone@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
