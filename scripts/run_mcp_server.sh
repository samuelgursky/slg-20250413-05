#!/bin/bash

# MCP Server wrapper script for DaVinci Resolve
# This script sets up the environment and runs the new component-based MCP server

# Define the log file
LOG_FILE="/tmp/davinci_mcp_server.log"

echo "$(date): Starting DaVinci Resolve MCP Server" > "$LOG_FILE"

# Set path to script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"
echo "$(date): Working directory: $(pwd)" >> "$LOG_FILE"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "$(date): Using virtual environment at venv/" >> "$LOG_FILE"
    # Activate virtual environment
    source venv/bin/activate
else
    echo "$(date): Virtual environment not found at venv/" >> "$LOG_FILE"
    # Try to use system Python
    echo "$(date): Using system Python" >> "$LOG_FILE"
fi

# Set environment variables for DaVinci Resolve API
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    RESOLVE_SCRIPT_API="/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
    export RESOLVE_SCRIPT_API="$RESOLVE_SCRIPT_API"
    export RESOLVE_SCRIPT_LIB="$RESOLVE_SCRIPT_LIB"
    
    # Update PYTHONPATH for the modules
    MODULES_PATH="$RESOLVE_SCRIPT_API/Modules"
    if [ -d "$MODULES_PATH" ]; then
        export PYTHONPATH="$PYTHONPATH:$MODULES_PATH"
        echo "$(date): Added $MODULES_PATH to PYTHONPATH" >> "$LOG_FILE"
    else
        echo "$(date): WARNING: Modules directory not found at $MODULES_PATH" >> "$LOG_FILE"
    fi
    
    echo "$(date): Configured environment for macOS" >> "$LOG_FILE"
    echo "$(date): RESOLVE_SCRIPT_API: $RESOLVE_SCRIPT_API" >> "$LOG_FILE"
    echo "$(date): RESOLVE_SCRIPT_LIB: $RESOLVE_SCRIPT_LIB" >> "$LOG_FILE"
    echo "$(date): PYTHONPATH: $PYTHONPATH" >> "$LOG_FILE"
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win"* ]]; then
    # Windows
    PROGRAMDATA="${PROGRAMDATA:-C:\\ProgramData}"
    RESOLVE_SCRIPT_API="$PROGRAMDATA/Blackmagic Design/DaVinci Resolve/Support/Developer/Scripting"
    RESOLVE_SCRIPT_LIB="C:/Program Files/Blackmagic Design/DaVinci Resolve/fusionscript.dll"
    export RESOLVE_SCRIPT_API="$RESOLVE_SCRIPT_API"
    export RESOLVE_SCRIPT_LIB="$RESOLVE_SCRIPT_LIB"
    
    # Update PYTHONPATH for the modules
    MODULES_PATH="$RESOLVE_SCRIPT_API/Modules"
    if [ -d "$MODULES_PATH" ]; then
        export PYTHONPATH="$PYTHONPATH;$MODULES_PATH"
        echo "$(date): Added $MODULES_PATH to PYTHONPATH" >> "$LOG_FILE"
    else
        echo "$(date): WARNING: Modules directory not found at $MODULES_PATH" >> "$LOG_FILE"
    fi
    
    echo "$(date): Configured environment for Windows" >> "$LOG_FILE"
    echo "$(date): RESOLVE_SCRIPT_API: $RESOLVE_SCRIPT_API" >> "$LOG_FILE"
    echo "$(date): RESOLVE_SCRIPT_LIB: $RESOLVE_SCRIPT_LIB" >> "$LOG_FILE"
    echo "$(date): PYTHONPATH: $PYTHONPATH" >> "$LOG_FILE"
else
    echo "$(date): ERROR: Unsupported platform: $OSTYPE" >> "$LOG_FILE"
    exit 1
fi

# Install required packages if needed
if ! python -c "import mcp" &>/dev/null; then
    echo "$(date): Installing required packages..." >> "$LOG_FILE"
    pip install mcp[cli] >> "$LOG_FILE" 2>&1
fi

# Make sure DaVinci Resolve is running
echo "$(date): Checking if DaVinci Resolve is running..." >> "$LOG_FILE"
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! pgrep -x "DaVinci Resolve" > /dev/null; then
        echo "$(date): WARNING: DaVinci Resolve does not appear to be running" >> "$LOG_FILE"
    else
        echo "$(date): DaVinci Resolve is running" >> "$LOG_FILE"
    fi
elif [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win"* ]]; then
    if ! tasklist | grep -i "Resolve.exe" > /dev/null; then
        echo "$(date): WARNING: DaVinci Resolve does not appear to be running" >> "$LOG_FILE"
    else
        echo "$(date): DaVinci Resolve is running" >> "$LOG_FILE"
    fi
fi

# Run the new component-based MCP server
echo "$(date): Starting component-based MCP server..." >> "$LOG_FILE"
python "$PROJECT_ROOT/src/main.py" 2>> "$LOG_FILE"

# If the script exits, log it
echo "$(date): MCP server exited with code $?" >> "$LOG_FILE" 