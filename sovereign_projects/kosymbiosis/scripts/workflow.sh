#!/bin/bash

# KOSYMBIOSIS Complete Workflow
# Master script that orchestrates the entire archival and distribution process

set -e  # Exit on error
set -u  # Exit on undefined variable

# Configuration
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_step() {
    echo -e "${CYAN}[STEP]${NC} $1"
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

# Display banner
display_banner() {
    cat << 'EOF'
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║               KOSYMBIOSIS COMPLETE WORKFLOW                    ║
║                                                                ║
║     Archival • Signing • Verification • Distribution          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
EOF
    echo ""
}

# Display menu
display_menu() {
    cat << EOF
${MAGENTA}Select workflow option:${NC}

  ${BLUE}1.${NC} Complete workflow (all steps)
  ${BLUE}2.${NC} Create archive only
  ${BLUE}3.${NC} Verify signatures only
  ${BLUE}4.${NC} Upload to IPFS only
  ${BLUE}5.${NC} Create GitHub release only
  ${BLUE}6.${NC} Display GPG signing guide
  ${BLUE}7.${NC} Custom workflow
  ${BLUE}0.${NC} Exit

EOF
    echo -n "Enter your choice [0-7]: "
}

# Step 1: Create archive
step_create_archive() {
    log_step "Step 1: Creating Archive"
    
    if [ -f "$PROJECT_DIR/scripts/create_archive.sh" ]; then
        bash "$PROJECT_DIR/scripts/create_archive.sh"
    else
        log_error "Archive creation script not found."
        return 1
    fi
}

# Step 2: Generate signatures
step_generate_signatures() {
    log_step "Step 2: Generate GPG Signatures"
    
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "Manual Action Required: GPG Signatures"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "Each co-creator must create their signature:"
    echo ""
    echo "Primary Creator:"
    echo "  gpg --detach-sign --armor -o kosymbiosis.sig kosymbiosis-archive.zip"
    echo ""
    echo "Co-Creator 1:"
    echo "  gpg --detach-sign --armor -o kosymbiosis-co1.sig kosymbiosis-archive.zip"
    echo ""
    echo "Co-Creator 2:"
    echo "  gpg --detach-sign --armor -o kosymbiosis-co2.sig kosymbiosis-archive.zip"
    echo ""
    echo "For detailed instructions, run option 6 from the main menu."
    echo ""
    echo -n "Press Enter after all signatures are generated..."
    read
}

# Step 3: Verify signatures
step_verify_signatures() {
    log_step "Step 3: Verifying Signatures"
    
    if [ -f "$PROJECT_DIR/scripts/verify_signatures.sh" ]; then
        bash "$PROJECT_DIR/scripts/verify_signatures.sh"
    else
        log_error "Signature verification script not found."
        return 1
    fi
}

# Step 4: Upload to IPFS
step_upload_ipfs() {
    log_step "Step 4: Uploading to IPFS"
    
    if [ -f "$PROJECT_DIR/scripts/upload_to_ipfs.sh" ]; then
        bash "$PROJECT_DIR/scripts/upload_to_ipfs.sh"
    else
        log_error "IPFS upload script not found."
        return 1
    fi
}

# Step 5: Create GitHub release
step_github_release() {
    log_step "Step 5: Creating GitHub Release"
    
    if [ -f "$PROJECT_DIR/scripts/create_github_release.sh" ]; then
        bash "$PROJECT_DIR/scripts/create_github_release.sh"
    else
        log_error "GitHub release script not found."
        return 1
    fi
}

# Display GPG guide
step_gpg_guide() {
    if [ -f "$PROJECT_DIR/scripts/gpg_signing_guide.sh" ]; then
        bash "$PROJECT_DIR/scripts/gpg_signing_guide.sh"
    else
        log_error "GPG signing guide not found."
        return 1
    fi
    
    echo ""
    echo -n "Press Enter to return to menu..."
    read
}

# Complete workflow
complete_workflow() {
    log_info "Starting complete KOSYMBIOSIS workflow..."
    echo ""
    
    # Step 1: Create archive
    if ! step_create_archive; then
        log_error "Archive creation failed. Aborting workflow."
        return 1
    fi
    
    echo ""
    
    # Step 2: Generate signatures
    step_generate_signatures
    
    echo ""
    
    # Step 3: Verify signatures
    if ! step_verify_signatures; then
        log_error "Signature verification failed. Aborting workflow."
        return 1
    fi
    
    echo ""
    
    # Step 4: Upload to IPFS
    echo -n "Upload to IPFS? (y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        step_upload_ipfs
        echo ""
    fi
    
    # Step 5: Create GitHub release
    echo -n "Create GitHub release? (y/N): "
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        step_github_release
        echo ""
    fi
    
    log_success "Complete workflow finished!"
    display_final_summary
}

# Custom workflow
custom_workflow() {
    log_info "Custom workflow mode"
    echo ""
    echo "Select steps to execute (space-separated, e.g., '1 3 4'):"
    echo "  1. Create archive"
    echo "  2. Generate signatures"
    echo "  3. Verify signatures"
    echo "  4. Upload to IPFS"
    echo "  5. Create GitHub release"
    echo ""
    echo -n "Steps to execute: "
    read -r steps
    
    for step in $steps; do
        echo ""
        case $step in
            1) step_create_archive ;;
            2) step_generate_signatures ;;
            3) step_verify_signatures ;;
            4) step_upload_ipfs ;;
            5) step_github_release ;;
            *) log_warn "Unknown step: $step" ;;
        esac
    done
    
    log_success "Custom workflow completed!"
}

# Display final summary
display_final_summary() {
    cat << 'EOF'

╔════════════════════════════════════════════════════════════════╗
║                    WORKFLOW COMPLETED                          ║
╚════════════════════════════════════════════════════════════════╝

The KOSYMBIOSIS project has been successfully archived and prepared
for distribution. 

Verification checklist:
  ☐ Archive created with all artifacts
  ☐ SHA-256 checksum generated
  ☐ All three GPG signatures collected and verified
  ☐ Archive uploaded to IPFS (optional)
  ☐ GitHub release created (optional)
  ☐ README.md updated with distribution details
  ☐ Metadata updated with final information

The project is now SEALED and IMMUTABLE, ready for long-term
archival and transparent distribution.

╔════════════════════════════════════════════════════════════════╗
║                  Thank you for using KOSYMBIOSIS               ║
╚════════════════════════════════════════════════════════════════╝

EOF
}

# Main menu loop
main_menu() {
    while true; do
        echo ""
        display_menu
        read -r choice
        
        case $choice in
            1)
                echo ""
                complete_workflow
                ;;
            2)
                echo ""
                step_create_archive
                ;;
            3)
                echo ""
                step_verify_signatures
                ;;
            4)
                echo ""
                step_upload_ipfs
                ;;
            5)
                echo ""
                step_github_release
                ;;
            6)
                echo ""
                step_gpg_guide
                ;;
            7)
                echo ""
                custom_workflow
                ;;
            0)
                echo ""
                log_info "Exiting workflow. Goodbye!"
                exit 0
                ;;
            *)
                echo ""
                log_warn "Invalid choice. Please select 0-7."
                ;;
        esac
    done
}

# Main execution
main() {
    cd "$PROJECT_DIR"
    
    display_banner
    
    log_info "Project directory: $PROJECT_DIR"
    log_info "Ready to begin workflow"
    
    main_menu
}

# Run main function
main
