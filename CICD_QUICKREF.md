# CI/CD Quick Reference

A quick reference guide for the Euystacio Helmi AI CI/CD workflows.

## Workflow Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| **build.yml** | Push/PR to main/develop | Build and test all components |
| **docker-build-push.yml** | Push to main/develop, tags | Build and push Docker images |
| **deploy-staging.yml** | Push to develop | Deploy to staging environment |
| **deploy-production.yml** | Push tag v*.*.* | Deploy to production |
| **deploy-contracts.yml** | Manual only | Deploy smart contracts |
| **release-publish.yml** | Push tag v*.*.* | Create GitHub Release |

## Common Tasks

### Start a New Feature
```bash
git checkout -b feature/my-feature
# Make changes
git commit -m "Add new feature"
git push origin feature/my-feature
# Create PR → Triggers build.yml
```

### Deploy to Staging
```bash
git checkout develop
git merge feature/my-feature
git push origin develop
# Triggers: build.yml, docker-build-push.yml, deploy-staging.yml
```

### Deploy to Production
```bash
git checkout main
git merge develop
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin main
git push origin v1.0.0
# Triggers: build.yml, docker-build-push.yml, deploy-production.yml, release-publish.yml
```

### Deploy Smart Contracts
1. Go to Actions tab
2. Select "Deploy Smart Contracts"
3. Click "Run workflow"
4. Choose network and environment
5. Click "Run workflow"

### Build Docker Image Locally
```bash
docker build -t euystacio-helmi-ai:local .
docker run -p 3000:3000 euystacio-helmi-ai:local
```

## Docker Image Tags

| Tag Pattern | Example | Description |
|-------------|---------|-------------|
| `latest` | `latest` | Latest from main branch |
| `develop` | `develop` | Latest from develop branch |
| `v*.*.*` | `v1.0.0` | Specific version |
| `*.*` | `1.0` | Major.minor version |
| `*` | `1` | Major version |
| `branch-sha` | `main-abc1234` | Branch + commit SHA |

## Required Secrets

### Deployment Secrets
- `RENDER_DEPLOY_HOOK_STAGING` - Staging deploy webhook
- `RENDER_DEPLOY_HOOK_PRODUCTION` - Production deploy webhook

### Smart Contract Secrets
- `SEPOLIA_RPC_URL` - Sepolia RPC endpoint
- `POLYGON_RPC_URL` - Polygon RPC endpoint
- `PRIVATE_KEY_DEPLOYER` - Deployer wallet key
- `FOUNDATION_WALLET` - Foundation address
- `STABLE_TOKEN_ADDRESS` - Stable token address
- `SUSTAINMENT_MIN_USD` - Min sustainment (e.g., "10000")
- `SUSTAINMENT_PERCENT_BPS` - Percent BPS (e.g., "200")

### Optional Secrets
- `DOCKERHUB_USERNAME` - Docker Hub username
- `DOCKERHUB_TOKEN` - Docker Hub token
- `NPM_TOKEN` - npm registry token
- `PYPI_TOKEN` - PyPI token

## Environment Setup

### Staging Environment
- Name: `staging`
- Deployment branch: `develop`
- Protection: Optional
- URL: Configure in workflow

### Production Environment
- Name: `production`
- Deployment branch: Tags only
- Protection: **Recommended** (required reviewers)
- URL: Configure in workflow

## Build Commands

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Compile contracts
npm run compile

# Run tests
npm test                    # All contract tests
npm run test:sustainment    # Sustainment tests
npm run test:ov             # OV authentication tests
npm run test:oi             # OI environment tests
npm run test:all            # All tests (102 tests)

# Build static pages
python build_static.py

# Docker
docker-compose up -d        # Start with compose
docker-compose down         # Stop services
docker build -t app .       # Build image
docker run -p 3000:3000 app # Run container
```

## Workflow Outputs

### Build Artifacts
- Contract compilation artifacts
- Test results
- Static site builds

### Docker Images
- `ghcr.io/hannesmitterer/euystacio-helmi-ai:TAG`
- Multi-platform: linux/amd64, linux/arm64

### Release Artifacts
- Source code (zip, tar.gz)
- Compiled contracts
- Documentation bundle

### Deployment Records
- Location: `deployments/{network}/`
- Format: JSON with timestamp, addresses, config

## Health Checks

### Application Health
```bash
curl http://localhost:3000/healthz
# Response: {"status":"ok","time":"2025-12-12T00:00:00.000Z"}
```

### Docker Health
```bash
docker ps --filter "name=euystacio" --format "{{.Status}}"
# Shows: Up X seconds (healthy)
```

### Deployment Health
- Staging: Check workflow run status
- Production: Automated health check in workflow

## Troubleshooting

### Build Fails
- Check Actions logs
- Verify dependencies in package.json/requirements.txt
- Run `npm install` and `npm test` locally

### Docker Build Fails
- Check Dockerfile syntax
- Verify base images are available
- Review build logs for specific errors

### Deployment Fails
- Verify secrets are configured
- Check deployment service logs
- Review health check endpoints

### Contract Deployment Fails
- Ensure RPC URLs are accessible
- Verify deployer has sufficient balance
- Check hardhat.config.js network config

## Monitoring

### Check Workflow Status
1. Go to Actions tab
2. View recent workflow runs
3. Click run for detailed logs

### Check Deployments
1. Go to Code tab
2. Click Deployments (right side)
3. View deployment history

### Check Releases
1. Go to Releases section
2. View all published releases
3. Download artifacts

## Quick Links

- [Full CI/CD Documentation](CICD.md)
- [Implementation Summary](CICD_SUMMARY.md)
- [Workflows Directory](.github/workflows/)
- [Deployment Records](deployments/)

---

For detailed information, see [CICD.md](CICD.md)
