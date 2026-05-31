# Use a lightweight Python base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY app /app/app
COPY config /app/config
COPY tests /app/tests

# Expose the port the application will run on
EXPOSE ${APP_PORT:-8000}

# Command to run the application (placeholder)
CMD ["python", "app/main.py"]
