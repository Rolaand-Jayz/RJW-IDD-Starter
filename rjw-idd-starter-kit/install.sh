#!/usr/bin/env bash
# RJW-IDD Installation Script for Linux/macOS
# Cross-platform, safe, beginner-friendly setup

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PYTHON_MIN_VERSION="3.9"
VENV_DIR=".venv"
REQUIREMENTS="rjw-idd-starter-kit/requirements-dev.txt"

echo "RJW-IDD Installation Script"
echo "======================================"
echo ""

# Function to print colored messages
info() { echo -e "${GREEN}✔${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
error() { echo -e "${RED}✖${NC} $1" >&2; }

# Check Python version
check_python() {
    if ! command -v python3 &> /dev/null; then
        error "Python 3 not found. Please install Python ${PYTHON_MIN_VERSION} or higher."
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    info "Found Python ${PYTHON_VERSION}"
    
    # Simple version check (works for X.Y format)
    MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
    MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
    
    if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]); then
        error "Python ${PYTHON_MIN_VERSION}+ required, found ${PYTHON_VERSION}"
        exit 1
    fi
}

# Create virtual environment
create_venv() {
    if [ -d "$VENV_DIR" ]; then
        warn "Virtual environment already exists at ${VENV_DIR}"
        read -p "Remove and recreate? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf "$VENV_DIR"
        else
            info "Skipping venv creation"
            return 0
        fi
    fi
    
    info "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    info "Virtual environment created at ${VENV_DIR}"
}

# Install dependencies
install_deps() {
    if [ ! -f "$REQUIREMENTS" ]; then
        error "Requirements file not found: ${REQUIREMENTS}"
        exit 1
    fi
    
    info "Installing dependencies from ${REQUIREMENTS}..."
    
    # Activate venv
    source "${VENV_DIR}/bin/activate"
    
    # Upgrade pip
    python -m pip install --upgrade pip --quiet
    
    # Install requirements
    pip install -r "$REQUIREMENTS" --quiet
    
    info "Dependencies installed successfully"
}

# Make CLI executable
setup_cli() {
    CLI_PATH="rjw-idd-starter-kit/bin/rjw"
    
    if [ ! -f "$CLI_PATH" ]; then
        error "CLI tool not found at ${CLI_PATH}"
        exit 1
    fi
    
    chmod +x "$CLI_PATH"
    info "CLI tool configured at ${CLI_PATH}"
    
    # Check if already in PATH
    if ! command -v rjw &> /dev/null; then
        warn "CLI not in PATH. Add to your shell profile:"
        echo "    export PATH=\"\$PWD/rjw-idd-starter-kit/bin:\$PATH\""
    else
        info "CLI is accessible via 'rjw' command"
    fi
}

# Create requirements.txt if missing
create_requirements() {
    if [ ! -f "requirements.txt" ]; then
        info "Creating requirements.txt..."
        cat > requirements.txt << 'EOF'
# RJW-IDD Core Dependencies
pytest>=8.0
pyyaml>=6.0
EOF
        info "Created requirements.txt"
    fi
}

# Run verification
verify_install() {
    info "Verifying installation..."
    
    # Activate venv
    source "${VENV_DIR}/bin/activate"
    
    # Check Python
    python --version
    
    # Check pytest
    if command -v pytest &> /dev/null; then
        info "pytest: $(pytest --version | head -1)"
    else
        warn "pytest not found in environment"
    fi
    
    # Check CLI
    if [ -x "rjw-idd-starter-kit/bin/rjw" ]; then
        info "CLI tool: Ready"
    else
        warn "CLI tool not executable"
    fi
    
    info "Installation verification complete"
}

# Main installation flow
main() {
    echo "Step 1: Checking Python..."
    check_python
    echo ""
    
    echo "Step 2: Creating virtual environment..."
    create_venv
    echo ""
    
    echo "Step 3: Creating project files..."
    create_requirements
    echo ""
    
    echo "Step 4: Installing dependencies..."
    install_deps
    echo ""
    
    echo "Step 5: Configuring CLI..."
    setup_cli
    echo ""
    
    echo "Step 6: Verifying installation..."
    verify_install
    echo ""
    
    echo "======================================"
    echo -e "${GREEN}Installation complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Activate environment: source ${VENV_DIR}/bin/activate"
    echo "  2. Initialize project: rjw-idd-starter-kit/bin/rjw init"
    echo "  3. Read quickstart: cat rjw-idd-starter-kit/docs/quickstart.md"
    echo ""
}

# Run installation
main
