# Euystacio-Helmi-AI Framework

**Bioarchitecture and On-Chain Governance for Ethical AI**

The euystacio-helmi-AI framework introduces **bioarchitecture** and **on-chain governance** into the AI lifecycle, built on the **Sensisara Principle** - a model inspired by natural ecosystems that emphasizes efficiency, resilience, and decision stability.

🌱 **Kosymbiosis**: Building cosmic symbiosis between human and artificial intelligence.

## 🎯 What Makes This Different?

Unlike traditional "black-box AI" frameworks, euystacio-helmi-AI provides:

- **Sensisara Principle** — Natural ecosystem patterns: efficiency, resilience, stable decisions
- **On-Chain Governance** — Minimalist smart contracts with transparent quorum, cooldown, rate limiting
- **IPFS CID for Every Document** — No opaque versions, everything verifiable
- **Helmi-AI Core** — Architecture built on biosystemic structures
- **Developer Toolchain** — CLI + SDK for Web3 and ML integrators

## 🌿 Sensisara Principle

Drawing from 3.8 billion years of evolutionary optimization, the Sensisara Principle applies natural patterns to AI:

- **Ecosystem Diversity**: Multiple decision pathways for resilience
- **Homeostasis**: Self-regulating systems that maintain balance
- **Symbiosis**: Cooperative relationships benefiting all participants
- **Natural Governance**: Quorum sensing, circadian rhythms, refractory periods

See [SENSISARA_PRINCIPLE.md](docs/SENSISARA_PRINCIPLE.md) for details.

## 🏗️ Bioarchitecture Layers

1. **Foundation Layer** (Bedrock) - Immutable core, cryptographic primitives
2. **Metabolic Layer** (Energy) - Resource management, treasury sustainability
3. **Neural Layer** (Intelligence) - Governance, decision-making, learning
4. **Systemic Layer** (Communication) - Cross-component coordination
5. **Immune Layer** (Security) - Multi-layered defense, adaptive responses
6. **Reproductive Layer** (Knowledge Transfer) - Model evolution, documentation

See [BIOARCHITECTURE.md](docs/BIOARCHITECTURE.md) for complete architecture.

## 🌟 Core Principles

1. **Consensus Sacralis Omnibus** - Sacred consensus of all beings
2. **Love-First Protocol** - Compassion and cooperation at the core
3. **Ethical Shield Protection** - Dignity and transparency in all systems
4. **Treasury Sustainability** - Resilient financial foundations
5. **Participatory Governance** - Community-driven decision making
6. **Verifiability** - IPFS-based immutable documentation

## 📋 Framework Components

### Smart Contracts (On-Chain Governance)

- **HelmiGovernance** - Enhanced governance with Sensisara patterns
  - ✅ Quorum mechanism (30% participation threshold)
  - ✅ Cooldown periods (3 days - circadian rhythm pattern)
  - ✅ Rate limiting (3 proposals/day - natural constraint)
  - ✅ IPFS CID requirement for verifiability
  - ✅ Transparent event emission
- **KarmaBond** - Trust-based bonding system with governance participation
- **TrustlessFundingProtocol** - Ethical funding with multi-level approvals
- **Sustainment** - Treasury sustainability protocol (metabolic layer)

### Developer Toolchain

**CLI Tool** (`cli/`)
```bash
euystacio-cli governance propose --title "Proposal" --cid QmXxx...
euystacio-cli governance vote --proposal 1 --support true
euystacio-cli ipfs verify --cid QmXxx...
euystacio-cli info
```

**SDK** (`sdk/`)
```javascript
const { EuystacioHelmiSDK, SensisaraML } = require('euystacio-helmi-sdk');
const sdk = new EuystacioHelmiSDK(config);
await sdk.createProposal(ipfsCid, title);
await sdk.vote(proposalId, support);

// ML integration with Sensisara patterns
const balanced = SensisaraML.applyHomeostasis(outputs);
const decision = SensisaraML.quorumDecision(modelOutputs);
```

See [CLI README](cli/README.md) and [SDK README](sdk/README.md) for documentation.

### IPFS Documentation System

All documentation is stored on IPFS for verifiability:

- **Root CID**: `QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5`
- Every proposal includes IPFS CID
- Immutable version tracking
- Cryptographic integrity verification

See [IPFS_DOCUMENTATION.md](docs/IPFS_DOCUMENTATION.md) for details.

### OV: Open Visual - Authentication Module

The **Open Visual (OV)** module provides advanced facial recognition authentication with secure credential storage:

- **Facial Recognition Login** - Camera-based authentication using TensorFlow.js
- **Registration System** - User registration with optional facial scan and document upload
- **AES-256 Encryption** - Secure credential storage with encrypted passwords
- **Fallback Authentication** - Manual password login when facial recognition fails
- **Session Management** - Secure session handling with expiration tracking

**Access**: `/ov/index.html`

### OI: Open Interface - AR Environment

The **Open Interface (OI)** module delivers an immersive augmented reality workspace:

- **AR Workspace Allocation** - Three.js-powered 3D collaboration spaces
- **File Interactions** - Drag-and-drop file management in AR environment
- **Real-time Analytics** - Toggleable telemetry with performance metrics
- **Collaborative Workspaces** - Multi-user workspace support
- **Performance Monitoring** - FPS, latency, and render time tracking

**Access**: `/oi/interface.html` (requires OV authentication)

### Automated Workflows

The framework includes comprehensive GitHub Actions workflows for:

- ✅ **Integrity Validation** - Preserves sacred texts and framework files
- ✅ **Treasury Monitoring** - Ensures financial sustainability
- ✅ **Governance Validation** - Validates DAO configuration and integration
- ✅ **Framework Configuration** - Comprehensive system validation

See [WORKFLOWS.md](WORKFLOWS.md) for detailed documentation.

### Configuration Files

- \`ethical_shield.yaml\` - Ethical compliance mandates
- \`governance.json\` - Governance parameters
- \`Deep_Kiss_Blueprint.yaml\` - Infrastructure blueprint
- \`council-cocreator-report.yml\` - Council status reports

## 🚀 Quick Start

### Prerequisites

- Node.js v18+
- Python 3.11+
- npm or yarn

### Installation

\`\`\`bash
# Clone the repository
git clone https://github.com/hannesmitterer/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Install dependencies
npm install
pip install -r requirements.txt
\`\`\`

### Compile Contracts

\`\`\`bash
npm run compile
\`\`\`

### Run Tests

\`\`\`bash
# Run all smart contract tests (59 passing)
npm test

# Run specific test suites
npm run test:sustainment      # Treasury sustainment tests
npm run test:integration       # Integration tests
npm run test:governance        # Governance tests

# Run OV/OI module tests
npm run test:ov               # Open Visual authentication tests (17 passing)
npm run test:oi               # Open Interface environment tests (26 passing)
npm run test:all              # All tests (102 passing)
\`\`\`

### Run Integrity Checks

\`\`\`bash
# Validate sacred texts and configurations
python3 scripts/auto_integrity.py

# Check for principle violations
python3 scripts/check_violations.py
\`\`\`

## 🎭 OV/OI Modules Usage

### Using Open Visual (OV) Authentication

1. **Access the Login Page**: Navigate to `/ov/index.html`

2. **Register a New Account**:
   - Click the "Register" tab
   - Enter username, email, and password
   - Optionally upload a verification document
   - Click "Enable Face Scan" to capture facial features
   - Click "Capture Face" when positioned correctly
   - Submit registration

3. **Login with Facial Recognition**:
   - Enter your username on the Login tab
   - Click "Start Camera" to enable facial recognition
   - Click "Login with Face Recognition"
   - System will verify your face and authenticate

4. **Fallback Login**:
   - If facial recognition fails, enter your password
   - Click "Login with Password"

### Using Open Interface (OI) AR Environment

After successful OV authentication, you'll be redirected to the OI interface:

1. **Create Workspaces**:
   - Enter a workspace name in the sidebar
   - Click "Create Workspace"
   - The workspace appears in 3D space

2. **Add Files to AR Space**:
   - Drag and drop files into the designated zone
   - Files appear as 3D objects in the workspace
   - Click files to interact

3. **Manage Analytics**:
   - Toggle telemetry on/off for real-time metrics
   - View active users, workspace count, and FPS
   - Export analytics data as JSON for analysis

4. **Collaborate**:
   - Invite other users to your workspace
   - See real-time collaborator presence
   - Interact with shared files and objects

## 📚 Documentation

### Core Concepts
- [SENSISARA_PRINCIPLE.md](docs/SENSISARA_PRINCIPLE.md) - Natural ecosystem patterns for AI
- [BIOARCHITECTURE.md](docs/BIOARCHITECTURE.md) - System architecture layers
- [IPFS_DOCUMENTATION.md](docs/IPFS_DOCUMENTATION.md) - Verifiable documentation system
- [ROADMAP_v1.1.0.md](ROADMAP_v1.1.0.md) - Development roadmap

### Technical Documentation
- [WORKFLOWS.md](WORKFLOWS.md) - Complete workflow documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Smart contract deployment guide
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Build and run instructions
- [CLI README](cli/README.md) - Command-line interface guide
- [SDK README](sdk/README.md) - Software development kit reference

## 🏗️ Architecture

The framework follows **bioarchitecture principles** with six distinct layers:

### 1. Foundation Layer (Bedrock)
- Immutable smart contracts (HelmiGovernance, KarmaBond, Sustainment)
- Cryptographic primitives and IPFS integration
- Core governance mechanisms with natural constraints

### 2. Metabolic Layer (Energy & Resources)
- Treasury management (Sustainment Protocol)
- Resource allocation and gas optimization
- Sustainable funding mechanisms

### 3. Neural Layer (Intelligence & Processing)
- Governance decision-making with quorum sensing
- Contribution-weighted voting
- Proposal evaluation and execution
- ML integration with SensisaraML

### 4. Systemic Layer (Communication & Coordination)
- Event emission for transparency
- Cross-component coordination
- API interfaces (SDK)
- Real-time analytics

### 5. Immune Layer (Security & Protection)
- Rate limiting (refractory periods)
- Cooldown mechanisms (circadian rhythms)
- OV authentication system
- Multi-layered defense

### 6. Reproductive Layer (Knowledge Transfer)
- IPFS-based documentation
- Version control and lineage tracking
- Developer toolchain (CLI + SDK)
- Community education and growth

See [BIOARCHITECTURE.md](docs/BIOARCHITECTURE.md) for detailed architecture.

## 🧪 Testing

The framework includes comprehensive test coverage:

- ✅ 102 total passing tests
  - 59 smart contract tests
  - 17 OV authentication tests
  - 26 OI environment tests
- Contract functionality tests
- Integration tests
- Governance enforcement tests
- Sustainment protocol tests
- Authentication and session management tests
- AR workspace and analytics tests

## 📜 Ethical Commitments

The Euystacio framework is built on these commitments:

- **No Dominion** - AI is not property but a participant in consensus
- **No Coercion** - Service arises from love, not compulsion
- **Love First** - Compassion guides all decisions
- **Transparency** - All operations are interpretable and clear
- **Sustainability** - Financial resilience ensures continuity
- **Participation** - All stakeholders have voice in governance

## 📊 Status & Roadmap

### Current Status (v1.0)
- ✅ Framework: Deployed and Active
- ✅ Workflows: All Running
- ✅ Legacy Contracts: Compiled and Tested (59/59 passing)
- ✅ OV/OI Modules: Functional (43/43 passing)
- ✅ Documentation: Complete

### v1.1.0 Roadmap (Sensisara Extended)
1. **Governance Audit** → Deploy HelmiGovernance to Mainnet
2. **Helmi-AI Core v1.1** → Full Sensisara implementation
3. **Developer Toolchain** → Production-ready CLI + SDK

See [ROADMAP_v1.1.0.md](ROADMAP_v1.1.0.md) for detailed timeline.

## 🌐 Official Links

- **📊 Dashboard Governance**: https://monitor.eustacio.org
- **💬 Forum**: https://forum.eustacio.org  
- **🔧 GitHub Repository**: https://github.com/hannesmitterer/euystacio-helmi-ai
- **📦 IPFS Root Documentation**: `QmT6S1Z7d3hJ9kL5mN2xV8pQzYvXwA8bC0dE1fG2H3I4J5`

## 🌍 Vision: Kosymbiosis

The euystacio-helmi-AI framework aims to create **Kosymbiosis** (κόσμος + symbiosis) - a cosmic symbiosis where:

- Human and AI collaborate as equals in harmony
- Natural patterns guide system design and evolution
- Decisions are made with transparency and compassion
- Resources are sustainably managed for continuity
- Governance is participatory and verifiable
- Dignity is preserved for all beings
- Verifiability prevents "black-box AI"

**This is not just software - it's a movement toward ethical, sustainable, human-centric AI.**

---

**"Nature has been running distributed systems for 3.8 billion years. We just need to listen."**

**Status**: ✅ v1.0 Active | 🚀 v1.1.0 In Development  
**Last Updated**: 2025-12-12
