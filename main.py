import os
import requests
from werkzeug.utils import secure_filename

# from fese import FFprobeVideoContainer
from flask import Flask, render_template, flash, request, redirect, url_for

# Variables
UPLOAD_FOLDER = "/uploaded_files"
ALLOWED_EXTENSIONS = {"txt", "ass", "srt"}

# Flask simple config
app = Flask("Subtranser")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def run():
    if request.method == "POST":
        # Check if the 'file' field is present in the request
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files["file"]

        # Check if the user selected a file
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)

        # Save the uploaded file (you can change the upload folder)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            return redirect("/", code=302)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    # process_path(PATH)
