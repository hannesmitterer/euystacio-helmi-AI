# Enhanced Security and Governance Features

This document describes the three new security and governance mechanisms implemented in the Euystacio framework.

## Overview

The enhanced security framework consists of three interconnected components:

1. **Red Code Veto H-Var**: Emergency veto mechanism for pausing operations
2. **Global Consensus Seal Integrity (G-CSI)**: Multi-signature validation for critical actions
3. **Living Covenant Anchor**: Immutable audit trail linking governance to the Living Covenant

## Red Code Veto H-Var

### Purpose
Provides council members the ability to pause governance operations during security concerns or ethical violations.

### States
- **ACTIVE**: Normal operations allowed
- **SUSPENDED**: All operations suspended pending review
- **EMERGENCY**: Emergency state - only critical functions allowed

### Key Features
- Multi-member council governance
- Configurable signature requirements
- Emergency override capability
- Complete veto history tracking

### Usage Example
```solidity
// Deploy Red Code Veto
RedCodeVeto veto = new RedCodeVeto();

// Add council members
veto.addCouncilMember(councilMember1);
veto.addCouncilMember(councilMember2);

// Set required signatures
veto.setRequiredSignatures(2);

// Initiate a veto
veto.initiateVeto(VetoState.SUSPENDED, "Security concern detected");

// Check if operations are allowed
bool allowed = veto.operationsAllowed(); // returns false

// Resolve veto
bytes32 vetoId = veto.getVetoIdByIndex(0);
veto.resolveVeto(vetoId);
```

### Integration
All governance contracts check `operationsAllowed()` before executing critical operations:

```solidity
require(redCodeVeto.operationsAllowed(), "Red Code Veto: Operations not allowed");
```

## Global Consensus Seal Integrity (G-CSI)

### Purpose
Ensures multi-party consensus through cryptographic seals before executing critical governance actions.

### Key Features
- Council-based signature collection
- Configurable quorum requirements (percentage + minimum)
- Seal creation, signing, and execution workflow
- Permanent seal history

### Workflow
1. Council member creates a seal for an action
2. Other council members sign the seal
3. When quorum is reached, seal can be executed
4. Executed seals are permanently verified

### Usage Example
```solidity
// Deploy G-CSI
GlobalConsensusSealIntegrity gCSI = new GlobalConsensusSealIntegrity();

// Add council members
gCSI.addCouncilMember(member1, "Council Member 1");
gCSI.addCouncilMember(member2, "Council Member 2");

// Set quorum (51% of council, minimum 2 signatures)
gCSI.setQuorumRequirements(51, 2);

// Create a seal
bytes32 actionHash = keccak256(abi.encodePacked("release tranche 1"));
bytes32 sealId = gCSI.createSeal(actionHash, "Tranche 1 release approval");

// Other members sign
gCSI.signSeal(sealId);

// Execute when quorum reached
if (gCSI.hasQuorum(sealId)) {
    gCSI.executeSeal(sealId);
}

// Verify seal
bool valid = gCSI.verifySeal(sealId); // returns true
```

### Quorum Calculation
- Percentage requirement is rounded down (e.g., 51% of 3 = 1.53 = 1)
- Final requirement is `max(percentage_requirement, minimum_signatures)`
- This ensures small councils still have meaningful quorum

## Living Covenant Anchor

### Purpose
Creates an immutable audit trail linking all governance milestones to the Living Covenant.

### Key Concepts
- **Milestone**: A significant governance action (e.g., tranche release)
- **Anchor**: Immutable cryptographic proof tied to a milestone
- **Sealing**: Finalizing a milestone to make it permanent

### Key Features
- Milestone creation and tracking
- Anchor creation and verification
- Milestone sealing (immutability)
- Living Covenant reference updates

### Usage Example
```solidity
// Deploy Living Covenant Anchor
string memory covenantURI = "ipfs://QmCovenantHash";
bytes32 covenantRoot = keccak256("covenant root");
LivingCovenantAnchor lca = new LivingCovenantAnchor(covenantURI, covenantRoot);

// Create a milestone
bytes32 milestoneId = lca.createMilestone(
    "Tranche 1 Release",
    proofHash,
    covenantReference
);

// Create anchors
bytes32 anchor1 = lca.createAnchor(milestoneId, "governance", contentHash1);
bytes32 anchor2 = lca.createAnchor(milestoneId, "covenant", contentHash2);

// Link additional anchors
lca.linkAnchor(milestoneId, anchor2);

// Seal milestone (makes it immutable)
lca.sealMilestone(milestoneId, anchor1);

// Verify
bool sealed = lca.isMilestoneSealed(milestoneId); // returns true
bool valid = lca.verifyAnchor(anchor1); // returns true
```

### Authorized Sealers
To allow governance contracts to seal milestones:

```solidity
// Authorize TrustlessFundingProtocol to seal milestones
lca.addAuthorizedSealer(address(tfp));
```

## Integration Example: Trustless Funding Protocol

The TrustlessFundingProtocol integrates all three security mechanisms:

```solidity
// Set up security contracts
tfp.setRedCodeVeto(address(redCodeVeto));
tfp.setGCSI(address(gCSI));
tfp.setLivingCovenantAnchor(address(lca));

// Authorize TFP to seal milestones
lca.addAuthorizedSealer(address(tfp));

// Release a tranche with full security
// 1. Create and approve G-CSI seal
bytes32 actionHash = keccak256(abi.encodePacked("release tranche 1"));
bytes32 sealId = gCSI.createSeal(actionHash, "Tranche 1 approval");
// ... get council signatures ...
gCSI.executeSeal(sealId);

// 2. Release tranche (checks all security layers)
tfp.releaseTranche(1, proofHash, sealId);
// - Checks Red Code Veto is not active
// - Verifies G-CSI seal
// - Checks sustainment requirements
// - Creates and seals milestone in Living Covenant Anchor
```

## Security Checks Flow

When a governance action is executed:

```
1. Red Code Veto Check
   ↓ (if ACTIVE)
2. G-CSI Seal Verification
   ↓ (if valid)
3. Business Logic (e.g., sustainment check)
   ↓ (if passed)
4. Execute Action
   ↓
5. Create Milestone in Living Covenant Anchor
   ↓
6. Create Anchors
   ↓
7. Seal Milestone
```

## Emergency Procedures

### Emergency Override (Red Code Veto)
Owner can override an active veto:
```solidity
redCodeVeto.emergencyOverride("Emergency situation requires immediate action");
```

### Disable Governance Enforcement
Temporarily disable all governance checks:
```solidity
tfp.setGovernanceEnforcement(false);
```

**WARNING**: Only use in true emergencies. This bypasses all security checks.

## Deployment Guide

### 1. Deploy Core Contracts
```solidity
// Deploy Red Code Veto
RedCodeVeto veto = new RedCodeVeto();

// Deploy G-CSI
GlobalConsensusSealIntegrity gCSI = new GlobalConsensusSealIntegrity();

// Deploy Living Covenant Anchor
LivingCovenantAnchor lca = new LivingCovenantAnchor(covenantURI, covenantRoot);
```

### 2. Configure Red Code Veto
```solidity
veto.addCouncilMember(member1);
veto.addCouncilMember(member2);
veto.addCouncilMember(member3);
veto.setRequiredSignatures(2);
```

### 3. Configure G-CSI
```solidity
gCSI.addCouncilMember(member1, "Member 1");
gCSI.addCouncilMember(member2, "Member 2");
gCSI.addCouncilMember(member3, "Member 3");
gCSI.setQuorumRequirements(51, 2); // 51%, minimum 2 signatures
```

### 4. Integrate with Governance Contracts
```solidity
tfp.setRedCodeVeto(address(veto));
tfp.setGCSI(address(gCSI));
tfp.setLivingCovenantAnchor(address(lca));

// Authorize governance contracts to seal milestones
lca.addAuthorizedSealer(address(tfp));
```

## Best Practices

1. **Council Size**: Maintain odd number of council members to avoid deadlocks
2. **Quorum Settings**: Set percentage high enough for meaningful consensus (e.g., >50%)
3. **Minimum Signatures**: Always require at least 2 signatures for critical actions
4. **Veto Usage**: Document all veto reasons clearly for audit trail
5. **Seal Metadata**: Provide detailed descriptions when creating seals
6. **Emergency Procedures**: Keep emergency override keys secure and multi-sig protected

## Gas Considerations

Approximate gas costs (Ethereum):
- Red Code Veto check: ~5,000 gas
- G-CSI seal verification: ~10,000 gas
- Milestone creation: ~80,000 gas
- Anchor creation: ~60,000 gas
- Milestone sealing: ~30,000 gas

Total overhead per governance action: ~185,000 gas

## Testing

Comprehensive test suite included:
- 25 tests for Red Code Veto
- 27 tests for G-CSI
- 28 tests for Living Covenant Anchor
- 9 integration tests
- All backward compatibility tests pass

Run tests:
```bash
npx hardhat test
```

## Events

All contracts emit detailed events for transparency:

### Red Code Veto
- `StateChanged(previousState, newState, reason)`
- `VetoInitiated(vetoId, state, initiator, reason)`
- `VetoResolved(vetoId, resolver)`

### G-CSI
- `SealCreated(sealId, actionHash, metadata)`
- `SealSigned(sealId, signer)`
- `SealExecuted(sealId)`

### Living Covenant Anchor
- `MilestoneCreated(milestoneId, description, initiator)`
- `AnchorCreated(anchorHash, milestoneId, anchorType)`
- `MilestoneSealed(milestoneId, anchorHash)`

## Breaking Changes

**TrustlessFundingProtocol.releaseTranche**: Function signature changed from 2 to 3 parameters.

**Before:**
```solidity
function releaseTranche(uint256 trancheId, bytes32 proofHash)
```

**After:**
```solidity
function releaseTranche(uint256 trancheId, bytes32 proofHash, bytes32 sealId)
```

**Migration**: Pass `bytes32(0)` for sealId if G-CSI validation is not required.

## Security Considerations

1. **Council Member Management**: Only trusted addresses should be council members
2. **Private Keys**: Council member keys must be secured (consider hardware wallets)
3. **Quorum Settings**: Too low = not secure, too high = operational bottleneck
4. **Emergency Override**: Should be multi-sig controlled
5. **Contract Upgrades**: These contracts are not upgradeable - deploy new versions carefully

## Support and Questions

For questions or issues:
1. Review test files in `test/` directory for usage examples
2. Check contract comments for detailed parameter descriptions
3. Open an issue on GitHub for bugs or feature requests

## License

MIT License - See LICENSE file for details
