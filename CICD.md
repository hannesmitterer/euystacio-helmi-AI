# CI/CD Workflows Documentation

## Overview

This repository implements comprehensive CI/CD workflows for automated build, test, deployment, and publishing processes. The workflows follow modern DevOps practices and ensure scalable, reliable deployments.

## Workflows

### 1. Build and Test (`build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches
- Manual workflow dispatch

**Jobs:**
- **build-node**: Builds Node.js components and compiles smart contracts
- **build-python**: Builds Python components and static pages
- **validate-config**: Validates YAML and JSON configuration files
- **security-scan**: Runs security audits on dependencies

**Artifacts:**
- Contract compilation artifacts
- Test results
- Static build output

### 2. Docker Build and Push (`docker-build-push.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Push of version tags (`v*.*.*`)
- Pull requests to `main`
- Manual workflow dispatch

**Features:**
- Multi-stage Docker builds for optimized image size
- Multi-platform builds (linux/amd64, linux/arm64)
- Pushes to GitHub Container Registry (GHCR)
- Optional Docker Hub integration
- Image tagging strategy:
  - `latest` for main branch
  - `develop` for develop branch
  - Semantic versioning for tags (e.g., `v1.0.0`, `1.0`, `1`)
  - SHA-based tags for commit traceability

**Registry:**
- Primary: GitHub Container Registry (`ghcr.io`)
- Optional: Docker Hub (configure secrets)

### 3. Deploy to Staging (`deploy-staging.yml`)

**Triggers:**
- Push to `develop` branch
- Manual workflow dispatch

**Environment:** `staging`

**Features:**
- Automated deployment to staging environment
- Deployment tracking via GitHub Deployments
- Health check verification
- Smoke tests after deployment
- Supports multiple cloud providers:
  - Render.com (default)
  - AWS ECS (configurable)
  - Google Cloud Run (configurable)

### 4. Deploy to Production (`deploy-production.yml`)

**Triggers:**
- Push of version tags (`v*.*.*`)
- Manual workflow dispatch with version input

**Environment:** `production`

**Features:**
- Version validation
- Automated deployment to production
- Enhanced health checks with retries
- Automatic GitHub Release creation
- Production verification tests
- Deployment tracking and rollback support

### 5. Deploy Smart Contracts (`deploy-contracts.yml`)

**Triggers:**
- Manual workflow dispatch only (for safety)

**Inputs:**
- `network`: Target blockchain network (sepolia, polygon, hardhat)
- `environment`: Deployment environment (staging, production)

**Features:**
- Smart contract compilation
- Network configuration validation
- Automated deployment using Hardhat
- Deployment artifact creation
- Deployment record tracking (committed to repo)
- Contract verification support

**Required Secrets:**
- `SEPOLIA_RPC_URL` - Sepolia testnet RPC URL
- `POLYGON_RPC_URL` - Polygon mainnet RPC URL
- `PRIVATE_KEY_DEPLOYER` - Deployer wallet private key
- `FOUNDATION_WALLET` - Foundation wallet address
- `STABLE_TOKEN_ADDRESS` - Stable token contract address
- `SUSTAINMENT_MIN_USD` - Minimum sustainment amount
- `SUSTAINMENT_PERCENT_BPS` - Sustainment percentage in basis points

### 6. Release and Publish (`release-publish.yml`)

**Triggers:**
- Push of version tags (`v*.*.*`)
- Manual workflow dispatch

**Jobs:**
- **create-release**: Creates GitHub Release with changelog
- **build-artifacts**: Builds and packages release artifacts
- **publish-npm**: Publishes to npm (optional, disabled by default)
- **publish-pypi**: Publishes to PyPI (optional, disabled by default)
- **notify-release**: Creates deployment summary

**Artifacts:**
- Source code archives (zip, tar.gz)
- Compiled contract artifacts
- Documentation bundle
- Release packages

## Deployment Environments

### Staging
- **Purpose**: Pre-production testing
- **Branch**: `develop`
- **URL**: Configure in workflow (e.g., `https://euystacio-staging.onrender.com`)
- **Auto-deploy**: Yes (on push to develop)

### Production
- **Purpose**: Live production system
- **Branch**: Version tags (`v*.*.*`)
- **URL**: Configure in workflow (e.g., `https://euystacio.onrender.com`)
- **Auto-deploy**: Yes (on version tag push)
- **Manual trigger**: Available with version selection

## Setup Instructions

### 1. Configure GitHub Secrets

Navigate to **Settings → Secrets and variables → Actions** and add:

#### Required for Deployments:
- `RENDER_DEPLOY_HOOK_STAGING` - Render.com staging deploy hook URL
- `RENDER_DEPLOY_HOOK_PRODUCTION` - Render.com production deploy hook URL

#### Required for Smart Contract Deployments:
- `SEPOLIA_RPC_URL` - Sepolia testnet RPC endpoint
- `POLYGON_RPC_URL` - Polygon mainnet RPC endpoint
- `PRIVATE_KEY_DEPLOYER` - Deployer wallet private key (keep secure!)
- `PRIVATE_KEY` - Alternative private key
- `FOUNDATION_WALLET` - Foundation wallet address
- `STABLE_TOKEN_ADDRESS` - Stable token contract address
- `SUSTAINMENT_MIN_USD` - Minimum sustainment amount (e.g., "10000")
- `SUSTAINMENT_PERCENT_BPS` - Sustainment percentage in BPS (e.g., "200" for 2%)

#### Optional for Docker Hub:
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub access token

#### Optional for Package Publishing:
- `NPM_TOKEN` - npm registry token
- `PYPI_TOKEN` - PyPI registry token

### 2. Configure GitHub Environments

Navigate to **Settings → Environments** and create:

1. **staging**
   - Deployment branch: `develop`
   - Protection rules: Optional (e.g., required reviewers)

2. **production**
   - Deployment branch: Tags only (`refs/tags/v*`)
   - Protection rules: Recommended (e.g., required reviewers, wait timer)

### 3. Enable GitHub Pages (for documentation)

Navigate to **Settings → Pages**:
- Source: GitHub Actions
- The `deploy.yml` workflow handles deployment

## Usage

### Building and Testing

Push to `main` or `develop`, or create a pull request:
```bash
git push origin main
```

The build workflow automatically runs and validates:
- Node.js dependencies and smart contracts
- Python dependencies and static builds
- Configuration files (YAML, JSON)
- Security vulnerabilities

### Deploying to Staging

Push to the `develop` branch:
```bash
git checkout develop
git merge feature-branch
git push origin develop
```

Staging deployment runs automatically.

### Deploying to Production

Create and push a version tag:
```bash
git checkout main
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

Production deployment runs automatically and creates a GitHub Release.

Alternatively, manually trigger via GitHub Actions UI:
1. Go to **Actions → Deploy to Production**
2. Click **Run workflow**
3. Enter version tag (e.g., `v1.0.0`)

### Deploying Smart Contracts

**Important**: Smart contract deployment is manual-only for safety.

1. Go to **Actions → Deploy Smart Contracts**
2. Click **Run workflow**
3. Select:
   - Network: `sepolia`, `polygon`, or `hardhat`
   - Environment: `staging` or `production`
4. Click **Run workflow**

The workflow will:
- Compile contracts
- Validate network configuration
- Deploy to selected network
- Create deployment record
- Commit deployment info to repository

### Creating a Release

Releases are automatically created when pushing version tags:
```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

The release workflow will:
- Generate changelog from commits
- Build release artifacts
- Create GitHub Release
- Upload source and binary artifacts

### Building Docker Images

Docker images are automatically built and pushed:

**For development:**
```bash
git push origin develop
```
Creates image tagged as `develop`

**For production:**
```bash
git tag v1.0.0
git push origin v1.0.0
```
Creates images tagged as `v1.0.0`, `1.0`, `1`, and `latest`

**Pull images:**
```bash
# Latest from main branch
docker pull ghcr.io/hannesmitterer/euystacio-helmi-ai:latest

# Specific version
docker pull ghcr.io/hannesmitterer/euystacio-helmi-ai:v1.0.0

# Development version
docker pull ghcr.io/hannesmitterer/euystacio-helmi-ai:develop
```

## Local Development

### Using Docker Compose

Start the entire stack locally:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f euystacio
```

Stop services:
```bash
docker-compose down
```

### Building Docker Image Locally

```bash
docker build -t euystacio-helmi-ai:local .
docker run -p 3000:3000 euystacio-helmi-ai:local
```

### Running Without Docker

Install dependencies:
```bash
npm install
pip install -r requirements.txt
```

Compile contracts:
```bash
npm run compile
```

Run tests:
```bash
npm test
```

Start server:
```bash
npm start
```

## Workflow Monitoring

### View Workflow Runs
Navigate to **Actions** tab in GitHub repository.

### Deployment Status
Navigate to **Deployments** section (in code tab) for deployment history.

### Release History
Navigate to **Releases** section for all published releases.

## Troubleshooting

### Build Failures
- Check workflow logs in Actions tab
- Verify all dependencies are correctly specified
- Ensure configuration files are valid

### Deployment Failures
- Verify environment secrets are correctly configured
- Check deployment service logs (Render, AWS, etc.)
- Review health check endpoints

### Smart Contract Deployment Issues
- Ensure RPC URLs are accessible
- Verify deployer account has sufficient balance
- Check network configuration in hardhat.config.js
- Review contract compilation output

### Docker Build Issues
- Verify Dockerfile syntax
- Check base image availability
- Ensure all COPY paths exist
- Review build logs for specific errors

## Security Best Practices

1. **Never commit secrets** - Always use GitHub Secrets
2. **Review contract deployments** - Smart contracts are immutable
3. **Test in staging first** - Always test in staging before production
4. **Use environment protection** - Configure required reviewers for production
5. **Rotate credentials regularly** - Update API keys and tokens periodically
6. **Monitor deployments** - Set up alerts for failed deployments
7. **Audit dependencies** - Review security scan results regularly

## Integration with Existing Workflows

The new CI/CD workflows integrate with existing repository workflows:
- `integrity.yml` - Auto-integrity & compliance checks
- `deploy.yml` - GitHub Pages deployment (renamed from original)
- `framework-configuration.yml` - Framework validation
- `treasury-sustainability.yml` - Treasury monitoring
- `governance-framework.yml` - Governance validation

All workflows can run independently and in parallel without conflicts.

## Versioning Strategy

### Semantic Versioning
Follow [Semantic Versioning 2.0.0](https://semver.org/):
- `MAJOR.MINOR.PATCH` (e.g., `v1.0.0`)
- Increment MAJOR for breaking changes
- Increment MINOR for new features
- Increment PATCH for bug fixes

### Tagging Convention
```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0: Initial production release"

# Push tag to trigger release
git push origin v1.0.0
```

## Support

For issues or questions:
1. Check existing workflow runs in Actions tab
2. Review deployment logs
3. Consult this documentation
4. Open an issue in the repository

---

**Last Updated**: 2025-12-12  
**Maintained by**: Euystacio Framework Team  
**License**: MIT
