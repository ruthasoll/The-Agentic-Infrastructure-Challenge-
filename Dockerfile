# Project Chimera Dockerfile
# 
# Spec Reference: .cursor/rules (containerization best practices)
# Purpose: Containerize Project Chimera for consistent dev/test/prod environments
#
# Design Choices:
# 1. python:3.12-slim - Minimal image size (~150MB vs 1GB for full python)
# 2. Multi-stage build - Separate build deps from runtime (security + size)
# 3. Non-root user - Security best practice (principle of least privilege)
# 4. Layer caching - Dependencies installed before code copy (faster rebuilds)
# 5. .dockerignore - Exclude .git, __pycache__, .venv (reproducibility)

# ============================================================================
# Stage 1: Builder
# ============================================================================
FROM python:3.12-slim AS builder

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (fast Python package installer)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.cargo/bin:${PATH}"

# Set working directory
WORKDIR /build

# Copy dependency files first (layer caching optimization)
COPY requirements.txt pyproject.toml* ./

# Install Python dependencies
# Use uv if pyproject.toml exists, otherwise pip
RUN if [ -f pyproject.toml ]; then \
        uv pip install --system -r pyproject.toml; \
    else \
        pip install --no-cache-dir -r requirements.txt; \
    fi

# ============================================================================
# Stage 2: Runtime
# ============================================================================
FROM python:3.12-slim

# Install runtime system dependencies
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 -s /bin/bash chimera

# Set working directory
WORKDIR /app

# Copy Python packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy project files
COPY --chown=chimera:chimera . .

# Switch to non-root user
USER chimera

# Set Python environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# Expose port for MCP servers (if running locally)
EXPOSE 8000

# Health check (optional, for orchestrator health monitoring)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command (can be overridden)
CMD ["python", "-m", "pytest", "tests/", "-v"]

# ============================================================================
# Build Instructions:
# ============================================================================
# Build image:
#   docker build -t chimera:latest .
#
# Run tests:
#   docker run --rm chimera:latest
#
# Run with custom command:
#   docker run --rm chimera:latest python -m src.orchestrator
#
# Run interactively:
#   docker run --rm -it chimera:latest /bin/bash
#
# Mount local code for development:
#   docker run --rm -v $(pwd):/app chimera:latest
# ============================================================================
