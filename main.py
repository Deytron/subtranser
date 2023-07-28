import os
import requests

# from fese import FFprobeVideoContainer
from flask import Flask

# Flask simple config
app = Flask("app")


def process_path(path):
    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist.")
        return

    # If path is a file
    if os.path.isfile(path):
        formatted = check_format(path)
        send_to_api(formatted)
    elif os.path.isdir(path):
        for root, _, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                check_format(file_path)
                # send_to_api(file_path)
    else:
        print(f"Error: '{path}' is neither a file nor a folder.")


def check_format(is_file):
    _, extension = os.path.splitext(is_file)
    ext = extension[1:]
    if ext == "mkv":
        subname = is_file[:-4]
        print("file is mkv")
        print(is_file)
        os.system(f"ffmpeg -i {is_file} | grep Subtitle:")


def send_to_api(text):
    params = {"target_lang": TG, "text": text}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return None


@app.route("/", methods=["GET", "POST"])
def run():
    if requests.method == "POST":
        # Check if the 'file' field is present in the request
        if "file" not in requests.files:
            return "No file part in the request."

        file = requests.files["file"]

        # Check if the user selected a file
        if file.filename == "":
            return "No file selected."

        # Save the uploaded file (you can change the upload folder)
        file.save("uploaded_file.txt")
        return "File uploaded successfully."

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    # process_path(PATH)
