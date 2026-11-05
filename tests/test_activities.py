"""
Tests for the Mergington High School Activities API.

Uses the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and preconditions
- Act: Execute the action being tested
- Assert: Verify the results
"""

import pytest


class TestRootEndpoint:
    """Test the root endpoint."""

    def test_root_redirects_to_index(self, client):
        # Arrange: Client is ready to make requests
        
        # Act: Make GET request to root
        response = client.get("/", follow_redirects=False)
        
        # Assert: Should redirect to /static/index.html
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"


class TestGetActivities:
    """Test the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client):
        # Arrange: No additional setup needed (fixtures handle it)
        
        # Act: Fetch all activities
        response = client.get("/activities")
        
        # Assert: Should return 200 and contain all activities
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data

    def test_get_activities_contains_activity_details(self, client):
        # Arrange: No additional setup needed
        
        # Act: Fetch all activities
        response = client.get("/activities")
        data = response.json()
        chess_club = data["Chess Club"]
        
        # Assert: Activity should have all required fields
        assert "description" in chess_club
        assert "schedule" in chess_club
        assert "max_participants" in chess_club
        assert "participants" in chess_club

    def test_get_activities_shows_current_participants(self, client):
        # Arrange: Chess Club has initial participants
        
        # Act: Fetch activities
        response = client.get("/activities")
        data = response.json()
        
        # Assert: Participants list should match fixture data
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]


class TestSignupEndpoint:
    """Test the POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client, sample_email):
        # Arrange: Prepare a new student email and activity
        activity_name = "Chess Club"
        
        # Act: Sign up the student
        response = client.post(
            f"/activities/{activity_name}/signup?email={sample_email}"
        )
        
        # Assert: Should return 200 and confirm signup
        assert response.status_code == 200
        assert "Signed up" in response.json()["message"]
        assert sample_email in response.json()["message"]

    def test_signup_adds_participant_to_activity(self, client, sample_email):
        # Arrange: Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Act: Sign up new student
        client.post(f"/activities/Chess Club/signup?email={sample_email}")
        
        # Assert: Participant count should increase by 1
        response = client.get("/activities")
        new_count = len(response.json()["Chess Club"]["participants"])
        assert new_count == initial_count + 1
        assert sample_email in response.json()["Chess Club"]["participants"]

    def test_signup_duplicate_email_fails(self, client, existing_email):
        # Arrange: existing_email is already registered for Chess Club
        
        # Act: Try to sign up the same email again
        response = client.post(
            f"/activities/Chess Club/signup?email={existing_email}"
        )
        
        # Assert: Should return 400 Bad Request
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_invalid_activity_fails(self, client, sample_email):
        # Arrange: Use a non-existent activity name
        
        # Act: Try to sign up for non-existent activity
        response = client.post(
            f"/activities/Fake Activity/signup?email={sample_email}"
        )
        
        # Assert: Should return 404 Not Found
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterEndpoint:
    """Test the DELETE /activities/{activity_name}/unregister endpoint."""

    def test_unregister_successful(self, client, existing_email):
        # Arrange: existing_email is registered for Chess Club
        
        # Act: Unregister the student
        response = client.delete(
            f"/activities/Chess Club/unregister?email={existing_email}"
        )
        
        # Assert: Should return 200 and confirm unregistration
        assert response.status_code == 200
        assert "Unregistered" in response.json()["message"]
        assert existing_email in response.json()["message"]

    def test_unregister_removes_participant_from_activity(self, client, existing_email):
        # Arrange: Get initial participant count
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Act: Unregister student
        client.delete(f"/activities/Chess Club/unregister?email={existing_email}")
        
        # Assert: Participant count should decrease by 1
        response = client.get("/activities")
        new_count = len(response.json()["Chess Club"]["participants"])
        assert new_count == initial_count - 1
        assert existing_email not in response.json()["Chess Club"]["participants"]

    def test_unregister_non_existent_participant_fails(self, client, sample_email):
        # Arrange: sample_email is not registered for Chess Club
        
        # Act: Try to unregister a student who isn't signed up
        response = client.delete(
            f"/activities/Chess Club/unregister?email={sample_email}"
        )
        
        # Assert: Should return 400 Bad Request
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_unregister_invalid_activity_fails(self, client, existing_email):
        # Arrange: Use a non-existent activity
        
        # Act: Try to unregister from non-existent activity
        response = client.delete(
            f"/activities/Fake Activity/unregister?email={existing_email}"
        )
        
        # Assert: Should return 404 Not Found
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestActivityCapacity:
    """Test activity capacity and spots remaining."""

    def test_spots_calculation(self, client):
        # Arrange: Chess Club has max 12 and 2 participants
        
        # Act: Get activity details
        response = client.get("/activities")
        chess_club = response.json()["Chess Club"]
        
        # Assert: Spots left calculation
        spots_left = chess_club["max_participants"] - len(chess_club["participants"])
        assert spots_left == 10

    def test_capacity_not_enforced_yet(self, client, sample_email):
        # Arrange: Create a full activity by adding many participants
        
        # Act: Try to sign up for Gym Class (max 30, has 2)
        # This should succeed as capacity limits aren't enforced yet
        response = client.post(
            f"/activities/Gym Class/signup?email={sample_email}"
        )
        
        # Assert: Should succeed for now
        assert response.status_code == 200
