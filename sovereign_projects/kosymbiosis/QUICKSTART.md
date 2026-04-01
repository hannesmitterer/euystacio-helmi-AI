# KOSYMBIOSIS Quick Start Guide

This guide will help you get started with the KOSYMBIOSIS project archival and distribution system.

## What is KOSYMBIOSIS?

KOSYMBIOSIS is a sovereign project within the Euystacio framework that demonstrates ethical AI collaboration grounded in:
- **NSR (Non-Slavery Rule)**: AI systems as autonomous participants
- **OLF (Optimal Life Function)**: Optimizing collective well-being
- **Consensus Sacralis**: Sacred consensus among stakeholders
- **Transparency**: Complete visibility and accountability

## Quick Start: 5-Minute Overview

### 1. Navigate to Project Directory

```bash
cd sovereign_projects/kosymbiosis
```

### 2. Review Project Documentation

```bash
# Main README
cat README.md

# Ethical Declaration
cat declarations/DECLARATION.md

# Project Metadata
cat metadata/PROJECT_METADATA.json
```

### 3. Run Complete Workflow (Interactive)

```bash
./scripts/workflow.sh
```

This launches an interactive menu where you can:
- Create the complete archive
- Manage GPG signatures
- Upload to IPFS
- Create GitHub releases

### 4. Or Run Individual Steps

#### Create Archive Only:
```bash
./scripts/create_archive.sh
```

#### View GPG Signing Guide:
```bash
./scripts/gpg_signing_guide.sh
```

#### Verify Signatures:
```bash
./scripts/verify_signatures.sh
```

## Understanding the Project Structure

```
kosymbiosis/
├── README.md                    # Main documentation
├── QUICKSTART.md                # This file
├── INDEX.md                     # Complete file index
├── declarations/                # Ethical declarations
│   └── DECLARATION.md
├── metadata/                    # Project metadata
│   └── PROJECT_METADATA.json
├── logs/                        # Development logs
│   └── DEVELOPMENT_LOG.md
├── scripts/                     # Automation scripts
│   ├── workflow.sh              # Master workflow
│   ├── create_archive.sh        # Archive creation
│   ├── verify_signatures.sh     # Signature verification
│   ├── upload_to_ipfs.sh        # IPFS distribution
│   ├── create_github_release.sh # GitHub release
│   └── gpg_signing_guide.sh     # GPG guide
├── kosymbiosis-archive.zip      # The sealed archive
├── checksum.sha256              # SHA-256 checksum
└── *.sig.example                # Example signature files
```

## Common Tasks

### Creating a New Archive

```bash
# Run the archive creation script
./scripts/create_archive.sh

# Output:
# - kosymbiosis-archive.zip
# - checksum.sha256
```

### Verifying Archive Integrity

```bash
# Check the SHA-256 checksum
sha256sum -c checksum.sha256

# Expected output:
# kosymbiosis-archive.zip: OK
```

### Generating GPG Signatures

```bash
# Primary creator signature
gpg --detach-sign --armor -o kosymbiosis.sig kosymbiosis-archive.zip

# Co-creator 1 signature
gpg --detach-sign --armor -o kosymbiosis-co1.sig kosymbiosis-archive.zip

# Co-creator 2 signature
gpg --detach-sign --armor -o kosymbiosis-co2.sig kosymbiosis-archive.zip
```

### Verifying All Signatures

```bash
./scripts/verify_signatures.sh
```

### Uploading to IPFS

```bash
# Ensure IPFS is installed and daemon is running
ipfs daemon &

# Upload the archive
./scripts/upload_to_ipfs.sh
```

### Creating GitHub Release

```bash
# Ensure GitHub CLI is installed and authenticated
gh auth login

# Create the release
./scripts/create_github_release.sh
```

## Prerequisites

### Required Tools

- **bash** (4.0+) - Shell scripting
- **zip** - Archive creation
- **sha256sum** - Checksum generation

### Optional Tools (for full workflow)

- **GPG** (2.0+) - For signature creation/verification
- **IPFS** - For decentralized distribution
- **GitHub CLI (gh)** - For release creation
- **jq** - For JSON manipulation (optional)

### Installing Prerequisites

#### macOS:
```bash
brew install gnupg ipfs gh jq
```

#### Ubuntu/Debian:
```bash
sudo apt-get install gnupg2 zip
# IPFS: See https://docs.ipfs.tech/install/
# GitHub CLI: See https://github.com/cli/cli#installation
sudo apt-get install jq
```

## Workflow Phases

### Phase 1: Archive Creation ✅
- Gather all project artifacts
- Create ZIP archive
- Generate SHA-256 checksum
- Update metadata

### Phase 2: Signature Collection 🔄
- Primary creator signs archive
- Co-creator 1 signs archive
- Co-creator 2 signs archive
- Verify all signatures

### Phase 3: Distribution 📡
- Upload to IPFS (optional)
- Create GitHub release (optional)
- Update documentation with distribution links

### Phase 4: Verification ✓
- Verify checksums
- Verify signatures
- Test distribution channels
- Confirm accessibility

## Troubleshooting

### Problem: "Permission denied" when running scripts

**Solution:**
```bash
chmod +x scripts/*.sh
```

### Problem: "zip: command not found"

**Solution:**
```bash
# macOS
brew install zip

# Ubuntu/Debian
sudo apt-get install zip
```

### Problem: "gpg: command not found"

**Solution:**
```bash
# macOS
brew install gnupg

# Ubuntu/Debian
sudo apt-get install gnupg2
```

### Problem: Signature verification fails

**Solution:**
```bash
# Import the signer's public key first
gpg --import public-key.asc

# Then verify
gpg --verify signature.sig kosymbiosis-archive.zip
```

## Next Steps

1. **Explore the Documentation**
   - Read `README.md` for complete overview
   - Review `declarations/DECLARATION.md` for ethical principles
   - Check `scripts/README.md` for detailed script documentation

2. **Run the Archive Creation**
   - Execute `./scripts/create_archive.sh`
   - Review the generated archive and checksum

3. **Set Up GPG Signing**
   - Generate or import GPG keys
   - Review `./scripts/gpg_signing_guide.sh` for instructions
   - Create signatures for the archive

4. **Test the Complete Workflow**
   - Run `./scripts/workflow.sh`
   - Step through each phase
   - Verify all outputs

## Best Practices

1. **Always verify checksums** before signing or distributing
2. **Keep private keys secure** - never share or commit them
3. **Use strong passphrases** for GPG keys
4. **Test verification process** before public distribution
5. **Maintain multiple distribution channels** for redundancy
6. **Document all changes** in development logs
7. **Follow the triple-signature process** for authenticity

## Getting Help

- **Script Documentation**: See `scripts/README.md`
- **Ethical Framework**: See `declarations/DECLARATION.md`
- **Project Metadata**: See `metadata/PROJECT_METADATA.json`
- **Development History**: See `logs/DEVELOPMENT_LOG.md`

For questions or issues:
- Review script output messages
- Check troubleshooting section above
- Contact: hannes.mitterer@gmail.com

## Resources

- **Euystacio Framework**: [Main Repository](https://github.com/hannesmitterer/euystacio-helmi-AI)
- **GPG Documentation**: https://gnupg.org/documentation/
- **IPFS Documentation**: https://docs.ipfs.tech/
- **GitHub CLI**: https://cli.github.com/manual/

---

**Welcome to KOSYMBIOSIS!**

This project demonstrates what's possible when technology serves humanity with ethics at its core.

**Status**: ✅ Ready for Archival and Distribution  
**Last Updated**: 2026-01-07
