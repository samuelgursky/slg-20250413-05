"""
Graph Component for DaVinci Resolve API
Handles node graph-related operations for the color page
"""

import logging
import os
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.graph")

def get_current_graph_helper():
    """Helper function to get the current node graph from the current clip in DaVinci Resolve."""
    project = get_current_project()
    if not project:
        logger.error("No project is currently open")
        return None
    
    try:
        # First check if we are on the color page
        from ..project import get_current_page
        page_result = get_current_page()
        if page_result.get("success", False):
            current_page = page_result.get("result", {}).get("page", "")
            if current_page != "color":
                logger.error("Current page is not the color page. Graph operations require the color page.")
                return None
        
        # Get the current timeline
        timeline = project.GetCurrentTimeline()
        if not timeline:
            logger.error("No timeline is currently open")
            return None
        
        # Get the current clip (timeline item)
        current_item = timeline.GetCurrentVideoItem()
        if not current_item:
            logger.error("No clip is currently selected")
            return None
        
        # Get the node graph for the current clip
        graph = current_item.GetNodeGraph()
        if not graph:
            logger.error("Failed to get node graph for the current clip")
            return None
        
        return graph
    except Exception as e:
        logger.error(f"Error getting current node graph: {str(e)}")
        return None

def get_num_nodes() -> Dict[str, Any]:
    """
    Get the number of nodes in the current node graph
    
    Returns:
        Dictionary with node count or error
    """
    return safe_api_call(
        lambda: (
            helper_get_num_nodes()
        ),
        "Error getting number of nodes"
    )

def helper_get_num_nodes() -> Dict[str, Any]:
    """Helper function to get the number of nodes in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Get the number of nodes
    node_count = graph.GetNumNodes()
    
    return {
        "success": True,
        "result": {
            "node_count": node_count
        }
    }

def set_lut(node_index: int, lut_path: str) -> Dict[str, Any]:
    """
    Set LUT for a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        lut_path: Path to the LUT file
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_lut(node_index, lut_path)
        ),
        "Error setting LUT"
    )

def helper_set_lut(node_index: int, lut_path: str) -> Dict[str, Any]:
    """Helper function to set LUT for a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Validate LUT path
    if not os.path.exists(lut_path):
        return {"success": False, "error": f"LUT file not found: {lut_path}"}
    
    # Set the LUT
    result = graph.SetLUT(node_index, lut_path)
    
    if not result:
        return {"success": False, "error": f"Failed to set LUT for node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "lut_path": lut_path
        }
    }

def get_lut(node_index: int) -> Dict[str, Any]:
    """
    Get LUT information for a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        
    Returns:
        Dictionary with LUT information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_lut(node_index)
        ),
        "Error getting LUT"
    )

def helper_get_lut(node_index: int) -> Dict[str, Any]:
    """Helper function to get LUT information for a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Get the LUT information
    lut_info = graph.GetLUT(node_index)
    
    if not lut_info:
        return {"success": False, "error": f"Failed to get LUT information for node {node_index} or no LUT is applied"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "lut_info": lut_info
        }
    }

def set_node_cache_mode(node_index: int, cache_mode: str) -> Dict[str, Any]:
    """
    Set cache mode for a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        cache_mode: Cache mode to set ("auto", "on", or "off")
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_node_cache_mode(node_index, cache_mode)
        ),
        "Error setting node cache mode"
    )

def helper_set_node_cache_mode(node_index: int, cache_mode: str) -> Dict[str, Any]:
    """Helper function to set cache mode for a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Validate cache mode
    valid_modes = ["auto", "on", "off"]
    if cache_mode.lower() not in valid_modes:
        return {"success": False, "error": f"Invalid cache mode: {cache_mode}. Valid modes are: {', '.join(valid_modes)}"}
    
    # Set the cache mode
    result = graph.SetNodeCacheMode(node_index, cache_mode.lower())
    
    if not result:
        return {"success": False, "error": f"Failed to set cache mode for node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "cache_mode": cache_mode.lower()
        }
    }

def get_node_cache_mode(node_index: int) -> Dict[str, Any]:
    """
    Get cache mode for a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        
    Returns:
        Dictionary with cache mode information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_node_cache_mode(node_index)
        ),
        "Error getting node cache mode"
    )

def helper_get_node_cache_mode(node_index: int) -> Dict[str, Any]:
    """Helper function to get cache mode for a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Get the cache mode
    cache_mode = graph.GetNodeCacheMode(node_index)
    
    if cache_mode is None or cache_mode == "":
        return {"success": False, "error": f"Failed to get cache mode for node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "cache_mode": cache_mode
        }
    }

def get_node_label(node_index: int) -> Dict[str, Any]:
    """
    Get the label of a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        
    Returns:
        Dictionary with node label or error
    """
    return safe_api_call(
        lambda: (
            helper_get_node_label(node_index)
        ),
        "Error getting node label"
    )

def helper_get_node_label(node_index: int) -> Dict[str, Any]:
    """Helper function to get the label of a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Get the node label
    label = graph.GetNodeLabel(node_index)
    
    if label is None:
        return {"success": False, "error": f"Failed to get label for node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "label": label
        }
    }

def get_tools_in_node(node_index: int) -> Dict[str, Any]:
    """
    Get the list of tools in a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        
    Returns:
        Dictionary with tools information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_tools_in_node(node_index)
        ),
        "Error getting tools in node"
    )

def helper_get_tools_in_node(node_index: int) -> Dict[str, Any]:
    """Helper function to get the list of tools in a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Get the tools in the node
    tools = graph.GetToolsInNode(node_index)
    
    if tools is None:
        return {"success": False, "error": f"Failed to get tools for node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "tools": tools,
            "tool_count": len(tools) if isinstance(tools, list) else 0
        }
    }

def set_node_enabled(node_index: int, enabled: bool) -> Dict[str, Any]:
    """
    Enable or disable a specific node in the current node graph
    
    Args:
        node_index: Index of the node
        enabled: Whether the node should be enabled (True) or disabled (False)
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_node_enabled(node_index, enabled)
        ),
        "Error setting node enabled state"
    )

def helper_set_node_enabled(node_index: int, enabled: bool) -> Dict[str, Any]:
    """Helper function to enable or disable a specific node in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate node index
    node_count = graph.GetNumNodes()
    if node_index < 1 or node_index > node_count:
        return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Set the node enabled state
    result = graph.SetNodeEnabled(node_index, enabled)
    
    if not result:
        return {"success": False, "error": f"Failed to {'enable' if enabled else 'disable'} node {node_index}"}
    
    return {
        "success": True,
        "result": {
            "node_index": node_index,
            "enabled": enabled
        }
    }

def apply_grade_from_drx(drx_path: str, node_index: Optional[int] = None, still_offset: int = 0) -> Dict[str, Any]:
    """
    Apply a grade from a DRX file to the current node graph
    
    Args:
        drx_path: Path to the DRX file
        node_index: (Optional) Index of the node to apply the grade to
        still_offset: (Optional) Still offset for the grade
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_apply_grade_from_drx(drx_path, node_index, still_offset)
        ),
        "Error applying grade from DRX"
    )

def helper_apply_grade_from_drx(drx_path: str, node_index: Optional[int], still_offset: int) -> Dict[str, Any]:
    """Helper function to apply a grade from a DRX file to the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate DRX path
    if not os.path.exists(drx_path):
        return {"success": False, "error": f"DRX file not found: {drx_path}"}
    
    # Validate node index if provided
    if node_index is not None:
        node_count = graph.GetNumNodes()
        if node_index < 1 or node_index > node_count:
            return {"success": False, "error": f"Invalid node index: {node_index}. Valid range is 1-{node_count}"}
    
    # Apply the grade
    # The API might support different parameter combinations, adjust as needed
    if node_index is not None:
        result = graph.ApplyGradeFromDRX(drx_path, node_index, still_offset)
    else:
        result = graph.ApplyGradeFromDRX(drx_path, still_offset)
    
    if not result:
        return {"success": False, "error": f"Failed to apply grade from DRX file: {drx_path}"}
    
    return {
        "success": True,
        "result": {
            "drx_path": drx_path,
            "node_index": node_index,
            "still_offset": still_offset
        }
    }

def apply_arri_cdl_lut(cdl_path: str) -> Dict[str, Any]:
    """
    Apply an ARRI CDL LUT to the current node graph
    
    Args:
        cdl_path: Path to the CDL file
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_apply_arri_cdl_lut(cdl_path)
        ),
        "Error applying ARRI CDL LUT"
    )

def helper_apply_arri_cdl_lut(cdl_path: str) -> Dict[str, Any]:
    """Helper function to apply an ARRI CDL LUT to the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Validate CDL path
    if not os.path.exists(cdl_path):
        return {"success": False, "error": f"CDL file not found: {cdl_path}"}
    
    # Apply the ARRI CDL LUT
    result = graph.ApplyArriCdlLut(cdl_path)
    
    if not result:
        return {"success": False, "error": f"Failed to apply ARRI CDL LUT: {cdl_path}"}
    
    return {
        "success": True,
        "result": {
            "cdl_path": cdl_path
        }
    }

def reset_all_grades() -> Dict[str, Any]:
    """
    Reset all grades in the current node graph
    
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_reset_all_grades()
        ),
        "Error resetting all grades"
    )

def helper_reset_all_grades() -> Dict[str, Any]:
    """Helper function to reset all grades in the current node graph."""
    graph = get_current_graph_helper()
    
    if not graph:
        return {"success": False, "error": "Failed to get current node graph"}
    
    # Reset all grades
    result = graph.ResetAllGrades()
    
    if not result:
        return {"success": False, "error": "Failed to reset all grades"}
    
    return {
        "success": True,
        "result": {
            "message": "All grades have been reset successfully"
        }
    } 