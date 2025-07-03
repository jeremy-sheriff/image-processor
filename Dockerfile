# Use official Python image
FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Create folders if they don't exist
RUN mkdir -p /app/source_folder /app/processed_folder

ENV OPENAI_API_KEY="REMOVED_SECRET"

# Run the script
CMD ["python", "app.py"]
