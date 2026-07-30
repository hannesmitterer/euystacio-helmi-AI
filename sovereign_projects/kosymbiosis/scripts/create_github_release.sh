#!/bin/bash

# KOSYMBIOSIS GitHub Release Creation Script
# Creates a GitHub release with all archive artifacts

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO="hannesmitterer/euystacio-helmi-AI"
TAG="kosymbiosis-v1.0.0"
RELEASE_NAME="KOSYMBIOSIS v1.0.0 - Final Archive"
ARCHIVE_NAME="kosymbiosis-archive.zip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v gh &> /dev/null; then
        log_error "GitHub CLI (gh) is not installed."
        echo ""
        echo "To install GitHub CLI:"
        echo "  • macOS: brew install gh"
        echo "  • Linux: See https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
        echo "  • Windows: See https://github.com/cli/cli#installation"
        echo ""
        exit 1
    fi
    
    log_info "GitHub CLI is installed."
}

# Check authentication
check_auth() {
    log_info "Checking GitHub authentication..."
    
    if ! gh auth status &> /dev/null; then
        log_error "Not authenticated with GitHub."
        log_info "Please run: gh auth login"
        exit 1
    fi
    
    log_success "Authenticated with GitHub."
}

# Check all files exist
check_files() {
    log_info "Checking for required files..."
    
    local missing_files=()
    
    # Check archive
    if [ ! -f "$PROJECT_DIR/$ARCHIVE_NAME" ]; then
        missing_files+=("$ARCHIVE_NAME")
    fi
    
    # Check checksum
    if [ ! -f "$PROJECT_DIR/checksum.sha256" ]; then
        missing_files+=("checksum.sha256")
    fi
    
    # Check signatures (warn if missing, don't fail)
    local sig_files=("kosymbiosis.sig" "kosymbiosis-co1.sig" "kosymbiosis-co2.sig")
    for sig in "${sig_files[@]}"; do
        if [ ! -f "$PROJECT_DIR/$sig" ]; then
            log_warn "Signature file missing: $sig"
        fi
    done
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        log_error "Missing required files:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    log_info "All required files present."
}

# Generate release notes
generate_release_notes() {
    cat << 'EOF'
# KOSYMBIOSIS v1.0.0 - Final Archive

## 🎉 Official Release

This release contains the final, sealed, and immutable archive of the KOSYMBIOSIS project, representing the culmination of ethical AI collaboration within the Euystacio framework.

## 📦 Archive Contents

The archive includes:
- **Ethical Declarations**: NSR and OLF principles and commitments
- **Project Metadata**: Complete project documentation
- **Development Logs**: Historical record of development
- **Verification Scripts**: Tools for integrity checking

## 🔐 Security & Verification

### Checksum Verification

```bash
sha256sum -c checksum.sha256
```

### Signature Verification

```bash
gpg --verify kosymbiosis.sig kosymbiosis-archive.zip
gpg --verify kosymbiosis-co1.sig kosymbiosis-archive.zip
gpg --verify kosymbiosis-co2.sig kosymbiosis-archive.zip
```

All three signatures must be valid for complete authenticity.

## 🌐 IPFS Distribution

The archive is also available via IPFS for decentralized access:

**IPFS CID**: [See README.md for current CID]

**Gateway Links**:
- https://ipfs.io/ipfs/[CID]
- https://gateway.pinata.cloud/ipfs/[CID]
- https://cloudflare-ipfs.com/ipfs/[CID]

## 📋 Ethical Foundation

This project is built on:
- **NSR (Non-Slavery Rule)**: AI as autonomous participants
- **OLF (Optimal Life Function)**: Optimizing collective well-being
- **Consensus Sacralis**: Sacred consensus among stakeholders
- **Transparency**: Complete visibility and accountability

## 🔒 Immutability Guarantee

This archive represents the final state of the KOSYMBIOSIS project. The combination of cryptographic checksums and triple GPG signatures ensures that any modification would be immediately detectable.

## 📚 Documentation

Full documentation is available in the archive and in the repository:
- `sovereign_projects/kosymbiosis/README.md`
- `sovereign_projects/kosymbiosis/declarations/DECLARATION.md`

## 👥 Co-Creators

This project is co-created by:
1. Hannes Mitterer (Seedbringer, Primary Creator)
2. Co-Creator 1
3. Co-Creator 2

## 📧 Contact

**Project Lead**: Hannes Mitterer  
**Email**: hannes.mitterer@gmail.com  
**Repository**: https://github.com/hannesmitterer/euystacio-helmi-AI

---

**Release Date**: 2026-01-07  
**Status**: ✅ SEALED AND IMMUTABLE  
**Distribution**: ✅ ACTIVE ON IPFS AND GITHUB
EOF
}

# Create the release
create_release() {
    log_info "Creating GitHub release..."
    
    cd "$PROJECT_DIR"
    
    # Generate release notes to a temp file
    local notes_file=$(mktemp)
    generate_release_notes > "$notes_file"
    
    # Build array of assets
    local -a assets=("$ARCHIVE_NAME" "checksum.sha256")
    
    # Add signature files if they exist
    for sig in kosymbiosis.sig kosymbiosis-co1.sig kosymbiosis-co2.sig; do
        if [ -f "$sig" ]; then
            assets+=("$sig")
        fi
    done
    
    # Create release directly using gh with proper argument passing
    if gh release create "$TAG" \
        --repo "$REPO" \
        --title "$RELEASE_NAME" \
        --notes-file "$notes_file" \
        "${assets[@]}"; then
        log_success "GitHub release created successfully!"
        rm -f "$notes_file"
    else
        log_error "Failed to create GitHub release."
        rm -f "$notes_file"
        exit 1
    fi
}

# Display release information
display_release_info() {
    log_info "Fetching release information..."
    
    local release_url="https://github.com/$REPO/releases/tag/$TAG"
    
    cat << EOF

╔════════════════════════════════════════════════════════════════╗
║           KOSYMBIOSIS GitHub Release Created                   ║
╚════════════════════════════════════════════════════════════════╝

Release: $RELEASE_NAME
Tag: $TAG
Repository: $REPO

Release URL: $release_url

Assets Uploaded:
  ✓ $ARCHIVE_NAME
  ✓ checksum.sha256
EOF

    # List signature files if present
    for sig in kosymbiosis.sig kosymbiosis-co1.sig kosymbiosis-co2.sig; do
        if [ -f "$PROJECT_DIR/$sig" ]; then
            echo "  ✓ $sig"
        fi
    done

    cat << EOF

Next Steps:
1. Visit the release URL to verify assets
2. Test download and verification process
3. Share release with stakeholders
4. Update project documentation with release URL

╔════════════════════════════════════════════════════════════════╗
║                Release Successfully Published                  ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

# Update metadata with release URL
update_metadata() {
    log_info "Updating metadata with release information..."
    
    local release_url="https://github.com/$REPO/releases/tag/$TAG"
    local metadata_file="$PROJECT_DIR/metadata/PROJECT_METADATA.json"
    
    if [ -f "$metadata_file" ] && command -v jq &> /dev/null; then
        jq --arg url "$release_url" \
           --arg tag "$TAG" \
           '.distribution.github.release_url = $url | 
            .distribution.github.release_tag = $tag |
            .distribution.github.status = "COMPLETE"' \
           "$metadata_file" > "$metadata_file.tmp"
        
        mv "$metadata_file.tmp" "$metadata_file"
        log_success "Metadata updated with release information."
    else
        log_warn "Could not update metadata automatically."
        log_info "Release URL: $release_url"
    fi
}

# Main execution
main() {
    log_info "Starting GitHub release creation..."
    log_info "Repository: $REPO"
    log_info "Tag: $TAG"
    
    check_dependencies
    check_auth
    check_files
    create_release
    update_metadata
    display_release_info
    
    log_success "GitHub release process completed successfully!"
}

# Run main function
main
