import os
import cv2
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Basic OMR Grading Logic
def grade_image(image_bytes):
    # 1. Convert uploaded bytes to an OpenCV image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if img is None:
        return {"error": "Could not decode image"}

    # 2. Convert to grayscale and blur
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # 3. Apply threshold (convert to black and white)
    # This makes dark bubbles black (0) and paper white (255)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # 4. Count the dark pixels
    # For a real app, you would crop specific regions here.
    # For this "Hello World" test, we just count total dark pixels to prove it works.
    total_dark_pixels = cv2.countNonZero(thresh)
    
    # Fake grading logic for demonstration:
    # If the image is "mostly dark", we say 100%. If "mostly light", 0%.
    score = min(int((total_dark_pixels / (img.shape[0] * img.shape[1])) * 1000), 100)

    return {
        "status": "success",
        "score": score, 
        "message": f"Processed image with {total_dark_pixels} dark pixels"
    }

@app.route('/', methods=['GET'])
def home():
    return "GradeSnap Server is Running!"

@app.route('/grade', methods=['POST'])
def upload_file():
    if 'photo' not in request.files:
        return jsonify({"error": "No photo part"}), 400
    
    file = request.files['photo']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Read file into memory
    file_bytes = file.read()
    
    # Process it
    result = grade_image(file_bytes)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)