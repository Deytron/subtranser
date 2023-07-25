import os
import requests
from dotenv import load_dotenv
from fese import FFprobeVideoContainer

# Get Dotenv configuration
load_dotenv()

BACK = os.getenv("SUB_BACKEND")
HOST = os.getenv("SUB_HOST")
TG = os.getenv("SUB_TARGET_LANGUAGE")
PATH = os.getenv("SUB_PATH")

# Other variables
API_URL = f'http://{HOST}:24080/translate'

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

if __name__ == "__main__":
    process_path(PATH)
