#!/bin/bash

# KOSYMBIOSIS Archive Creation Script
# This script creates a complete archive of the KOSYMBIOSIS project
# including all artifacts, with SHA-256 checksum generation

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_NAME="kosymbiosis-archive.zip"
CHECKSUM_FILE="checksum.sha256"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

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

# Check dependencies
check_dependencies() {
    log_info "Checking dependencies..."
    
    if ! command -v zip &> /dev/null; then
        log_error "zip is not installed. Please install it first."
        exit 1
    fi
    
    if ! command -v sha256sum &> /dev/null; then
        log_error "sha256sum is not installed. Please install it first."
        exit 1
    fi
    
    log_info "All dependencies satisfied."
}

# Clean up old archives
cleanup_old_archives() {
    log_info "Cleaning up old archives..."
    
    if [ -f "$PROJECT_DIR/$ARCHIVE_NAME" ]; then
        log_warn "Removing old archive: $ARCHIVE_NAME"
        rm -f "$PROJECT_DIR/$ARCHIVE_NAME"
    fi
    
    if [ -f "$PROJECT_DIR/$CHECKSUM_FILE" ]; then
        log_warn "Removing old checksum: $CHECKSUM_FILE"
        rm -f "$PROJECT_DIR/$CHECKSUM_FILE"
    fi
}

# Create the archive
create_archive() {
    log_info "Creating archive: $ARCHIVE_NAME"
    
    cd "$PROJECT_DIR"
    
    # Create ZIP archive with all project files
    zip -r "$ARCHIVE_NAME" \
        README.md \
        declarations/ \
        metadata/ \
        logs/ \
        scripts/ \
        -x "*.sig" \
        -x "$ARCHIVE_NAME" \
        -x "$CHECKSUM_FILE"
    
    if [ $? -eq 0 ]; then
        log_info "Archive created successfully."
        
        # Display archive size
        ARCHIVE_SIZE=$(du -h "$ARCHIVE_NAME" | cut -f1)
        log_info "Archive size: $ARCHIVE_SIZE"
    else
        log_error "Failed to create archive."
        exit 1
    fi
}

# Generate checksum
generate_checksum() {
    log_info "Generating SHA-256 checksum..."
    
    cd "$PROJECT_DIR"
    
    sha256sum "$ARCHIVE_NAME" > "$CHECKSUM_FILE"
    
    if [ $? -eq 0 ]; then
        log_info "Checksum generated successfully."
        
        # Display checksum
        CHECKSUM=$(cat "$CHECKSUM_FILE")
        log_info "Checksum: $CHECKSUM"
    else
        log_error "Failed to generate checksum."
        exit 1
    fi
}

# Verify the archive
verify_archive() {
    log_info "Verifying archive integrity..."
    
    cd "$PROJECT_DIR"
    
    sha256sum -c "$CHECKSUM_FILE"
    
    if [ $? -eq 0 ]; then
        log_info "Archive integrity verified successfully."
    else
        log_error "Archive integrity verification failed."
        exit 1
    fi
}

# Update metadata
update_metadata() {
    log_info "Updating metadata with archive information..."
    
    # Get archive size in bytes
    ARCHIVE_SIZE_BYTES=$(stat -f%z "$PROJECT_DIR/$ARCHIVE_NAME" 2>/dev/null || stat -c%s "$PROJECT_DIR/$ARCHIVE_NAME")
    
    # Read checksum
    CHECKSUM=$(sha256sum "$PROJECT_DIR/$ARCHIVE_NAME" | cut -d' ' -f1)
    
    # Update PROJECT_METADATA.json
    # Note: This uses jq if available, otherwise manual update required
    if command -v jq &> /dev/null; then
        METADATA_FILE="$PROJECT_DIR/metadata/PROJECT_METADATA.json"
        
        # Create temporary file with updated metadata
        jq --arg size "$ARCHIVE_SIZE_BYTES" \
           --arg checksum "$CHECKSUM" \
           --arg timestamp "$TIMESTAMP" \
           '.archive.size_bytes = ($size | tonumber) | 
            .archive.checksum = $checksum | 
            .archive.created = $timestamp' \
           "$METADATA_FILE" > "$METADATA_FILE.tmp"
        
        mv "$METADATA_FILE.tmp" "$METADATA_FILE"
        
        log_info "Metadata updated successfully."
    else
        log_warn "jq not found. Please manually update metadata/PROJECT_METADATA.json"
        log_info "Archive size (bytes): $ARCHIVE_SIZE_BYTES"
        log_info "SHA-256: $CHECKSUM"
    fi
}

# Generate archive summary
generate_summary() {
    log_info "Generating archive summary..."
    
    cat << EOF

╔════════════════════════════════════════════════════════════════╗
║             KOSYMBIOSIS Archive Creation Summary               ║
╚════════════════════════════════════════════════════════════════╝

Archive: $ARCHIVE_NAME
Checksum File: $CHECKSUM_FILE
Created: $TIMESTAMP

Next Steps:
1. Review the archive contents
2. Generate GPG signatures:
   - gpg --detach-sign --armor -o kosymbiosis.sig $ARCHIVE_NAME
   - Collect signatures from co-creators
3. Verify all signatures:
   - Run scripts/verify_signatures.sh
4. Upload to IPFS:
   - ipfs add $ARCHIVE_NAME
5. Create GitHub release:
   - Include archive, checksum, and all signature files
6. Update README.md with IPFS CID and release URL

╔════════════════════════════════════════════════════════════════╗
║                    Archive Ready for Signing                   ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

# Main execution
main() {
    log_info "Starting KOSYMBIOSIS archive creation..."
    log_info "Project directory: $PROJECT_DIR"
    
    check_dependencies
    cleanup_old_archives
    create_archive
    generate_checksum
    verify_archive
    update_metadata
    generate_summary
    
    log_info "Archive creation completed successfully!"
}

# Run main function
main
