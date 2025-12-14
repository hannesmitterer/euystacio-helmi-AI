# Deployment Instructions for IPFS and Blockchain Anchoring

## Current Status

✅ **Documentation Complete**
- Executive Master Document created
- All supporting documentation in place
- Hash generation and verification scripts ready
- README updated with access information

📄 **Document Hash Generated**
```
SHA-256: b29947ba95e264f2eb4074b6d6644ec53f66163b2bcccde35561f744aab38825
Ethereum: 0xb29947ba95e264f2eb4074b6d6644ec53f66163b2bcccde35561f744aab38825
```

## Next Steps for Full Deployment

### Step 1: IPFS Deployment

Follow the instructions in [docs/governance/IPFS_DEPLOYMENT_GUIDE.md](docs/governance/IPFS_DEPLOYMENT_GUIDE.md)

**Quick Start:**

```bash
# 1. Install IPFS (if not already installed)
# Download from https://github.com/ipfs/ipfs-desktop/releases
# Or use CLI: https://docs.ipfs.tech/install/

# 2. Add document to IPFS
ipfs add docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# 3. Note the CID that is returned
# Example output: added QmXxxx... docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# 4. Pin on Pinata (requires account and API keys)
# See IPFS_DEPLOYMENT_GUIDE.md for detailed instructions

# 5. Pin on Web3.Storage (requires account and token)
# See IPFS_DEPLOYMENT_GUIDE.md for detailed instructions

# 6. Pin on NFT.Storage (optional, requires account and token)
# See IPFS_DEPLOYMENT_GUIDE.md for detailed instructions
```

**After IPFS deployment, update these files with the CID:**
- `docs/governance/EXECUTIVE_MASTER_DOCUMENT.md` (line 262)
- `docs/governance/README.md` (line 130)
- `README.md` (line 10)

### Step 2: Blockchain Anchoring

Follow the instructions in [docs/governance/BLOCKCHAIN_ANCHORING_GUIDE.md](docs/governance/BLOCKCHAIN_ANCHORING_GUIDE.md)

**Prerequisites:**
- Sepolia testnet ETH (get from https://sepoliafaucet.com)
- Ethereum wallet (MetaMask or similar)
- Private key for deployment (keep secure!)

**Quick Start:**

```bash
# 1. Set up environment variables
cp .env.example .env
# Edit .env and add:
# SEPOLIA_RPC_URL=https://rpc.sepolia.org
# PRIVATE_KEY=your_private_key
# ETHERSCAN_API_KEY=your_etherscan_api_key

# 2. Deploy the DocumentAnchor contract (if not already done)
# See BLOCKCHAIN_ANCHORING_GUIDE.md for contract code
npx hardhat run scripts/deploy-anchor.js --network sepolia

# 3. Set contract address
export ANCHOR_CONTRACT_ADDRESS=0x... # from deployment

# 4. Set IPFS CID (from Step 1)
export IPFS_CID=QmXxxx... # from IPFS deployment

# 5. Anchor the document
npx hardhat run scripts/anchor-master-doc.js --network sepolia

# 6. Note the transaction details returned
```

**After blockchain anchoring, update these files:**
- `docs/governance/EXECUTIVE_MASTER_DOCUMENT.md` (lines 264-271)
- `docs/governance/README.md` (lines 137-143)
- `README.md` (lines 14-16)

### Step 3: Update Documentation

Replace all `[To be added]` placeholders with actual values:

**IPFS CID:**
- Replace `[To be added after IPFS deployment]` with actual CID
- Replace `[CID]` in URLs with actual CID

**Blockchain Details:**
- Replace `[To be deployed]` with contract address
- Replace `[To be added]` with transaction hash, block number, etc.

**Files to update:**
1. `docs/governance/EXECUTIVE_MASTER_DOCUMENT.md`
2. `docs/governance/README.md`
3. `README.md`
4. `docs/governance/COMMUNITY_ANNOUNCEMENTS.md`

### Step 4: Verify Everything

```bash
# Verify IPFS access
ipfs cat YOUR_CID_HERE

# Verify via HTTP gateway
curl https://ipfs.io/ipfs/YOUR_CID_HERE

# Verify document hash
node scripts/verify-document.js --current

# Verify blockchain anchor (after deployment)
node scripts/verify-document.js CONTRACT_ADDRESS ANCHOR_ID
```

### Step 5: Community Announcement

Use templates from [docs/governance/COMMUNITY_ANNOUNCEMENTS.md](docs/governance/COMMUNITY_ANNOUNCEMENTS.md)

**Channels:**
1. GitHub Discussions - Post announcement
2. Twitter/X - Post thread (6 tweets)
3. Discord - Post in #announcements
4. Reddit - Post in r/ethereum, r/dao, r/ethdev
5. Email Newsletter - Send to subscribers

**Timing:**
- Coordinate announcements across all channels
- Post within same 24-hour window
- Monitor and respond to feedback

## Verification Checklist

Before announcing:

- [ ] Document is on IPFS
- [ ] CID is pinned on Pinata
- [ ] CID is pinned on Web3.Storage
- [ ] CID is pinned on NFT.Storage (optional)
- [ ] All IPFS gateways accessible
- [ ] Smart contract deployed on Sepolia
- [ ] Document hash anchored on-chain
- [ ] Transaction confirmed (100+ blocks)
- [ ] Contract verified on Etherscan
- [ ] All documentation updated with real values
- [ ] Verification scripts tested and working
- [ ] Community announcements prepared
- [ ] All links tested and functional

## Manual Deployment Notes

If you need to perform deployment manually:

### IPFS Manual Pinning

**Pinata:**
1. Visit https://app.pinata.cloud
2. Login to your account
3. Click "Upload" → "CID"
4. Enter your CID
5. Add metadata (name, description)
6. Click "Pin"

**Web3.Storage:**
1. Visit https://web3.storage
2. Login to your account
3. Click "Upload"
4. Select the file or enter CID
5. Confirm upload

### Blockchain Manual Anchoring

**Via Etherscan:**
1. Visit https://sepolia.etherscan.io/address/CONTRACT_ADDRESS
2. Go to "Write Contract"
3. Connect wallet
4. Call `anchorDocument` with:
   - `_documentHash`: 0xb29947ba95e264f2eb4074b6d6644ec53f66163b2bcccde35561f744aab38825
   - `_documentName`: "Euystacio Framework - Executive Master Document v1.0"
   - `_ipfsCID`: YOUR_IPFS_CID
5. Submit transaction
6. Wait for confirmation
7. Note transaction hash and block number

## Support

If you encounter issues:

1. Check the detailed guides:
   - [IPFS Deployment Guide](docs/governance/IPFS_DEPLOYMENT_GUIDE.md)
   - [Blockchain Anchoring Guide](docs/governance/BLOCKCHAIN_ANCHORING_GUIDE.md)

2. Review error messages and troubleshooting sections

3. Reach out on:
   - GitHub Issues
   - Discord #help channel
   - Community discussions

## Security Notes

⚠️ **Important:**
- Never commit private keys to Git
- Use `.env` for sensitive configuration
- Verify all contracts on Etherscan
- Test on testnet before mainnet
- Keep backup of all deployment details

## Cost Estimates

**Sepolia Testnet (FREE):**
- Get test ETH from faucets
- No real money required
- Perfect for testing

**Mainnet (if moving to production):**
- Contract deployment: ~$50-100 USD
- Anchoring transaction: ~$5-10 USD
- Consider L2 solutions for lower costs

**IPFS Pinning:**
- Free tiers available on all services
- Paid plans start at $20/month for larger storage

---

**Last Updated**: December 14, 2025  
**Status**: Ready for Deployment
