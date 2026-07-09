# KOSYMBIOSIS Project Index

Complete file and directory reference for the KOSYMBIOSIS project.

## Project Root

### Documentation Files

| File | Description | Status |
|------|-------------|--------|
| `README.md` | Main project documentation and overview | ✅ Complete |
| `QUICKSTART.md` | Quick start guide for new users | ✅ Complete |
| `INDEX.md` | This file - complete project index | ✅ Complete |

### Archive Files

| File | Description | Generated |
|------|-------------|-----------|
| `kosymbiosis-archive.zip` | Complete sealed archive (25KB) | ✅ Yes |
| `checksum.sha256` | SHA-256 integrity checksum | ✅ Yes |
| `kosymbiosis.sig.example` | Example primary signature file | 📝 Template |
| `kosymbiosis-co1.sig.example` | Example co-creator 1 signature | 📝 Template |
| `kosymbiosis-co2.sig.example` | Example co-creator 2 signature | 📝 Template |

**Note**: `.example` files are templates. Actual `.sig` files should be generated with GPG.

## Directory: `declarations/`

Ethical declarations and commitments.

| File | Description | Type |
|------|-------------|------|
| `DECLARATION.md` | Complete ethical declaration | Core Document |

**Purpose**: Establishes the ethical foundation including NSR, OLF, Consensus Sacralis, and stakeholder rights.

## Directory: `metadata/`

Project metadata and configuration.

| File | Description | Format |
|------|-------------|--------|
| `PROJECT_METADATA.json` | Complete project metadata | JSON |

**Contains**:
- Project information (name, version, status)
- Ethical framework details
- Co-creator information
- Archive specifications
- Distribution configuration
- License terms

## Directory: `logs/`

Development and decision logs.

| File | Description | Type |
|------|-------------|------|
| `DEVELOPMENT_LOG.md` | Complete development history | Chronological Log |

**Covers**:
- Project timeline and milestones
- Technical decisions and rationale
- Challenges and solutions
- Lessons learned

## Directory: `scripts/`

Automation scripts for archival and distribution.

### Script Files

| File | Purpose | Executable |
|------|---------|------------|
| `README.md` | Scripts documentation | 📄 Doc |
| `workflow.sh` | Interactive master workflow | ✅ Yes |
| `create_archive.sh` | Archive creation and checksums | ✅ Yes |
| `verify_signatures.sh` | Signature verification | ✅ Yes |
| `gpg_signing_guide.sh` | GPG signing instructions | ✅ Yes |
| `upload_to_ipfs.sh` | IPFS distribution | ✅ Yes |
| `create_github_release.sh` | GitHub release automation | ✅ Yes |

### Script Categories

#### Master Workflow
- **workflow.sh**: Orchestrates entire process with interactive menu

#### Archive Management
- **create_archive.sh**: Creates ZIP, generates checksums, updates metadata

#### Signature Management
- **verify_signatures.sh**: Verifies all three GPG signatures
- **gpg_signing_guide.sh**: Complete GPG signing guide

#### Distribution
- **upload_to_ipfs.sh**: IPFS upload and documentation update
- **create_github_release.sh**: GitHub release with assets

## File Relationships

```
Archive Creation Flow:
  create_archive.sh
    ↓
  kosymbiosis-archive.zip + checksum.sha256
    ↓
  Manual GPG signing by co-creators
    ↓
  *.sig files
    ↓
  verify_signatures.sh

Distribution Flow:
  kosymbiosis-archive.zip + checksum.sha256 + *.sig
    ↓
  upload_to_ipfs.sh → IPFS CID
    ↓
  create_github_release.sh → GitHub Release
    ↓
  Updates to README.md and metadata
```

## Archive Contents

The `kosymbiosis-archive.zip` file contains:

```
kosymbiosis-archive/
├── README.md
├── declarations/
│   └── DECLARATION.md
├── metadata/
│   └── PROJECT_METADATA.json
├── logs/
│   └── DEVELOPMENT_LOG.md
└── scripts/
    ├── README.md
    ├── create_archive.sh
    ├── verify_signatures.sh
    ├── gpg_signing_guide.sh
    ├── upload_to_ipfs.sh
    ├── create_github_release.sh
    └── workflow.sh
```

**Total Size**: ~25 KB compressed

## File Checksums

Current archive checksum (SHA-256):
```
0c75638f8ee00f0d1eb25900f7456e9ec5e53976c35212563e7e18e40556b1ce
```

Verify with:
```bash
sha256sum -c checksum.sha256
```

## File Permissions

All script files should be executable:
```bash
chmod +x scripts/*.sh
```

Current permissions:
- Documentation files: `644` (rw-r--r--)
- Script files: `755` (rwxr-xr-x)
- Archive files: `644` (rw-r--r--)

## Dependencies by File

### create_archive.sh
- `zip` - Archive creation
- `sha256sum` - Checksum generation
- `jq` - JSON manipulation (optional)

### verify_signatures.sh
- `gpg` - GPG signature verification
- `sha256sum` - Checksum verification

### upload_to_ipfs.sh
- `ipfs` - IPFS daemon and client
- `jq` - JSON manipulation (optional)

### create_github_release.sh
- `gh` - GitHub CLI
- `jq` - JSON manipulation (optional)

## Version Information

| Component | Version | Date |
|-----------|---------|------|
| Project | 1.0.0-final | 2026-01-07 |
| Archive | 1.0.0 | 2026-01-07 |
| Scripts | 1.0.0 | 2026-01-07 |
| Documentation | 1.0.0 | 2026-01-07 |

## File Sizes

| File/Directory | Size |
|----------------|------|
| `README.md` | ~4.5 KB |
| `QUICKSTART.md` | ~8.7 KB |
| `INDEX.md` | ~5.0 KB |
| `declarations/` | ~4.6 KB |
| `metadata/` | ~3.2 KB |
| `logs/` | ~6.1 KB |
| `scripts/` | ~47 KB total |
| `kosymbiosis-archive.zip` | ~25 KB |
| **Total (uncompressed)** | ~104 KB |

## Metadata Fields

### PROJECT_METADATA.json Structure

```json
{
  "project": { /* Project information */ },
  "ethical_framework": { /* NSR, OLF, principles */ },
  "co_creators": [ /* Creator details */ ],
  "archive": { /* Archive specifications */ },
  "signatures": { /* Signature requirements */ },
  "distribution": { /* IPFS, GitHub config */ },
  "contents": { /* Directory listing */ },
  "license": { /* License terms */ },
  "verification": { /* Verification status */ }
}
```

## Access Patterns

### For First-Time Users
1. Start with `QUICKSTART.md`
2. Review `README.md`
3. Run `./scripts/workflow.sh`

### For Technical Implementation
1. Review `scripts/README.md`
2. Check `metadata/PROJECT_METADATA.json`
3. Run individual scripts as needed

### For Ethical Review
1. Read `declarations/DECLARATION.md`
2. Review `logs/DEVELOPMENT_LOG.md`
3. Check ethical framework in metadata

### For Verification
1. Verify `checksum.sha256`
2. Run `./scripts/verify_signatures.sh`
3. Check `metadata` verification status

## Maintenance

### Regular Updates
- Development logs after significant milestones
- Metadata after archive regeneration
- README after distribution changes

### Immutable Files
Once sealed, these files should never change:
- `kosymbiosis-archive.zip`
- `checksum.sha256`
- `*.sig` files (once generated)

### Version-Controlled Files
All files in this project are tracked in git:
- Full history available
- Changes traceable
- Rollback possible

## References

### Internal References
- Main framework: `../../README.md` (repository root)
- Other sovereign projects: `../` (sibling directories)

### External References
- Repository: https://github.com/hannesmitterer/euystacio-helmi-AI
- IPFS Gateway: [To be added after upload]
- GitHub Release: [To be added after creation]

## Navigation Guide

```
From project root:
  cd sovereign_projects/kosymbiosis

View documentation:
  cat README.md        # Main docs
  cat QUICKSTART.md    # Quick start
  cat INDEX.md         # This index

Run workflows:
  ./scripts/workflow.sh              # Interactive menu
  ./scripts/create_archive.sh        # Create archive
  ./scripts/verify_signatures.sh     # Verify sigs

Access declarations:
  cat declarations/DECLARATION.md    # Ethical declaration

Check metadata:
  cat metadata/PROJECT_METADATA.json # Project metadata
  jq . metadata/PROJECT_METADATA.json # Formatted view

Review logs:
  cat logs/DEVELOPMENT_LOG.md        # Development history
```

---

**Index Status**: ✅ Complete  
**Last Updated**: 2026-01-07  
**Maintainer**: KOSYMBIOSIS Co-Creators
