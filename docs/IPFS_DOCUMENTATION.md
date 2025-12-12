# IPFS Documentation Structure

## Overview

All euystacio-helmi-AI documentation follows a verifiable, immutable structure using IPFS (InterPlanetary File System). This ensures transparency, prevents retroactive alterations, and provides cryptographic proof of content integrity.

## Root CID

**Official Documentation Root**: `QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5`

This CID serves as the canonical entry point for all framework documentation. It contains a directory structure with versioned documents and their corresponding hashes.

## Document Categories

### 1. Foundation Documents

Core principles and architectural decisions:

- **Sensisara Principle**: Philosophy and natural patterns
- **Bioarchitecture**: System design and layers
- **Governance Model**: Decision-making processes
- **Ethical Framework**: AI rights and responsibilities

### 2. Technical Specifications

Implementation details and APIs:

- **Smart Contract Specs**: Governance, Treasury, Bonding
- **API Documentation**: Endpoints and data formats
- **Integration Guides**: Web3 and ML toolchain
- **Security Audits**: Vulnerability assessments

### 3. Governance Records

On-chain and community decisions:

- **Proposals**: Full text with IPFS CIDs
- **Voting Records**: Transparent tallies
- **Execution Logs**: Implementation of passed proposals
- **Amendment History**: Changes to core documents

### 4. Development Resources

Tools and guides for contributors:

- **CLI Documentation**: Command reference
- **SDK Reference**: API and usage examples
- **Tutorial Series**: Step-by-step guides
- **Example Projects**: Reference implementations

## CID Verification Process

### Step 1: Retrieve Document

```bash
ipfs get QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5
```

### Step 2: Verify Content Hash

```bash
ipfs add -n <document-path>
# Compare output CID with expected CID
```

### Step 3: Check Signature

Many documents include GPG signatures for additional verification:

```bash
gpg --verify document.txt.asc document.txt
```

## Document Lifecycle

### 1. Creation

1. Author creates document
2. Document is reviewed by community
3. Final version is uploaded to IPFS
4. CID is recorded in governance contract

### 2. Versioning

Each version gets a unique CID:

```
v1.0.0 → QmAbc123...
v1.1.0 → QmDef456...
v2.0.0 → QmGhi789...
```

The root directory tracks all versions with metadata:

```json
{
  "document": "Sensisara Principle",
  "versions": [
    {
      "version": "1.0.0",
      "cid": "QmAbc123...",
      "date": "2025-01-15",
      "author": "hannesmitterer"
    },
    {
      "version": "1.1.0",
      "cid": "QmDef456...",
      "date": "2025-03-20",
      "author": "community"
    }
  ]
}
```

### 3. Governance Integration

Proposals must reference IPFS CIDs:

```solidity
function createProposal(
    string memory ipfsCid,  // e.g., "QmXxx..."
    string memory title
) external returns (uint256)
```

This ensures:
- **Immutability**: Cannot change proposal after creation
- **Transparency**: Anyone can verify proposal content
- **Auditability**: Full history is preserved

## Pinning Strategy

### Primary Pinning

Documents are pinned on multiple nodes:

1. **Project Infrastructure**: Main IPFS nodes
2. **Pinata**: Commercial pinning service
3. **Web3.Storage**: Decentralized storage
4. **Community Nodes**: Volunteer pinners

### Redundancy

Critical documents are pinned with redundancy:
- Minimum 5 nodes for core documents
- Minimum 3 nodes for governance proposals
- Minimum 2 nodes for development resources

## Access Methods

### Via IPFS Gateway

```
https://ipfs.io/ipfs/QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5
```

### Via Local Node

```bash
ipfs cat QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5
```

### Via Public Gateways

Multiple gateways for resilience:
- `https://ipfs.io/ipfs/<CID>`
- `https://cloudflare-ipfs.com/ipfs/<CID>`
- `https://gateway.pinata.cloud/ipfs/<CID>`

## Document Templates

### Proposal Template

```markdown
# Proposal: [Title]

**IPFS CID**: QmXxx...
**Author**: [address/name]
**Date**: [ISO 8601]
**Version**: [semver]

## Summary
[Brief description]

## Motivation
[Why this proposal]

## Specification
[Technical details]

## Implementation
[How to execute]

## Security Considerations
[Risks and mitigations]

## References
[Links to related documents]
```

### Technical Specification Template

```markdown
# [Component Name] Specification

**IPFS CID**: QmXxx...
**Version**: [semver]
**Status**: [Draft/Proposed/Accepted/Implemented]

## Abstract
[Brief overview]

## Specification
[Detailed technical spec]

## Rationale
[Design decisions]

## Implementation
[Code references]

## Test Cases
[Validation]

## References
[Related specs]
```

## Verification Tools

### CLI Verification

```bash
# Verify document exists and get content
euystacio-cli ipfs verify QmXxx...

# List all versions of a document
euystacio-cli ipfs versions sensisara-principle

# Download and verify signature
euystacio-cli ipfs get QmXxx... --verify-sig
```

### Web Dashboard

Access via: `monitor.eustacio.org/ipfs-verify`

Features:
- Visual CID verification
- Version comparison
- Pinning status check
- Signature validation

## Benefits

1. **Transparency**: All changes are visible
2. **Immutability**: Content cannot be altered
3. **Verifiability**: Anyone can validate
4. **Resilience**: Distributed storage
5. **Permanence**: Content persists indefinitely
6. **Trust**: Cryptographic proof of integrity

## Best Practices

1. **Always pin important documents** to multiple nodes
2. **Use descriptive filenames** that include version
3. **Include metadata** in directory structures
4. **Sign critical documents** with GPG
5. **Reference CIDs** in governance proposals
6. **Update root directory** when adding new versions
7. **Test CIDs** before referencing in contracts

## Migration from Legacy Docs

1. Upload document to IPFS
2. Record CID in migration log
3. Update references in code/contracts
4. Keep old URLs as redirects (with notice)
5. Archive old versions with CIDs

---

*"Verifiable documentation is the foundation of trustless systems."*
