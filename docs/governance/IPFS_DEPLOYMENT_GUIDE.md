# IPFS Distribution Guide

## Overview

This document provides instructions for deploying the Euystacio Framework Executive Master Document to IPFS (InterPlanetary File System) for permanent, decentralized, and censorship-resistant access.

## What is IPFS?

IPFS is a peer-to-peer hypermedia protocol designed to make the web faster, safer, and more open. Content is addressed by its cryptographic hash (Content Identifier or CID) rather than location, ensuring:

- **Immutability**: Content cannot be changed without changing its CID
- **Permanence**: Content persists as long as at least one node pins it
- **Censorship Resistance**: No central authority can block access
- **Verification**: Anyone can verify content integrity via CID

## Deployment Process

### Step 1: Install IPFS

#### Option A: IPFS Desktop (Recommended for beginners)
1. Download from https://github.com/ipfs/ipfs-desktop/releases
2. Install and launch IPFS Desktop
3. Wait for initialization to complete

#### Option B: IPFS CLI (Advanced users)
```bash
# Download and install (check https://dist.ipfs.io/#kubo for latest version)
# Example using Kubo v0.24.0 - replace with latest stable version
wget https://dist.ipfs.io/kubo/v0.24.0/kubo_v0.24.0_linux-amd64.tar.gz
tar -xvzf kubo_v0.24.0_linux-amd64.tar.gz
cd kubo
sudo bash install.sh

# Initialize IPFS repository
ipfs init

# Start IPFS daemon
ipfs daemon
```

### Step 2: Add Document to IPFS

#### Via IPFS Desktop
1. Open IPFS Desktop
2. Go to "Files" tab
3. Click "Import" → "File"
4. Select `docs/governance/EXECUTIVE_MASTER_DOCUMENT.md`
5. Note the CID displayed after import

#### Via IPFS CLI
```bash
# Navigate to repository root
cd /home/runner/work/euystacio-helmi-AI/euystacio-helmi-AI

# Add the master document
ipfs add docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# Output will show CID, for example:
# added QmXxxx... docs/governance/EXECUTIVE_MASTER_DOCUMENT.md
```

### Step 3: Pin on Multiple Services

For redundancy and permanence, pin the content on multiple IPFS pinning services.

#### Pinata (https://www.pinata.cloud)

**Setup:**
1. Create account at https://www.pinata.cloud
2. Generate API key in account settings
3. Save API Key and API Secret

**Pin via API:**
```bash
# Set credentials
export PINATA_API_KEY="your_api_key"
export PINATA_SECRET_KEY="your_secret_key"

# Pin by CID
curl -X POST "https://api.pinata.cloud/pinning/pinByHash" \
  -H "Content-Type: application/json" \
  -H "pinata_api_key: $PINATA_API_KEY" \
  -H "pinata_secret_api_key: $PINATA_SECRET_KEY" \
  -d '{
    "hashToPin": "YOUR_CID_HERE",
    "pinataMetadata": {
      "name": "Euystacio Framework - Executive Master Document",
      "keyvalues": {
        "version": "1.0",
        "type": "governance_document"
      }
    }
  }'
```

**Pin via Web Interface:**
1. Log in to Pinata dashboard
2. Click "Upload" → "CID"
3. Enter your CID
4. Add name and metadata
5. Click "Pin"

#### Web3.Storage (https://web3.storage)

**Setup:**
1. Create account at https://web3.storage
2. Generate API token
3. Save token securely

**Pin via CLI:**
```bash
# Install w3 CLI
npm install -g @web3-storage/w3cli

# Login
w3 login your-email@example.com

# Upload file
w3 put docs/governance/EXECUTIVE_MASTER_DOCUMENT.md --name "Euystacio Master Document"

# Pin existing CID
w3 pin add YOUR_CID_HERE
```

**Pin via API:**
```bash
# Set token
export WEB3_STORAGE_TOKEN="your_token"

# Pin by CID
curl -X POST "https://api.web3.storage/pins" \
  -H "Authorization: Bearer $WEB3_STORAGE_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "cid": "YOUR_CID_HERE",
    "name": "Euystacio Framework - Executive Master Document"
  }'
```

#### NFT.Storage (https://nft.storage)

**Setup:**
1. Create account at https://nft.storage
2. Generate API token
3. Save token securely

**Pin via API:**
```bash
# Set token
export NFT_STORAGE_TOKEN="your_token"

# Upload file
curl -X POST "https://api.nft.storage/upload" \
  -H "Authorization: Bearer $NFT_STORAGE_TOKEN" \
  -F file=@docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# Response includes CID
```

### Step 4: Verify Pinning

Check that content is pinned on all services:

```bash
# Check Pinata
curl "https://api.pinata.cloud/data/pinList?hashContains=YOUR_CID" \
  -H "pinata_api_key: $PINATA_API_KEY" \
  -H "pinata_secret_api_key: $PINATA_SECRET_KEY"

# Check Web3.Storage
w3 pin ls YOUR_CID_HERE

# Verify IPFS gateway access
curl https://ipfs.io/ipfs/YOUR_CID_HERE
curl https://gateway.pinata.cloud/ipfs/YOUR_CID_HERE
curl https://w3s.link/ipfs/YOUR_CID_HERE
```

### Step 5: Document CID Details

Update the master document and README with CID information.

**Template - Replace placeholder values with actual deployment details:**

```markdown
**IPFS Distribution:**
- **CID**: QmXxxx... (replace with actual CID from Step 2)
- **IPFS Gateway**: https://ipfs.io/ipfs/QmXxxx... (replace QmXxxx... with your CID)
- **Pinata Gateway**: https://gateway.pinata.cloud/ipfs/QmXxxx... (replace QmXxxx... with your CID)
- **Web3.Storage Gateway**: https://w3s.link/ipfs/QmXxxx... (replace QmXxxx... with your CID)
- **Pinned On**: Pinata, Web3.Storage, NFT.Storage
- **Pin Date**: YYYY-MM-DD (replace with actual date)
```

**Example with sample CID:**
```markdown
**IPFS Distribution:**
- **CID**: QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
- **IPFS Gateway**: https://ipfs.io/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
- **Pinata Gateway**: https://gateway.pinata.cloud/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
- **Web3.Storage Gateway**: https://w3s.link/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG
- **Pinned On**: Pinata, Web3.Storage, NFT.Storage
- **Pin Date**: 2025-12-14
```

## Access Methods

### Via IPFS Desktop/CLI
```bash
# Download content
ipfs get YOUR_CID_HERE

# Cat content to stdout
ipfs cat YOUR_CID_HERE

# Open in browser via local gateway
open http://localhost:8080/ipfs/YOUR_CID_HERE
```

### Via Public Gateways
- IPFS.io: `https://ipfs.io/ipfs/YOUR_CID_HERE`
- Cloudflare: `https://cloudflare-ipfs.com/ipfs/YOUR_CID_HERE`
- Pinata: `https://gateway.pinata.cloud/ipfs/YOUR_CID_HERE`
- Web3.Storage: `https://w3s.link/ipfs/YOUR_CID_HERE`

### Via Browser Extension
1. Install IPFS Companion browser extension
2. Navigate to `ipfs://YOUR_CID_HERE`
3. Extension automatically resolves via local node or gateway

## Verification

### Verify Content Integrity
```bash
# Get content
ipfs cat YOUR_CID_HERE > downloaded_document.md

# Compute hash of original
sha256sum docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# Compute hash of downloaded
sha256sum downloaded_document.md

# Hashes should match
```

### Verify Pinning Status
```bash
# Check if locally pinned
ipfs pin ls YOUR_CID_HERE

# Check pin stats
ipfs pin ls --type=recursive | grep YOUR_CID_HERE
```

### Verify Replication
```bash
# Find peers providing content
ipfs dht findprovs YOUR_CID_HERE

# Should show multiple providers including pinning services
```

## Maintenance

### Monitor Pinning Status

Create a script to regularly verify pins:

```bash
#!/bin/bash
# check_pins.sh

CID="YOUR_CID_HERE"

echo "Checking pinning status for $CID"

# Check Pinata
echo "Pinata:"
curl -s "https://api.pinata.cloud/data/pinList?hashContains=$CID" \
  -H "pinata_api_key: $PINATA_API_KEY" \
  -H "pinata_secret_api_key: $PINATA_SECRET_KEY" | jq '.count'

# Check IPFS gateway accessibility
echo "IPFS.io Gateway:"
if curl -s -f "https://ipfs.io/ipfs/$CID" > /dev/null; then
  echo "✅ Accessible"
else
  echo "❌ Not accessible"
fi

echo "Pinata Gateway:"
if curl -s -f "https://gateway.pinata.cloud/ipfs/$CID" > /dev/null; then
  echo "✅ Accessible"
else
  echo "❌ Not accessible"
fi
```

Run monthly to ensure continued availability.

### Re-pin if Needed

If a pin is lost:

```bash
# Re-pin on Pinata
curl -X POST "https://api.pinata.cloud/pinning/pinByHash" \
  -H "pinata_api_key: $PINATA_API_KEY" \
  -H "pinata_secret_api_key: $PINATA_SECRET_KEY" \
  -d '{"hashToPin": "YOUR_CID_HERE"}'

# Re-pin on Web3.Storage
w3 pin add YOUR_CID_HERE
```

## Best Practices

1. **Multiple Pins**: Always pin on at least 3 different services
2. **Regular Verification**: Check pin status monthly
3. **Document CID**: Update all documentation with CID
4. **Gateway Diversity**: Use multiple gateways for access
5. **Backup CID**: Store CID in multiple secure locations
6. **Version Control**: Track CID in git repository
7. **Community Pinning**: Encourage community to pin important content

## Troubleshooting

### Content Not Found
- Wait 5-10 minutes for IPFS propagation
- Try different gateways
- Check if CID is correct
- Verify pinning services

### Slow Access
- Use faster gateway (Cloudflare often fastest)
- Pin content locally for instant access
- Consider IPFS cluster for production use

### Pin Verification Failed
- Re-authenticate with pinning service
- Check API key validity
- Verify sufficient storage quota
- Contact pinning service support

## Cost Considerations

### Pinata
- Free tier: 1 GB storage, unlimited bandwidth
- Paid plans from $20/month for 100 GB

### Web3.Storage
- Free for public data
- Sponsored by Protocol Labs (Filecoin)

### NFT.Storage
- Free for NFTs and public data
- Sponsored by Protocol Labs

### Recommendations
- Use free tiers for public documents
- Upgrade as needed for large content
- Distribute costs across multiple services

## Security Notes

1. **Public Content**: Everything on IPFS is public
2. **Immutable**: Cannot edit content after adding (must add new version)
3. **CID is Address**: Treat CID as permanent identifier
4. **API Keys**: Keep pinning service API keys secure
5. **No PII**: Never put personally identifiable information on IPFS

## Community Pinning

Encourage community members to help pin important content:

```markdown
### Help Keep Euystacio Available

Pin the Executive Master Document on your IPFS node:

\`\`\`bash
ipfs pin add YOUR_CID_HERE
\`\`\`

This ensures the content remains available even if official pins fail.
```

## Automation

### GitHub Actions Workflow

Create `.github/workflows/ipfs-deploy.yml`:

```yaml
name: Deploy to IPFS

on:
  push:
    paths:
      - 'docs/governance/EXECUTIVE_MASTER_DOCUMENT.md'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Web3.Storage
        uses: web3-storage/add-to-web3@v2
        with:
          path_to_add: docs/governance/EXECUTIVE_MASTER_DOCUMENT.md
          web3_token: ${{ secrets.WEB3_STORAGE_TOKEN }}
      
      - name: Update README with CID
        run: |
          echo "CID: ${{ steps.deploy.outputs.cid }}" >> DEPLOYMENT_LOG.md
```

---

**Document Version:** 1.0  
**Last Updated:** December 14, 2025  
**Status:** Active Guide
