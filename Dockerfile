# Use Python 3.11 (latest LTS) slim base image
FROM python:3.11-slim

# Add container name label
LABEL container_name="ai-document-api-python"

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port (adjust if needed)
EXPOSE 8080

# Run the application
CMD ["python", "server.py"]