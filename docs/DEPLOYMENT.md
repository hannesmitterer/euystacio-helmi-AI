# 🌳 Euystacio Dashboard Deployment Guide

## Firewall Configuration & GitHub Actions Setup

This guide provides comprehensive instructions for deploying the Euystacio Dashboard while addressing firewall considerations for GitHub Actions and dependency management.

---

## 🔥 Firewall Configuration Requirements

### **IMPORTANT: Configure These Settings BEFORE Enabling Strict Firewall Rules**

GitHub Actions and the deployment process require access to several external services. Configure your firewall to allow these connections:

### Core GitHub Services
```
# GitHub.com - Required for repository access
github.com:443
api.github.com:443
raw.githubusercontent.com:443
objects.githubusercontent.com:443
ghcr.io:443

# GitHub Actions Infrastructure
actions-results-receiver-production.githubapp.com:443
pipelines.actions.githubusercontent.com:443
vscode.tunnel.azure.com:443
```

### Python Package Index (PyPI)
```
# PyPI - Required for pip install commands
pypi.org:443
pypi.python.org:443
files.pythonhosted.org:443

# CDN and mirrors
*.ssl.fastly.com:443
*.global.ssl.fastly.com:443
```

### Container Registry (if using Docker)
```
# Docker Hub
registry-1.docker.io:443
index.docker.io:443
dseasb33srnrn.cloudfront.net:443

# GitHub Container Registry
ghcr.io:443
```

### Deployment Targets (Configure as needed)
```
# Heroku
api.heroku.com:443
git.heroku.com:443

# Digital Ocean
api.digitalocean.com:443
*.digitaloceanspaces.com:443

# Railway
railway.app:443
api.railway.app:443

# Vercel
api.vercel.com:443
vercel.com:443
```

---

## 🔧 Pre-Deployment Setup

### 1. Environment Preparation

**Before enabling firewall restrictions:**

```bash
# Test connectivity to required services
curl -I https://api.github.com
curl -I https://pypi.org
curl -I https://files.pythonhosted.org

# Verify Python package installation works
pip install flask --dry-run
```

### 2. GitHub Actions Secrets Configuration

Set up the following secrets in your GitHub repository:

- `HEROKU_API_KEY` (if deploying to Heroku)
- `DIGITALOCEAN_ACCESS_TOKEN` (if deploying to Digital Ocean)
- `RAILWAY_TOKEN` (if deploying to Railway)

**Path:** Repository → Settings → Secrets and variables → Actions

### 3. Dependencies Pre-caching

To minimize external requests during deployment, consider pre-caching dependencies:

```bash
# Create a requirements hash for caching
pip-compile requirements.txt > requirements.lock

# Pre-download wheels
pip download -r requirements.txt -d wheels/
```

---

## 🚀 Deployment Options

### Option 1: Heroku Deployment

```yaml
# Add to .github/workflows/deploy.yml
- name: Deploy to Heroku
  uses: akhileshns/heroku-deploy@v3.12.14
  with:
    heroku_api_key: ${{ secrets.HEROKU_API_KEY }}
    heroku_app_name: "euystacio-dashboard"
    heroku_email: "your-email@example.com"
```

**Firewall Requirements for Heroku:**
- `api.heroku.com:443`
- `git.heroku.com:443`

### Option 2: Digital Ocean App Platform

```yaml
# Add to .github/workflows/deploy.yml
- name: Deploy to Digital Ocean
  uses: digitalocean/app_action@v1.1.5
  with:
    app_name: euystacio-dashboard
    token: ${{ secrets.DIGITALOCEAN_ACCESS_TOKEN }}
```

**Firewall Requirements for Digital Ocean:**
- `api.digitalocean.com:443`
- `*.digitaloceanspaces.com:443`

### Option 3: Railway

```bash
# Install Railway CLI in workflow
npm install -g @railway/cli

# Deploy
railway deploy
```

**Firewall Requirements for Railway:**
- `railway.app:443`
- `api.railway.app:443`

---

## 🛡️ Security Best Practices

### 1. Staged Firewall Implementation

**Recommended approach:**

1. **Phase 1**: Deploy with open firewall
2. **Phase 2**: Allow listed domains/IPs
3. **Phase 3**: Enable strict mode
4. **Phase 4**: Monitor and adjust

### 2. Network Monitoring

```bash
# Monitor outbound connections during deployment
netstat -ant | grep :443
ss -tuln | grep :443

# Log DNS queries
dig +trace github.com
dig +trace pypi.org
```

### 3. Fallback Strategies

If strict firewall causes issues:

```bash
# Use internal package mirror
pip install -i http://internal-pypi.company.com/simple/ flask

# Use pre-downloaded wheels
pip install --no-index --find-links wheels/ flask

# Offline installation
pip install --no-deps package.whl
```

---

## 📋 Deployment Checklist

### Pre-Deployment
- [ ] **Firewall allow-list configured** with all required domains
- [ ] **GitHub Actions secrets** configured for chosen deployment platform
- [ ] **Dependencies tested** with current network restrictions
- [ ] **Repository permissions** verified for GitHub Actions
- [ ] **Deployment target** (Heroku/DO/Railway) account and app configured

### During Deployment
- [ ] **Monitor GitHub Actions logs** for network-related failures
- [ ] **Check firewall logs** for blocked connections
- [ ] **Verify all API endpoints** are accessible
- [ ] **Test dashboard functionality** post-deployment

### Post-Deployment
- [ ] **Dashboard accessibility** confirmed
- [ ] **All features working** (pulse submission, data loading)
- [ ] **SSL certificate** properly configured
- [ ] **Domain configuration** completed
- [ ] **Monitoring** and alerting set up

---

## 🔧 Troubleshooting Common Firewall Issues

### Issue: pip install fails
```bash
# Solution: Add PyPI domains to allow-list
pypi.org:443
files.pythonhosted.org:443
*.ssl.fastly.com:443
```

### Issue: GitHub Actions checkout fails
```bash
# Solution: Add GitHub domains to allow-list
github.com:443
api.github.com:443
objects.githubusercontent.com:443
```

### Issue: Deployment to platform fails
```bash
# Solution: Add platform-specific domains
# See deployment options section above
```

### Issue: Container registry access fails
```bash
# Solution: Add container registry domains
registry-1.docker.io:443
ghcr.io:443
```

---

## 🌍 Environment Variables

### Required for Production

```env
# Flask Configuration
FLASK_ENV=production
SECRET_KEY=your-secret-key-here

# Dashboard Configuration
EUYSTACIO_LOG_LEVEL=INFO
EUYSTACIO_DEBUG=false

# Optional: External Integrations
DATABASE_URL=your-database-url
REDIS_URL=your-redis-url
```

### Security Configuration

```env
# HTTPS Enforcement
FORCE_HTTPS=true

# CORS Configuration
ALLOWED_ORIGINS=https://yourdomain.com

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_PER_MINUTE=60
```

---

## 📊 Monitoring & Maintenance

### Health Check Endpoints

The dashboard includes these monitoring endpoints:

- `GET /api/red_code` - Core system status
- `GET /api/pulses` - Pulse system health
- `GET /api/tutors` - Tutor system status
- `GET /api/reflections` - Reflection system health

### Performance Monitoring

```bash
# Monitor response times
curl -w "@curl-format.txt" -s -o /dev/null https://your-dashboard.com/api/red_code

# Check resource usage
htop
iostat 1
```

### Log Monitoring

```bash
# Monitor application logs
tail -f /var/log/euystacio/app.log

# Monitor access logs
tail -f /var/log/nginx/access.log
```

---

## 🎯 Next Steps

1. **Choose your deployment platform** (Heroku, Digital Ocean, Railway, etc.)
2. **Configure firewall rules** using the provided domain lists
3. **Set up GitHub Actions secrets** for your chosen platform
4. **Test the deployment process** in a staging environment first
5. **Monitor the deployment** and adjust firewall rules as needed

---

## 📞 Support

If you encounter firewall-related deployment issues:

1. **Check GitHub Actions logs** for specific error messages
2. **Review firewall logs** for blocked connections
3. **Verify domain allow-lists** against the requirements above
4. **Test connectivity** to required services manually

Remember: **"Presence before perfection. Rhythm before logic."** 🌳

The dashboard is designed to be resilient and gracefully handle network restrictions while maintaining its core functionality.