# Blockchain Anchoring Guide

## Overview

This guide provides instructions for anchoring the Euystacio Framework Executive Master Document on the Ethereum Sepolia testnet, creating cryptographic proof of existence and immutability.

## What is Blockchain Anchoring?

Blockchain anchoring is the process of recording a cryptographic hash of data on a blockchain to prove:

- **Existence**: The data existed at a specific point in time
- **Immutability**: The data has not been tampered with since anchoring
- **Verification**: Anyone can verify the data's integrity
- **Timestamp**: Blockchain provides tamper-proof timestamp

## Prerequisites

### Required Tools
- Node.js v18+
- Web3.js or Ethers.js library
- MetaMask or similar Web3 wallet
- Sepolia testnet ETH (from faucet)

### Setup

```bash
# Install dependencies
npm install ethers

# Or with web3.js
npm install web3
```

## Step 1: Generate Document Hash

### Using SHA-256

```bash
# Generate hash of the master document
sha256sum docs/governance/EXECUTIVE_MASTER_DOCUMENT.md

# Output format:
# abc123def456... docs/governance/EXECUTIVE_MASTER_DOCUMENT.md
```

### Using Node.js

```javascript
// generate-hash.js
const crypto = require('crypto');
const fs = require('fs');

const content = fs.readFileSync(
  'docs/governance/EXECUTIVE_MASTER_DOCUMENT.md',
  'utf8'
);

const hash = crypto
  .createHash('sha256')
  .update(content)
  .digest('hex');

console.log('Document Hash:', hash);
console.log('With 0x prefix:', '0x' + hash);
```

Run:
```bash
node generate-hash.js
```

### Record Hash
Save the hash for use in smart contract:
```
Document Hash: 0xabc123def456...
```

## Step 2: Deploy Anchoring Smart Contract

### Contract Code

Create `contracts/DocumentAnchor.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

/**
 * @title DocumentAnchor
 * @dev Anchors document hashes on-chain for immutability proof
 */
contract DocumentAnchor {
    struct Anchor {
        bytes32 documentHash;
        string documentName;
        string ipfsCID;
        address anchoredBy;
        uint256 timestamp;
        uint256 blockNumber;
    }
    
    // Mapping from document ID to anchor data
    mapping(uint256 => Anchor) public anchors;
    
    // Counter for anchor IDs
    uint256 public anchorCount;
    
    // Events
    event DocumentAnchored(
        uint256 indexed anchorId,
        bytes32 indexed documentHash,
        string documentName,
        string ipfsCID,
        address indexed anchoredBy,
        uint256 timestamp,
        uint256 blockNumber
    );
    
    /**
     * @dev Anchor a document hash on-chain
     * @param _documentHash SHA-256 hash of the document
     * @param _documentName Name/title of the document
     * @param _ipfsCID IPFS Content Identifier for the document
     */
    function anchorDocument(
        bytes32 _documentHash,
        string memory _documentName,
        string memory _ipfsCID
    ) external returns (uint256) {
        require(_documentHash != bytes32(0), "Invalid hash");
        require(bytes(_documentName).length > 0, "Name required");
        
        uint256 anchorId = anchorCount++;
        
        anchors[anchorId] = Anchor({
            documentHash: _documentHash,
            documentName: _documentName,
            ipfsCID: _ipfsCID,
            anchoredBy: msg.sender,
            timestamp: block.timestamp,
            blockNumber: block.number
        });
        
        emit DocumentAnchored(
            anchorId,
            _documentHash,
            _documentName,
            _ipfsCID,
            msg.sender,
            block.timestamp,
            block.number
        );
        
        return anchorId;
    }
    
    /**
     * @dev Verify a document hash against anchored data
     * @param _anchorId ID of the anchor to verify
     * @param _documentHash Hash to verify
     * @return bool True if hash matches
     */
    function verifyDocument(
        uint256 _anchorId,
        bytes32 _documentHash
    ) external view returns (bool) {
        require(_anchorId < anchorCount, "Invalid anchor ID");
        return anchors[_anchorId].documentHash == _documentHash;
    }
    
    /**
     * @dev Get full anchor details
     * @param _anchorId ID of the anchor
     */
    function getAnchor(uint256 _anchorId) 
        external 
        view 
        returns (Anchor memory) 
    {
        require(_anchorId < anchorCount, "Invalid anchor ID");
        return anchors[_anchorId];
    }
}
```

### Deployment Script

Create `scripts/deploy-anchor.js`:

```javascript
const { ethers } = require("hardhat");

async function main() {
  console.log("Deploying DocumentAnchor contract to Sepolia...");

  // Get deployer account
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with account:", deployer.address);

  // Check balance
  const balance = await ethers.provider.getBalance(deployer.address);
  console.log("Account balance:", ethers.formatEther(balance), "ETH");

  // Deploy contract
  const DocumentAnchor = await ethers.getContractFactory("DocumentAnchor");
  const documentAnchor = await DocumentAnchor.deploy();
  
  await documentAnchor.waitForDeployment();
  const address = await documentAnchor.getAddress();

  console.log("DocumentAnchor deployed to:", address);
  console.log("Save this address for verification and use!");

  // Verify deployment
  const anchorCount = await documentAnchor.anchorCount();
  console.log("Initial anchor count:", anchorCount.toString());

  return address;
}

main()
  .then((address) => {
    console.log("\nDeployment successful!");
    console.log("Contract address:", address);
    process.exit(0);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Configure Hardhat

Update `hardhat.config.js`:

```javascript
require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.19",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155111
    }
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY
  }
};
```

### Environment Variables

Create `.env`:
```bash
SEPOLIA_RPC_URL=https://rpc.sepolia.org
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_api_key
```

**Security**: Never commit `.env` to git!

### Deploy Contract

```bash
# Compile contract
npx hardhat compile

# Deploy to Sepolia
npx hardhat run scripts/deploy-anchor.js --network sepolia

# Output:
# DocumentAnchor deployed to: 0x1234567890abcdef...
```

### Verify on Etherscan

```bash
npx hardhat verify --network sepolia CONTRACT_ADDRESS
```

## Step 3: Anchor the Document

### Using Script

Create `scripts/anchor-master-doc.js`:

```javascript
const { ethers } = require("hardhat");
const crypto = require("crypto");
const fs = require("fs");

async function main() {
  // Read document
  const docPath = "docs/governance/EXECUTIVE_MASTER_DOCUMENT.md";
  const content = fs.readFileSync(docPath, "utf8");
  
  // Generate hash
  const hash = crypto.createHash("sha256").update(content).digest();
  const hashHex = "0x" + hash.toString("hex");
  
  console.log("Document Hash:", hashHex);
  
  // Contract details
  const contractAddress = process.env.ANCHOR_CONTRACT_ADDRESS;
  const ipfsCID = process.env.IPFS_CID || "TO_BE_ADDED";
  
  // Get contract instance
  const DocumentAnchor = await ethers.getContractAt(
    "DocumentAnchor",
    contractAddress
  );
  
  console.log("Anchoring document...");
  
  // Anchor document
  const tx = await DocumentAnchor.anchorDocument(
    hashHex,
    "Euystacio Framework - Executive Master Document v1.0",
    ipfsCID
  );
  
  console.log("Transaction sent:", tx.hash);
  console.log("Waiting for confirmation...");
  
  const receipt = await tx.wait();
  console.log("Transaction confirmed in block:", receipt.blockNumber);
  
  // Get anchor ID from event
  const event = receipt.logs.find(
    log => log.fragment && log.fragment.name === "DocumentAnchored"
  );
  
  if (event) {
    const anchorId = event.args.anchorId;
    console.log("Anchor ID:", anchorId.toString());
    
    // Retrieve and display anchor data
    const anchor = await DocumentAnchor.getAnchor(anchorId);
    console.log("\nAnchor Details:");
    console.log("- Document Name:", anchor.documentName);
    console.log("- Document Hash:", anchor.documentHash);
    console.log("- IPFS CID:", anchor.ipfsCID);
    console.log("- Anchored By:", anchor.anchoredBy);
    console.log("- Timestamp:", new Date(Number(anchor.timestamp) * 1000));
    console.log("- Block Number:", anchor.blockNumber.toString());
  }
  
  return {
    transactionHash: tx.hash,
    blockNumber: receipt.blockNumber,
    contractAddress: contractAddress
  };
}

main()
  .then((result) => {
    console.log("\nAnchoring successful!");
    console.log(JSON.stringify(result, null, 2));
    process.exit(0);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Execute Anchoring

```bash
# Set environment variables
export ANCHOR_CONTRACT_ADDRESS=0x1234... # From deployment
export IPFS_CID=QmXxxx... # From IPFS deployment

# Run anchoring script
npx hardhat run scripts/anchor-master-doc.js --network sepolia
```

### Record Details

Save the output:
```json
{
  "transactionHash": "0xabcdef...",
  "blockNumber": 12345678,
  "contractAddress": "0x1234567890...",
  "anchorId": 0,
  "documentHash": "0xabc123...",
  "timestamp": "2025-12-14T23:30:00.000Z"
}
```

## Step 4: Verification Process

### Verify Document Integrity

Anyone can verify the document using:

```javascript
// verify-document.js
const { ethers } = require("hardhat");
const crypto = require("crypto");
const fs = require("fs");

async function verifyDocument(contractAddress, anchorId, documentPath) {
  // Read and hash document
  const content = fs.readFileSync(documentPath, "utf8");
  const hash = crypto.createHash("sha256").update(content).digest();
  const hashHex = "0x" + hash.toString("hex");
  
  // Get contract
  const DocumentAnchor = await ethers.getContractAt(
    "DocumentAnchor",
    contractAddress
  );
  
  // Verify
  const isValid = await DocumentAnchor.verifyDocument(anchorId, hashHex);
  
  if (isValid) {
    // Get anchor details
    const anchor = await DocumentAnchor.getAnchor(anchorId);
    
    console.log("✅ Document verified successfully!");
    console.log("\nAnchor Information:");
    console.log("- Document:", anchor.documentName);
    console.log("- Hash:", anchor.documentHash);
    console.log("- IPFS CID:", anchor.ipfsCID);
    console.log("- Anchored on:", new Date(Number(anchor.timestamp) * 1000));
    console.log("- Block:", anchor.blockNumber.toString());
    console.log("- By:", anchor.anchoredBy);
  } else {
    console.log("❌ Document verification failed!");
    console.log("The document has been modified since anchoring.");
  }
  
  return isValid;
}

// Usage
const contractAddress = process.argv[2];
const anchorId = process.argv[3];
const documentPath = process.argv[4] || "docs/governance/EXECUTIVE_MASTER_DOCUMENT.md";

verifyDocument(contractAddress, anchorId, documentPath);
```

### Command Line Verification

```bash
# Verify document
node verify-document.js 0x1234... 0 docs/governance/EXECUTIVE_MASTER_DOCUMENT.md
```

### Web-based Verification

Users can verify via Etherscan:

1. Go to https://sepolia.etherscan.io
2. Navigate to contract address
3. Click "Read Contract"
4. Use `getAnchor(0)` to view anchor details
5. Use `verifyDocument(0, hash)` to verify

## Step 5: Documentation

### Update Master Document

Add anchoring details to the master document:

```markdown
### Blockchain Anchoring

**Ethereum Sepolia Testnet:**
- **Contract Address**: 0x1234567890abcdef...
- **Anchor ID**: 0
- **Document Hash**: 0xabc123def456...
- **Transaction Hash**: 0xabcdef123456...
- **Block Number**: 12345678
- **Timestamp**: 2025-12-14 23:30:00 UTC

**Verification:**
Visit [Sepolia Etherscan](https://sepolia.etherscan.io/address/CONTRACT_ADDRESS)
to view the immutable anchor on-chain.
```

### Update README

Add verification section to README.md:

```markdown
## Document Verification

### IPFS Verification
\`\`\`bash
# Download from IPFS
ipfs cat QmXxxx... > document.md

# Verify hash
sha256sum document.md
\`\`\`

### Blockchain Verification
\`\`\`bash
# Verify on Ethereum Sepolia
node scripts/verify-document.js 0x1234... 0
\`\`\`

Or visit: https://sepolia.etherscan.io/address/0x1234...
```

## Monitoring & Maintenance

### Monitor Transaction Status

```javascript
// monitor-anchor.js
const { ethers } = require("hardhat");

async function monitorAnchor(contractAddress, anchorId) {
  const DocumentAnchor = await ethers.getContractAt(
    "DocumentAnchor",
    contractAddress
  );
  
  const anchor = await DocumentAnchor.getAnchor(anchorId);
  const currentBlock = await ethers.provider.getBlockNumber();
  
  const confirmations = currentBlock - Number(anchor.blockNumber);
  
  console.log("Anchor Status:");
  console.log("- Confirmations:", confirmations);
  console.log("- Age:", Math.floor((Date.now()/1000 - Number(anchor.timestamp)) / 86400), "days");
  
  if (confirmations > 1000) {
    console.log("✅ Anchor is well-confirmed and permanent");
  }
}
```

### Backup Anchor Data

```bash
#!/bin/bash
# backup-anchor.sh

CONTRACT_ADDRESS="0x1234..."
ANCHOR_ID="0"

# Get anchor data via etherscan API
curl "https://api-sepolia.etherscan.io/api?module=proxy&action=eth_call&to=$CONTRACT_ADDRESS&data=0x..." \
  > anchor_backup_$(date +%Y%m%d).json
```

## Cost Estimation

### Sepolia Testnet (Free)
- Get test ETH from faucet: https://sepoliafaucet.com
- Deployment cost: ~0.01 test ETH
- Anchoring cost: ~0.0005 test ETH per document

### Mainnet (Production)
- Deployment: ~$50-100 (varies with gas price)
- Anchoring: ~$5-10 per document
- Consider using L2 (Polygon, Arbitrum) for lower costs

## Security Considerations

1. **Private Keys**: Never expose private keys
2. **Contract Verification**: Always verify contract on Etherscan
3. **Test First**: Test on Sepolia before mainnet
4. **Audit**: Consider smart contract audit for production
5. **Upgrades**: Use proxy pattern for upgradeable contracts

## Best Practices

1. **Multiple Chains**: Consider anchoring on multiple chains
2. **Regular Verification**: Periodically verify anchors
3. **Documentation**: Keep detailed records of all anchors
4. **Automation**: Automate anchoring for new versions
5. **Community**: Encourage community verification

---

**Document Version:** 1.0  
**Last Updated:** December 14, 2025  
**Status:** Active Guide
