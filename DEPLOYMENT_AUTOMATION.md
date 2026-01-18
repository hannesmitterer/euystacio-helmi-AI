# Auto-Deployment Configuration Guide

## Overview

This repository implements automated deployment via GitHub Actions with comprehensive security measures, NSR protocol compliance, and automatic rollback capabilities.

## Workflow: `auto-deploy.yml`

### Features

1. **Security Validation (SovereignShield)**
   - D6 Stealth Mode activation
   - Input audit validation via `audit_input` method
   - Malicious content detection and isolation
   - NTRU-Lattice-Base encryption verification

2. **Build Automation**
   - Automatic asset building from source
   - NSR configuration file validation
   - Build artifact verification

3. **Regional Priority Deployment**
   - Primary region deployment to GitHub Pages
   - Concurrent deployment control
   - Environment-specific configuration

4. **Automatic Rollback**
   - Post-deployment health checks
   - NSR latency compliance validation (max 2.71ms)
   - Automatic rollback on test failures

5. **NSR Protocol Compliance**
   - **NSR (Non-Slavery Resonance)**: Max latency validation
   - **OLF (One Love First)**: Continuous ethics improvement
   - **TFK (Tuttifruttikarma)**: Self-correction protocol

## SECRET_KEY Management

### GitHub Secrets Configuration

To ensure NSR protocol compliance and secure deployments, configure the following secrets in your GitHub repository:

#### Required Secrets

1. **SECRET_KEY** (Required for production)
   - Navigate to: Repository Settings → Secrets and variables → Actions
   - Click "New repository secret"
   - Name: `SECRET_KEY`
   - Value: Generate a secure random key (recommended: 64+ characters)
   
   ```bash
   # Generate a secure SECRET_KEY using Python
   python -c "import secrets; print(secrets.token_urlsafe(64))"
   ```

2. **POLYGON_RPC_URL** (Optional - for blockchain deployments)
   - Your Polygon RPC endpoint URL
   
3. **PRIVATE_KEY** (Optional - for blockchain deployments)
   - Your deployment private key (NEVER commit this to code)

### Environment Variables

The workflow uses the following environment variables:

- `NSR_MAX_LATENCY_MS`: Maximum allowed latency (default: 2.71ms)
- `NSR_MIN_DELTA_CSI`: Minimum delta for continuous ethics improvement (default: 0.000)
- `DEPLOYMENT_REGION`: Target deployment region (default: "primary")

### SECRET_KEY Usage

The SECRET_KEY is used for:
- JWT token signing and validation
- Session management security
- NSR protocol cryptographic operations
- OAuth state verification

**Security Best Practices:**
- Never hardcode SECRET_KEY in source code
- Use GitHub Secrets for production deployments
- Rotate keys periodically (recommended: every 90 days)
- Use different keys for different environments (dev, staging, prod)

## Workflow Jobs

### 1. Security Validation
- Activates D6 Stealth Mode
- Runs SovereignShield security tests
- Validates audit_input functionality
- Verifies SECRET_KEY configuration

### 2. Build Assets
- Validates NSR configuration files
- Builds static assets via `build_static.py`
- Verifies build artifacts
- Uploads artifacts for deployment

### 3. Regional Priority Deployment
- Deploys to primary region (GitHub Pages)
- Only runs on `main` branch
- Requires NSR compliance validation
- Provides deployment URL

### 4. Post-Deployment Validation
- Runs security tests on deployed version
- Validates deployment health
- Checks NSR latency requirements
- Triggers rollback on failure

### 5. Deployment Summary
- Generates comprehensive deployment report
- Shows status of all jobs
- Reports NSR compliance status

## Triggering Deployments

### Automatic Deployment
- Push to `main` branch triggers full deployment
- Pull requests run validation and build only (no deployment)

### Manual Deployment
Use workflow_dispatch to manually trigger deployment:
```bash
# Via GitHub UI: Actions → Auto-Deploy → Run workflow

# Via GitHub CLI
gh workflow run auto-deploy.yml
```

## Rollback Mechanism

The workflow includes automatic rollback on failures:

1. **Detection**: Post-deployment validation runs comprehensive tests
2. **Trigger**: Any test failure activates rollback protocol
3. **Action**: Workflow fails with clear error message
4. **Recovery**: Previous deployment remains active (no broken state)

### Manual Rollback

If needed, rollback manually by:
```bash
# Revert the problematic commit
git revert <commit-hash>

# Push to trigger new deployment with previous code
git push origin main
```

## NSR Compliance Checks

The workflow validates NSR protocol requirements:

1. **Max Latency Check**: Response time < 2.71ms
2. **Configuration Validation**: Required NSR files present
3. **Security Metrics**: Proof of Witness validation
4. **Ethics Alignment**: Continuous System Integrity improvement

## Monitoring Deployment

### View Deployment Status
1. Go to repository Actions tab
2. Select "Auto-Deploy with Security & NSR Compliance"
3. View real-time job execution

### Deployment Logs
Each job provides detailed logs showing:
- Security validation results
- Build process output
- Deployment status
- NSR compliance metrics

## Troubleshooting

### Common Issues

**Issue**: SECRET_KEY warning on main branch
**Solution**: Configure SECRET_KEY in GitHub Secrets (see above)

**Issue**: NSR validation fails
**Solution**: Ensure `Proof_of_Witness.md` contains required NSR metrics

**Issue**: Build artifacts not found
**Solution**: Check `build_static.py` runs successfully and creates `docs/` directory

**Issue**: Deployment fails post-validation
**Solution**: Review security test failures and ensure NSR latency requirements met

## Security Considerations

1. **Never commit secrets** to the repository
2. **Use GitHub Secrets** for all sensitive data
3. **Enable branch protection** on main branch
4. **Require PR reviews** before merging to main
5. **Monitor security alerts** in GitHub Security tab

## Additional Resources

- [SovereignShield Security Implementation](security_fusion.py)
- [NSR Protocol Specification](Proof_of_Witness.md)
- [Build System Documentation](BUILD_INSTRUCTIONS.md)
- [Deployment Guide](DEPLOYMENT_GUIDE.md)
