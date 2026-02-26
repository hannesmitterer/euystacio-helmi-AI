# CI/CD Quick Reference Guide

Quick reference for developers working with the Euystacio Helmi AI CI/CD pipelines.

## 🚀 Quick Commands

### Local Development

```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run tests
npm test              # Smart contract tests
npm run test:ov       # OV authentication tests
npm run test:oi       # OI environment tests
npm run test:all      # All tests

# Build
npm run compile       # Compile smart contracts

# Run locally
npm start             # Node.js server
python app.py         # Python Flask app
```

### Docker

```bash
# Build image
docker build -t euystacio-helmi-ai .

# Run container
docker run -p 5000:5000 -p 3000:3000 euystacio-helmi-ai

# Using docker-compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Git Workflow

```bash
# Create feature branch
git checkout -b feat/your-feature

# Commit with conventional commits
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update README"

# Push and create PR
git push origin feat/your-feature
```

## 🔄 CI/CD Workflows

### Automatic Triggers

| Workflow | Trigger | Purpose |
|----------|---------|---------|
| CI Build & Test | Push/PR to main | Run tests and build checks |
| Docker Build | Push to main/develop | Build and push container images |
| GitHub Pages | Push to main | Deploy static documentation |
| CodeQL | Push/PR/Weekly | Security scanning |
| Dependencies | Weekly | Update dependencies |

### Manual Triggers

All workflows can be triggered manually via GitHub Actions UI:
1. Go to **Actions** tab
2. Select workflow
3. Click **Run workflow**
4. Choose parameters (if any)

## 📦 Release Process

### Creating a Release

```bash
# Update version
npm version patch  # 1.0.0 -> 1.0.1
npm version minor  # 1.0.0 -> 1.1.0
npm version major  # 1.0.0 -> 2.0.0

# Create and push tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

This automatically:
- Creates GitHub Release
- Builds artifacts
- Triggers production deployment
- Publishes to registries (if configured)

### Deployment Environments

| Environment | URL | Deployment |
|-------------|-----|------------|
| Staging | https://euystacio-helmi-ai-staging.onrender.com | Auto on main push |
| Production | https://euystacio-helmi-ai.onrender.com | On release or manual |
| GitHub Pages | https://hannesmitterer.github.io/euystacio-helmi-AI | Auto on main push |

## 🔒 Security

### Required Secrets

Set in **Settings → Secrets → Actions**:

```
RENDER_DEPLOY_HOOK_STAGING      # Staging deployment webhook
RENDER_DEPLOY_HOOK_PRODUCTION   # Production deployment webhook
NPM_TOKEN                        # npm publishing (optional)
```

### Security Checks

Every PR runs:
- ✅ CodeQL analysis (JavaScript, Python)
- ✅ Dependency scanning
- ✅ Secret scanning
- ✅ SAST with Semgrep
- ✅ Container vulnerability scan

## 📝 Conventional Commits

Use semantic commit messages:

```
feat: add new feature
fix: resolve bug
docs: update documentation
style: format code
refactor: restructure code
perf: improve performance
test: add tests
build: update build system
ci: modify CI/CD
chore: routine tasks
revert: revert changes
```

## 🐛 Troubleshooting

### CI Build Fails

```bash
# Check logs in GitHub Actions
# Fix issues locally first
npm test
npm run compile

# Then commit and push
```

### Docker Build Fails

```bash
# Test locally
docker build -t test .

# Check Dockerfile syntax
# Verify dependencies are correct
```

### Deployment Fails

1. Check workflow logs
2. Verify environment variables
3. Check deployment hook/credentials
4. Review application logs in hosting platform

## 📊 Monitoring

### Workflow Status

- **Badge in README**: Shows current status
- **Actions Tab**: Full workflow history
- **Email Notifications**: Configure in GitHub settings

### Health Checks

- Daily workflow health monitoring
- Automatic issue creation on failures
- Health check endpoints in application

## 🔧 Customization

### Modify Workflows

Edit files in `.github/workflows/`:
- `ci.yml` - Build and test configuration
- `docker.yml` - Container build settings
- `deploy-environments.yml` - Deployment configuration
- `codeql-analysis.yml` - Security scanning
- `dependencies.yml` - Dependency updates

### Add New Workflow

1. Create `.github/workflows/your-workflow.yml`
2. Define triggers and jobs
3. Test with `workflow_dispatch` trigger
4. Commit and push

## 📚 Resources

- [Full Deployment Guide](CICD_DEPLOYMENT.md)
- [Workflows Documentation](WORKFLOWS.md)
- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Docker Docs](https://docs.docker.com/)

## 🆘 Getting Help

- Check existing [Issues](https://github.com/hannesmitterer/euystacio-helmi-AI/issues)
- Review [Discussions](https://github.com/hannesmitterer/euystacio-helmi-AI/discussions)
- Create new issue with `question` label

---

**Last Updated:** December 2025
