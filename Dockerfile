# Multi-stage Dockerfile for Euystacio Helmi AI
# Stage 1: Build Node.js dependencies and compile contracts
FROM node:18-alpine AS node-builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source files for contract compilation
COPY hardhat.config.js ./
COPY contracts ./contracts

# Compile contracts if needed (optional - can be done in CI)
# RUN npm run compile

# Stage 2: Build Python environment
FROM python:3.11-slim AS python-builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt ./

# Install Python dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 3: Final runtime image
FROM python:3.11-slim

WORKDIR /app

# Install Node.js from NodeSource with verification
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gnupg && \
    curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /usr/share/keyrings/nodesource.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/nodesource.gpg] https://deb.nodesource.com/node_18.x nodistro main" > /etc/apt/sources.list.d/nodesource.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get remove -y curl gnupg && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy Python virtual environment from builder
COPY --from=python-builder /opt/venv /opt/venv

# Copy Node.js dependencies from builder
COPY --from=node-builder /app/node_modules ./node_modules

# Copy application code
COPY . .

# Set environment
ENV PATH="/opt/venv/bin:$PATH" \
    PORT=3000 \
    PYTHONUNBUFFERED=1

# Expose port
EXPOSE 3000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD ["node", "healthcheck.js"]

# Default command (can be overridden)
CMD ["node", "server.js"]
