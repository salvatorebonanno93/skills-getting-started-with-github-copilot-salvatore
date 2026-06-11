"""
Tests for the signup endpoint (POST /activities/{activity_name}/signup)

AAA Pattern:
- Arrange: Set up TestClient instance and test data
- Act: Call the signup endpoint
- Assert: Verify response status, message, and side effects
"""

from fastapi.testclient import TestClient
from src.app import app


def test_signup_success():
    """Test successful signup for an activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"


def test_signup_adds_participant_to_activity():
    """Test that signup adds participant to the activity's participant list"""
    # Arrange
    client = TestClient(app)
    activity_name = "Programming Class"
    new_email = "newtester@mergington.edu"

    # Act - Sign up the student
    client.post(f"/activities/{activity_name}/signup", params={"email": new_email})

    # Act - Get activities to verify participant was added
    response = client.get("/activities")
    activities = response.json()

    # Assert
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_email_returns_400():
    """Test that signing up with duplicate email returns 400 error"""
    # Arrange
    client = TestClient(app)
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"  # Already signed up

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_nonexistent_activity_returns_404():
    """Test that signing up for non-existent activity returns 404 error"""
    # Arrange
    client = TestClient(app)
    fake_activity = "Fake Activity That Does Not Exist"
    email = "student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{fake_activity}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_with_multiple_new_students():
    """Test that multiple different students can sign up for the same activity"""
    # Arrange
    client = TestClient(app)
    activity_name = "Art Club"
    students = ["student1@mergington.edu", "student2@mergington.edu", "student3@mergington.edu"]

    # Act - Sign up all students
    for email in students:
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

    # Act - Verify all students are in the participant list
    response = client.get("/activities")
    activity = response.json()[activity_name]

    # Assert
    for email in students:
        assert email in activity["participants"]
