# Use official Python base image
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . /app

# Install system dependencies
RUN apt update -y && apt install awscli -y
RUN apt-get update && pip install -r requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the FastAPI app
CMD["python3", "app.py"]