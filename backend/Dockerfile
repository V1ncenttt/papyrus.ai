# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app:/app/src

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first for better caching
COPY requirements.txt .

# Install Python dependencies AS ROOT
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Create config directories and set permissions BEFORE switching users
RUN mkdir -p /app/config && chmod 777 /app/config
RUN chmod -R 777 /usr/local/lib/python3.11/site-packages/pdf2bib/ || true
RUN chmod -R 777 /usr/local/lib/python3.11/site-packages/pdf2doi/ || true
ENV PDF2BIB_CONFIG_DIR=/app/config
ENV PDF2DOI_CONFIG_DIR=/app/config

# Copy source code
COPY src/ ./src/
COPY tests/ ./tests/

# Create non-root user and set ownership
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

# Switch to non-root user AFTER setting permissions
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]