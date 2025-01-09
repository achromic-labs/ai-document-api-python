# Use Python 3.11 (latest LTS) slim base image
FROM python:3.11-slim

# Add container name label
LABEL container_name="ai-document-api-python"

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies and cloudflared
RUN apt-get update && apt-get install -y curl gpg && \
    curl -L https://pkg.cloudflare.com/cloudflare-main.gpg -o /usr/share/keyrings/cloudflare-main.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared focal main' | tee /etc/apt/sources.list.d/cloudflared.list && \
    apt-get update && \
    apt-get install -y cloudflared && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# # Create start script
# RUN echo '#!/bin/bash\npython server.py & \ncloudflared tunnel --url http://localhost:8080' > start.sh && \
#     chmod +x start.sh

# Run both commands
CMD ["./start_server_tunnel.sh"]