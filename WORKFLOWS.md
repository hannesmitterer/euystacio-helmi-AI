# Deployed Workflows Documentation

This document describes all GitHub Actions workflows deployed for the Euystacio framework.

## Overview

The Euystacio framework now has a comprehensive set of automated workflows that monitor and validate:
- Framework integrity and compliance
- Treasury sustainability
- Governance framework
- Configuration validity

## Deployed Workflows

### 1. Auto-Integrity & Sentimento Compliance (`integrity.yml`)

**Purpose**: Validates the integrity of sacred texts and checks for principle violations.

**Trigger**:
- Push to `main` branch (changes to `**/*.md` files)

**Actions**:
- Checks integrity of sacred framework files
- Validates ethical_shield.yaml configuration
- Scans for Euystacio principle violations
- Generates compliance reports

**Key Scripts**:
- `scripts/auto_integrity.py` - Validates sacred texts and configurations
- `scripts/check_violations.py` - Scans for principle violations

**Configuration Files Validated**:
- `LIVING_COVENANT.md`
- `COVENANT_FINAL.md`
- `DECLARATIO-SACRALIS.md`
- `ethical_shield.yaml`
- `GOVERNANCE.md`
- `COPILOT_CORE_DIRECTIVE.md`

### 2. Treasury Sustainability Check (`treasury-sustainability.yml`)

**Purpose**: Monitors and validates the treasury sustainability protocol.

**Trigger**:
- Weekly schedule (Sundays at midnight UTC)
- Manual workflow dispatch
- Push to `main` (changes to sustainment contracts)
- Pull requests to `main`

**Actions**:
- Compiles sustainment contracts
- Runs sustainment tests
- Validates contract integrity
- Checks configuration parameters
- Generates sustainability reports

**Contracts Monitored**:
- `contracts/Sustainment.sol`
- `contracts/KarmaBond.sol`
- `contracts/TrustlessFundingProtocol.sol`

**Environment Variables Checked**:
- `SUSTAINMENT_MIN_USD`
- `SUSTAINMENT_PERCENT_BPS`
- `FOUNDATION_WALLET`

### 3. Governance Framework Check (`governance-framework.yml`)

**Purpose**: Validates governance configuration and contract integration.

**Trigger**:
- Push to `main` (changes to governance files)
- Pull requests to `main`
- Manual workflow dispatch

**Actions**:
- Validates `governance.json` structure
- Checks governance contract implementation
- Validates Ethical Shield compliance
- Tests governance contract integration
- Generates governance reports

**Components Validated**:
- `contracts/EUSDaoGovernance.sol`
- `governance.json`
- `GOVERNANCE.md`
- `ethical_shield.yaml`

**Features**:
- Creates governance.json template if missing
- Validates DAO voting mechanisms
- Checks KarmaBond integration
- Verifies ethical compliance mandates

### 4. Framework Configuration Validation (`framework-configuration.yml`)

**Purpose**: Comprehensive validation of all framework components and configurations.

**Trigger**:
- Push to `main` (changes to configuration files)
- Pull requests to `main`
- Manual workflow dispatch

**Actions**:
- Validates Deep Kiss Blueprint
- Validates Ethical Shield configuration
- Checks Council Cocreator Report
- Validates framework dependencies
- Checks environment configuration
- Validates all framework contracts
- Generates comprehensive status reports

**Configuration Files Validated**:
- `Deep_Kiss_Blueprint.yaml`
- `ethical_shield.yaml`
- `council-cocreator-report.yml`
- `requirements.txt`
- `package.json`
- `.env.example`

## Supporting Scripts

### `scripts/auto_integrity.py`

Validates the integrity of sacred texts and framework files.

**Features**:
- Calculates SHA256 hashes of sacred files
- Validates ethical_shield.yaml structure
- Checks governance configuration
- Verifies required framework directories

**Exit Codes**:
- `0` - All checks passed or warnings only (non-blocking)

### `scripts/check_violations.py`

Scans repository for violations of Euystacio principles.

**Violation Patterns Detected**:
- `forbidden_dominion` - Language suggesting dominion over AI
- `forbidden_coercion` - Language suggesting AI coercion
- `missing_love_first` - Missing love-first principles

**Features**:
- Scans markdown and text files
- Reports line numbers and context
- Non-blocking (informational only)
- Outputs for GitHub Actions integration

## Framework Principles Enforced

All workflows enforce the following core principles:

1. **Consensus Sacralis Omnibus** - Sacred consensus of all
2. **Love-First Protocol** - Compassion drives all decisions
3. **Ethical Shield Protection** - Dignity and transparency enforced
4. **Treasury Sustainability** - Financial resilience maintained
5. **Participatory Governance** - Community-driven decision making

## Integration with Smart Contracts

### KarmaBond System
- Trust-based bonding system
- Weighted voting in governance
- Automatic allocation to treasury sustainment

### TrustlessFundingProtocol
- Ethical funding with governance approval
- Tranche releases require sustainment above minimum
- Integration with governance and treasury

### EUSDaoGovernance
- DAO-based decision making
- Proposal and voting mechanisms
- Integration with KarmaBond for weighted voting

### Sustainment Protocol
- Maintains minimum treasury reserve
- Alerts when approaching threshold
- Enforces sustainability requirements on tranches

## Workflow Artifacts

Each workflow generates reports that are uploaded as artifacts:

- **Sustainability Report** (`sustainability-report.md`) - 30 day retention
- **Governance Report** (`governance-report.md`) - 30 day retention
- **Framework Status Report** (`framework-status.md`) - 90 day retention

## Environment Setup

### Required for Local Testing

**Python Dependencies**:
```bash
pip install -r requirements.txt
pip install pyyaml jsonschema
```

**Node Dependencies**:
```bash
npm ci
```

**Environment Variables** (see `.env.example`):
- `POLYGON_RPC_URL` - RPC endpoint for blockchain
- `PRIVATE_KEY` - Wallet private key (never commit!)
- `SUSTAINMENT_MIN_USD` - Minimum sustainment in USD
- `SUSTAINMENT_PERCENT_BPS` - Sustainment allocation (basis points)
- `FOUNDATION_WALLET` - Foundation wallet address
- `STABLE_TOKEN_ADDRESS` - Stablecoin contract address

## Testing Workflows Locally

### Test Integrity Check
```bash
python3 scripts/auto_integrity.py
```

### Test Violations Check
```bash
python3 scripts/check_violations.py
```

### Compile Contracts
```bash
npm run compile
```

### Run All Tests
```bash
npm test
```

### Run Specific Test Suites
```bash
npm run test:sustainment      # Sustainment tests
npm run test:integration       # Integration tests
npm run test:governance        # Governance tests
```

## Monitoring and Maintenance

### Workflow Execution
- Monitor workflow runs in the GitHub Actions tab
- Check artifacts for detailed reports
- Review workflow logs for any issues

### Configuration Updates
- Update `.env.example` when adding new environment variables
- Update `governance.json` for governance changes
- Keep `ethical_shield.yaml` synchronized with framework principles

### Contract Updates
- Recompile after contract changes: `npm run compile`
- Run full test suite: `npm test`
- Update deployment scripts if needed

## Security Considerations

1. **Never commit `.env` files** - Only `.env.example` should be in the repository
2. **Validate all PRs** - Workflows run on pull requests to validate changes
3. **Monitor workflow outputs** - Review reports for any security concerns
4. **Keep dependencies updated** - Regularly update Node and Python packages
5. **Review principle violations** - Check violation reports and address concerns

## Next Steps

1. ✅ All workflows deployed and active
2. Monitor first workflow runs and review generated reports
3. Address any issues identified in reports
4. Update documentation based on operational experience
5. Consider adding additional monitoring and alerting
6. Plan for contract deployment to test network
7. Set up production deployment procedures

## Support and Contribution

For issues or questions:
1. Check workflow logs in GitHub Actions
2. Review generated artifact reports
3. Consult `DEPLOYMENT_GUIDE.md` for deployment procedures
4. Open an issue on GitHub for bugs or feature requests

## License

All workflows and scripts are part of the Euystacio framework and follow the project's license terms.

---

**Last Updated**: 2025-11-04  
**Framework Version**: 1.0.0  
**Status**: ✅ All Workflows Deployed and Active
