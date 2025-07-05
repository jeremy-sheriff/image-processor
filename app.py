import os
import csv
import base64
import re
import json
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# Initialize OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
UPLOAD_FOLDER = "uploads"
PROCESSED_FOLDER = "processed"
OUTPUT_CSV = "output.csv"

# Make folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Initialize Flask app
app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET"])
def upload_page():
    return render_template("upload.html")


@app.route("/process", methods=["POST"])
def process_files():
    files = request.files.getlist("files")
    if not files:
        return "No files uploaded", 400

    # Start a fresh CSV
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Number", "Name", "Quantity"])

    for file in files:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        print(f"Processing {filename}")

        with open(file_path, "rb") as img_f:
            b64_data = base64.b64encode(img_f.read()).decode()

        # OpenAI Vision API call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that extracts tabular data from an image."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "Extract the table rows as JSON array with fields: number, name, quantity."
                                " Only return valid JSON, no other text."
                            )
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{b64_data}"}
                        }
                    ]
                }
            ],
            temperature=0
        )

        json_text = response.choices[0].message.content.strip()
        match = re.search(r"\[.*\]", json_text, re.DOTALL)
        if not match:
            print(f"No JSON found in {filename}")
            continue

        try:
            data = json.loads(match.group(0))
        except json.JSONDecodeError as e:
            print(f"JSON decode error in {filename}: {e}")
            continue

        with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow([row["number"], row["name"], row["quantity"]])

        os.rename(file_path, os.path.join(PROCESSED_FOLDER, filename))

    return "OK"


@app.route("/download")
def download_csv():
    return send_file(OUTPUT_CSV, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
