"""
DaVinci Resolve MCP Server
Main module that combines all components and provides MCP tools
"""

import os
import sys
import logging
import json
from typing import Dict, Any, List

from mcp.server.fastmcp import FastMCP

# Import existing components
from .components.project import get_project_info, get_project_settings, get_all_timelines
from .components.media_pool import list_media_pool_items, get_folder_structure, set_media_pool_current_folder
from .components.timeline import get_timeline_details, get_timeline_tracks, get_timeline_items

# Import the tool registration system
from .tools.registration import get_all_tools, get_tools_by_component, execute_tool as tools_execute

# Import from resolve_api
from .resolve_api import get_project_manager  # Critical import for server functionality

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("davinci_resolve_mcp")

# Create the MCP server
proxy_mcp = FastMCP("DaVinci Resolve MCP")

# Define the existing tools with their components
LEGACY_TOOLS = {
    # Project tools
    "get_project_info": {
        "name": "get_project_info",
        "description": "Get information about the current project in DaVinci Resolve",
        "component": "project",
        "function": get_project_info
    },
    "get_project_settings": {
        "name": "get_project_settings",
        "description": "Get all settings for the current project",
        "component": "project",
        "function": get_project_settings
    },
    "get_all_timelines": {
        "name": "get_all_timelines",
        "description": "Get a list of all timelines in the current project",
        "component": "project",
        "function": get_all_timelines
    },
    
    # Media Pool tools
    "list_media_pool_items": {
        "name": "list_media_pool_items",
        "description": "List items in the current media pool folder",
        "component": "media_pool",
        "function": list_media_pool_items
    },
    "get_folder_structure": {
        "name": "get_folder_structure",
        "description": "Get the media pool folder structure",
        "component": "media_pool",
        "function": get_folder_structure
    },
    
    # Timeline tools
    "get_timeline_details": {
        "name": "get_timeline_details",
        "description": "Get details about the current timeline",
        "component": "timeline",
        "function": get_timeline_details
    },
    "get_timeline_tracks": {
        "name": "get_timeline_tracks",
        "description": "Get details about all tracks in the current timeline",
        "component": "timeline",
        "function": get_timeline_tracks
    },
    "get_timeline_items": {
        "name": "get_timeline_items",
        "description": "Get details about items in the current timeline",
        "component": "timeline",
        "function": get_timeline_items
    }
}

# Add new tools to global registry
# These will be directly accessible by the execute function
NEW_TOOLS = {
    # Resolve tools
    "get_product_info": {
        "name": "get_product_info",
        "description": "Get DaVinci Resolve product information (name and version)",
        "component": "resolve",
        "function": lambda: tools_execute("get_product_info", {})
    },
    "get_current_page": {
        "name": "get_current_page",
        "description": "Get the current page displayed in DaVinci Resolve",
        "component": "resolve",
        "function": lambda: tools_execute("get_current_page", {})
    },
    "open_page": {
        "name": "open_page",
        "description": "Switch to the specified page in DaVinci Resolve",
        "component": "resolve",
        "function": lambda page_name: tools_execute("open_page", {"page_name": page_name})
    },
    "get_keyframe_mode": {
        "name": "get_keyframe_mode",
        "description": "Get the current keyframe mode",
        "component": "resolve",
        "function": lambda: tools_execute("get_keyframe_mode", {})
    },
    "set_keyframe_mode": {
        "name": "set_keyframe_mode",
        "description": "Set the keyframe mode",
        "component": "resolve",
        "function": lambda mode: tools_execute("set_keyframe_mode", {"mode": mode})
    },
    "quit_resolve": {
        "name": "quit_resolve",
        "description": "Quit DaVinci Resolve application",
        "component": "resolve",
        "function": lambda: tools_execute("quit_resolve", {})
    }
}

@proxy_mcp.tool()
async def search() -> list:
    """
    Search for available tools to interact with DaVinci Resolve.
    
    Returns:
        A list of tools with their names and descriptions.
    """
    logger.info("Search function called")
    
    # Start with legacy tools
    tools_by_component = {}
    for tool_id, tool_info in LEGACY_TOOLS.items():
        component = tool_info["component"]
        if component not in tools_by_component:
            tools_by_component[component] = []
            
        tools_by_component[component].append({
            "name": tool_info["name"],
            "description": tool_info["description"]
        })
    
    # Add direct tools from NEW_TOOLS dictionary
    for tool_id, tool_info in NEW_TOOLS.items():
        component = tool_info["component"]
        if component not in tools_by_component:
            tools_by_component[component] = []
            
        # Check if tool already exists with same name
        if not any(existing["name"] == tool_info["name"] for existing in tools_by_component[component]):
            tools_by_component[component].append({
                "name": tool_info["name"],
                "description": tool_info["description"]
            })
    
    # Also try to get tools from the registration system
    try:
        new_tools = get_all_tools()
        logger.info(f"Found {len(new_tools)} new tools from registration system in search")
        
        for tool in new_tools:
            component = tool["component"]
            if component not in tools_by_component:
                tools_by_component[component] = []
                
            # Check if tool already exists with same name
            if not any(existing["name"] == tool["name"] for existing in tools_by_component[component]):
                tools_by_component[component].append({
                    "name": tool["name"],
                    "description": tool["description"]
                })
    except Exception as e:
        logger.error(f"Error getting tools from registration system: {str(e)}")
    
    # Convert to a flat list for compatibility with existing client
    result = []
    for component, component_tools in tools_by_component.items():
        result.extend(component_tools)
    
    logger.info(f"Returning {len(result)} total tools")
    logger.info(f"Tools: {json.dumps(result)}")
    return result

@proxy_mcp.tool()
async def execute(tool_name: str, parameters: dict = None) -> dict:
    """
    Execute a tool to interact with DaVinci Resolve.
    
    Args:
        tool_name: The name of the tool to execute.
        parameters: Optional parameters to pass to the tool.
        
    Returns:
        The result of the tool execution.
    """
    if parameters is None:
        parameters = {}
    
    logger.info(f"Executing tool '{tool_name}' with parameters: {parameters}")
    
    try:
        # First check in legacy tools
        if tool_name in LEGACY_TOOLS:
            logger.info(f"Executing legacy tool: {tool_name}")
            function = LEGACY_TOOLS[tool_name]["function"]
            result = function(**parameters)
            return result
        
        # Then check in direct new tools
        if tool_name in NEW_TOOLS:
            logger.info(f"Executing direct new tool: {tool_name}")
            function = NEW_TOOLS[tool_name]["function"]
            if parameters:
                result = function(**parameters)
            else:
                result = function()
            return result
            
        # Then try registration system
        logger.info(f"Executing registered tool: {tool_name}")
        result = tools_execute(tool_name, parameters)
        return result
    except Exception as e:
        logger.error(f"Error executing tool '{tool_name}': {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return {"success": False, "error": str(e)}

def run_server():
    """Run the MCP server"""
    logger.info("Starting DaVinci Resolve MCP Server...")
    
    # Test connection to Resolve but continue anyway
    try:
        # Debug the tool registration system
        new_tools = get_all_tools()
        logger.info(f"Found {len(new_tools)} new tools from registration system")
        for tool in new_tools:
            logger.info(f"Tool: {tool['name']} - {tool['component']}")
    except Exception as e:
        logger.warning(f"Error loading tools: {str(e)}")
        logger.warning("The server will start, but tools may not be available until DaVinci Resolve is running.")
    
    # Set up a signal handler for graceful shutdown
    import signal
    def signal_handler(sig, frame):
        logger.info("Received signal to shut down MCP server")
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Run the MCP server
    logger.info("Starting MCP server...")
    
    while True:
        try:
            proxy_mcp.run()
        except Exception as e:
            if "client closed" in str(e).lower():
                logger.info("Client connection closed, restarting server...")
                continue
            else:
                logger.error(f"Error running MCP server: {str(e)}")
                import traceback
                logger.error(traceback.format_exc())
                sys.exit(1)

if __name__ == "__main__":
    run_server() 