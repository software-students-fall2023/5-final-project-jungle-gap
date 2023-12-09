"""
simple face recognition and analysis client
"""

import face_recognition as fr
import cv2

# from textblob import TextBlob
from collections import namedtuple

SentimentResult = namedtuple("SentimentResult", ["polarity", "subjectivity"])


def recognition_image(file_path):
    """
    recognition the given image file
    """
    # r = sr.Recognizer()

    print("[recognition_image] file_path=", file_path)

    image = fr.load_image_file(file_path)
    face_locations = fr.face_locations(image)

    img = cv2.imread(file_path)

    print("face_locations=", face_locations)

    for p in face_locations:
        print(p)
        cv2.rectangle(img, (p[3], p[0]), (p[1], p[2]), (0, 0, 255), 5)

    cv2.imwrite(file_path, img)

    return file_path


