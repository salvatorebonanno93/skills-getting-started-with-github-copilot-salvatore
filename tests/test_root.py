"""
Tests for the root endpoint (GET /)

AAA Pattern:
- Arrange: Set up TestClient instance
- Act: Call the root endpoint
- Assert: Verify redirect response
"""

from fastapi.testclient import TestClient
from src.app import app


def test_root_redirect():
    """Test that root endpoint redirects to static index.html"""
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"
