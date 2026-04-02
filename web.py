from plate_detection import detect_plate
from flask import Flask, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ✅ TEMP safe function (prevents crash)
def detect_plate(image_path):
    return "TEST1234"

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":

        if "image" not in request.files:
            return "No file part❌"

        file = request.files["image"]

        if file.filename == "":
            return "No file selected❌"

        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # 👉 run model safely
            result = detect_plate(filepath)

            return f"Detected Plate: {result}🚗"

        except Exception as e:
            return f"Error: {str(e)}❌"

    return '''
    <h2>Upload Image🚗</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <input type="submit" value="Upload">
    </form>
    '''