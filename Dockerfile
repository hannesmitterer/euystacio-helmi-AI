# Multi-stage Dockerfile for Euystacio Helmi AI
# Build arguments for metadata
ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

# Stage 1: Build stage for Node.js dependencies
FROM node:20-alpine AS node-builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Final production image
FROM python:3.11-slim

# Install Node.js runtime
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Node.js dependencies from builder
COPY --from=node-builder /app/node_modules ./node_modules

# Copy package files
COPY package*.json ./
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs data/solar_sovereign

# Add labels for metadata
LABEL org.opencontainers.image.created="${BUILD_DATE}" \
      org.opencontainers.image.title="euystacio-helmi-ai" \
      org.opencontainers.image.description="Euystacio Helmi AI with Sustainment Protocol" \
      org.opencontainers.image.version="${VERSION}" \
      org.opencontainers.image.revision="${VCS_REF}" \
      org.opencontainers.image.vendor="hannesmitterer" \
      org.opencontainers.image.source="https://github.com/hannesmitterer/euystacio-helmi-AI"

# Environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=5000 \
    NODE_ENV=production

# Expose ports
EXPOSE 5000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/healthz || exit 1

# Default command (can be overridden)
CMD ["python", "app.py"]
