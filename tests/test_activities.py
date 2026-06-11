"""
Tests for the activities endpoint (GET /activities)

AAA Pattern:
- Arrange: Set up TestClient instance and expected data
- Act: Call the activities endpoint
- Assert: Verify response structure and content
"""

from fastapi.testclient import TestClient
from src.app import app


def test_get_all_activities():
    """Test that GET /activities returns all activities"""
    # Arrange
    client = TestClient(app)
    expected_activity_count = 9
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Soccer Team",
        "Swimming Club",
        "Art Club",
        "Drama Club",
        "Science Olympiad",
        "Robotics Club"
    ]

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert len(activities) == expected_activity_count
    for activity_name in expected_activities:
        assert activity_name in activities


def test_activity_has_required_fields():
    """Test that each activity has all required fields"""
    # Arrange
    client = TestClient(app)
    required_fields = {"description", "schedule", "max_participants", "participants"}

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert required_fields.issubset(activity_data.keys()), \
            f"Activity '{activity_name}' missing required fields: {required_fields - activity_data.keys()}"


def test_activity_fields_have_correct_types():
    """Test that activity fields have the correct data types"""
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)
        # Verify all participants are email strings
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)


def test_activities_have_participants():
    """Test that activities are pre-populated with participants"""
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")
    activities = response.json()

    # Assert
    for activity_name, activity_data in activities.items():
        assert len(activity_data["participants"]) > 0, \
            f"Activity '{activity_name}' should have pre-populated participants"
