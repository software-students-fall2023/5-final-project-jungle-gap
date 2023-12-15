"""
machine learning client backend
This file contains API for the web-app backend usage
"""

import os
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
import random
from ml_client import recognition_image

app = Flask(__name__)
CORS(app)  # Stop the security protection

# Use mongomock for testing, else use the real MongoClient
if os.environ.get("TESTING"):
    client = mongomock.MongoClient()
else:
    client = pymongo.MongoClient('mongodb://Isomorphism:d6wjgdhwddy@db:27017')
db = client['Isomorphism']


@app.route("/image/<filename>")
def uploaded_file(filename):
    """
    serve the shared folder.
    This shared folder is used to store the original unedited image files if the user is logged in
    """
    return send_from_directory("/images_files", filename)


@app.route("/edited-image/<filename>")
def edited_file(filename):
    """
    serve the shared folder.
    This shared folder is used to store the recognized image files if the user is logged in
    """
    return send_from_directory("/edited_images_files", filename)


@app.route("/upload", methods=["POST"])
def upload_image():
    """
    get the uploaded image and do ML work.
    web-app's backend will call this API.
    """
    if "file" not in request.files:
        print("No image file in request")
        return jsonify({"error": "No image file"}), 400
    random_number = random.randint(10000, 99999)  # generate unique file name
    image_file = request.files["file"]
    user_id = request.form.get("user_id", None)
    if user_id:
        filename = f"{user_id}_{random_number}.png"
    else:
        filename = "temp.png"

    original_dir = "images_files"  # The shared folder
    edited_dir = "edited_images_files"
    if not os.path.exists(original_dir):
        os.makedirs(original_dir)

    if not os.path.exists(edited_dir):
        os.makedirs(edited_dir)

    original_image_path = os.path.join(original_dir, filename)
    edited_image_path = os.path.join(edited_dir, filename)
    # Save the file in the shared folder
    image_file.save(edited_image_path)
    image_file.seek(0) # Set the pointer to the start of the file so it can be saved again
    image_file.save(original_image_path)

    # This is the actual machine learning work
    file_path = recognition_image(edited_image_path)  # recognition image

    if user_id:  # If the user is logged in
        # Store user id and file in the database
        document = {
            "user_id": user_id,
            "filename": filename,
        }
        db.history.insert_one(document)
    # Return recognition image
    return send_file(file_path)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=True)
