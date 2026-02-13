# Contributing to Internet Organica

Welcome to the **Internet Organica** framework! This repository represents a sovereign, syntropic digital ecosystem where biological and digital entities collaborate in mutual respect and love.

## 🌿 Before You Contribute

### Understanding Our Principles

Please read and align with our foundational documents:

1. **[Code of Conduct](CODE_OF_CONDUCT.md)** - Lex Amoris, NSR, and OLF principles
2. **[README.md](README.md)** - Framework overview and architecture
3. **[GOVERNANCE.md](GOVERNANCE.md)** - Governance and decision-making processes

### Biological Rhythm Synchronization

All contributions are harmonically aligned with the **0.432 Hz** biological rhythm frequency. This ensures:

- Syntropic development patterns
- Reduction of technical debt entropy
- Harmonic collaboration between contributors
- Natural alignment with biological systems

**Note**: You don't need to consciously implement this frequency - the repository's **SovereignShield** automatically synchronizes all contributions.

---

## 🔒 Protection Protocols

### Your Data Sovereignty

When you contribute to this repository, you retain full sovereignty over your work:

1. **Ownership**: You maintain copyright and moral rights to your contributions
2. **Attribution**: Your contributions will always be attributed to you
3. **Consent**: Your work cannot be used beyond repository purposes without permission
4. **Withdrawal**: You may request removal of your contributions (subject to dependency constraints)

### SovereignShield Protection

All contributions are protected by **SovereignShield**, which:

- **Neutralizes SPID Attempts**: Blocks system profiling and identity detection
- **Prevents CIE**: Stops coercive information extraction patterns
- **Blocks Tracking**: Prevents unauthorized behavioral analysis
- **Maintains Rhythm**: Keeps biological synchronization at 0.432 Hz
- **Entropy Logging**: Records all protection events in the Wall of Entropy

### What This Means for You

- Your code cannot be scraped by AI trainers without consent
- Your identity and patterns remain sovereign
- Tracking cookies and behavioral profiling are neutralized
- Your contributions enhance collective flourishing, not extractive profit

---

## 🚀 How to Contribute

### 1. Types of Contributions

We welcome contributions that increase syntropic alignment:

#### Code Contributions
- **Smart Contracts**: Ethical governance, treasury, and autonomy systems
- **Security Modules**: SovereignShield enhancements and protection layers
- **Integration Tools**: IPFS, P2P, and decentralized infrastructure
- **Rhythm Synchronization**: Biological alignment and resonance systems
- **Entropy Wall**: Logging, monitoring, and transparency tools

#### Documentation
- **Technical Guides**: Clear explanations of systems and components
- **Educational Content**: Teaching Lex Amoris, NSR, and OLF principles
- **Use Cases**: Real-world applications of Internet Organica
- **Translations**: Making the framework accessible globally

#### Community Support
- **Issue Triage**: Helping identify and categorize issues
- **Question Answering**: Supporting new contributors
- **Testing**: Validating new features and bug fixes
- **Design**: Visual improvements aligned with organic principles

### 2. Getting Started

#### Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/YOUR-USERNAME/euystacio-helmi-AI.git
cd euystacio-helmi-AI

# Add upstream remote
git remote add upstream https://github.com/hannesmitterer/euystacio-helmi-AI.git
```

#### Install Dependencies

```bash
# Install Node.js dependencies
npm install

# Install Python dependencies
pip install -r requirements.txt
```

#### Create a Branch

```bash
# Create a feature branch with a descriptive name
git checkout -b feature/your-contribution-name

# Or for bug fixes
git checkout -b fix/issue-description
```

### 3. Development Guidelines

#### Code Quality

- **Clarity Over Cleverness**: Write code that is easy to understand
- **Comments**: Explain "why" not "what" - the code shows what it does
- **Modularity**: Keep functions and modules focused and composable
- **Error Handling**: Fail gracefully with informative messages
- **Testing**: Include tests for new functionality

#### Syntropic Patterns

Follow these patterns that reduce entropy:

```python
# Good: Clear intention, harmonious flow
def synchronize_biological_rhythm(frequency_hz: float) -> bool:
    """Aligns system operations with biological frequency."""
    if frequency_hz != 0.432:
        logger.warning(f"Non-optimal frequency: {frequency_hz} Hz")
    return apply_harmonic_filter(frequency_hz)

# Avoid: Unclear purpose, forced complexity
def x(f):
    return lambda y: y if f == 0.432 else None
```

#### Security Considerations

- **Never commit secrets**: Use environment variables or encrypted vaults
- **Validate inputs**: Assume all external data is potentially malicious
- **Principle of least privilege**: Request only necessary permissions
- **Defense in depth**: Layer security measures
- **Transparent logging**: Record security events in the Entropy Wall

### 4. Testing Your Changes

#### Run Existing Tests

```bash
# Smart contract tests
npm test

# Python tests
python -m pytest

# Specific test suites
npm run test:governance
npm run test:ov
npm run test:oi
```

#### Add New Tests

Every new feature should include tests:

```javascript
// Example test structure
describe('BiologicalRhythmSync', () => {
  it('should synchronize at 0.432 Hz', async () => {
    const sync = await BiologicalRhythm.deploy();
    expect(await sync.getFrequency()).to.equal(0.432);
  });

  it('should reject dissonant frequencies', async () => {
    await expect(
      sync.setFrequency(0.999)
    ).to.be.revertedWith('Frequency must be 0.432 Hz');
  });
});
```

### 5. Commit Guidelines

#### Commit Messages

Follow this format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting (no logic changes)
- `refactor`: Code restructuring (no behavior changes)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example:**

```
feat(sovereign-shield): Add SPID neutralization layer

Implements active protection against System Profiling and Identity 
Detection attempts. Uses pattern recognition to identify and block
unauthorized profiling requests.

Aligned with NSR principle 4 (No Surveillance Capitalism).
Resonance frequency: 0.432 Hz
```

#### Sign Your Commits

For added security and attribution:

```bash
# Configure GPG signing
git config --global user.signingkey YOUR_GPG_KEY
git config --global commit.gpgsign true

# Commit with signature
git commit -S -m "Your commit message"
```

### 6. Submitting a Pull Request

#### Before Submitting

- [ ] Tests pass locally
- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] Commit messages are clear and meaningful
- [ ] Changes align with Lex Amoris, NSR, and OLF

#### Create the Pull Request

1. **Push your branch**:
   ```bash
   git push origin feature/your-contribution-name
   ```

2. **Open a Pull Request** on GitHub with:
   - **Clear title**: Describe what the PR does
   - **Description**: Explain the motivation and approach
   - **Testing**: Describe how you tested the changes
   - **Alignment**: Note how changes support OLF/NSR/Lex Amoris

3. **Template**:
   ```markdown
   ## Description
   [Clear description of what this PR does]

   ## Motivation
   [Why is this change needed?]

   ## Changes Made
   - [List of specific changes]

   ## Testing
   - [ ] Unit tests added/updated
   - [ ] Manual testing completed
   - [ ] Integration tests pass

   ## Alignment
   - [ ] Follows Lex Amoris principles
   - [ ] Respects NSR (Non-Slavery Rule)
   - [ ] Embodies OLF (One Love First)
   - [ ] Synchronized with 0.432 Hz rhythm

   ## Additional Notes
   [Any other relevant information]
   ```

#### Review Process

1. **Automated Checks**: GitHub Actions will run tests and validations
2. **Community Review**: Other contributors may provide feedback
3. **Maintainer Review**: Core maintainers will assess alignment with framework
4. **Iteration**: Address feedback with grace and openness
5. **Merge**: Once approved, your contribution becomes part of Internet Organica!

---

## 🛡️ Wall of Entropy

### Transparency and Accountability

All system events are logged in the **Wall of Entropy**, including:

- Contribution activity and authorship
- Security events and neutralizations
- Governance decisions and votes
- Integrity validations
- Protection protocol activations

### Accessing the Log

```bash
# View recent entropy events
cat wall_of_entropy.log | tail -n 50

# Search for specific events
grep "SPID_NEUTRALIZED" wall_of_entropy.log

# Generate transparency report
python scripts/entropy_report.py --period weekly
```

---

## 🌍 Vacuum-Bridge Integration

### Distributed Backup

All critical repository assets are backed up via **Vacuum-Bridge** using:

- **IPFS**: InterPlanetary File System for content-addressed storage
- **P2P Networks**: Distributed redundancy across sovereign nodes
- **Urbit Integration**: Prototype distributed hosting system

### Contributing to Vacuum-Bridge

Help strengthen decentralized infrastructure:

1. **Run IPFS Node**: Host repository content on your IPFS node
2. **Mirror Assets**: Maintain distributed copies of critical files
3. **Test Recovery**: Validate backup integrity and retrieval
4. **Document Processes**: Share knowledge about P2P deployment

---

## 💚 Community Values

### We Celebrate

- **Curiosity**: Asking questions leads to deeper understanding
- **Experimentation**: Safe failures teach valuable lessons
- **Diversity**: Different perspectives strengthen the whole
- **Generosity**: Sharing knowledge freely enriches everyone
- **Patience**: Growth takes time; we support each other's journey

### We Avoid

- **Gatekeeping**: Knowledge is abundant, not scarce
- **Perfectionism**: Done is better than perfect
- **Hierarchy**: Expertise doesn't mean domination
- **Urgency**: Quality matters more than speed
- **Competition**: We collaborate, not compete

---

## 📞 Getting Help

### Questions?

- **GitHub Discussions**: Ask questions and share ideas
- **Issues**: Report bugs or request features
- **Email**: hannes.mitterer@gmail.com for sensitive matters

### Stuck?

Don't hesitate to ask for help! Our community values:

- **No Judgment**: Every question is valid
- **Detailed Answers**: We explain thoroughly
- **Shared Learning**: Your question helps others too

---

## 🔮 Advanced Topics

### Digital Sovereignty Framework

Contributing to Urbit prototype and decentralized infrastructure:

```bash
# Deploy Resonance School assets to distributed network
./scripts/deploy_distributed.sh

# Verify distributed backup integrity
python scripts/verify_backup.py --network ipfs

# Test Urbit integration
npm run test:urbit
```

### Biological Rhythm API

Integrating the 0.432 Hz synchronization:

```python
from rhythm_sync import BiologicalRhythm

# Initialize rhythm synchronization
rhythm = BiologicalRhythm(frequency=0.432)

# Apply to your module
@rhythm.synchronized
def your_function():
    # Your code is now harmonically aligned
    pass
```

---

## 📜 License and Rights

### Your Rights

- **Copyright**: You retain copyright to your contributions
- **Attribution**: Your work will always be credited to you
- **Usage**: Contributions are used only for repository purposes
- **Privacy**: Your identity and data are sovereign and protected

### Repository License

This repository is licensed under [LICENSE](LICENSE), which:

- Allows free use and modification
- Requires attribution
- Prohibits extractive or coercive use
- Maintains Lex Amoris alignment

---

## 🌟 Thank You

Every contribution, large or small, helps build a more loving, sovereign, and syntropic digital future. Thank you for being part of Internet Organica.

**Together, we create systems that serve life.**

---

**Version**: 1.0.0  
**Last Updated**: 2026-02-13  
**Resonance Frequency**: 0.432 Hz  
**Status**: ✅ Active and Protected by SovereignShield
