"""
ColorGroup Component for DaVinci Resolve API
Handles color group operations for the color page
"""

import logging
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call, get_current_timeline

logger = logging.getLogger("resolve_api.color_group")

def get_color_group_helper(group_name: str):
    """Helper function to find a ColorGroup object by name."""
    project = get_current_project()
    if not project:
        logger.error("No project is currently open")
        return None
    
    groups = project.GetColorGroupsList()
    if not groups:
        logger.error("Failed to get color groups list")
        return None
    
    for group in groups:
        if group.GetName() == group_name:
            return group
    
    logger.error(f"Color group '{group_name}' not found")
    return None

def get_name(group_name: str) -> Dict[str, Any]:
    """
    Get the name of a color group
    
    Args:
        group_name: Name of the color group
        
    Returns:
        Dictionary with group name or error
    """
    return safe_api_call(
        lambda: (
            helper_get_name(group_name)
        ),
        f"Error getting name of color group '{group_name}'"
    )

def helper_get_name(group_name: str) -> Dict[str, Any]:
    """Helper function to get the name of a color group."""
    group = get_color_group_helper(group_name)
    
    if not group:
        return {"success": False, "error": f"Color group '{group_name}' not found"}
    
    name = group.GetName()
    
    return {
        "success": True,
        "result": {
            "name": name
        }
    }

def set_name(group_name: str, new_name: str) -> Dict[str, Any]:
    """
    Set the name of a color group
    
    Args:
        group_name: Current name of the color group
        new_name: New name for the color group
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_name(group_name, new_name)
        ),
        f"Error setting name of color group '{group_name}'"
    )

def helper_set_name(group_name: str, new_name: str) -> Dict[str, Any]:
    """Helper function to set the name of a color group."""
    group = get_color_group_helper(group_name)
    
    if not group:
        return {"success": False, "error": f"Color group '{group_name}' not found"}
    
    result = group.SetName(new_name)
    
    if not result:
        return {"success": False, "error": f"Failed to set name of color group '{group_name}' to '{new_name}'"}
    
    return {
        "success": True,
        "result": {
            "previous_name": group_name,
            "new_name": new_name
        }
    }

def get_clips_in_timeline(group_name: str) -> Dict[str, Any]:
    """
    Get the clips in the timeline that belong to a color group
    
    Args:
        group_name: Name of the color group
        
    Returns:
        Dictionary with clips information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_clips_in_timeline(group_name)
        ),
        f"Error getting clips in timeline for color group '{group_name}'"
    )

def helper_get_clips_in_timeline(group_name: str) -> Dict[str, Any]:
    """Helper function to get the clips in the timeline that belong to a color group."""
    group = get_color_group_helper(group_name)
    
    if not group:
        return {"success": False, "error": f"Color group '{group_name}' not found"}
    
    # Ensure we're on a timeline
    timeline = get_current_timeline()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    # Get clips in timeline that belong to this group
    clips = group.GetClipsInTimeline()
    
    if clips is None:
        return {"success": False, "error": f"Failed to get clips in timeline for color group '{group_name}'"}
    
    # Since we can't return the actual clip objects through MCP,
    # return the count and clip IDs if possible
    clip_info = []
    for clip in clips:
        try:
            clip_info.append({
                "name": clip.GetName(),
                "id": clip.GetUniqueId() if hasattr(clip, "GetUniqueId") else None
            })
        except Exception as e:
            logger.error(f"Error getting clip info: {str(e)}")
    
    return {
        "success": True,
        "result": {
            "group_name": group_name,
            "clip_count": len(clips),
            "clips": clip_info
        }
    }

def get_pre_clip_node_graph(group_name: str) -> Dict[str, Any]:
    """
    Get the pre-clip node graph of a color group
    
    Args:
        group_name: Name of the color group
        
    Returns:
        Dictionary with node graph information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_pre_clip_node_graph(group_name)
        ),
        f"Error getting pre-clip node graph for color group '{group_name}'"
    )

def helper_get_pre_clip_node_graph(group_name: str) -> Dict[str, Any]:
    """Helper function to get the pre-clip node graph of a color group."""
    group = get_color_group_helper(group_name)
    
    if not group:
        return {"success": False, "error": f"Color group '{group_name}' not found"}
    
    # Get the pre-clip node graph
    graph = group.GetPreClipNodeGraph()
    
    if not graph:
        return {"success": False, "error": f"Failed to get pre-clip node graph for color group '{group_name}'"}
    
    # Since we can't return the actual graph object through MCP,
    # return basic information about it
    try:
        node_count = graph.GetNumNodes()
    except Exception:
        node_count = 0
    
    return {
        "success": True,
        "result": {
            "group_name": group_name,
            "node_count": node_count,
            "graph_type": "pre-clip"
        }
    }

def get_post_clip_node_graph(group_name: str) -> Dict[str, Any]:
    """
    Get the post-clip node graph of a color group
    
    Args:
        group_name: Name of the color group
        
    Returns:
        Dictionary with node graph information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_post_clip_node_graph(group_name)
        ),
        f"Error getting post-clip node graph for color group '{group_name}'"
    )

def helper_get_post_clip_node_graph(group_name: str) -> Dict[str, Any]:
    """Helper function to get the post-clip node graph of a color group."""
    group = get_color_group_helper(group_name)
    
    if not group:
        return {"success": False, "error": f"Color group '{group_name}' not found"}
    
    # Get the post-clip node graph
    graph = group.GetPostClipNodeGraph()
    
    if not graph:
        return {"success": False, "error": f"Failed to get post-clip node graph for color group '{group_name}'"}
    
    # Since we can't return the actual graph object through MCP,
    # return basic information about it
    try:
        node_count = graph.GetNumNodes()
    except Exception:
        node_count = 0
    
    return {
        "success": True,
        "result": {
            "group_name": group_name,
            "node_count": node_count,
            "graph_type": "post-clip"
        }
    } 