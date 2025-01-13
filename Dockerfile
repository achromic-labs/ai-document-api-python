# Use Python 3.11 (latest LTS) slim base image
FROM python:3.11-slim

# Add container name label
LABEL container_name="potext-api-python"

# Set working directory
WORKDIR /app

# Install dependencies and cloudflared
RUN apt-get update && apt-get install -y curl gpg && \
    curl -L https://pkg.cloudflare.com/cloudflare-main.gpg -o /usr/share/keyrings/cloudflare-main.gpg && \
    echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared focal main' | tee /etc/apt/sources.list.d/cloudflared.list && \
    apt-get update && \
    apt-get install -y cloudflared && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Run both commands
CMD ["./start_server_tunnel.sh"]