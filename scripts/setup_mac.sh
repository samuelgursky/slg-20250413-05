#!/bin/bash

# DaVinci Resolve MCP Setup Script for macOS
# This script sets up the environment for running the DaVinci Resolve MCP

echo "DaVinci Resolve MCP - macOS Setup Script"
echo "========================================"

# Set path to script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"
echo "Working directory: $(pwd)"

# Check Python installation
echo "Checking Python installation..."
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo "Error: Python not found. Please install Python 3.9 or newer."
    echo "You can download it from https://www.python.org/downloads/"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo "Found Python $PYTHON_VERSION"

# Version comparison
if [[ "$(printf '%s\n' "3.9" "$PYTHON_VERSION" | sort -V | head -n1)" != "3.9" ]]; then
    echo "Warning: Python 3.9 or newer is recommended. You have Python $PYTHON_VERSION."
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Set up virtual environment
echo "Setting up virtual environment..."
if [ ! -d "venv" ]; then
    $PYTHON_CMD -m venv venv
    echo "Created virtual environment at venv/"
else
    echo "Virtual environment already exists at venv/"
fi

# Activate virtual environment
source venv/bin/activate
echo "Activated virtual environment"

# Install required packages
echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Configure DaVinci Resolve paths
echo "Configuring DaVinci Resolve API paths..."

# Check if DaVinci Resolve is installed
if [ ! -d "/Applications/DaVinci Resolve" ]; then
    echo "Warning: DaVinci Resolve doesn't appear to be installed in the standard location."
    echo "Make sure DaVinci Resolve is installed before running the MCP server."
fi

# Set environment variables for DaVinci Resolve API
RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"

# Check if paths exist
if [ ! -d "$RESOLVE_SCRIPT_API" ]; then
    echo "Warning: DaVinci Resolve Script API directory not found at $RESOLVE_SCRIPT_API"
else
    echo "Found DaVinci Resolve Script API at $RESOLVE_SCRIPT_API"
fi

if [ ! -f "$RESOLVE_SCRIPT_LIB" ]; then
    echo "Warning: DaVinci Resolve Script Library not found at $RESOLVE_SCRIPT_LIB"
else
    echo "Found DaVinci Resolve Script Library at $RESOLVE_SCRIPT_LIB"
fi

# Create or update .env file with environment variables
ENV_FILE="$PROJECT_ROOT/.env"
echo "Creating environment file at $ENV_FILE"
cat > "$ENV_FILE" << EOF
# DaVinci Resolve API environment variables
RESOLVE_SCRIPT_API="$RESOLVE_SCRIPT_API"
RESOLVE_SCRIPT_LIB="$RESOLVE_SCRIPT_LIB"
PYTHONPATH="\$PYTHONPATH:$RESOLVE_SCRIPT_API/Modules"
EOF

echo "Configuration complete!"

# Remind user about DaVinci Resolve settings
echo ""
echo "IMPORTANT: Before using the MCP server, make sure to:"
echo "1. Open DaVinci Resolve"
echo "2. Go to Preferences > System > General"
echo "3. Enable 'Allow scripts to control application'"
echo "4. Enable 'External scripting using'"
echo "5. Restart DaVinci Resolve"
echo ""
echo "To run the MCP server, use: ./scripts/run_mcp_server.sh"
echo ""

# Make run_mcp_server.sh executable
chmod +x "$SCRIPT_DIR/run_mcp_server.sh"
echo "Made run_mcp_server.sh executable"

echo "Setup completed successfully!" 