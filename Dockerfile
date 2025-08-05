# Redmine MCP Server - Docker MCP Registry Compatible
FROM python:3.11-slim

# Metadata labels for Docker MCP Registry
LABEL org.opencontainers.image.title="Redmine MCP Server"
LABEL org.opencontainers.image.description="A comprehensive MCP server for Redmine project management integration"
LABEL org.opencontainers.image.version="1.0.3"
LABEL org.opencontainers.image.authors="Redmine MCP Contributors"
LABEL org.opencontainers.image.url="https://github.com/umutkocak/redmine-mcp"
LABEL org.opencontainers.image.documentation="https://github.com/umutkocak/redmine-mcp/blob/main/README.md"
LABEL org.opencontainers.image.source="https://github.com/umutkocak/redmine-mcp"
LABEL org.opencontainers.image.licenses="MIT"

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy Python dependencies
COPY requirements.txt  ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY pyproject.toml ./

# Install the package in development mode
RUN pip install -e .

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash mcp
USER mcp

# Environment variables (will be provided by Docker MCP)
ENV REDMINE_URL=""
ENV REDMINE_API_KEY=""
ENV LOG_LEVEL="INFO"

# Health check to ensure MCP server is responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.path.insert(0, 'src'); from main import main; print('MCP server healthy')" || exit 1

# Expose MCP stdio interface
CMD ["python", "src/main.py"]
