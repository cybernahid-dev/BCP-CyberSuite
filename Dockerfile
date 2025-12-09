# BCP-CyberSuite Dockerfile
FROM python:3.9-slim

LABEL maintainer="Bangladesh Cyber Panthers <info.bcp404@gmail.com>"
LABEL version="4.0"
LABEL description="BCP-CyberSuite - Next-Gen Cyber Recon Framework"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Create app directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    nmap \
    dnsutils \
    whois \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p reports/html reports/json reports/screenshots \
    databases/fingerprints databases/payloads databases/wordlists

# Create non-root user
RUN useradd -m -u 1000 bcpuser && \
    chown -R bcpuser:bcpuser /app
USER bcpuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; import bs4; print('Dependencies OK')" || exit 1

# Default command
CMD ["python", "bcp.py"]
