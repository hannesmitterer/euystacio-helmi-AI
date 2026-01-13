# EuystacioSTAnchor - Deployment Sealing & Red Code Veto H-Var

## Overview

The **EuystacioSTAnchor** contract implements the deployment sealing process for the Euystacio-Helmi-AI framework, providing:

1. **Red Code Veto H-Var Capabilities** - Ultimate ethical override through Human Variable (H-Var) authority
2. **Deployment Key Locking** - Immutable deployment key registry with IPFS backing
3. **Runtime Parameter Sealing** - Lock critical runtime parameters to reflect immutable governance states
4. **G-CSI IPFS Anchoring** - Link governance documents with IPFS-backed cryptographic validation

## Key Features

### 🔴 Red Code Veto H-Var (Human Variable)

The Red Code Veto mechanism ensures that human ethical oversight remains supreme over all automated governance decisions:

- **Immutable Veto Authority**: Set at deployment, cannot be changed
- **Ultimate Override**: Can be invoked even when deployment is sealed
- **Governance Integration**: Authorized governance contracts can invoke veto on behalf of authority
- **IPFS-Backed Ethics**: Red Code ethical framework anchored on IPFS for transparency

```solidity
// Invoke Red Code Veto - ultimate ethical override
function invokeRedCodeVeto(string calldata reason) external;

// Set Red Code IPFS CID
function setRedCodeIPFS(string calldata ipfsCID) external;
```

### 🔒 Deployment Sealing

Irreversible deployment sealing process that locks the entire governance system:

```solidity
// Lock governance state (prevents parameter changes)
function lockGovernanceState() external;

// Seal deployment (prevents any further configuration)
function sealDeployment() external;
```

**Sealing Workflow:**
1. Configure all deployment keys
2. Set all runtime parameters
3. Anchor governance documents
4. Lock critical components
5. Lock governance state
6. Seal deployment (IRREVERSIBLE)

### 🔑 Deployment Key Management

Secure registry for deployment keys with IPFS documentation:

```solidity
struct DeploymentKey {
    string name;
    bytes32 keyHash;
    bool locked;
    uint256 lockedAt;
    string ipfsCID;  // IPFS documentation
}

// Register a deployment key
function registerDeploymentKey(
    bytes32 keyId,
    string calldata name,
    bytes32 keyHash,
    string calldata ipfsCID
) external;

// Lock a deployment key (irreversible)
function lockDeploymentKey(bytes32 keyId) external;
```

### ⚙️ Runtime Parameter Locking

Lock runtime parameters to reflect immutable governance states:

```solidity
struct RuntimeParameter {
    string name;
    bytes32 valueHash;
    bool locked;
    uint256 lockedAt;
    string description;
}

// Set a runtime parameter
function setRuntimeParameter(
    bytes32 paramId,
    string calldata name,
    bytes32 valueHash,
    string calldata description
) external;

// Lock a runtime parameter (irreversible)
function lockRuntimeParameter(bytes32 paramId) external;
```

### 📚 G-CSI IPFS Anchoring

Link Governance-CSI (G-CSI) with IPFS-backed anchoring graphs for cryptographic validation:

```solidity
struct GovernanceDocument {
    string name;
    string ipfsCID;
    bytes32 contentHash;  // For cryptographic validation
    uint256 timestamp;
    bool validated;
}

// Anchor a governance document
function anchorGovernanceDocument(
    bytes32 docId,
    string calldata name,
    string calldata ipfsCID,
    bytes32 contentHash
) external;

// Validate document's cryptographic hash
function validateGovernanceDocument(bytes32 docId) external;

// Update G-CSI anchoring graph
function updateGCSIAnchoringGraph(string calldata ipfsCID) external;
```

## Integration with EUSDaoGovernance

The EUSDaoGovernance contract now integrates with EuystacioSTAnchor for Red Code Veto capabilities:

```solidity
// Set the STAnchor contract
function setSTAnchor(address _stAnchor) external onlyOwner;

// Enable Red Code Veto integration
function setRedCodeVetoEnabled(bool enabled) external onlyOwner;

// Invoke Red Code Veto from governance (requires veto authority)
function invokeRedCodeVetoFromGovernance(string calldata reason) external;

// Check if governance is operating under sealed deployment
function isGovernanceSealed() external view returns (bool);
```

## Deployment

### 1. Deploy EuystacioSTAnchor

```bash
# Set environment variables
export RED_CODE_VETO_AUTHORITY=0x... # Veto authority address
export RED_CODE_IPFS_CID=Qm...       # Optional: Red Code IPFS CID
export GCSI_GRAPH_CID=Qm...          # Optional: G-CSI graph CID

# Deploy
npm run deploy:stanchor
```

### 2. Configure Integration with Governance

```javascript
// Deploy and configure
const anchor = await EuystacioSTAnchor.deploy(vetoAuthority);
const governance = await EUSDaoGovernance.deploy();

// Set up integration
await governance.setSTAnchor(anchor.address);
await governance.setRedCodeVetoEnabled(true);

// Authorize governance to invoke veto
await anchor.setAuthorizedGovernanceContract(governance.address, true);
```

### 3. Complete Deployment Sealing

```javascript
// 1. Set Red Code IPFS
await anchor.connect(vetoAuthority).setRedCodeIPFS("QmRedCode...");

// 2. Register deployment keys
await anchor.registerDeploymentKey(
    keyId, "MainDeployKey", keyHash, "QmKeyDoc..."
);

// 3. Set runtime parameters
await anchor.setRuntimeParameter(
    paramId, "MaxSupply", valueHash, "Max token supply"
);

// 4. Anchor governance documents
await anchor.anchorGovernanceDocument(
    docId, "Charter", "QmCharter...", contentHash
);
await anchor.validateGovernanceDocument(docId);

// 5. Update G-CSI graph
await anchor.updateGCSIAnchoringGraph("QmGCSI...");

// 6. Lock everything
await anchor.lockDeploymentKey(keyId);
await anchor.lockRuntimeParameter(paramId);
await anchor.lockGovernanceState();
await anchor.sealDeployment(); // IRREVERSIBLE!
```

## Testing

```bash
# Test EuystacioSTAnchor contract
npm run test:stanchor

# Test governance integration
npm test -- test/stanchor-governance-integration.test.js

# Run all tests
npm test
```

## Security Considerations

1. **Veto Authority**: The Red Code Veto Authority address is immutable after deployment. Choose wisely.
2. **Sealing is Irreversible**: Once `sealDeployment()` is called, no configuration changes are possible.
3. **Lock Before Seal**: Ensure all keys and parameters are locked before sealing.
4. **IPFS Persistence**: Ensure all IPFS CIDs are pinned and permanently accessible.
5. **Content Hash Validation**: Always validate governance documents after anchoring.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│          EuystacioSTAnchor Contract                 │
│  (Deployment Sealing & Red Code Veto H-Var)        │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │ Red Code Veto H-Var (Human Variable)     │     │
│  │ - Immutable veto authority               │     │
│  │ - Ultimate ethical override              │     │
│  │ - IPFS-backed ethical framework          │     │
│  └──────────────────────────────────────────┘     │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │ Deployment Key Registry                  │     │
│  │ - IPFS-backed documentation              │     │
│  │ - Irreversible locking                   │     │
│  └──────────────────────────────────────────┘     │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │ Runtime Parameter Locking                │     │
│  │ - Immutable governance states             │     │
│  │ - Hash-based validation                  │     │
│  └──────────────────────────────────────────┘     │
│                                                     │
│  ┌──────────────────────────────────────────┐     │
│  │ G-CSI IPFS Anchoring                     │     │
│  │ - Governance document registry           │     │
│  │ - Cryptographic validation               │     │
│  │ - Anchoring graph management             │     │
│  └──────────────────────────────────────────┘     │
│                                                     │
└─────────────────────────────────────────────────────┘
                       │
                       │ Integration
                       ▼
┌─────────────────────────────────────────────────────┐
│          EUSDaoGovernance Contract                  │
│                                                     │
│  - Red Code Veto integration                       │
│  - Sealed governance state checks                  │
│  - Authorized veto invocation                      │
└─────────────────────────────────────────────────────┘
```

## Events

```solidity
event DeploymentSealed(uint256 timestamp, address sealedBy);
event GovernanceStateLocked(uint256 timestamp, address lockedBy);
event RedCodeVetoInvoked(address invoker, string reason, uint256 timestamp);
event DeploymentKeyRegistered(bytes32 indexed keyId, string name, string ipfsCID);
event DeploymentKeyLocked(bytes32 indexed keyId, uint256 timestamp);
event RuntimeParameterSet(bytes32 indexed paramId, string name, bytes32 valueHash);
event RuntimeParameterLocked(bytes32 indexed paramId, uint256 timestamp);
event GovernanceDocumentAnchored(bytes32 indexed docId, string ipfsCID, bytes32 contentHash);
event GCSIAnchoringGraphUpdated(string ipfsCID, uint256 timestamp);
event RedCodeIPFSUpdated(string ipfsCID, uint256 timestamp);
event GovernanceContractAuthorized(address indexed govContract, bool authorized);
```

## License

MIT License - See LICENSE file for details

## Ethical Commitment

This contract embodies the Euystacio framework's commitment to:
- Human-centric AI governance
- Transparent and immutable ethical principles
- Decentralized validation through IPFS
- Ultimate human oversight via Red Code Veto H-Var

The Red Code Veto ensures that human ethical judgment always has the final say, even in fully automated systems.
