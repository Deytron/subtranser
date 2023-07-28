import os
import requests
from werkzeug.utils import secure_filename
from easynmt import EasyNMT

# Model to use
model = EasyNMT("m2m_100_1.2B")

# Available languages
target_lang = [
    {"display": "English", "lang": "en"},
    {"display": "French", "lang": "fr"},
    {"display": "Spanish", "lang": "es"},
]

# from fese import FFprobeVideoContainer
from flask import Flask, render_template, flash, request, redirect, url_for

# Variables
UPLOAD_FOLDER = "/uploaded_files"
ALLOWED_EXTENSIONS = {"txt", "ass", "srt"}
VIDEO_EXTENSIONS = {"mkv", "avi", "mp4"}

# Flask simple config
app = Flask("Subtranser")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def run():
    if request.method == "POST":
        files = request.files.getlist("file")

        # Check if the user selected a file
        for file in files:
            # Check if the 'file' field is present in the request
            if "file" not in request.files:
                flash("No file part")
                return redirect(request.url)

            if file.filename == "":
                flash("No selected file")
                return redirect(request.url)

            # Save the uploaded file (you can change the upload folder)
            if file and allowed_file(file.filename):
                # TODO: Warning for time to process if file is video
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return redirect("/", code=302)

                # Translate step

    return render_template("index.html", inqueue=list_files(), target_lang=target_lang)


@app.route("/result", methods=["POST"])
def translate():
    tg = request.form.get("tg_lang")
    print(tg)
    translate_step(tg)
    return redirect("/", code=302)


def translate_step(target):
    for file in list_files():
        with open(f"{UPLOAD_FOLDER}/{file}", "r") as file:
            data = file.read()
            data = f'"""{data}"""'
            print(data)
            result = model.translate(data, source_lang="en", target_lang=target)
            print(result)


def list_files():
    return os.listdir(UPLOAD_FOLDER)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
