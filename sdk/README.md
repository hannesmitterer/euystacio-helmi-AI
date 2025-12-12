# Euystacio-Helmi SDK

Software Development Kit for Web3 and ML integrators.

## Installation

```bash
npm install euystacio-helmi-sdk
```

Or use from repository:

```bash
cd sdk
npm install
```

## Quick Start

### Basic Setup

```javascript
const { EuystacioHelmiSDK } = require('euystacio-helmi-sdk');

const sdk = new EuystacioHelmiSDK({
  rpcUrl: 'https://mainnet.infura.io/v3/YOUR-PROJECT-ID',
  privateKey: 'YOUR-PRIVATE-KEY', // Optional, for write operations
  governanceAddress: '0xGovernanceContractAddress'
});

await sdk.initialize();
```

### Environment Variables

Create a `.env` file:

```env
RPC_URL=https://mainnet.infura.io/v3/YOUR-PROJECT-ID
PRIVATE_KEY=your-private-key
GOVERNANCE_ADDRESS=0xGovernanceContractAddress
```

Then:

```javascript
require('dotenv').config();
const sdk = new EuystacioHelmiSDK();
await sdk.initialize();
```

## Governance Operations

### Create a Proposal

```javascript
const result = await sdk.createProposal(
  'QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5',
  'Proposal to upgrade treasury'
);

console.log('Proposal ID:', result.proposalId);
```

### Vote on a Proposal

```javascript
await sdk.vote(1, true); // Vote yes on proposal 1
await sdk.vote(2, false); // Vote no on proposal 2
```

### Get Proposal Details

```javascript
const proposal = await sdk.getProposal(1);
console.log('Title:', proposal.title);
console.log('IPFS CID:', proposal.ipfsCid);
console.log('Votes For:', proposal.votesFor);
console.log('Votes Against:', proposal.votesAgainst);
console.log('Status:', proposal.executed ? 'Executed' : 'Pending');
```

### Check Proposal Status

```javascript
const hasQuorum = await sdk.hasQuorum(1);
const isPassed = await sdk.isPassed(1);

console.log('Quorum reached:', hasQuorum);
console.log('Proposal passed:', isPassed);
```

### Get Voting Power

```javascript
const myPower = await sdk.getVotingPower();
console.log('My voting power:', myPower);

// Check another address
const theirPower = await sdk.getVotingPower('0xOtherAddress');
console.log('Their voting power:', theirPower);
```

## IPFS Operations

### Fetch Document

```javascript
const content = await sdk.fetchFromIPFS('QmXxx...');
console.log('Document content:', content);
```

### Verify CID

```javascript
const verification = await sdk.verifyIPFSCID('QmXxx...');
console.log('Valid:', verification.valid);
console.log('Content length:', verification.contentLength);
```

## ML Integration with Sensisara Principle

### Homeostatic Balancing

Apply natural bounds and smoothing to model outputs:

```javascript
const { SensisaraML } = require('euystacio-helmi-sdk');

const rawOutputs = [0.95, 0.02, 0.88, 0.12];

const balanced = SensisaraML.applyHomeostasis(rawOutputs, {
  minThreshold: 0.1,   // Minimum output value
  maxThreshold: 0.9,   // Maximum output value
  smoothingFactor: 0.3 // Damping factor
});

console.log('Balanced outputs:', balanced);
```

### Quorum-Based Decisions

Combine multiple models with consensus requirement:

```javascript
const { SensisaraML } = require('euystacio-helmi-sdk');

// Outputs from 3 different models
const model1 = [0.8, 0.2, 0.7];
const model2 = [0.75, 0.25, 0.72];
const model3 = [0.82, 0.18, 0.68];

const decision = SensisaraML.quorumDecision(
  [model1, model2, model3],
  0.6 // 60% confidence threshold
);

console.log('Consensus outputs:', decision.outputs);
console.log('Confidence:', decision.confidence);
console.log('Meets quorum:', decision.meetsQuorum);
console.log('Average confidence:', decision.averageConfidence);
```

## Advanced Usage

### Get Governance Parameters

```javascript
const params = await sdk.getGovernanceParams();
console.log('Cooldown period:', params.proposalCooldown);
console.log('Voting period:', params.votingPeriod);
console.log('Quorum percentage:', params.quorumPercentage);
```

### Check Voting History

```javascript
const proposalCount = await sdk.getProposalCount();

for (let i = 1; i <= proposalCount; i++) {
  const hasVoted = await sdk.hasVoted(i);
  console.log(`Proposal ${i}: ${hasVoted ? 'Voted' : 'Not voted'}`);
}
```

## Web3 Integration Example

```javascript
const { EuystacioHelmiSDK } = require('euystacio-helmi-sdk');
const { ethers } = require('ethers');

// Connect with MetaMask or other Web3 provider
const provider = new ethers.BrowserProvider(window.ethereum);
const signer = await provider.getSigner();

const sdk = new EuystacioHelmiSDK({
  rpcUrl: await provider.getNetwork().then(n => n.rpcUrls[0]),
  governanceAddress: '0xGovernanceAddress'
});

// Override signer for transactions
sdk.signer = signer;

// Now you can make transactions
await sdk.vote(1, true);
```

## Error Handling

```javascript
try {
  const result = await sdk.createProposal(cid, title);
  console.log('Success:', result.proposalId);
} catch (error) {
  if (error.message.includes('Cooldown period active')) {
    console.log('Please wait before creating another proposal');
  } else if (error.message.includes('Rate limit exceeded')) {
    console.log('Too many proposals in this period');
  } else {
    console.error('Error:', error.message);
  }
}
```

## Testing

```javascript
// Use with test networks
const sdk = new EuystacioHelmiSDK({
  rpcUrl: 'https://sepolia.infura.io/v3/YOUR-PROJECT-ID',
  privateKey: 'TEST-PRIVATE-KEY',
  governanceAddress: '0xTestGovernanceAddress'
});
```

## TypeScript Support

Type definitions are included:

```typescript
import { EuystacioHelmiSDK, SensisaraML } from 'euystacio-helmi-sdk';

const sdk = new EuystacioHelmiSDK({
  rpcUrl: string,
  privateKey?: string,
  governanceAddress?: string
});
```

## License

MIT

## Support

- Documentation: https://github.com/hannesmitterer/euystacio-helmi-ai
- Forum: https://forum.eustacio.org
- Dashboard: https://monitor.eustacio.org
