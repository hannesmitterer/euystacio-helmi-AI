# Deployment Guide

This document provides comprehensive information about the CI/CD pipelines, deployment processes, and DevOps practices for the Euystacio Helmi AI project.

## Table of Contents

- [Overview](#overview)
- [CI/CD Workflows](#cicd-workflows)
- [Deployment Environments](#deployment-environments)
- [Docker Deployment](#docker-deployment)
- [Release Process](#release-process)
- [Security](#security)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Overview

The project uses GitHub Actions for continuous integration and deployment. The workflows are designed to:

- Automatically build and test code changes
- Build and publish Docker images
- Deploy to staging and production environments
- Create releases and publish artifacts
- Scan for security vulnerabilities
- Keep dependencies up to date

## CI/CD Workflows

### 1. CI - Build and Test (`ci.yml`)

**Triggers:**
- Push to `main`, `develop`, or `copilot/**` branches
- Pull requests to `main` or `develop`

**Jobs:**
- **Node.js Build**: Tests across Node.js 16.x, 18.x, and 20.x
  - Installs dependencies
  - Compiles smart contracts with Hardhat
  - Runs test suites (Hardhat, OV, OI)
  
- **Python Build**: Tests across Python 3.9, 3.10, and 3.11
  - Installs dependencies
  - Runs available Python tests
  
- **Code Quality**: Linting and code style checks
  - JavaScript/TypeScript linting
  - Python code analysis with flake8, black, pylint
  
- **Security**: Dependency vulnerability scanning
  - npm audit for Node.js packages
  - Safety checks for Python packages

### 2. Docker Build and Push (`docker.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Git tags matching `v*.*.*`
- Pull requests to `main`
- Manual workflow dispatch

**Features:**
- Multi-platform builds (linux/amd64, linux/arm64)
- Publishes to GitHub Container Registry (ghcr.io)
- Smart tagging strategy:
  - `latest` for main branch
  - Semantic version tags (e.g., `v1.2.3`, `v1.2`, `v1`)
  - Branch-specific tags
  - SHA-based tags
- Build caching for faster builds
- Security scanning with Trivy
- Build attestation for provenance

**Accessing Images:**
```bash
# Pull the latest image
docker pull ghcr.io/hannesmitterer/euystacio-helmi-ai:latest

# Pull a specific version
docker pull ghcr.io/hannesmitterer/euystacio-helmi-ai:v1.0.0
```

### 3. Deploy to Environments (`deploy-environments.yml`)

**Triggers:**
- Push to `main` → Staging deployment
- Release published → Production deployment
- Manual workflow dispatch (choose environment)

**Environments:**

#### Staging
- **Purpose**: Pre-production testing
- **Auto-deploy**: Yes (on main branch push)
- **URL**: https://euystacio-helmi-ai-staging.onrender.com (example)

#### Production
- **Purpose**: Live environment
- **Auto-deploy**: On release only
- **Manual approval**: Required for manual deploys
- **URL**: https://euystacio-helmi-ai.onrender.com (example)

**Manual Deployment:**
1. Go to Actions → Deploy to Environments
2. Click "Run workflow"
3. Select environment (staging/production)
4. Confirm deployment

### 4. Release and Publish (`release.yml`)

**Triggers:**
- Git tags matching `v*.*.*`
- Manual workflow dispatch with version input

**Process:**
1. Creates GitHub Release with changelog
2. Builds release artifacts (source, contracts)
3. Uploads artifacts to release
4. (Optional) Publishes to npm if configured
5. Triggers production deployment

**Creating a Release:**
```bash
# Tag a new version
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or use GitHub's release interface
```

### 5. CodeQL Security Analysis (`codeql-analysis.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests
- Weekly schedule (Monday 00:00 UTC)
- Manual workflow dispatch

**Security Checks:**
- CodeQL static analysis (JavaScript, Python)
- Dependency review on PRs
- Semgrep SAST scanning
- Bandit Python security checks
- TruffleHog secret scanning

### 6. Dependency Updates (`dependencies.yml`)

**Triggers:**
- Weekly schedule (Monday 09:00 UTC)
- Manual workflow dispatch

**Features:**
- Automated npm dependency updates
- Automated Python dependency updates
- Security vulnerability patching
- Automatic PR creation for updates

## Deployment Environments

### Local Development

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run the Node.js server
npm start

# Run the Python Flask app
python app.py

# Run with Docker
docker build -t euystacio-helmi-ai .
docker run -p 5000:5000 -p 3000:3000 euystacio-helmi-ai
```

### Environment Variables

Create a `.env` file based on `.env.example`:

```bash
# Copy example environment file
cp .env.example .env

# Edit with your values
nano .env
```

**Required Variables:**
- `PORT`: Server port (default: 5000)
- `NODE_ENV`: Environment (development/production)
- `GOOGLE_CLIENT_ID`: OAuth client ID
- `GOOGLE_CLIENT_SECRET`: OAuth client secret
- `JWT_SECRET_KEY`: JWT signing key
- `POLYGON_RPC_URL`: Blockchain RPC URL
- `PRIVATE_KEY`: Deployer private key

### Render Deployment

The project is configured for Render deployment via `render.yaml`:

```yaml
services:
- type: web
  name: Euystacio
  runtime: python
  buildCommand: pip install -r requirements.txt
  startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
  autoDeployTrigger: commit
```

**Deploy to Render:**
1. Connect your GitHub repository to Render
2. Configure environment variables in Render dashboard
3. Deployments happen automatically on push

### Netlify Deployment

For static site deployment, the project uses `netlify.toml`:

```toml
[build]
  command = "echo 'Build executed'"
  publish = "/"

[[redirects]]
  from = "/api/*"
  to = "https://euystacio-backend.srv-xyz.onrender.com/:splat"
  status = 200
```

## Docker Deployment

### Building the Image

```bash
# Build for local platform
docker build -t euystacio-helmi-ai .

# Build with version info
docker build \
  --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
  --build-arg VCS_REF=$(git rev-parse --short HEAD) \
  --build-arg VERSION=1.0.0 \
  -t euystacio-helmi-ai:1.0.0 .
```

### Running the Container

```bash
# Run with default command (Python app)
docker run -p 5000:5000 euystacio-helmi-ai

# Run with environment variables
docker run -p 5000:5000 \
  -e PORT=5000 \
  -e NODE_ENV=production \
  --env-file .env \
  euystacio-helmi-ai

# Run Node.js server instead
docker run -p 3000:3000 \
  euystacio-helmi-ai \
  node server.js
```

### Docker Compose (Optional)

Create `docker-compose.yml`:

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "5000:5000"
      - "3000:3000"
    env_file:
      - .env
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
```

Run with: `docker-compose up -d`

## Release Process

### Versioning Strategy

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** version: Breaking changes
- **MINOR** version: New features (backward compatible)
- **PATCH** version: Bug fixes (backward compatible)

### Creating a Release

1. **Update Version Numbers**
   ```bash
   # Update package.json version
   npm version patch  # or minor, or major
   ```

2. **Create and Push Tag**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```

3. **Automated Process**
   - GitHub Actions creates the release
   - Builds and uploads artifacts
   - Triggers production deployment

4. **Manual Process**
   - Go to GitHub → Releases → Draft a new release
   - Choose or create tag
   - Fill in release notes
   - Publish release

## Security

### Security Scanning

The project includes multiple security layers:

1. **CodeQL Analysis**: Detects code vulnerabilities
2. **Dependency Scanning**: Checks for vulnerable dependencies
3. **Secret Scanning**: Prevents secret leaks
4. **Container Scanning**: Scans Docker images with Trivy

### Security Best Practices

- Never commit secrets or API keys
- Use GitHub Secrets for sensitive data
- Regularly update dependencies
- Review security alerts in the Security tab
- Enable Dependabot alerts

### Setting Up Secrets

Add secrets in GitHub Settings → Secrets and variables → Actions:

- `RENDER_DEPLOY_HOOK_STAGING`: Render staging webhook
- `RENDER_DEPLOY_HOOK_PRODUCTION`: Render production webhook
- `NPM_TOKEN`: npm publishing token (if publishing packages)

## Monitoring and Maintenance

### Health Checks

The application includes health check endpoints:

```bash
# Check application health
curl https://your-domain.com/healthz
```

Docker health checks run automatically every 30 seconds.

### Logs and Debugging

```bash
# View Docker logs
docker logs <container-id>

# Follow logs in real-time
docker logs -f <container-id>

# View logs in Render
# Go to Render Dashboard → Your Service → Logs
```

### Workflow Status

Check workflow status:
- GitHub repository → Actions tab
- View logs for failed jobs
- Re-run failed workflows if needed

### Maintenance Windows

For production deployments:
1. Announce maintenance window
2. Deploy to staging first
3. Run smoke tests
4. Deploy to production
5. Monitor for issues

## Troubleshooting

### Common Issues

**Build fails on npm install:**
- Clear cache: `npm ci --cache .npm`
- Check Node.js version compatibility

**Python dependency conflicts:**
- Use virtual environment
- Pin versions in requirements.txt
- Clear pip cache

**Docker build fails:**
- Check Dockerfile syntax
- Verify base image availability
- Review build logs for errors

**Deployment fails:**
- Check environment variables
- Verify deployment hooks/credentials
- Review application logs

### Getting Help

- Check GitHub Actions logs
- Review this documentation
- Check existing issues
- Create new issue with details

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Documentation](https://docs.docker.com/)
- [Render Documentation](https://render.com/docs)
- [Netlify Documentation](https://docs.netlify.com/)

---

**Last Updated:** December 2025  
**Maintained By:** Euystacio Team
