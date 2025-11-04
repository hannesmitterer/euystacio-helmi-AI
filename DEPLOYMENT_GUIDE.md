# Euystacio Sustainment Protocol - Deployment Guide

## Overview

This guide provides step-by-step instructions for deploying the Euystacio smart contracts with the integrated Sustainment Protocol to Polygon or other EVM-compatible networks.

## Prerequisites

1. **Node.js** (v16 or higher)
2. **npm** or **yarn**
3. **Hardhat** (installed via package.json)
4. **Wallet** with native tokens for gas (MATIC on Polygon)
5. **Stablecoin contract** address (e.g., USDC on Polygon: `0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174`)

## Environment Setup

### 1. Clone and Install Dependencies

```bash
git clone <repository-url>
cd euystacio-helmi-AI
npm install
```

### 2. Configure Environment

Create a `.env` file from the example:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Network Configuration
POLYGON_RPC_URL=https://polygon-rpc.com
PRIVATE_KEY=your_private_key_here_without_0x_prefix

# Sustainment Configuration
SUSTAINMENT_MIN_USD=10000
SUSTAINMENT_PERCENT_BPS=200

# Contract Addresses
STABLE_TOKEN_ADDRESS=0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174
FOUNDATION_WALLET=0x5d61a4B25034393A37ef9307C8Ba3aE99e49944b
```

**Important:** Never commit your `.env` file to version control!

## Compilation

Compile all smart contracts:

```bash
npx hardhat compile
```

Expected output:
```
Compiled 15 Solidity files successfully
```

## Testing

### Run All Tests

```bash
npm test
```

Expected: 59 passing tests

### Run Specific Test Suites

```bash
# Sustainment contract tests
npm run test:sustainment

# Integration tests
npm run test:integration

# Governance tests
npm run test:governance
```

## Deployment

### Local Development (Hardhat Network)

Test deployment locally:

```bash
npx hardhat run scripts/deploy_karmabond.js
```

### Polygon Testnet (Mumbai)

1. Update `.env` with Mumbai RPC URL:
```env
POLYGON_RPC_URL=https://rpc-mumbai.maticvigil.com
```

2. Get test MATIC from [Mumbai Faucet](https://faucet.polygon.technology/)

3. Deploy:
```bash
npx hardhat run scripts/deploy_karmabond.js --network polygon
```

### Polygon Mainnet

**⚠️ Warning: This will deploy to production!**

1. Ensure `.env` has mainnet RPC and your production wallet
2. Fund wallet with sufficient MATIC for gas
3. Deploy:
```bash
npx hardhat run scripts/deploy_karmabond.js --network polygon
```

## Post-Deployment Steps

### 1. Save Contract Addresses

The deployment script outputs a JSON with all contract addresses. Save this to a file:

```json
{
  "network": "polygon",
  "deployer": "0x...",
  "timestamp": "2025-11-04T...",
  "contracts": {
    "Sustainment": "0x...",
    "EUSDaoGovernance": "0x...",
    "KarmaBond": "0x...",
    "TrustlessFundingProtocol": "0x..."
  },
  "config": {
    "stableToken": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
    "foundationWallet": "0x...",
    "sustainmentMinUSD": 10000,
    "sustainmentPercentBPS": 200
  }
}
```

### 2. Verify Contracts on Polygonscan

```bash
npx hardhat verify --network polygon <CONTRACT_ADDRESS> <CONSTRUCTOR_ARGS>
```

Example for Sustainment:
```bash
npx hardhat verify --network polygon 0x... \
  "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174" \
  6 \
  10000
```

### 3. Transfer Ownership

For production, transfer ownership to a multisig wallet:

```javascript
const sustainment = await ethers.getContractAt("Sustainment", SUSTAINMENT_ADDRESS);
await sustainment.transferOwnership(MULTISIG_ADDRESS);
```

### 4. Initialize Sustainment Pool (Optional)

Optionally fund the initial sustainment reserve:

```javascript
// Approve and deposit stablecoins to sustainment
const usdc = await ethers.getContractAt("IERC20", USDC_ADDRESS);
await usdc.approve(SUSTAINMENT_ADDRESS, ethers.parseUnits("10000", 6));
await sustainment.depositToSustainment(ethers.parseUnits("10000", 6));
```

## Configuration Updates

### Change Sustainment Minimum

```javascript
const sustainment = await ethers.getContractAt("Sustainment", SUSTAINMENT_ADDRESS);
await sustainment.setMinSustainment(15000); // $15,000 USD
```

### Change Sustainment Allocation Percentage

```javascript
const karmaBond = await ethers.getContractAt("KarmaBond", KARMABOND_ADDRESS);
await karmaBond.setSustainmentPercent(300); // 3% (300 basis points)
```

### Emergency: Disable Governance Enforcement

```javascript
const tfp = await ethers.getContractAt("TrustlessFundingProtocol", TFP_ADDRESS);
await tfp.setGovernanceEnforcement(false);
```

## Monitoring

### Events to Monitor

Use a service like The Graph or Dune Analytics to monitor:

- `SustainmentDeposited` - Track incoming funds
- `SustainmentWithdrawn` - Track outgoing payments
- `SustainmentAlertNearThreshold` - Alert when approaching minimum
- `BondMinted` - Track bond issuance
- `SustainmentAllocated` - Track allocation from bonds
- `TrancheReleased` - Track governance approvals
- `TrancheRejectedInsufficientSustainment` - Track blocked tranches

### View Functions for Frontend

```javascript
// Check sustainment status
const isAbove = await sustainment.isAboveMinimum();
const reserve = await sustainment.getSustainmentReserve();
const minimum = await sustainment.minSustainment();

// Check if tranche can be released
const [canRelease, reason] = await tfp.canReleaseTranche(trancheId);

// Get bond info
const bondBalance = await karmaBond.getBondBalance(userAddress);
const stableReserve = await karmaBond.stableReserve();
```

## Troubleshooting

### "Insufficient funds" Error
- Ensure deployer wallet has enough MATIC for gas
- On mainnet, expect 0.1-0.5 MATIC per deployment

### "Nonce too high" Error
- Reset your Hardhat cache: `rm -rf cache/ artifacts/`
- Clear your MetaMask/wallet nonce

### Tests Failing
- Ensure you're using Node.js v16+
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check that all dependencies are compatible

### Contract Not Verifying
- Ensure constructor arguments match deployment exactly
- Check that Solidity compiler version matches (0.8.20)
- Optimization settings must match hardhat.config.js

## Security Checklist

Before deploying to production:

- [ ] All tests passing (59/59)
- [ ] Environment variables properly configured
- [ ] Contracts compiled without warnings
- [ ] Ownership will be transferred to multisig
- [ ] Backup of private keys and contract addresses
- [ ] Team members aware of deployment
- [ ] Monitoring and alerts configured
- [ ] Emergency procedures documented
- [ ] Consider professional security audit

## Support

For issues or questions:
1. Check `docs/SUSTAINMENT.md` for protocol details
2. Review `contracts/README.md` for architecture
3. Open an issue on GitHub

## License

MIT License - See LICENSE file for details
