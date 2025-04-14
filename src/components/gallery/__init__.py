"""
Gallery Component for DaVinci Resolve API
Handles gallery-related operations
"""

import logging
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.gallery")

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

def get_album_name(album_name: str) -> Dict[str, Any]:
    """
    Get the name of a gallery album
    
    Args:
        album_name: Name of the album to get information about
        
    Returns:
        Dictionary with album name or error
    """
    return safe_api_call(
        lambda: (
            helper_get_album_name(album_name)
        ),
        "Error getting album name"
    )

def helper_get_album_name(album_name: str) -> Dict[str, Any]:
    """Helper function to get the name of a gallery album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Check if album exists
    albums = gallery.GetGalleryStillAlbums()
    album_found = False
    for album in albums:
        if album.GetName() == album_name:
            album_found = True
            break
    
    if not album_found:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    return {
        "success": True,
        "result": {
            "name": album_name
        }
    }

def set_album_name(album_name: str, new_name: str) -> Dict[str, Any]:
    """
    Set the name of a gallery album
    
    Args:
        album_name: Current name of the album
        new_name: New name for the album
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_album_name(album_name, new_name)
        ),
        "Error setting album name"
    )

def helper_set_album_name(album_name: str, new_name: str) -> Dict[str, Any]:
    """Helper function to set the name of a gallery album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Find the album
    albums = gallery.GetGalleryStillAlbums()
    target_album = None
    for album in albums:
        if album.GetName() == album_name:
            target_album = album
            break
    
    if not target_album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Set the album name
    result = target_album.SetLabel(new_name)
    
    if not result:
        return {"success": False, "error": f"Failed to set album name to '{new_name}'"}
    
    return {
        "success": True,
        "result": {
            "previous_name": album_name,
            "new_name": new_name
        }
    }

def get_current_still_album() -> Dict[str, Any]:
    """
    Get information about the current still album
    
    Returns:
        Dictionary with current still album information or error
    """
    return safe_api_call(
        lambda: (
            helper_get_current_still_album()
        ),
        "Error getting current still album"
    )

def helper_get_current_still_album() -> Dict[str, Any]:
    """Helper function to get information about the current still album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Get the current still album
    current_album = gallery.GetCurrentStillAlbum()
    
    if not current_album:
        return {"success": False, "error": "No current still album or failed to get current album"}
    
    # Get album information
    album_name = current_album.GetLabel()
    stills = current_album.GetStills() or []
    
    return {
        "success": True,
        "result": {
            "name": album_name,
            "still_count": len(stills)
        }
    }

def set_current_still_album(album_name: str) -> Dict[str, Any]:
    """
    Set the current still album
    
    Args:
        album_name: Name of the album to set as current
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_current_still_album(album_name)
        ),
        "Error setting current still album"
    )

def helper_set_current_still_album(album_name: str) -> Dict[str, Any]:
    """Helper function to set the current still album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Find the album
    albums = gallery.GetGalleryStillAlbums()
    target_album = None
    for album in albums:
        if album.GetLabel() == album_name:
            target_album = album
            break
    
    if not target_album:
        return {"success": False, "error": f"Album '{album_name}' not found"}
    
    # Set the current still album
    result = gallery.SetCurrentStillAlbum(target_album)
    
    if not result:
        return {"success": False, "error": f"Failed to set current still album to '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "current_album": album_name
        }
    }

def get_gallery_still_albums() -> Dict[str, Any]:
    """
    Get a list of all gallery still albums
    
    Returns:
        Dictionary with list of gallery still albums or error
    """
    return safe_api_call(
        lambda: (
            helper_get_gallery_still_albums()
        ),
        "Error getting gallery still albums"
    )

def helper_get_gallery_still_albums() -> Dict[str, Any]:
    """Helper function to get a list of all gallery still albums."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Get all still albums
    albums = gallery.GetGalleryStillAlbums()
    
    if albums is None:
        return {"success": False, "error": "Failed to get gallery still albums"}
    
    # Collect album information
    album_info = []
    for album in albums:
        stills = album.GetStills() or []
        album_info.append({
            "name": album.GetLabel(),
            "still_count": len(stills)
        })
    
    return {
        "success": True,
        "result": {
            "albums": album_info,
            "count": len(album_info)
        }
    }

def get_gallery_power_grade_albums() -> Dict[str, Any]:
    """
    Get a list of all gallery power grade albums
    
    Returns:
        Dictionary with list of gallery power grade albums or error
    """
    return safe_api_call(
        lambda: (
            helper_get_gallery_power_grade_albums()
        ),
        "Error getting gallery power grade albums"
    )

def helper_get_gallery_power_grade_albums() -> Dict[str, Any]:
    """Helper function to get a list of all gallery power grade albums."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Get all power grade albums
    albums = gallery.GetGalleryPowerGradeAlbums()
    
    if albums is None:
        return {"success": False, "error": "Failed to get gallery power grade albums"}
    
    # Collect album information
    album_info = []
    for album in albums:
        album_info.append({
            "name": album.GetLabel()
        })
    
    return {
        "success": True,
        "result": {
            "albums": album_info,
            "count": len(album_info)
        }
    }

def create_gallery_still_album(album_name: str) -> Dict[str, Any]:
    """
    Create a new gallery still album
    
    Args:
        album_name: Name for the new album
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_create_gallery_still_album(album_name)
        ),
        "Error creating gallery still album"
    )

def helper_create_gallery_still_album(album_name: str) -> Dict[str, Any]:
    """Helper function to create a new gallery still album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Check if album with this name already exists
    albums = gallery.GetGalleryStillAlbums()
    for album in albums:
        if album.GetLabel() == album_name:
            return {"success": False, "error": f"Album '{album_name}' already exists"}
    
    # Create the new album
    new_album = gallery.CreateGalleryStillAlbum(album_name)
    
    if not new_album:
        return {"success": False, "error": f"Failed to create gallery still album '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "name": album_name,
            "still_count": 0
        }
    }

def create_gallery_power_grade_album(album_name: str) -> Dict[str, Any]:
    """
    Create a new gallery power grade album
    
    Args:
        album_name: Name for the new power grade album
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_create_gallery_power_grade_album(album_name)
        ),
        "Error creating gallery power grade album"
    )

def helper_create_gallery_power_grade_album(album_name: str) -> Dict[str, Any]:
    """Helper function to create a new gallery power grade album."""
    gallery = get_gallery_helper()
    
    if not gallery:
        return {"success": False, "error": "Failed to get gallery"}
    
    # Check if album with this name already exists
    albums = gallery.GetGalleryPowerGradeAlbums()
    for album in albums:
        if album.GetLabel() == album_name:
            return {"success": False, "error": f"Power grade album '{album_name}' already exists"}
    
    # Create the new power grade album
    new_album = gallery.CreateGalleryPowerGradeAlbum(album_name)
    
    if not new_album:
        return {"success": False, "error": f"Failed to create gallery power grade album '{album_name}'"}
    
    return {
        "success": True,
        "result": {
            "name": album_name
        }
    } 