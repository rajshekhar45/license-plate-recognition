 from flask import Flask, request
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        
        # Check if file part exists
        if "image" not in request.files:
            return "No file part ❌"

        file = request.files["image"]

        # Check if file is selected
        if file.filename == "":
            return "No file selected ❌"

        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            return f"Uploaded: {filename} ✅"

    return '''
    <h2>Upload Image 🚗</h2>
    <form method="POST" enctype="multipart/form-data">
        <input type="file" name="image" required>
        <input type="submit" value="Upload">
    </form>
    '''