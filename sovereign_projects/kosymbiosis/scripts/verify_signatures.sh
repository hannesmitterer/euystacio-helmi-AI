#!/bin/bash

# KOSYMBIOSIS Signature Verification Script
# Verifies all three GPG signatures for the KOSYMBIOSIS archive

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARCHIVE_NAME="kosymbiosis-archive.zip"
SIGNATURES=(
    "kosymbiosis.sig"
    "kosymbiosis-co1.sig"
    "kosymbiosis-co2.sig"
)

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
    
    if ! command -v gpg &> /dev/null; then
        log_error "gpg is not installed. Please install GnuPG first."
        exit 1
    fi
    
    log_info "All dependencies satisfied."
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

# Verify checksum
verify_checksum() {
    log_info "Verifying archive checksum..."
    
    cd "$PROJECT_DIR"
    
    if [ ! -f "checksum.sha256" ]; then
        log_error "Checksum file not found."
        exit 1
    fi
    
    if sha256sum -c checksum.sha256 &> /dev/null; then
        log_success "Checksum verification passed ✓"
        return 0
    else
        log_error "Checksum verification failed ✗"
        exit 1
    fi
}

# Verify a single signature
verify_signature() {
    local sig_file=$1
    local sig_name=$2
    
    log_info "Verifying signature: $sig_name"
    
    cd "$PROJECT_DIR"
    
    if [ ! -f "$sig_file" ]; then
        log_warn "Signature file not found: $sig_file"
        return 1
    fi
    
    # Attempt to verify the signature using exit code
    if gpg --verify "$sig_file" "$ARCHIVE_NAME" 2>&1 > /dev/null; then
        log_success "Signature valid: $sig_name ✓"
        return 0
    else
        log_error "Signature invalid or cannot be verified: $sig_name ✗"
        return 1
    fi
}

# Verify all signatures
verify_all_signatures() {
    log_info "Verifying all signatures..."
    
    local total_sigs=${#SIGNATURES[@]}
    local verified_sigs=0
    local failed_sigs=0
    
    for sig_file in "${SIGNATURES[@]}"; do
        if verify_signature "$sig_file" "$sig_file"; then
            ((verified_sigs++))
        else
            ((failed_sigs++))
        fi
    done
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "Signature Verification Summary"
    echo "═══════════════════════════════════════════════════════════"
    echo "Total signatures expected: $total_sigs"
    echo "Signatures verified: $verified_sigs"
    echo "Signatures failed/missing: $failed_sigs"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    
    if [ $verified_sigs -eq $total_sigs ]; then
        log_success "All signatures verified successfully! ✓✓✓"
        return 0
    else
        log_error "Not all signatures could be verified."
        log_error "Required: $total_sigs signatures"
        log_error "Verified: $verified_sigs signatures"
        return 1
    fi
}

# Display signature information
display_signature_info() {
    log_info "Displaying signature details..."
    
    cd "$PROJECT_DIR"
    
    for sig_file in "${SIGNATURES[@]}"; do
        if [ -f "$sig_file" ]; then
            echo ""
            echo "─────────────────────────────────────────────────────────"
            echo "Signature: $sig_file"
            echo "─────────────────────────────────────────────────────────"
            gpg --verify "$sig_file" "$ARCHIVE_NAME" 2>&1 || true
        fi
    done
}

# Generate verification report
generate_report() {
    local status=$1
    
    cat << EOF

╔════════════════════════════════════════════════════════════════╗
║          KOSYMBIOSIS Signature Verification Report             ║
╚════════════════════════════════════════════════════════════════╝

Archive: $ARCHIVE_NAME
Verification Date: $(date -u +"%Y-%m-%d %H:%M:%S UTC")

Required Signatures: ${#SIGNATURES[@]}
Status: $status

Signatures Checked:
EOF

    for sig_file in "${SIGNATURES[@]}"; do
        if [ -f "$PROJECT_DIR/$sig_file" ]; then
            echo "  ✓ $sig_file"
        else
            echo "  ✗ $sig_file (missing)"
        fi
    done

    cat << EOF

═══════════════════════════════════════════════════════════════

Verification Instructions:

1. Ensure all three signature files are present
2. Import co-creator public keys if not already done:
   gpg --import <public-key-file>
3. Run this script to verify all signatures
4. All three signatures must be valid for complete verification

For manual verification of a specific signature:
   gpg --verify <signature-file> $ARCHIVE_NAME

╔════════════════════════════════════════════════════════════════╗
║                     End of Verification Report                 ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

# Main execution
main() {
    log_info "Starting KOSYMBIOSIS signature verification..."
    log_info "Project directory: $PROJECT_DIR"
    
    check_dependencies
    check_archive
    verify_checksum
    
    echo ""
    
    if verify_all_signatures; then
        display_signature_info
        generate_report "✅ ALL VERIFIED"
        exit 0
    else
        display_signature_info
        generate_report "❌ VERIFICATION FAILED"
        exit 1
    fi
}

# Run main function
main
