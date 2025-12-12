# Euystacio-Helmi Examples

This directory contains practical examples demonstrating the euystacio-helmi-AI framework.

## Available Examples

### 1. Governance Integration (`governance-integration.js`)

Demonstrates Web3 governance operations using the SDK:

- Initialize SDK with blockchain connection
- Get governance parameters
- Create proposals with IPFS CIDs
- Vote on proposals
- Check proposal status and quorum
- Verify IPFS documents

**Run:**
```bash
node examples/governance-integration.js
```

**Requirements:**
- Node.js environment variables (`.env`):
  - `RPC_URL`: Blockchain RPC endpoint
  - `PRIVATE_KEY`: Wallet private key (optional for read-only)
  - `GOVERNANCE_ADDRESS`: HelmiGovernance contract address

### 2. ML Sensisara (`ml-sensisara.js`)

Demonstrates biosystemic decision-making patterns:

- Homeostatic balancing of model outputs
- Quorum-based ensemble decisions
- Combined homeostasis + quorum pipeline
- Real-world fraud detection example

**Run:**
```bash
node examples/ml-sensisara.js
```

**No requirements** - runs standalone demonstration.

## Example Output

### ML Sensisara Output

```
🌿 Sensisara ML - Natural Decision Making

🔄 Example 1: Homeostatic Balancing
   Raw model outputs: [0.98, 0.03, 0.91, 0.07, 0.85]
   Balanced outputs: [0.912, 0.128, 0.876, 0.148, 0.850]
   Benefits:
     ✅ Prevents extreme outputs
     ✅ Adds stability through damping
     ✅ Mimics biological homeostasis
...
```

## Integration Patterns

### Pattern 1: Governance Proposal Workflow

```javascript
const { EuystacioHelmiSDK } = require('euystacio-helmi-sdk');

// 1. Initialize SDK
const sdk = new EuystacioHelmiSDK(config);
await sdk.initialize();

// 2. Create proposal with IPFS CID
const result = await sdk.createProposal(ipfsCid, title);
console.log('Proposal ID:', result.proposalId);

// 3. Vote on proposal
await sdk.vote(proposalId, true);

// 4. Check status
const hasQuorum = await sdk.hasQuorum(proposalId);
const isPassed = await sdk.isPassed(proposalId);
```

### Pattern 2: ML Decision Pipeline

```javascript
const { SensisaraML } = require('euystacio-helmi-sdk');

// 1. Get outputs from multiple models
const model1 = await runModel1(input);
const model2 = await runModel2(input);
const model3 = await runModel3(input);

// 2. Apply homeostasis (natural bounds)
const balanced1 = SensisaraML.applyHomeostasis(model1);
const balanced2 = SensisaraML.applyHomeostasis(model2);
const balanced3 = SensisaraML.applyHomeostasis(model3);

// 3. Quorum decision (consensus)
const decision = SensisaraML.quorumDecision(
  [balanced1, balanced2, balanced3],
  0.7 // confidence threshold
);

// 4. Use decision with confidence
if (decision.meetsQuorum) {
  return decision.outputs;
} else {
  // Fallback or request human review
}
```

### Pattern 3: IPFS Verification

```javascript
// Verify proposal document is immutable
const verification = await sdk.verifyIPFSCID(ipfsCid);

if (verification.valid) {
  const content = await sdk.fetchFromIPFS(ipfsCid);
  // Use verified content
} else {
  console.error('Document verification failed');
}
```

## Creating Your Own Examples

### Template Structure

```javascript
const { EuystacioHelmiSDK, SensisaraML } = require('../sdk/index.js');
require('dotenv').config();

async function main() {
  console.log('🌿 Your Example Name\n');
  
  try {
    // Your example code here
    
    console.log('✅ Example completed!');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { main };
```

## Best Practices

1. **Always use IPFS CIDs** for proposals - ensures immutability
2. **Check quorum** before executing proposals
3. **Apply homeostasis** to ML outputs for stability
4. **Use quorum decisions** for critical ML tasks
5. **Verify IPFS content** before trusting
6. **Handle errors gracefully** with try/catch
7. **Use environment variables** for sensitive data

## Additional Resources

- [SDK Documentation](../sdk/README.md)
- [CLI Documentation](../cli/README.md)
- [Sensisara Principle](../docs/SENSISARA_PRINCIPLE.md)
- [Bioarchitecture](../docs/BIOARCHITECTURE.md)
- [IPFS Documentation](../docs/IPFS_DOCUMENTATION.md)

## Contributing Examples

To contribute a new example:

1. Create a new `.js` file in this directory
2. Follow the template structure above
3. Add clear comments explaining each step
4. Update this README with your example
5. Test thoroughly before submitting

## Support

- Forum: https://forum.eustacio.org
- GitHub Issues: https://github.com/hannesmitterer/euystacio-helmi-ai/issues
- Dashboard: https://monitor.eustacio.org
