# KOSYMBIOSIS Scripts

This directory contains automation scripts for the KOSYMBIOSIS project archival and distribution process.

## Scripts Overview

### 1. `workflow.sh` - Master Workflow Orchestrator

**Purpose**: Interactive menu-driven workflow for the complete archival process.

**Usage**:
```bash
./scripts/workflow.sh
```

**Features**:
- Complete workflow automation
- Individual step execution
- Custom workflow builder
- GPG signing guide access

### 2. `create_archive.sh` - Archive Creation

**Purpose**: Creates a ZIP archive of all project artifacts and generates SHA-256 checksum.

**Usage**:
```bash
./scripts/create_archive.sh
```

**Output**:
- `kosymbiosis-archive.zip` - Complete project archive
- `checksum.sha256` - SHA-256 checksum file

**What it does**:
1. Validates dependencies (zip, sha256sum)
2. Cleans up old archives
3. Creates new ZIP archive with all artifacts
4. Generates SHA-256 checksum
5. Verifies archive integrity
6. Updates project metadata

### 3. `verify_signatures.sh` - Signature Verification

**Purpose**: Verifies all three GPG signatures for authenticity.

**Usage**:
```bash
./scripts/verify_signatures.sh
```

**Requirements**:
- GPG installed
- Public keys imported for all signatories
- All three signature files present

**What it does**:
1. Checks GPG availability
2. Verifies archive checksum
3. Verifies each signature file
4. Generates verification report
5. Returns success only if all signatures valid

### 4. `gpg_signing_guide.sh` - GPG Signing Guide

**Purpose**: Displays comprehensive instructions for creating GPG signatures.

**Usage**:
```bash
./scripts/gpg_signing_guide.sh
```

**Covers**:
- GPG key generation
- Creating detached signatures
- Exporting public keys
- Troubleshooting common issues
- Best practices

### 5. `upload_to_ipfs.sh` - IPFS Distribution

**Purpose**: Uploads archive to IPFS and updates documentation with CID.

**Usage**:
```bash
./scripts/upload_to_ipfs.sh
```

**Requirements**:
- IPFS installed and daemon running
- Archive and signatures verified

**What it does**:
1. Checks IPFS installation and daemon
2. Verifies signatures before upload
3. Uploads archive to IPFS
4. Pins content for persistence
5. Displays gateway links
6. Updates README and metadata with CID

### 6. `create_github_release.sh` - GitHub Release Creation

**Purpose**: Creates a GitHub release with all archive artifacts.

**Usage**:
```bash
./scripts/create_github_release.sh
```

**Requirements**:
- GitHub CLI (gh) installed
- Authenticated with GitHub
- All files (archive, checksum, signatures) present

**What it does**:
1. Validates GitHub CLI and authentication
2. Checks all required files
3. Generates release notes
4. Creates GitHub release with tag
5. Uploads all assets
6. Updates metadata with release URL

## Workflow Order

### Recommended Complete Workflow:

1. **Create Archive**
   ```bash
   ./scripts/create_archive.sh
   ```

2. **Generate Signatures** (Manual - each co-creator)
   ```bash
   # Primary creator
   gpg --detach-sign --armor -o kosymbiosis.sig kosymbiosis-archive.zip
   
   # Co-creator 1
   gpg --detach-sign --armor -o kosymbiosis-co1.sig kosymbiosis-archive.zip
   
   # Co-creator 2
   gpg --detach-sign --armor -o kosymbiosis-co2.sig kosymbiosis-archive.zip
   ```

3. **Verify Signatures**
   ```bash
   ./scripts/verify_signatures.sh
   ```

4. **Upload to IPFS** (Optional)
   ```bash
   ./scripts/upload_to_ipfs.sh
   ```

5. **Create GitHub Release** (Optional)
   ```bash
   ./scripts/create_github_release.sh
   ```

### Quick Start with Master Workflow:

```bash
./scripts/workflow.sh
```

Select option 1 for complete automated workflow with interactive prompts.

## Dependencies

### Required for All Scripts:
- bash (version 4.0+)
- Basic Unix tools (zip, sha256sum, grep, sed)

### Required for Signing:
- GPG (GnuPG) 2.0+
- GPG keys for all co-creators

### Required for IPFS Upload:
- IPFS (go-ipfs or kubo)
- IPFS daemon running
- jq (for JSON manipulation, optional)

### Required for GitHub Release:
- GitHub CLI (gh)
- Authenticated GitHub account with push access

## Script Permissions

All scripts should be executable. If needed, run:

```bash
chmod +x scripts/*.sh
```

## Environment Variables

### Optional Configuration:

```bash
# Override default repository
export KOSYMBIOSIS_REPO="username/repository"

# Override default tag
export KOSYMBIOSIS_TAG="kosymbiosis-v1.0.0"
```

## Error Handling

All scripts use `set -e` and `set -u` for robust error handling:
- `set -e`: Exit immediately if any command fails
- `set -u`: Treat undefined variables as errors

Exit codes:
- `0`: Success
- `1`: Error occurred

## Logging

Scripts use colored output for clarity:
- 🟢 **[INFO]**: General information (green)
- 🟡 **[WARN]**: Warnings (yellow)
- 🔴 **[ERROR]**: Errors (red)
- 🔵 **[STEP]**: Workflow steps (cyan)
- ✅ **[SUCCESS]**: Success messages (green)

## Troubleshooting

### Archive Creation Issues

**Problem**: "zip: command not found"
**Solution**: Install zip utility
```bash
# Ubuntu/Debian
sudo apt-get install zip

# macOS
brew install zip
```

### Signature Verification Issues

**Problem**: "gpg: Can't check signature: No public key"
**Solution**: Import the signer's public key
```bash
gpg --import public-key.asc
```

### IPFS Upload Issues

**Problem**: "ipfs daemon is not running"
**Solution**: Start IPFS daemon
```bash
ipfs daemon &
```

### GitHub Release Issues

**Problem**: "gh: command not found"
**Solution**: Install GitHub CLI
```bash
# macOS
brew install gh

# Ubuntu/Debian
sudo apt install gh
```

## Security Considerations

1. **Private Keys**: Never share or commit GPG private keys
2. **Passphrases**: Use strong passphrases for GPG keys
3. **Verification**: Always verify checksums and signatures before distribution
4. **Backups**: Keep secure backups of all signature files

## Additional Resources

- **GPG Documentation**: https://gnupg.org/documentation/
- **IPFS Documentation**: https://docs.ipfs.tech/
- **GitHub CLI Documentation**: https://cli.github.com/manual/

## Support

For issues or questions:
- Check script output messages
- Review this documentation
- Contact project maintainers
- Open an issue in the repository

---

**Last Updated**: 2026-01-07  
**Version**: 1.0.0  
**Maintainer**: KOSYMBIOSIS Co-Creators
