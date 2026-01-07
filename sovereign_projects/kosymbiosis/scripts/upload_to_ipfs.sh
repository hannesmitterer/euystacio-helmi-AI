#!/bin/bash

# KOSYMBIOSIS IPFS Upload Script
# Uploads the archive to IPFS and updates metadata

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_NAME="kosymbiosis-archive.zip"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    
    if ! command -v ipfs &> /dev/null; then
        log_error "IPFS is not installed."
        echo ""
        echo "To install IPFS:"
        echo "  1. Visit https://docs.ipfs.tech/install/"
        echo "  2. Download and install IPFS for your platform"
        echo "  3. Initialize IPFS: ipfs init"
        echo "  4. Start IPFS daemon: ipfs daemon"
        echo ""
        exit 1
    fi
    
    log_info "IPFS is installed."
}

# Check IPFS daemon
check_ipfs_daemon() {
    log_info "Checking IPFS daemon status..."
    
    if ! ipfs id &> /dev/null; then
        log_warn "IPFS daemon is not running."
        log_info "Starting IPFS daemon in background..."
        
        ipfs daemon &
        DAEMON_PID=$!
        
        # Wait for daemon to start
        sleep 5
        
        if ipfs id &> /dev/null; then
            log_success "IPFS daemon started successfully."
        else
            log_error "Failed to start IPFS daemon."
            exit 1
        fi
    else
        log_info "IPFS daemon is running."
    fi
}

# Check archive exists
check_archive() {
    log_info "Checking for archive..."
    
    if [ ! -f "$PROJECT_DIR/$ARCHIVE_NAME" ]; then
        log_error "Archive not found: $ARCHIVE_NAME"
        log_error "Please run create_archive.sh first."
        exit 1
    fi
    
    log_info "Archive found: $ARCHIVE_NAME"
}

# Verify signatures before upload
verify_before_upload() {
    log_info "Verifying signatures before upload..."
    
    if [ -f "$PROJECT_DIR/scripts/verify_signatures.sh" ]; then
        if bash "$PROJECT_DIR/scripts/verify_signatures.sh"; then
            log_success "All signatures verified. Proceeding with upload."
        else
            log_warn "Signature verification had issues."
            echo -n "Do you want to proceed anyway? (y/N): "
            read -r response
            if [[ ! "$response" =~ ^[Yy]$ ]]; then
                log_info "Upload cancelled by user."
                exit 0
            fi
        fi
    else
        log_warn "Verification script not found. Skipping signature verification."
    fi
}

# Upload to IPFS
upload_to_ipfs() {
    log_info "Uploading archive to IPFS..."
    
    cd "$PROJECT_DIR"
    
    # Add file to IPFS
    IPFS_OUTPUT=$(ipfs add -Q "$ARCHIVE_NAME")
    
    if [ $? -eq 0 ]; then
        CID="$IPFS_OUTPUT"
        log_success "Upload successful!"
        echo ""
        echo "═══════════════════════════════════════════════════════════"
        echo -e "${BLUE}IPFS CID:${NC} $CID"
        echo "═══════════════════════════════════════════════════════════"
        echo ""
    else
        log_error "Failed to upload to IPFS."
        exit 1
    fi
}

# Pin the content
pin_content() {
    log_info "Pinning content to ensure persistence..."
    
    if ipfs pin add "$CID" &> /dev/null; then
        log_success "Content pinned successfully."
    else
        log_warn "Failed to pin content. It may already be pinned."
    fi
}

# Display gateway links
display_gateway_links() {
    log_info "IPFS Gateway Links:"
    
    echo ""
    echo "Access your archive via these IPFS gateways:"
    echo ""
    echo "  🌍 https://ipfs.io/ipfs/$CID"
    echo "  🌍 https://gateway.pinata.cloud/ipfs/$CID"
    echo "  🌍 https://cloudflare-ipfs.com/ipfs/$CID"
    echo ""
}

# Update README with CID
update_readme() {
    log_info "Updating README.md with IPFS CID..."
    
    README_FILE="$PROJECT_DIR/README.md"
    
    if [ -f "$README_FILE" ]; then
        # Replace placeholder with actual CID
        if grep -q "\[To be added after IPFS upload\]" "$README_FILE"; then
            sed -i.bak "s/\[To be added after IPFS upload\]/$CID/g" "$README_FILE"
            sed -i.bak "s/\[CID\]/$CID/g" "$README_FILE"
            rm -f "$README_FILE.bak"
            log_success "README.md updated with IPFS CID."
        else
            log_warn "CID placeholder not found in README.md"
            log_info "Please manually add CID: $CID"
        fi
    else
        log_warn "README.md not found."
    fi
}

# Update metadata
update_metadata() {
    log_info "Updating metadata with IPFS information..."
    
    METADATA_FILE="$PROJECT_DIR/metadata/PROJECT_METADATA.json"
    
    if [ -f "$METADATA_FILE" ] && command -v jq &> /dev/null; then
        jq --arg cid "$CID" \
           '.distribution.ipfs.cid = $cid | 
            .distribution.ipfs.upload_status = "COMPLETE"' \
           "$METADATA_FILE" > "$METADATA_FILE.tmp"
        
        mv "$METADATA_FILE.tmp" "$METADATA_FILE"
        log_success "Metadata updated with IPFS CID."
    else
        log_warn "Could not update metadata automatically."
        log_info "Please manually add CID to metadata: $CID"
    fi
}

# Generate upload summary
generate_summary() {
    cat << EOF

╔════════════════════════════════════════════════════════════════╗
║              KOSYMBIOSIS IPFS Upload Summary                   ║
╚════════════════════════════════════════════════════════════════╝

Archive: $ARCHIVE_NAME
IPFS CID: $CID

Status: ✅ UPLOADED AND PINNED

Gateway Links:
  • https://ipfs.io/ipfs/$CID
  • https://gateway.pinata.cloud/ipfs/$CID
  • https://cloudflare-ipfs.com/ipfs/$CID

Next Steps:
1. Test gateway links to ensure accessibility
2. Consider using a pinning service (Pinata, Infura) for redundancy
3. Update GitHub release with IPFS CID
4. Share gateway links with stakeholders

Optional: Pin to additional services
  • Pinata: https://pinata.cloud
  • Infura: https://infura.io
  • Web3.Storage: https://web3.storage

╔════════════════════════════════════════════════════════════════╗
║                 Archive Available on IPFS Network              ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

# Main execution
main() {
    log_info "Starting KOSYMBIOSIS IPFS upload..."
    log_info "Project directory: $PROJECT_DIR"
    
    check_dependencies
    check_ipfs_daemon
    check_archive
    verify_before_upload
    upload_to_ipfs
    pin_content
    display_gateway_links
    update_readme
    update_metadata
    generate_summary
    
    log_success "IPFS upload completed successfully!"
}

# Run main function
main
