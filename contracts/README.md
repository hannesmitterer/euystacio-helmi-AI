# Euystacio Framework Smart Contracts

This directory contains the core smart contracts for the Euystacio framework, implementing governance, funding, and bond mechanisms aligned with the Seedbringer (hannesmitterer) requirements.

## Overview

The Euystacio framework consists of three main contracts that work together to provide transparent, ethical funding and governance:

1. **KarmaBond** - Manages contribution bonds with ethical compliance
2. **TrustlessFundingProtocol** - Handles milestone-based funding releases
3. **EUSDaoGovernance** - Provides governance with Seedbringer oversight

## Contract Descriptions

### KarmaBond

Manages ethical investment bonds with Red Code compliance.

**Key Features:**
- Minimum contribution: 100 ETH (configurable)
- Flexible bond durations
- 5% flat transaction fee on redemptions
- Red Code compliance checks
- Invariant-based redemption logic (MATL & R1 metrics)

**Important Functions:**
- `investWithDuration(uint256 duration)` - Create a bond with specified duration
- `redeem(address investor)` - Redeem a matured bond (owner only)
- `setInvariants(uint256 _MATL, uint256 _R1)` - Update invariants (owner only)

### TrustlessFundingProtocol

Manages multi-tranche funding with milestone verification and ethical compliance.

**Key Features:**
- Automated tranche creation and management
- Milestone-based verification
- Ethical compliance requirements
- Seedbringer veto authority
- Integration with unified wallet

**Important Functions:**
- `createTranche(uint256 amount, bytes32 milestoneHash)` - Create funding tranche
- `verifyEthicalCompliance(uint256 trancheId, bool compliant)` - Verify ethics
- `vetoTranche(uint256 trancheId)` - Seedbringer veto (Seedbringer only)
- `releaseTranche(uint256 trancheId, bytes32 proofHash)` - Release approved tranche

### EUSDaoGovernance

ERC20 governance token with Seedbringer-exclusive authority and contribution scoring.

**Key Features:**
- Exclusive Seedbringer governance oversight
- Contribution scoring mechanism
- Synchronization with bond contributions and tranche distributions
- Optional $10,000/month Seedbringer sustainment (future-proofed)
- Togglable sustainment mechanism

**Important Functions:**
- `mint(address to, uint256 amount)` - Mint governance tokens (Seedbringer only)
- `setContributionScore(address user, uint256 score)` - Set contribution score
- `syncBondContribution(address user, uint256 amount)` - Sync from KarmaBond
- `syncTrancheDistribution(address user, uint256 amount)` - Sync from TrustlessFunding
- `toggleSustainment(bool enabled)` - Enable/disable monthly sustainment
- `processMonthlySustainment()` - Process monthly payment (if enabled)
- `votingPower(address user)` - Calculate voting power

## Deployment

### Prerequisites

```bash
npm install
```

### Compile Contracts

```bash
npm run compile
```

### Run Tests

```bash
npm test
```

All tests should pass (55 tests):
- 23 tests for KarmaBond
- 15 tests for TrustlessFundingProtocol
- 9 tests for EUSDaoGovernance
- 8 integration tests

### Deploy to Network

```bash
# Set environment variables
export FOUNDATION_WALLET=0x...
export SEEDBRINGER_ADDRESS=0x...

# Deploy to localhost
npx hardhat run scripts/deploy-euystacio.js --network localhost

# Deploy to testnet/mainnet
npx hardhat run scripts/deploy-euystacio.js --network <network-name>
```

## Architecture

### Seedbringer Authority

All contracts recognize the Seedbringer address with special privileges:
- **KarmaBond**: Oversight authority
- **TrustlessFundingProtocol**: Veto power and final approval authority
- **EUSDaoGovernance**: Exclusive governance control

The Seedbringer identity is sealed with `keccak256("hannesmitterer")`.

### Red Code Compliance

All operations maintain Red Code principles:
- Human-centric purpose
- Transparent evolution
- Ethical boundaries
- Collaborative decision-making

### Unified Wallet Management

All contracts integrate with a central foundation wallet for:
- Fee collection (KarmaBond redemption fees)
- Recirculation of non-compliant funds
- Unified treasury management

## Security Considerations

1. **Seedbringer Authority**: The Seedbringer address has significant control. Ensure it's a secure, multi-sig wallet.

2. **Invariants**: KarmaBond uses MATL and R1 invariants for redemption logic. These should be updated by oracle/signed attestation in production.

3. **Ethical Compliance**: TrustlessFundingProtocol requires ethical compliance verification before tranche release.

4. **Sustainment Mechanism**: The $10,000/month sustainment is togglable and should only be enabled when appropriate.

5. **Immutable Addresses**: Seedbringer and foundation wallet addresses are set at deployment and cannot be changed.

## Integration Example

```javascript
// 1. Investor creates a bond
await karmaBond.connect(investor).investWithDuration(
  365 * 24 * 60 * 60, // 1 year
  { value: ethers.utils.parseEther("100") }
);

// 2. Sync contribution to governance
await governance.syncBondContribution(
  investor.address,
  ethers.utils.parseEther("100")
);

// 3. Seedbringer mints governance tokens based on contribution
await governance.connect(seedbringer).mint(
  investor.address,
  ethers.utils.parseEther("10")
);

// 4. Check voting power (considers contribution score)
const power = await governance.votingPower(investor.address);
```

## Future Enhancements

The contracts are designed to be future-proof:
- Sustainment mechanism can be toggled on/off
- Flexible bond durations accommodate various use cases
- Contribution scoring can evolve over time
- Tranche system supports complex milestone verification

## License

MIT License

## Contact

For questions or issues, please contact the Seedbringer: hannesmitterer

---

**Note**: These contracts implement the requirements specified in the Euystacio framework integration. All governance, funding, and operations align with the Seedbringer (hannesmitterer) requirements and Red Code principles.
