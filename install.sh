#!/bin/bash
# Euystacio-Helmi AI Setup Script
# Automated installation with error handling and fallback options
#
# Usage: ./install.sh [--minimal]

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
check_directory() {
    if [[ ! -f "app.py" || ! -f "requirements.txt" ]]; then
        print_error "Please run this script from the euystacio-helmi-AI repository directory"
        print_status "Expected files: app.py, requirements.txt"
        exit 1
    fi
}

# Check Python version
check_python() {
    print_status "Checking Python version..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        print_status "Please install Python 3.8+ and try again"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Found Python $PYTHON_VERSION"
    
    # Check if version is sufficient
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [[ $PYTHON_MAJOR -lt 3 || ($PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -lt 8) ]]; then
        print_warning "Python $PYTHON_VERSION detected. Python 3.8+ is recommended."
        print_status "Continuing anyway, but you may encounter issues..."
    fi
}

# Setup virtual environment
setup_venv() {
    print_status "Setting up virtual environment..."
    
    if [[ -d "venv" ]]; then
        print_warning "Virtual environment already exists"
        read -p "Remove existing venv and create new one? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf venv
        else
            print_status "Using existing virtual environment"
            return
        fi
    fi
    
    python3 -m venv venv
    print_success "Virtual environment created"
}

# Activate virtual environment
activate_venv() {
    print_status "Activating virtual environment..."
    source venv/bin/activate
    pip install --upgrade pip
    print_success "Virtual environment activated"
}

# Install dependencies with fallback
install_dependencies() {
    local minimal_mode="$1"
    
    if [[ "$minimal_mode" == "true" ]]; then
        print_status "Installing minimal dependencies..."
        REQUIREMENTS_FILE="requirements-minimal.txt"
    else
        print_status "Installing full dependencies..."
        REQUIREMENTS_FILE="requirements.txt"
    fi
    
    # Try standard installation
    if pip install -r "$REQUIREMENTS_FILE"; then
        print_success "Dependencies installed successfully"
        return
    fi
    
    print_warning "Standard installation failed, trying alternative methods..."
    
    # Try with --no-cache-dir
    print_status "Trying installation without cache..."
    if pip install --no-cache-dir -r "$REQUIREMENTS_FILE"; then
        print_success "Dependencies installed successfully (without cache)"
        return
    fi
    
    # If we tried full installation and it failed, try minimal
    if [[ "$minimal_mode" != "true" ]]; then
        print_warning "Full installation failed, trying minimal installation..."
        if pip install -r requirements-minimal.txt; then
            print_success "Minimal dependencies installed successfully"
            print_warning "Some AI optimization features may be limited"
            print_status "You can try adding TensorFlow later with: pip install tensorflow==2.20.0"
            return
        fi
    fi
    
    print_error "All installation methods failed"
    print_status "Please run 'python diagnose_setup.py' for detailed diagnostics"
    exit 1
}

# Initialize submodules if they exist
init_submodules() {
    if [[ -f ".gitmodules" ]]; then
        print_status "Initializing git submodules..."
        if git submodule update --init --recursive; then
            print_success "Submodules initialized"
        else
            print_warning "Failed to initialize submodules (optional feature)"
        fi
    fi
}

# Run diagnostics
run_diagnostics() {
    print_status "Running setup diagnostics..."
    
    if python diagnose_setup.py; then
        print_success "Diagnostics completed - check output above for any issues"
    else
        print_warning "Diagnostics script encountered issues"
    fi
}

# Test installation
test_installation() {
    print_status "Testing installation..."
    
    # Test core imports
    if python -c "from core.red_code import RED_CODE; print('Core modules loaded successfully')"; then
        print_success "Core functionality test passed"
    else
        print_error "Core functionality test failed"
        return 1
    fi
    
    # Test Flask
    if python -c "from flask import Flask; print('Flask test passed')"; then
        print_success "Flask test passed"
    else
        print_error "Flask test failed"
        return 1
    fi
    
    print_success "All tests passed!"
}

# Main installation function
main() {
    local minimal_mode="false"
    
    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --minimal)
                minimal_mode="true"
                shift
                ;;
            -h|--help)
                echo "Euystacio-Helmi AI Setup Script"
                echo ""
                echo "Usage: $0 [--minimal]"
                echo ""
                echo "Options:"
                echo "  --minimal    Install minimal dependencies only"
                echo "  -h, --help   Show this help message"
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                echo "Use --help for usage information"
                exit 1
                ;;
        esac
    done
    
    echo "==============================================="
    echo "🌱 Euystacio-Helmi AI Setup Script"
    echo "==============================================="
    echo ""
    
    if [[ "$minimal_mode" == "true" ]]; then
        print_status "Running in minimal installation mode"
    fi
    
    # Run setup steps
    check_directory
    check_python
    setup_venv
    activate_venv
    install_dependencies "$minimal_mode"
    init_submodules
    run_diagnostics
    test_installation
    
    echo ""
    echo "==============================================="
    echo "🎉 Installation Complete!"
    echo "==============================================="
    echo ""
    print_success "Euystacio-Helmi AI is now ready to use"
    echo ""
    print_status "To start the application:"
    echo "  1. Activate the virtual environment: source venv/bin/activate"
    echo "  2. Run the application: python app.py"
    echo "  3. Open your browser to: http://localhost:5000"
    echo ""
    print_status "For troubleshooting, run: python diagnose_setup.py"
    
    if [[ "$minimal_mode" == "true" ]]; then
        echo ""
        print_warning "Minimal installation completed"
        print_status "To enable full AI features, run: pip install tensorflow==2.20.0"
    fi
}

# Run main function
main "$@"