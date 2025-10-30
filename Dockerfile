# Use official Python runtime as base image
FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file first to leverage Docker cache
COPY backend/requirements.txt .

# Install system dependencies and Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend/ .

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]