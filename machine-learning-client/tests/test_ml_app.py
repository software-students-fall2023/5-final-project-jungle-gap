"""
Tests for the webapp.
"""

import os
import pytest
from app import app


@pytest.fixture
def client():
    """
    Client fixture for test
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_upload_picture_no_file(client):
    """
    Test the /upload route without an image file
    """
    response = client.post("/upload", data={})
    assert response.status_code == 400
    assert b"No image file" in response.data


def test_upload_picture_with_file(client):
    """
    Test the /upload route with a valid audio file
    """
    # Path to the picture file
    picture_file_path = os.path.join("tests/test_pictures", "test_p.jpeg")

    # Open the file in binary mode
    with open(picture_file_path, "rb") as picture_file:
        data = {"file": (picture_file, "test_p.jpeg")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200


def test_upload_picture_with_file_non_trancriptable(client):
    """
    Test the /upload route with an picture file that has no english words
    """
    # Path to the picture file
    picture_file_path = os.path.join("tests/test_pictures", "test_p.jpeg")

    # Open the file in binary mode
    with open(picture_file_path, "rb") as picture_file:
        data = {"file": (picture_file, "test_p.jpeg")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == "N/A"


def test_upload_audio_correctness_short_file(client):
    """
    Test the /upload route with a short audio file
    """
    # Path to the file file
    picture_file_path = os.path.join("tests/test_pictures", "test_p.jpeg")

    # Open the file in binary mode
    with open(picture_file_path, "rb") as picture_file:
        data = {"file": (picture_file, "test_p.jpeg")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == "kids are talking by the door"


def test_upload_audio_correctness_long_file(client):
    """
    Test the /upload route with a long audio file
    """
    # Path to the audio file
    picture_file_path = os.path.join("tests/test_pictures", "test_p.jpeg")

    # Open the file in binary mode
    with open(picture_file_path, "rb") as picture_file:
        data = {"file": (picture_file, "test_p.jpeg")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get("transcript") == (
            "the stale smell of old beer lingers it takes heat to bring out the odor a cold dip "
            "restores health and zest a salt pickle taste fine with ham tacos al pastor are my "
            "favorite a zestful food is the hot cross bun"
        )


def test_upload_picture_with_jpg_format_file(client):
    """
    Test the /upload route with a .webm short picture file
    This is to test the format conversion function of the ml backend
    """
    # Path to the picture file
    picture_file_path = os.path.join("tests/test_pictures", "test_p.jpg")

    # Open the file in binary mode
    with open(picture_file_path, "rb") as picture_file:
        data = {"file": (picture_file, "test_p.jpg")}
        response = client.post("/upload", data=data, content_type="multipart/form-data")
        assert response.status_code == 200
        # json_data = response.get_json()
        # assert json_data.get("transcript") == "kids are talking by the door"
