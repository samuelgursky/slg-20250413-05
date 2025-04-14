#!/usr/bin/env python3
"""
DaVinci Resolve MCP Server - Main Entry Point
This script sets up the environment and runs the DaVinci Resolve MCP server
"""

import os
import sys
import logging
import pathlib

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/tmp/davinci_resolve_mcp.log")
    ]
)
logger = logging.getLogger("davinci_resolve_mcp.main")

def configure_environment() -> None:
    """Configure the environment for DaVinci Resolve API access"""
    # Add the project root to the Python path
    script_dir = pathlib.Path(__file__).parent.parent.absolute()
    sys.path.insert(0, str(script_dir))
    
    # Configure DaVinci Resolve API environment variables
    if sys.platform == "darwin":  # macOS
        resolve_script_api = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting"
        resolve_script_lib = "/Applications/DaVinci Resolve/DaVinci Resolve.app/Contents/Libraries/Fusion/fusionscript.so"
        
        # Create PYTHONPATH with the modules directory
        python_path = os.environ.get("PYTHONPATH", "")
        modules_path = os.path.join(resolve_script_api, "Modules")
        if python_path:
            os.environ["PYTHONPATH"] = f"{python_path}:{modules_path}"
        else:
            os.environ["PYTHONPATH"] = modules_path
            
        os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api
        os.environ["RESOLVE_SCRIPT_LIB"] = resolve_script_lib
        
    elif sys.platform == "win32":  # Windows
        program_data = os.environ.get("PROGRAMDATA", "C:\\ProgramData")
        resolve_script_api = os.path.join(program_data, "Blackmagic Design", "DaVinci Resolve", "Support", "Developer", "Scripting")
        resolve_script_lib = r"C:\Program Files\Blackmagic Design\DaVinci Resolve\fusionscript.dll"
        
        # Create PYTHONPATH with the modules directory
        python_path = os.environ.get("PYTHONPATH", "")
        modules_path = os.path.join(resolve_script_api, "Modules")
        if python_path:
            os.environ["PYTHONPATH"] = f"{python_path};{modules_path}"
        else:
            os.environ["PYTHONPATH"] = modules_path
            
        os.environ["RESOLVE_SCRIPT_API"] = resolve_script_api
        os.environ["RESOLVE_SCRIPT_LIB"] = resolve_script_lib
    else:
        logger.error(f"Unsupported platform: {sys.platform}")
        sys.exit(1)

    logger.info(f"Configured environment for {sys.platform}")
    logger.info(f"PYTHONPATH: {os.environ.get('PYTHONPATH')}")
    logger.info(f"RESOLVE_SCRIPT_API: {os.environ.get('RESOLVE_SCRIPT_API')}")
    logger.info(f"RESOLVE_SCRIPT_LIB: {os.environ.get('RESOLVE_SCRIPT_LIB')}")
    
    # Verify DaVinci Resolve API files
    modules_path = os.path.join(os.environ.get("RESOLVE_SCRIPT_API", ""), "Modules")
    if not os.path.exists(modules_path):
        logger.warning(f"Modules directory not found at: {modules_path}")
    else:
        logger.info(f"Modules directory found at: {modules_path}")

def main():
    """Main entry point for the DaVinci Resolve MCP server"""
    logger.info("Starting DaVinci Resolve MCP Server...")
    
    # Configure the environment
    configure_environment()
    
    try:
        # Import and run the server
        from src.davinci_resolve_mcp import run_server
        run_server()
    except ImportError as e:
        logger.error(f"Error importing server module: {str(e)}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error running server: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        sys.exit(1)

if __name__ == "__main__":
    main() 