"""
Resolve API Tools
Implements the general API functions available directly from the Resolve object
"""

import logging
from typing import Dict, Any, List, Optional, Union, Tuple

from ...resolve_api import get_resolve, safe_api_call

logger = logging.getLogger("resolve_api.tools.resolve")

# Define valid page names for OpenPage method
VALID_PAGES = ["media", "cut", "edit", "fusion", "color", "fairlight", "deliver"]

# Define keyframe modes
KEYFRAME_MODES = {
    "All": 0,
    "All+Dynamic": 1, 
    "Selected": 2,
    "Selected+Dynamic": 3
}

def get_product_info() -> Dict[str, Any]:
    """
    Get DaVinci Resolve product information (name and version)
    
    Returns:
        Dictionary with product information or error
    """
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "error": "Could not connect to DaVinci Resolve"}
    
    try:
        product_name = resolve.GetProductName()
        version_fields = resolve.GetVersion()
        version_string = resolve.GetVersionString()
        
        return {
            "success": True,
            "result": {
                "product_name": product_name,
                "version": {
                    "major": version_fields[0] if len(version_fields) > 0 else None,
                    "minor": version_fields[1] if len(version_fields) > 1 else None,
                    "patch": version_fields[2] if len(version_fields) > 2 else None,
                    "build": version_fields[3] if len(version_fields) > 3 else None,
                    "suffix": version_fields[4] if len(version_fields) > 4 else None,
                },
                "version_string": version_string
            }
        }
    except Exception as e:
        logger.error(f"Error getting product info: {str(e)}")
        return {"success": False, "error": str(e)}

def get_current_page() -> Dict[str, Any]:
    """
    Get the current page displayed in DaVinci Resolve
    
    Returns:
        Dictionary with current page information or error
    """
    return safe_api_call(
        lambda: {"page": get_resolve().GetCurrentPage()},
        "Error getting current page"
    )

def open_page(page_name: str) -> Dict[str, Any]:
    """
    Switch to the specified page in DaVinci Resolve
    
    Args:
        page_name: One of "media", "cut", "edit", "fusion", "color", "fairlight", "deliver"
        
    Returns:
        Dictionary with success status or error
    """
    if page_name not in VALID_PAGES:
        return {
            "success": False, 
            "error": f"Invalid page name: {page_name}. Must be one of {VALID_PAGES}"
        }
    
    return safe_api_call(
        lambda: {"switched": get_resolve().OpenPage(page_name)},
        f"Error switching to page {page_name}"
    )

def get_keyframe_mode() -> Dict[str, Any]:
    """
    Get the current keyframe mode
    
    Returns:
        Dictionary with keyframe mode information or error
    """
    return safe_api_call(
        lambda: {
            "keyframe_mode": get_resolve().GetKeyframeMode(),
            "keyframe_mode_name": next((name for name, mode in KEYFRAME_MODES.items() 
                                     if mode == get_resolve().GetKeyframeMode()), "Unknown")
        },
        "Error getting keyframe mode"
    )

def set_keyframe_mode(mode: Union[int, str]) -> Dict[str, Any]:
    """
    Set the keyframe mode
    
    Args:
        mode: Keyframe mode as integer (0-3) or string ("All", "All+Dynamic", "Selected", "Selected+Dynamic")
        
    Returns:
        Dictionary with success status or error
    """
    # Convert string mode to integer if needed
    if isinstance(mode, str):
        if mode not in KEYFRAME_MODES:
            return {
                "success": False, 
                "error": f"Invalid keyframe mode: {mode}. Must be one of {list(KEYFRAME_MODES.keys())}"
            }
        mode = KEYFRAME_MODES[mode]
    
    # Validate integer mode
    if not isinstance(mode, int) or mode < 0 or mode > 3:
        return {
            "success": False, 
            "error": f"Invalid keyframe mode: {mode}. Must be 0-3"
        }
    
    return safe_api_call(
        lambda: {"set": get_resolve().SetKeyframeMode(mode)},
        f"Error setting keyframe mode to {mode}"
    )

def manage_layout_preset(action: str, preset_name: str, file_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Manage layout presets (load, save, update, delete, import, export)
    
    Args:
        action: One of "load", "save", "update", "delete", "import", "export"
        preset_name: Name of the preset
        file_path: Path for import/export operations (optional)
        
    Returns:
        Dictionary with success status or error
    """
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "error": "Could not connect to DaVinci Resolve"}
    
    try:
        if action == "load":
            result = resolve.LoadLayoutPreset(preset_name)
            return {"success": True, "result": {"loaded": result}}
        
        elif action == "save":
            result = resolve.SaveLayoutPreset(preset_name)
            return {"success": True, "result": {"saved": result}}
        
        elif action == "update":
            result = resolve.UpdateLayoutPreset(preset_name)
            return {"success": True, "result": {"updated": result}}
        
        elif action == "delete":
            result = resolve.DeleteLayoutPreset(preset_name)
            return {"success": True, "result": {"deleted": result}}
        
        elif action == "export":
            if not file_path:
                return {"success": False, "error": "File path is required for export operation"}
            
            result = resolve.ExportLayoutPreset(preset_name, file_path)
            return {"success": True, "result": {"exported": result}}
        
        elif action == "import":
            if not file_path:
                return {"success": False, "error": "File path is required for import operation"}
            
            if preset_name:
                result = resolve.ImportLayoutPreset(file_path, preset_name)
            else:
                result = resolve.ImportLayoutPreset(file_path)
                
            return {"success": True, "result": {"imported": result}}
        
        else:
            return {"success": False, "error": f"Invalid action: {action}"}
            
    except Exception as e:
        logger.error(f"Error managing layout preset: {str(e)}")
        return {"success": False, "error": str(e)}

def manage_render_preset(action: str, preset_path: Optional[str] = None, preset_name: Optional[str] = None, 
                         export_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Manage render presets (import, export)
    
    Args:
        action: One of "import", "export"
        preset_path: Path for import operation (required for import)
        preset_name: Name of the preset (required for export)
        export_path: Path for export operation (required for export)
        
    Returns:
        Dictionary with success status or error
    """
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "error": "Could not connect to DaVinci Resolve"}
    
    try:
        if action == "import":
            if not preset_path:
                return {"success": False, "error": "Preset path is required for import operation"}
            
            result = resolve.ImportRenderPreset(preset_path)
            return {"success": True, "result": {"imported": result}}
        
        elif action == "export":
            if not preset_name or not export_path:
                return {"success": False, "error": "Preset name and export path are required for export operation"}
            
            result = resolve.ExportRenderPreset(preset_name, export_path)
            return {"success": True, "result": {"exported": result}}
        
        else:
            return {"success": False, "error": f"Invalid action: {action}"}
            
    except Exception as e:
        logger.error(f"Error managing render preset: {str(e)}")
        return {"success": False, "error": str(e)}

def manage_burn_in_preset(action: str, preset_path: Optional[str] = None, preset_name: Optional[str] = None, 
                          export_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Manage burn-in presets (import, export)
    
    Args:
        action: One of "import", "export"
        preset_path: Path for import operation (required for import)
        preset_name: Name of the preset (required for export)
        export_path: Path for export operation (required for export)
        
    Returns:
        Dictionary with success status or error
    """
    resolve = get_resolve()
    if not resolve:
        return {"success": False, "error": "Could not connect to DaVinci Resolve"}
    
    try:
        if action == "import":
            if not preset_path:
                return {"success": False, "error": "Preset path is required for import operation"}
            
            result = resolve.ImportBurnInPreset(preset_path)
            return {"success": True, "result": {"imported": result}}
        
        elif action == "export":
            if not preset_name or not export_path:
                return {"success": False, "error": "Preset name and export path are required for export operation"}
            
            result = resolve.ExportBurnInPreset(preset_name, export_path)
            return {"success": True, "result": {"exported": result}}
        
        else:
            return {"success": False, "error": f"Invalid action: {action}"}
            
    except Exception as e:
        logger.error(f"Error managing burn-in preset: {str(e)}")
        return {"success": False, "error": str(e)}

def quit_resolve() -> Dict[str, Any]:
    """
    Quit DaVinci Resolve application
    
    Returns:
        Dictionary with success status or error
    """
    return safe_api_call(
        lambda: {"quit": get_resolve().Quit() is None},
        "Error quitting DaVinci Resolve"
    ) 