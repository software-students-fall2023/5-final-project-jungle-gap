"""
machine learning client backend
This file contains API for the web-app backend usage
"""


import os

# import random
import traceback
import mongomock
from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    send_from_directory,
)
from flask_cors import CORS
import pymongo
from ml_client import recognition_image

app = Flask(__name__)
CORS(app)  # Stop the security protection

# Use mongomock for testing, else use the real MongoClient
if os.environ.get("TESTING"):
    client = mongomock.MongoClient()
else:
    client = pymongo.MongoClient("mongodb://db:27017")

db = client["Isomorphism"]
collection = db["history"]  # ml result and metadata are stored in this collection
app.config["SECRET_KEY"] = "supersecretkey"


@app.route("/image/<filename>")
def uploaded_file(filename):
    """
    serve the shared folder.
    This shared folder is used to store the original uneditted image files if the user is logged in
    """
    return send_from_directory("/images_files", filename)

@app.route("/edited-image/<filename>")
def uploaded_file(filename):
    """
    serve the shared folder.
    This shared folder is used to store the recognized image files if the user is logged in
    """
    return send_from_directory("/editted_images_files", filename)

@app.route("/upload", methods=["POST"])
def upload_image():
    """
    get the uploaded image and do ML work.
    web-app's backend will call this API.
    """
    try:
        if "file" not in request.files:
            print("No image file in request")
            return jsonify({"error": "No image file"}), 400
        # random_number = random.randint(10000, 99999)  # generate unique file name
        image_file = request.files["file"]
        print("[image_file]:", image_file)

        user_id = request.form.get("user_id", None)

        original_dir = "images_files"  # The shared folder
        editted_dir = "editted_images_files"
        if not os.path.exists(original_dir):
            os.makedirs(original_dir)

        if not os.path.exists(editted_dir):
            os.makedirs(editted_dir)

        print("image_file.filename", image_file.filename)
        original_image_path = os.path.join(original_dir, image_file.filename)
        editted_image_path = os.path.join(editted_dir, image_file.filename)
        print("xx image_path", editted_image_path)
        image_file.save(original_image_path)  # Save the file in the shared folder
        image_file.save(editted_image_path)

        # This is the actual machine learning work
        file_path = recognition_image(editted_image_path)  # recognition image

        if user_id:  # If the user is logged in
            # Store user id and file in the database
            document = {
                "user_id": user_id,
                "eddited_file_path": file_path,
                "original_file_path": original_image_path,
                "filename": image_file.filename,
            }
            collection.insert_one(document)
        # Return recognition image
        return send_file(file_path)
    except Exception as e:
        msg = traceback.format_exc()
        print(msg)
        return (
            jsonify({"err_msg": msg, "filename": image_file.filename}),
            500,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
