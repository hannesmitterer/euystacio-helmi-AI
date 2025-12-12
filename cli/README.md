# Euystacio-Helmi CLI

Command-line interface for the euystacio-helmi-AI framework.

## Installation

```bash
npm install -g euystacio-cli
```

Or use directly from the repository:

```bash
cd cli
npm install
npm link
```

## Usage

### Display Framework Information

```bash
euystacio-cli info
```

Shows framework overview, principles, and official links.

### Governance Commands

#### Create a Proposal

```bash
euystacio-cli governance propose \
  --title "Proposal Title" \
  --cid QmXxx... \
  --wallet 0xYourAddress
```

#### Vote on a Proposal

```bash
euystacio-cli governance vote \
  --proposal 1 \
  --support true \
  --wallet 0xYourAddress
```

#### List Proposals

```bash
euystacio-cli governance list
euystacio-cli governance list --status active
```

#### Get Proposal Status

```bash
euystacio-cli governance status --proposal 1
```

### IPFS Commands

#### Verify Document

```bash
euystacio-cli ipfs verify --cid QmXxx...
euystacio-cli ipfs verify --cid QmXxx... --sig
```

#### Download Document

```bash
euystacio-cli ipfs get --cid QmXxx... --output document.md
```

#### List Document Versions

```bash
euystacio-cli ipfs versions --document sensisara-principle
```

### Treasury Commands

#### Check Treasury Status

```bash
euystacio-cli treasury status
```

#### Check Treasury Balance

```bash
euystacio-cli treasury balance
```

### Analytics Commands

#### Open Dashboard

```bash
euystacio-cli analytics dashboard
```

#### View Metrics

```bash
euystacio-cli analytics metrics
```

### Utility Commands

#### Show Official Links

```bash
euystacio-cli links
```

## Development

The CLI is built with Commander.js and integrates with:
- HelmiGovernance smart contract
- IPFS for document verification
- Web3 for blockchain interaction
- Euystacio SDK for core functionality

## Next Steps

Current implementation provides command structure. Full integration requires:
1. Web3 provider configuration
2. Contract ABI integration
3. IPFS node connectivity
4. Wallet management

See SDK documentation for integration details.
