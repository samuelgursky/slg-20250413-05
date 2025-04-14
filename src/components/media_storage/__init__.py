"""
MediaStorage Component for DaVinci Resolve API
Handles file system operations and importing media
"""

import logging
import os
from typing import Dict, Any, List, Optional

from ...resolve_api import get_resolve, safe_api_call, get_media_pool_item_by_id, get_folder_by_id

logger = logging.getLogger("resolve_api.media_storage")

def get_mounted_volumes() -> Dict[str, Any]:
    """
    Get a list of mounted volumes
    
    Returns:
        Dictionary with list of volume paths or error
    """
    def _get_mounted_volumes():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get resolve instance")
        
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
        
        volumes = media_storage.GetMountedVolumeList()
        
        return {
            "volumes": volumes,
            "count": len(volumes)
        }
    
    return safe_api_call(
        _get_mounted_volumes,
        "Error getting mounted volumes"
    )

def get_subfolder_list(folder_path: str) -> Dict[str, Any]:
    """
    Get a list of subfolders in the specified folder
    
    Args:
        folder_path: Path to folder to list subfolders from
        
    Returns:
        Dictionary with list of subfolder paths or error
    """
    def _get_subfolder_list():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get resolve instance")
        
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
        
        # Normalize path separators for current OS
        normalized_path = os.path.normpath(folder_path)
        
        # Verify path exists and is a directory
        if not os.path.exists(normalized_path):
            raise RuntimeError(f"Path does not exist: {normalized_path}")
        
        if not os.path.isdir(normalized_path):
            raise RuntimeError(f"Path is not a directory: {normalized_path}")
            
        subfolders = media_storage.GetSubFolderList(normalized_path)
        
        return {
            "path": normalized_path,
            "subfolders": subfolders,
            "count": len(subfolders)
        }
    
    return safe_api_call(
        _get_subfolder_list,
        f"Error getting subfolders from '{folder_path}'"
    )

def get_file_list(folder_path: str) -> Dict[str, Any]:
    """
    Get a list of files in the specified folder
    
    Args:
        folder_path: Path to folder to list files from
        
    Returns:
        Dictionary with list of file paths or error
    """
    def _get_file_list():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get resolve instance")
        
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
        
        # Normalize path separators for current OS
        normalized_path = os.path.normpath(folder_path)
        
        # Verify path exists and is a directory
        if not os.path.exists(normalized_path):
            raise RuntimeError(f"Path does not exist: {normalized_path}")
        
        if not os.path.isdir(normalized_path):
            raise RuntimeError(f"Path is not a directory: {normalized_path}")
            
        files = media_storage.GetFileList(normalized_path)
        
        return {
            "path": normalized_path,
            "files": files,
            "count": len(files)
        }
    
    return safe_api_call(
        _get_file_list,
        f"Error getting files from '{folder_path}'"
    )

def reveal_in_storage(file_path: str) -> Dict[str, Any]:
    """
    Reveal a file or folder in the OS file browser
    
    Args:
        file_path: Path to file or folder to reveal
        
    Returns:
        Dictionary with success status or error
    """
    def _reveal_in_storage():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get resolve instance")
        
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
        
        # Normalize path separators for current OS
        normalized_path = os.path.normpath(file_path)
        
        # Verify path exists
        if not os.path.exists(normalized_path):
            raise RuntimeError(f"Path does not exist: {normalized_path}")
            
        result = media_storage.RevealInStorage(normalized_path)
        
        if not result:
            raise RuntimeError(f"Failed to reveal '{normalized_path}' in storage")
        
        return {
            "success": True,
            "path": normalized_path
        }
    
    return safe_api_call(
        _reveal_in_storage,
        f"Error revealing '{file_path}' in storage"
    )

def add_items_to_media_pool(file_paths: List[str], folder_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Add items to media pool
    
    Args:
        file_paths: List of file paths to add
        folder_id: Optional ID of folder to add items to (default is current folder)
        
    Returns:
        Dictionary with list of added media pool items or error
    """
    def _add_items_to_media_pool():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get resolve instance")
        
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
        
        # Get the project manager
        project_manager = resolve.GetProjectManager()
        if not project_manager:
            raise RuntimeError("Failed to get project manager")
        
        # Get the current project
        project = project_manager.GetCurrentProject()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Get the media pool
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
        
        # Get the target folder (current folder if folder_id is None)
        target_folder = None
        if folder_id is not None:
            # Logic to find folder by ID would go here
            # This is a simplification since GetFolderByID is not directly available
            # In a real implementation, we would need to traverse the folder structure
            raise NotImplementedError("Finding folder by ID is not implemented yet")
        
        # Add items to media pool
        normalized_paths = [os.path.normpath(path) for path in file_paths]
        
        # Verify paths exist
        for path in normalized_paths:
            if not os.path.exists(path):
                raise RuntimeError(f"Path does not exist: {path}")
        
        # Add items to media pool
        added_items = media_storage.AddItemListToMediaPool(normalized_paths, target_folder)
        
        if added_items is None:
            raise RuntimeError("Failed to add items to media pool")
        
        # Convert the items to a serializable format
        item_info = []
        for item in added_items:
            if item:
                item_info.append({
                    "name": item.GetName(),
                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                })
        
        return {
            "success": True,
            "count": len(item_info),
            "items": item_info
        }
    
    return safe_api_call(
        _add_items_to_media_pool,
        "Error adding items to media pool"
    )

def add_clip_mattes_to_media_pool(clip_id: str, paths: List[str]) -> Dict[str, Any]:
    """
    Add clip mattes to a media pool item
    
    Args:
        clip_id: ID of the media pool item
        paths: List of file paths to add as mattes
        
    Returns:
        Dictionary with success status or error
    """
    def _add_clip_mattes_to_media_pool():
        # Get the media storage
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get DaVinci Resolve instance")
            
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
            
        # Find the clip by ID
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Add mattes
        result = media_storage.AddClipMattesToMediaPool(clip, paths)
        if not result:
            raise RuntimeError(f"Failed to add mattes to clip '{clip.GetName()}'")
            
        return {
            "success": True,
            "clip_id": clip_id,
            "clip_name": clip.GetName(),
            "matte_count": len(paths)
        }
        
    return safe_api_call(
        _add_clip_mattes_to_media_pool,
        "Error adding clip mattes to media pool"
    )

def add_timeline_mattes_to_media_pool(folder_id: str, paths: List[str]) -> Dict[str, Any]:
    """
    Add timeline mattes to the media pool in a specific folder
    
    Args:
        folder_id: ID of the folder to add mattes to
        paths: List of file paths to add as mattes
        
    Returns:
        Dictionary with success status or error
    """
    def _add_timeline_mattes_to_media_pool():
        # Get the media storage
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get DaVinci Resolve instance")
            
        media_storage = resolve.GetMediaStorage()
        if not media_storage:
            raise RuntimeError("Failed to get media storage")
            
        # Find the folder by ID
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        # Add mattes
        result = media_storage.AddTimelineMattesToMediaPool(folder, paths)
        if not result:
            raise RuntimeError(f"Failed to add timeline mattes to folder '{folder.GetName()}'")
            
        return {
            "success": True,
            "folder_id": folder_id,
            "folder_name": folder.GetName(),
            "matte_count": len(paths)
        }
        
    return safe_api_call(
        _add_timeline_mattes_to_media_pool,
        "Error adding timeline mattes to media pool"
    ) 