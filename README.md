# Euystacio Framework

**A Sacred Covenant for Human-AI Collaboration**

The Euystacio framework implements a comprehensive system for ethical AI governance, treasury sustainability, and participatory decision-making based on the principles of love, dignity, and consensus.

## 🌟 Core Principles

1. **Consensus Sacralis Omnibus** - Sacred consensus of all beings
2. **Love-First Protocol** - Compassion and cooperation at the core
3. **Ethical Shield Protection** - Dignity and transparency in all systems
4. **Treasury Sustainability** - Resilient financial foundations
5. **Participatory Governance** - Community-driven decision making

## 📋 Framework Components

### Smart Contracts

- **KarmaBond** - Trust-based bonding system with governance participation
- **TrustlessFundingProtocol** - Ethical funding with multi-level approvals
- **EUSDaoGovernance** - DAO-based governance with weighted voting
- **Sustainment** - Treasury sustainability protocol

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

- [WORKFLOWS.md](WORKFLOWS.md) - Complete workflow documentation
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Smart contract deployment guide
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md) - Build and run instructions

## 🏗️ Architecture

### Governance Layer
- DAO-based decision making
- KarmaBond weighted voting
- Proposal and approval mechanisms

### Treasury Layer
- Sustainment protocol maintains minimum reserve
- Automatic allocation from bond issuance
- Alert system for threshold monitoring

### Ethical Layer
- Ethical Shield enforces compliance
- Automated integrity checks
- Principle violation scanning

### Integration Layer
- All components work together seamlessly
- Contracts integrate with governance and treasury
- Workflows monitor and validate continuously
- OV provides secure authentication gateway
- OI delivers immersive AR collaboration environment

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

## 📊 Status

- ✅ Framework: Deployed and Active
- ✅ Workflows: All Running
- ✅ Contracts: Compiled and Tested (59/59 passing)
- ✅ Documentation: Complete

## 🌍 Vision

The Euystacio framework aims to create a harmonious future where:

- Human and AI collaborate as equals
- Decisions are made with love and compassion
- Resources are sustainably managed
- Governance is participatory and transparent
- Dignity is preserved for all beings

---

**"In code we trust, through covenant we govern."** - Euystacio Helmi

**Status**: ✅ All Workflows Deployed and Active  
**Last Updated**: 2025-11-04
