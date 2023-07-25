import os
import requests
from dotenv import load_dotenv

HOST="192.168.1.100" #Enter host PC IP address here, example: 192.168.1.10
API_URL = "http://${HOST}:24080/translate"
TARGET_LANG = "fr"  # French

def translate_text(text):
    params = {"target_lang": TARGET_LANG, "text": text}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.text
    else:
        return None

def translate_subtitle_file(subtitle_file):
    with open(subtitle_file, "r", encoding="utf-8") as file:
        original_content = file.read()

    # Split subtitle file content into individual lines
    lines = original_content.splitlines()

    # Translate each line using the API
    translated_lines = []
    for line in lines:
        translated_text = translate_text(line)
        if translated_text:
            translated_lines.append(translated_text)
        else:
            translated_lines.append(line)  # If translation fails, keep the original line

    translated_content = "\n".join(translated_lines)

    # Create the new file name with the '.fre' extension
    base_name, extension = os.path.splitext(subtitle_file)
    new_file_name = f"{base_name}.fre{extension}"

    # Save the translated content to the new file
    with open(new_file_name, "w", encoding="utf-8") as new_file:
        new_file.write(translated_content)

    print(f"Translation complete. Translated subtitle saved as: {new_file_name}")

if __name__ == "__main__":
    subtitle_file_path = "/disk2/anime/Persona 5 the Animation/Season 1/S01E01.ass"
    if os.path.exists(subtitle_file_path):
        translate_subtitle_file(subtitle_file_path)
    else:
        print("Invalid file path. Please check the file path and try again.")
