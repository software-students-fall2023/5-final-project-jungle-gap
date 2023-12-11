"""Web-app test file."""

import os
from contextlib import contextmanager
from unittest.mock import patch
import pytest
from flask import template_rendered

# Set TESTING environment variable for the test session
os.environ["TESTING"] = "1"
from app import app


class MockResponse:
    """Mock response class for simulating HTTP responses."""

    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        """Return JSON data."""
        return self.json_data


@contextmanager
def captured_templates(app):
    """Capture templates for future assertions."""

    recorded = []

    def record(_sender, template, context, **_extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def client():
    """Pytest fixture for creating a test client for the web-app."""

    app.config["WTF_CSRF_ENABLED"] = False
    with app.test_client() as client:
        yield client


def test_user_signup_and_session(client):
    """Test the user signup process and session start."""

    response = client.post(
        "/user/signup", data={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 302

    with client.session_transaction() as session:
        assert session["logged_in"] is True
        assert "user" in session
        assert session["user"]["username"] == "testuser"


def test_signup_username_already_in_use(client):
    """Test signup with a username that is already in use."""

    username = "existing_user"
    client.post(
        "/user/signup",
        data={"username": username, "password": "password"},
        follow_redirects=True,
    )

    response = client.post(
        "/user/signup",
        data={"username": username, "password": "new_password"},
        follow_redirects=True,
    )

    assert b"Username already in use" in response.data


def test_login_view(client):
    """Test the rendering of the login view."""

    with captured_templates(app) as templates:
        response = client.get("/login")
        assert response.status_code == 200
        assert len(templates) == 1
        assert templates[0][0].name == "logIn.html"


def test_login(client):
    """Test the user login functionality."""

    client.post(
        "/user/signup",
        data={"username": "test_user", "password": "test_password"},
        follow_redirects=True,
    )
    response = client.post(
        "/user/login",
        data={"username": "test_user", "password": "test_password"},
        follow_redirects=True,
    )
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert sess["logged_in"] is True


def test_logout(client):
    """Test the user logout functionality."""

    response = client.post("/user/signout", follow_redirects=True)
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert "logged_in" not in sess


def test_upload_picture(client):
    """Test the image upload functionality."""

    mock_response_data = {
        "transcript": "test transcript",
        "sentiment": 0.5,
        "filename": "testfile.wav",
    }

    with patch(
        "requests.post",
        return_value=MockResponse(mock_response_data, 200),
    ) as mock_post:
        current_directory = os.path.dirname(os.path.abspath(__file__))

        image_file_path = current_directory + "/test_p.jpeg"

        # with open(image_file_path, "rb") as image:
        response = client.post(
            "/api/upload_image",
            data={"image": open(image_file_path, "rb")},
            content_type="multipart/form-data",
        )
        assert response.status_code == 200
        assert mock_post.called

        json_data = response.get_json()
        assert json_data["transcript"] == "test transcript"
        assert json_data["sentiment"] == 0.5
        assert json_data["filename"] == "testfile.wav"


def test_js_upload_picture(client):
    """Test the /api/js_upload_image endpoint for audio upload and JSON response."""

    mock_response_data = {
        "transcript": "test transcript",
        "sentiment": 0.5,
        "filename": "testfile.wav",
    }

    with patch(
        "requests.post", return_value=MockResponse(mock_response_data, 200)
    ) as mock_post:
        current_directory = os.path.dirname(os.path.abspath(__file__))

        image_file_path = current_directory + "/test_p.jpeg"

        with open(image_file_path, "rb") as image:
            response = client.post(
                "/api/js_upload_image",
                data={"image": image},
                content_type="multipart/form-data",
            )

        assert response.status_code == 200
        assert mock_post.called

        json_data = response.get_json()
        assert json_data["filename"] == "test_p.jepg"
