"""
web-page backend
"""

from functools import wraps
import os
import uuid
import requests
import pymongo
import mongomock
from dotenv import load_dotenv

load_dotenv()
from flask import (
    Flask,
    make_response,
    request,
    redirect,
    url_for,
    render_template,
    session,
    flash,
    jsonify,
)
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)

# Use mongomock for testing, else use the real MongoClient
if os.environ.get("TESTING"):
    client = mongomock.MongoClient()
else:
    client = pymongo.MongoClient('mongodb://Isomorphism:d6wjgdhwddy@db:27017')
db = client['Isomorphism']

# Set secret key for sessions
app.secret_key = b"\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5"


# Utilities
def login_required(f):
    """
    login required decorators
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        return redirect("/")

    return wrap


def start_session(user):
    """
    Create session containing user info
    """
    del user["password"]
    session["logged_in"] = True
    session["user"] = user
    return redirect("/")


# Views
@app.route("/")
def homescreen_view():
    """
    upload audio
    """
    return render_template("index.html")


@app.route("/archive")
@login_required
def archive_view():
    """
    View images generated for the user before
    """
    server_url = os.environ.get("SERVER_URL", "http://127.0.0.1")
    user_images = db.history.find({
        "user_id": session["user"]["_id"]
    }) # Find the images in the database that has user's id
    return render_template("archive.html", images=user_images, server_url=server_url)


@app.route("/login")
def login_view():
    """
    Display log in page
    """
    return render_template("logIn.html")


@app.route("/signup")
def signup_view():
    """
    Display sign up page
    """
    return render_template("signUp.html")


# Form handlers
@app.route("/api/js_upload_image", methods=["POST"])
def js_upload_image():
    """
    Endpoint specifically for JavaScript to upload image and get JSON response
    """
    print("js headers=", request.headers)

    image_file = request.files["image"]
    print("js image_file=", image_file)

    if not image_file:
        return jsonify({"error": "No image file provided"}), 400
    # Pass user id to the ml client if the user is logged in
    user_id = session["user"]["_id"] if "logged_in" in session else None
    data = {"user_id": user_id} if user_id else {}

    filename = f"{user_id}_temp.png"

    # file upload request
    files = [("file", (filename, image_file, "image/png"))]

    response = requests.post(
        "http://mlclient:5000/upload",
        files=files,
        data=data,
        timeout=60,
    )

    if response.status_code == 200:
        resp = make_response(response.content)

        resp.headers["Content-Type"] = "image/png"
        return resp  # For javascript display
    return (
        jsonify({"error": "Error processing audio", "details": response.text}),
        400,
    )


@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    """
    Endpoint specifically for image file upload and get JSON response
    """
    user_id = session["user"]["_id"] if "logged_in" in session else None
    data = {"user_id": user_id} if user_id else {}

    filename = f"{user_id}_temp.png"
    files = [("file", (filename, request.files["image"], "image/jpeg"))]

    response = requests.post(
        "http://mlclient:5000/upload",
        files=files,
        data=data,
        timeout=60,
    )

    if response.status_code == 200:
        resp = make_response(response.content)
        resp.headers["Content-Type"] = "image/png"
        return resp  # For javascript display
    return (
        jsonify(
            {
                "error": "Failed to process image. Please try again.",
                "err_code": response.status_code,
            }
        ),
        400,
    )


@app.route("/user/signup", methods=["POST"])
def signup():
    """
    sign up
    """
    # Create the user object
    user = {
        "_id": uuid.uuid4().hex,
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }

    # Encrypt the password
    user["password"] = pbkdf2_sha256.hash(user["password"])

    if db.users.find_one({"username": user["username"]}):
        # if user name in use, then flash a message and return to the same page
        flash("Username already in use", "error")
        return redirect(url_for("signup_view"))

    if db.users.insert_one(
        user
    ):  # save the user's account info in the users collection
        return start_session(user)  # auto login after registration

    flash("Signup failed", "error")  # we won't get here normally
    return redirect(url_for("signup_view"))


@app.route("/user/signout", methods=["POST"])
def signout():
    """
    signing out
    """
    session.clear()
    return redirect("/")


@app.route("/user/login", methods=["POST"])
def login():
    """
    login
    """
    user = db.users.find_one(
        {"username": request.form.get("username")}
    )  # find matches in the database
    if user and pbkdf2_sha256.verify(request.form.get("password"), user["password"]):
        return start_session(user)
    # if username and password does not match
    flash("Invalid Credentials", "error")
    return redirect(url_for("login_view"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
