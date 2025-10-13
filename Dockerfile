# Multi-stage Docker build for Crawl MCP

# Stage 1: Base image with dependencies
FROM python:3.11-slim as base

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Stage 2: Builder
FROM base as builder

WORKDIR /tmp

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --user -r requirements.txt

# Stage 3: Runtime
FROM base as runtime

# Create non-root user
RUN useradd -m -u 1000 crawluser && \
    mkdir -p /app /app/logs && \
    chown -R crawluser:crawluser /app

WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/crawluser/.local

# Copy application code
COPY --chown=crawluser:crawluser app/ ./app/
COPY --chown=crawluser:crawluser libs/ ./libs/
COPY --chown=crawluser:crawluser requirements.txt ./

# Update PATH
ENV PATH=/home/crawluser/.local/bin:$PATH

# Switch to non-root user
USER crawluser

# Expose port
EXPOSE 8012

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8012/health')"

# Run application
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]

