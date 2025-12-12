# Quick Start Guide - Euystacio-Helmi-AI

Get started with the euystacio-helmi-AI framework in minutes.

## 🎯 What You'll Learn

- Understand the Sensisara Principle
- Set up the framework
- Use CLI and SDK tools
- Apply biosystemic patterns to ML

## 📚 Prerequisites

- Node.js v18+ and npm
- Python 3.11+ (optional, for ML examples)
- Basic understanding of blockchain and AI/ML

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/hannesmitterer/euystacio-helmi-ai.git
cd euystacio-helmi-ai
```

### 2. Install Dependencies

```bash
npm install
pip install -r requirements.txt  # Optional for Python tools
```

### 3. Compile Smart Contracts

```bash
npm run compile
```

## 🌿 Understanding Sensisara

The **Sensisara Principle** applies natural ecosystem patterns to AI:

- **Homeostasis**: Self-regulating systems (like body temperature)
- **Quorum Sensing**: Collective decision-making (like bacterial colonies)
- **Circadian Rhythms**: Time-based constraints (cooldown periods)
- **Refractory Periods**: Natural rate limiting

Read more: [docs/SENSISARA_PRINCIPLE.md](docs/SENSISARA_PRINCIPLE.md)

## 🎯 Quick Examples

### Example 1: Run ML Sensisara Demo

```bash
node examples/ml-sensisara.js
```

This demonstrates:
- Homeostatic balancing of model outputs
- Quorum-based ensemble decisions
- Fraud detection with confidence scoring

**No blockchain required** - pure JavaScript demonstration.

### Example 2: Use the CLI

```bash
# Show framework information
node cli/index.js info

# Show official links
node cli/index.js links

# (Blockchain required for actual operations)
# node cli/index.js governance propose --title "My Proposal" --cid QmXxx...
```

### Example 3: SDK Integration

Create a file `my-app.js`:

```javascript
const { SensisaraML } = require('./sdk/index.js');

// Balance ML model outputs using natural patterns
const rawOutputs = [0.95, 0.02, 0.88];
const balanced = SensisaraML.applyHomeostasis(rawOutputs);

console.log('Raw:', rawOutputs);
console.log('Balanced:', balanced);
```

Run it:
```bash
node my-app.js
```

## 🏗️ Bioarchitecture Layers

The framework is organized in six biosystemic layers:

1. **Foundation** - Immutable smart contracts
2. **Metabolic** - Resource management
3. **Neural** - Decision-making
4. **Systemic** - Communication
5. **Immune** - Security
6. **Reproductive** - Knowledge transfer

Read more: [docs/BIOARCHITECTURE.md](docs/BIOARCHITECTURE.md)

## 🔗 On-Chain Governance

The HelmiGovernance contract implements natural governance patterns:

```javascript
const { EuystacioHelmiSDK } = require('./sdk/index.js');

const sdk = new EuystacioHelmiSDK({
  rpcUrl: 'YOUR_RPC_URL',
  privateKey: 'YOUR_PRIVATE_KEY',
  governanceAddress: 'CONTRACT_ADDRESS'
});

await sdk.initialize();

// Create proposal (requires IPFS CID)
await sdk.createProposal(
  'QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5',
  'Upgrade treasury protocol'
);

// Vote
await sdk.vote(1, true);
```

Features:
- ✅ 30% quorum requirement
- ✅ 3-day cooldown (circadian rhythm)
- ✅ Rate limiting (3 proposals/day)
- ✅ IPFS CID verification
- ✅ Transparent event emission

## 📦 IPFS Verification

All documentation is stored on IPFS:

**Root CID**: `QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5`

```javascript
// Verify document
const verification = await sdk.verifyIPFSCID('QmXxx...');
console.log('Valid:', verification.valid);

// Fetch content
const content = await sdk.fetchFromIPFS('QmXxx...');
```

Read more: [docs/IPFS_DOCUMENTATION.md](docs/IPFS_DOCUMENTATION.md)

## 🧪 Running Tests

The framework includes comprehensive tests:

```bash
# All tests (requires dependencies)
npm test

# Specific test suites
npm run test:sustainment
npm run test:governance
npm run test:ov
npm run test:oi
```

## 🛠️ Next Steps

### For Developers

1. Explore [examples/](examples/) directory
2. Read [SDK documentation](sdk/README.md)
3. Check [CLI documentation](cli/README.md)
4. Review smart contracts in [contracts/](contracts/)

### For AI/ML Engineers

1. Study [SENSISARA_PRINCIPLE.md](docs/SENSISARA_PRINCIPLE.md)
2. Run [examples/ml-sensisara.js](examples/ml-sensisara.js)
3. Integrate SensisaraML into your models
4. Apply homeostasis and quorum patterns

### For Web3 Builders

1. Study [HelmiGovernance.sol](contracts/HelmiGovernance.sol)
2. Review [governance integration example](examples/governance-integration.js)
3. Deploy contracts to testnet
4. Build on the bioarchitecture

### For Community Members

1. Visit [forum.eustacio.org](https://forum.eustacio.org)
2. Join governance discussions
3. Review proposals via dashboard
4. Participate in voting

## 🌐 Official Resources

- **Dashboard**: https://monitor.eustacio.org
- **Forum**: https://forum.eustacio.org
- **GitHub**: https://github.com/hannesmitterer/euystacio-helmi-ai
- **Root Documentation**: QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5

## 🎯 Roadmap

Check [ROADMAP_v1.1.0.md](ROADMAP_v1.1.0.md) for:
- Governance audit timeline
- Mainnet deployment plan
- Sensisara Extended features
- Developer toolchain completion

## 💡 Philosophy

> "Nature has been running distributed systems for 3.8 billion years. We just need to listen."

The euystacio-helmi-AI framework isn't just code—it's a movement toward:
- ✅ Verifiable AI (no black boxes)
- ✅ Natural governance patterns
- ✅ Sustainable systems
- ✅ Human-AI symbiosis (**Kosymbiosis**)

## 🆘 Getting Help

- **Issues**: [GitHub Issues](https://github.com/hannesmitterer/euystacio-helmi-ai/issues)
- **Discussions**: [Forum](https://forum.eustacio.org)
- **Documentation**: [docs/](docs/) directory
- **Examples**: [examples/](examples/) directory

## 🤝 Contributing

We welcome contributions! Areas of focus:

1. Smart contract auditing
2. SDK enhancements
3. CLI features
4. ML integration examples
5. Documentation improvements
6. Community building

---

**Welcome to the Kosymbiosis!** 🌱
