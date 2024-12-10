# Build stage
FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

WORKDIR /app

# Create non-root user for the final stage
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen

# Copy application code
COPY repo_tool ./repo_tool

# Final stage
FROM python:3.12-slim-bookworm

WORKDIR /app

# Install git in the final stage
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy non-root user from builder
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --from=builder /app/repo_tool /app/repo_tool

# Create directories for bind mounts
RUN mkdir -p /app/repositories /app/digests && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Set environment variables
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH=/app
ENV REPO_PATH=/app/repositories
ENV DIGEST_PATH=/app/digests

# Run the FastAPI application with hot reload
CMD ["uvicorn", "repo_tool.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
