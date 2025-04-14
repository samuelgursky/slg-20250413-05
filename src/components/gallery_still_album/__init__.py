"""
GalleryStillAlbum Component for DaVinci Resolve API
Handles gallery still album-related operations
"""

import logging
import os
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.gallery_still_album")

def get_gallery_helper():
    """Helper function to get the gallery from the current project."""
    project = get_current_project()
    if not project:
        logger.error("No project is currently open")
        return None
    
    gallery = project.GetGallery()
    if not gallery:
        logger.error("Failed to get Gallery")
        return None
    
    return gallery

def get_album_by_name(album_name: str):
    """Helper function to get a gallery still album by name."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return None
    
    # Get all still albums
    albums = gallery.GetGalleryStillAlbums()
    
    if not albums:
        return None
    
    # Find the album with the specified name
    for album in albums:
        if album.GetLabel() == album_name:
            return album
    
    return None

def get_stills(album_name: str) -> Dict[str, Any]:
    """
    Get all stills from a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        
    Returns:
        Dictionary with list of stills or error
    """
    return safe_api_call(
        lambda: (
            helper_get_stills(album_name)
        ),
        f"Error getting stills from album '{album_name}'"
    )

def helper_get_stills(album_name: str) -> Dict[str, Any]:
    """Helper function to get all stills from a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Get stills from the album
    stills = album.GetStills()
    
    if stills is None:
        return {"success": False, "error": f"Failed to get stills from album '{album_name}'"}
    
    # Collect information about each still
    still_info = []
    for still in stills:
        try:
            # The actual properties available for stills depend on DaVinci Resolve's API
            # These are likely properties, but might need adjustment based on the actual API
            still_info.append({
                "index": stills.index(still),
                "label": still.GetLabel() if hasattr(still, "GetLabel") else f"Still {stills.index(still)}"
            })
        except Exception as e:
            logger.error(f"Error processing still: {str(e)}")
    
    return {
        "success": True,
        "result": {
            "album_name": album_name,
            "stills": still_info,
            "count": len(still_info)
        }
    }

def get_label(album_name: str) -> Dict[str, Any]:
    """
    Get the label of a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        
    Returns:
        Dictionary with album label or error
    """
    return safe_api_call(
        lambda: (
            helper_get_label(album_name)
        ),
        f"Error getting label for album '{album_name}'"
    )

def helper_get_label(album_name: str) -> Dict[str, Any]:
    """Helper function to get the label of a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Get the label
    label = album.GetLabel()
    
    if not label:
        return {"success": False, "error": f"Failed to get label for album '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "name": album_name,
            "label": label
        }
    }

def set_label(album_name: str, label: str) -> Dict[str, Any]:
    """
    Set the label of a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        label: New label for the album
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_label(album_name, label)
        ),
        f"Error setting label for album '{album_name}'"
    )

def helper_set_label(album_name: str, label: str) -> Dict[str, Any]:
    """Helper function to set the label of a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Set the label
    result = album.SetLabel(label)
    
    if not result:
        return {"success": False, "error": f"Failed to set label for album '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "previous_name": album_name,
            "new_label": label
        }
    }

def import_stills(album_name: str, still_paths: List[str]) -> Dict[str, Any]:
    """
    Import stills into a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        still_paths: List of file paths to import as stills
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_import_stills(album_name, still_paths)
        ),
        f"Error importing stills into album '{album_name}'"
    )

def helper_import_stills(album_name: str, still_paths: List[str]) -> Dict[str, Any]:
    """Helper function to import stills into a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Validate paths
    valid_paths = []
    invalid_paths = []
    for path in still_paths:
        if os.path.exists(path) and os.path.isfile(path):
            valid_paths.append(path)
        else:
            invalid_paths.append(path)
    
    if not valid_paths:
        return {"success": False, "error": "No valid file paths provided"}
    
    # Import stills
    imported_count = 0
    failed_imports = []
    
    for path in valid_paths:
        try:
            result = album.ImportStills([path])
            if result:
                imported_count += 1
            else:
                failed_imports.append(path)
        except Exception as e:
            logger.error(f"Error importing still from {path}: {str(e)}")
            failed_imports.append(path)
    
    return {
        "success": imported_count > 0,
        "result": {
            "album_name": album_name,
            "imported_count": imported_count,
            "failed_imports": failed_imports,
            "invalid_paths": invalid_paths
        }
    }

def export_stills(album_name: str, still_indices: List[int], export_dir: str, file_prefix: str = "") -> Dict[str, Any]:
    """
    Export stills from a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        still_indices: List of still indices to export
        export_dir: Directory path to export stills to
        file_prefix: Optional prefix for exported still filenames
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_export_stills(album_name, still_indices, export_dir, file_prefix)
        ),
        f"Error exporting stills from album '{album_name}'"
    )

def helper_export_stills(album_name: str, still_indices: List[int], export_dir: str, file_prefix: str) -> Dict[str, Any]:
    """Helper function to export stills from a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Validate export directory
    if not os.path.exists(export_dir):
        try:
            os.makedirs(export_dir)
        except Exception as e:
            return {"success": False, "error": f"Failed to create export directory: {str(e)}"}
    
    if not os.path.isdir(export_dir):
        return {"success": False, "error": f"Export path is not a directory: {export_dir}"}
    
    # Get stills from the album
    stills = album.GetStills()
    
    if not stills:
        return {"success": False, "error": f"No stills found in album '{album_name}'"}
    
    # Validate still indices
    valid_indices = []
    invalid_indices = []
    for idx in still_indices:
        if 0 <= idx < len(stills):
            valid_indices.append(idx)
        else:
            invalid_indices.append(idx)
    
    if not valid_indices:
        return {"success": False, "error": "No valid still indices provided"}
    
    # Export stills
    exported_count = 0
    failed_exports = []
    
    for idx in valid_indices:
        try:
            still = stills[idx]
            export_path = os.path.join(export_dir, f"{file_prefix}still_{idx}.dpx")
            result = album.ExportStills([still], [export_path])
            if result:
                exported_count += 1
            else:
                failed_exports.append(idx)
        except Exception as e:
            logger.error(f"Error exporting still at index {idx}: {str(e)}")
            failed_exports.append(idx)
    
    return {
        "success": exported_count > 0,
        "result": {
            "album_name": album_name,
            "exported_count": exported_count,
            "failed_exports": failed_exports,
            "invalid_indices": invalid_indices,
            "export_directory": export_dir
        }
    }

def delete_stills(album_name: str, still_indices: List[int]) -> Dict[str, Any]:
    """
    Delete stills from a gallery still album
    
    Args:
        album_name: Name of the gallery still album
        still_indices: List of still indices to delete
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_stills(album_name, still_indices)
        ),
        f"Error deleting stills from album '{album_name}'"
    )

def helper_delete_stills(album_name: str, still_indices: List[int]) -> Dict[str, Any]:
    """Helper function to delete stills from a gallery still album."""
    # Get the album by name
    album = get_album_by_name(album_name)
    
    if not album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Get stills from the album
    stills = album.GetStills()
    
    if not stills:
        return {"success": False, "error": f"No stills found in album '{album_name}'"}
    
    # Validate still indices
    valid_indices = []
    invalid_indices = []
    for idx in still_indices:
        if 0 <= idx < len(stills):
            valid_indices.append(idx)
        else:
            invalid_indices.append(idx)
    
    if not valid_indices:
        return {"success": False, "error": "No valid still indices provided"}
    
    # Get stills to delete
    stills_to_delete = [stills[idx] for idx in valid_indices]
    
    # Delete stills
    result = album.DeleteStills(stills_to_delete)
    
    if not result:
        return {"success": False, "error": f"Failed to delete stills from album '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "album_name": album_name,
            "deleted_count": len(valid_indices),
            "invalid_indices": invalid_indices
        }
    } 