# Tokenomics V2.0 - Sensisara Evolved Cycle

## Overview

The Tokenomics V2.0 system implements a comprehensive incentive mechanism to promote participation in the Sensisara Evolved cycle. It provides verifiable on-chain rewards for ethical researchers, DAO validators, trusted service providers, and automation operators.

## System Architecture

### Core Components

1. **TokenomicsV2** - Main token contract with pool-based reward distribution
2. **EthicalDatasetRegistry** - Dataset validation with DAO voting
3. **ModelRetrainingEscrow** - Retraining proposals with token escrow
4. **EcosystemInteractionModule (EIM)** - External service provider integration
5. **KSyncOracle** - Automation operator management

## Token Allocation

| Category | Allocation | Purpose |
|----------|-----------|---------|
| Ethical Researchers | 35% | Dataset validation and error correction |
| DAO Validators | 20% | Quorum participation and voting |
| Trusted Providers | 15% | External service integrations (EIM) |
| Operators | 20% | K-Sync daemon automation |
| Community Reserve | 10% | Sustainability and growth |

**Total Initial Supply:** 10,000,000 SENS tokens

## Contract Descriptions

### 1. TokenomicsV2

The core ERC20 token contract that manages reward pools and distribution.

**Key Features:**
- Pool-based token allocation (35/20/15/20/10%)
- Authorized distributor system
- Controlled annual inflation (max 5%)
- Community reserve management

**Main Functions:**
- `distributeEthicalResearcherReward(address, uint256, string)` - Reward researchers
- `distributeDAOValidatorReward(address, uint256, string)` - Reward validators
- `distributeTrustedProviderReward(address, uint256, string)` - Reward providers
- `distributeOperatorReward(address, uint256, string)` - Reward operators
- `mintInflation(uint256)` - Mint controlled inflation (yearly, max 5%)

### 2. EthicalDatasetRegistry

Manages ethical corrected dataset (ECD) proposals with DAO validation.

**Workflow:**
1. Researcher submits dataset proposal with IPFS CID and impact factor
2. DAO members vote on proposal (3-day voting period)
3. After voting, proposal is executed if quorum and approval thresholds met
4. Researcher receives reward based on impact factor
5. Validators receive participation rewards

**Key Parameters:**
- Quorum: 50% of total voting power
- Approval Threshold: 60% of votes
- Voting Period: 3 days
- Base Reward: 1,000 SENS
- Impact Multiplier: Up to 3x based on error severity (1-100)

**Reward Formula:**
```
reward = baseReward * (1 + (impactFactor / 100) * maxImpactMultiplier)
```

### 3. ModelRetrainingEscrow

Manages model retraining proposals with token escrow to ensure serious submissions.

**Workflow:**
1. Proposer stakes minimum tokens and submits retraining proposal
2. DAO votes on proposal (5-day voting period)
3. If approved, operator can start retraining
4. Upon successful completion, proposer receives reward and escrow refund
5. If failed, escrow may be slashed or refunded based on circumstances

**Key Parameters:**
- Quorum: 40% of total voting power
- Approval Threshold: 60% of votes
- Voting Period: 5 days
- Minimum Escrow: 100 SENS
- Base Reward: 2,000 SENS
- Complexity Multiplier: Up to 5x (1-100)

**Reward Formula:**
```
reward = baseReward * (1 + (complexity / 100) * maxComplexityMultiplier)
```

### 4. EcosystemInteractionModule (EIM)

Manages external service provider integration with query-based micro-rewards.

**Provider Types:**
- Ocean Protocol integrations
- External oracles
- Data marketplace providers
- AI service integrators

**Reward Tiers:**
- **Standard Query:** 5 SENS per verified query
- **High-Value Query:** 55 SENS (requires 50+ reputation)
- **Premium Query:** 205 SENS (requires 80+ reputation)
- **Integration Bonus:** 1,000 SENS for new integrations

**Key Features:**
- Provider registration and reputation tracking
- Signed query verification
- Reputation-based query tier access
- Integration bonus rewards

### 5. KSyncOracle

Manages K-Sync daemon operators who execute model retraining.

**Workflow:**
1. Operator stakes minimum tokens to register
2. Operator provides API endpoint for automation
3. Owner assigns retraining executions to operators
4. Upon completion, operator receives reward + gas reimbursement
5. Failed executions result in stake slashing

**Key Parameters:**
- Minimum Stake: 500 SENS
- Base Execution Reward: 100 SENS
- Gas Reimbursement: 150% of actual gas cost
- Success Bonus: 2x multiplier
- Failure Penalty: 10 SENS
- Max Consecutive Failures: 3 (then deactivation)

**Reward Formula:**
```
reward = (baseReward + gasReimbursement) * successBonusMultiplier
```

## Deployment

### Prerequisites
```bash
npm install
```

### Compile Contracts
```bash
npx hardhat compile
```

### Run Tests
```bash
npx hardhat test
npx hardhat test test/tokenomicsv2/tokenomics.test.js
npx hardhat test test/tokenomicsv2/integration.test.js
```

### Deploy to Testnet
```bash
# Configure .env with SEPOLIA_RPC_URL and PRIVATE_KEY_DEPLOYER
npx hardhat run scripts/deploy_tokenomics_v2.js --network sepolia
```

### Deploy to Local Network
```bash
npx hardhat node
# In another terminal:
npx hardhat run scripts/deploy_tokenomics_v2.js --network localhost
```

## Usage Examples

### 1. Submit Dataset Proposal
```javascript
const datasetRegistry = await ethers.getContractAt("EthicalDatasetRegistry", ADDRESS);
await datasetRegistry.submitProposal(
  "QmYourIPFSCID",
  "Fixed bias in training data affecting model fairness",
  85 // High impact factor
);
```

### 2. Vote on Proposal
```javascript
const votingPower = await governanceToken.votingPower(voterAddress);
await datasetRegistry.castVote(proposalId, true, votingPower);
```

### 3. Register as Provider
```javascript
const eim = await ethers.getContractAt("EcosystemInteractionModule", ADDRESS);
// Must be called by owner
await eim.registerProvider(providerAddress, "Ocean Protocol Integration");
```

### 4. Register as Operator
```javascript
const ksync = await ethers.getContractAt("KSyncOracle", ADDRESS);
const stakeAmount = ethers.parseEther("500");

// Approve tokens
await tokenomics.approve(ksyncAddress, stakeAmount);

// Register
await ksync.registerOperator(stakeAmount, "https://your-ksync-daemon.com/api");
```

## Security Considerations

1. **Access Control:** Only authorized distributor contracts can distribute rewards
2. **Escrow Protection:** Retraining proposals require token escrow to prevent spam
3. **Reputation System:** Providers must build reputation for high-value queries
4. **Stake Slashing:** Operators are penalized for failed executions
5. **Inflation Control:** Maximum 5% annual inflation to maintain token value
6. **Reentrancy Guards:** All reward distributions protected against reentrancy attacks

## Integration with Existing System

The Tokenomics V2.0 system integrates with:
- **EUSDaoGovernance** - For voting power calculation
- **KarmaBond** - For staking mechanism compatibility
- **Sustainment** - For long-term treasury sustainability

## Governance Parameters

All governance parameters can be updated by the contract owner:

### EthicalDatasetRegistry
- `setGovernanceParameters(quorum, threshold, votingPeriod)`
- `setRewardParameters(baseReward, maxMultiplier, validatorReward)`

### ModelRetrainingEscrow
- `setGovernanceParameters(quorum, threshold, votingPeriod)`
- `setEscrowRewardParameters(minEscrow, baseReward, maxMultiplier)`

### EcosystemInteractionModule
- `setRewardParameters(microReward, highValueBonus, premiumBonus, integrationBonus)`
- `setReputationThresholds(minForHighValue, minForPremium)`

### KSyncOracle
- `setStakingParameters(minStake, failurePenalty, maxFailures)`
- `setRewardParameters(baseReward, gasReimbursementRate, successBonus)`

## Monitoring and Analytics

### Pool Balances
```javascript
const ethicalPool = await tokenomics.ethicalResearchersPool();
const validatorPool = await tokenomics.daoValidatorsPool();
const providerPool = await tokenomics.trustedProvidersPool();
const operatorPool = await tokenomics.operatorsPool();
const reservePool = await tokenomics.communityReservePool();
```

### Provider Statistics
```javascript
const [active, regTime, queries, rewards, service, reputation] = 
  await eim.getProvider(providerAddress);
```

### Operator Performance
```javascript
const [active, stake, regTime, total, successful, rewards, endpoint] = 
  await ksync.getOperator(operatorAddress);
const successRate = (successful * 100) / total;
```

## Next Steps

1. ✅ Deploy to testnet
2. ✅ Conduct security audit
3. ✅ Test with DAO governance
4. ✅ Integrate with existing IPFS infrastructure
5. ✅ Deploy K-Sync daemon
6. ✅ Onboard initial providers and operators
7. ✅ Launch on mainnet

## License

MIT License - See LICENSE file for details

## Support

For questions and support, please open an issue in the repository or contact the development team.
