"""
machine learning client backend
This file contains API for the web-app backend usage
"""

import logging
import os
import subprocess

# import random
import traceback
import mongomock
from flask import (
    Flask,
    make_response,
    request,
    jsonify,
    send_file,
    send_from_directory,
)
from flask_cors import CORS
import pymongo
from ml_client import recognition_image  # , analyze_sentiment

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
    This shared folder is used to store the image files if the user is logged in
    """
    return send_from_directory("/images_files", filename)


@app.route("/upload", methods=["POST"])
def upload_image():
    """
    get the uploaded image and do ML work.
    web-app's backend will call this API.
    """
    try:
        print("mlclient /upload request=", request.files)
        if "file" not in request.files:
            print("No image file in request")
            return jsonify({"error": "No image file"}), 400
        # random_number = random.randint(10000, 99999)  # generate unique file name
        image_file = request.files["file"]
        print("[image_file]:", image_file)

        user_id = request.form.get("user_id", None)

        upload_dir = "images_files"  # The shared folder
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        print("image_file.filename", image_file.filename)

        image_path = os.path.join(upload_dir, image_file.filename)
        print("xx image_path", image_path)
        image_file.save(image_path)  # Save the file in the shared folder

        # This is the actual machine learning work
        file_path = recognition_image(image_path)  # recognition image
        # sentiment = analyze_sentiment(transcript)  # Sentiment

        if user_id:  # If the user is logged in
            # Store user id and file in the database
            document = {
                "user_id": user_id,
                "file_path": file_path,
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
