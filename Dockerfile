# Use Python slim image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set Python unbuffered mode
ENV PYTHONUNBUFFERED=1

# Install system dependencies
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock
COPY . /app

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Astral)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/


# Ensure uv is in PATH
ENV PATH="/root/.cargo/bin:$PATH"

# Copy dependency metadata first (for Docker cache)
COPY pyproject.toml uv.lock ./

# Create non-root user first
RUN useradd -m -u 1000 mcpuser && \
    chown -R mcpuser:mcpuser /app

# Switch to non-root user
USER mcpuser

# Install dependencies from uv.lock (as mcpuser)
RUN uv sync --frozen --no-dev

# Copy application code
COPY --chown=mcpuser:mcpuser fast_mcp_server.py .

# Run the server via uv
CMD ["uv", "run", "app"]
