import os
import csv
import shutil
import base64
from openai import OpenAI
import re
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
SOURCE_FOLDER = "source_folder"
PROCESSED_FOLDER = "processed_folder"
OUTPUT_CSV = "output.csv"

# Make sure processed folder exists
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

# Check if output.csv exists, if not create it with headers
if not os.path.exists(OUTPUT_CSV):
    with open(OUTPUT_CSV, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Number", "Name", "Quantity"])

# Process each image
for filename in os.listdir(SOURCE_FOLDER):
    if filename.lower().endswith((".jpg", ".jpeg", ".png")):
        image_path = os.path.join(SOURCE_FOLDER, filename)

        print(f"Processing: {filename}")

        # Call OpenAI Vision API
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
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64.b64encode(open(image_path, 'rb').read()).decode()}"
                            }
                        }
                    ]
                }
            ],
            temperature=0
        )

        # Get the raw text
        json_text = response.choices[0].message.content.strip()

        # Extract JSON substring using regex
        match = re.search(r"\[.*\]", json_text, re.DOTALL)
        if not match:
            print(f"No JSON found in response for {filename}. Skipping.")
            continue

        json_str = match.group(0)

        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"JSON decode error for {filename}: {e}")
            continue

        # Append to CSV
        with open(OUTPUT_CSV, mode="a", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            for row in data:
                writer.writerow([row["number"], row["name"], row["quantity"]])

        # Move file to processed folder
        shutil.move(image_path, os.path.join(PROCESSED_FOLDER, filename))
        print(f"Done processing {filename}.\n")
