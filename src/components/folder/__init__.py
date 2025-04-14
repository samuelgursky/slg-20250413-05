"""
Folder Component for DaVinci Resolve API
Handles folder operations in the Media Pool
"""

import logging
import os
from typing import Dict, Any, List, Optional

from ...resolve_api import safe_api_call, get_current_project, get_current_media_pool

logger = logging.getLogger("resolve_api.folder")

def get_folder_by_id(folder_id: str) -> Optional[Any]:
    """
    Helper function to get a folder object by its ID
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Folder object or None if not found
    """
    media_pool = get_current_media_pool()
    if not media_pool:
        logger.error("No media pool available")
        return None
    
    # Get the root folder
    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        logger.error("Failed to get root folder")
        return None
    
    # If the requested folder is the root folder
    if folder_id == root_folder.GetUniqueId():
        return root_folder
    
    # Helper function to search for folder by ID
    def search_folder(folder, target_id):
        # Check if this is the folder we're looking for
        if folder.GetUniqueId() == target_id:
            return folder
        
        # Get subfolders
        subfolders = folder.GetSubFolderList()
        for subfolder in subfolders:
            result = search_folder(subfolder, target_id)
            if result:
                return result
        
        return None
    
    # Start search from root folder
    return search_folder(root_folder, folder_id)

def get_is_folder_stale(folder_id: str) -> Dict[str, Any]:
    """
    Check if a folder's content is stale and needs to be refreshed
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with stale status or error
    """
    def _get_is_folder_stale():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        is_stale = folder.GetIsFolderStale()
        
        return {
            "folder_id": folder_id,
            "is_stale": is_stale
        }
    
    return safe_api_call(
        _get_is_folder_stale,
        f"Error checking if folder {folder_id} is stale"
    )

def get_unique_id(folder_id: str) -> Dict[str, Any]:
    """
    Get the unique ID of a folder
    
    Args:
        folder_id: Current ID of the folder (to find the folder object)
        
    Returns:
        Dictionary with unique ID or error
    """
    def _get_unique_id():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        unique_id = folder.GetUniqueId()
        
        return {
            "folder_id": folder_id,
            "unique_id": unique_id
        }
    
    return safe_api_call(
        _get_unique_id,
        f"Error getting unique ID for folder {folder_id}"
    )

def export_folder(folder_id: str, file_path: str) -> Dict[str, Any]:
    """
    Export a folder to a specified file path
    
    Args:
        folder_id: Unique identifier of the folder
        file_path: Path where the folder will be exported
        
    Returns:
        Dictionary with export status or error
    """
    def _export_folder():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        result = folder.Export(file_path)
        if not result:
            raise RuntimeError(f"Failed to export folder to {file_path}")
            
        return {
            "success": True,
            "folder_id": folder_id,
            "export_path": file_path
        }
    
    return safe_api_call(
        _export_folder,
        f"Error exporting folder {folder_id} to {file_path}"
    )

def transcribe_audio(folder_id: str) -> Dict[str, Any]:
    """
    Transcribe audio content in a folder
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with transcription status or error
    """
    def _transcribe_audio():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        result = folder.TranscribeAudio()
        if not result:
            raise RuntimeError(f"Failed to transcribe audio in folder {folder_id}")
            
        return {
            "success": True,
            "folder_id": folder_id,
            "transcription_started": True
        }
    
    return safe_api_call(
        _transcribe_audio,
        f"Error transcribing audio in folder {folder_id}"
    )

def clear_transcription(folder_id: str) -> Dict[str, Any]:
    """
    Clear transcription data for a folder
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with operation status or error
    """
    def _clear_transcription():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        result = folder.ClearTranscription()
        if not result:
            raise RuntimeError(f"Failed to clear transcription in folder {folder_id}")
            
        return {
            "success": True,
            "folder_id": folder_id,
            "transcription_cleared": True
        }
    
    return safe_api_call(
        _clear_transcription,
        f"Error clearing transcription in folder {folder_id}"
    )

def get_clip_list(folder_id: str) -> Dict[str, Any]:
    """
    Get the list of clips in a folder
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with clip list or error
    """
    def _get_clip_list():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        clips = folder.GetClipList()
        if clips is None:
            raise RuntimeError(f"Failed to get clip list for folder {folder_id}")
        
        # Since we can't return the actual clip objects through MCP,
        # return the clip IDs and names
        clip_info = []
        for clip in clips:
            try:
                clip_info.append({
                    "name": clip.GetName(),
                    "id": clip.GetUniqueId()
                })
            except Exception as e:
                logger.error(f"Error getting clip info: {str(e)}")
        
        return {
            "folder_id": folder_id,
            "clip_count": len(clips),
            "clips": clip_info
        }
    
    return safe_api_call(
        _get_clip_list,
        f"Error getting clip list for folder {folder_id}"
    )

def get_name(folder_id: str) -> Dict[str, Any]:
    """
    Get the name of a folder
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with folder name or error
    """
    def _get_name():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        name = folder.GetName()
        
        return {
            "folder_id": folder_id,
            "name": name
        }
    
    return safe_api_call(
        _get_name,
        f"Error getting name for folder {folder_id}"
    )

def get_subfolder_list(folder_id: str) -> Dict[str, Any]:
    """
    Get the list of subfolders in a folder
    
    Args:
        folder_id: Unique identifier of the folder
        
    Returns:
        Dictionary with subfolder list or error
    """
    def _get_subfolder_list():
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        subfolders = folder.GetSubFolderList()
        if subfolders is None:
            raise RuntimeError(f"Failed to get subfolder list for folder {folder_id}")
        
        # Since we can't return the actual folder objects through MCP,
        # return the folder IDs and names
        subfolder_info = []
        for subfolder in subfolders:
            try:
                subfolder_info.append({
                    "name": subfolder.GetName(),
                    "id": subfolder.GetUniqueId()
                })
            except Exception as e:
                logger.error(f"Error getting subfolder info: {str(e)}")
        
        return {
            "folder_id": folder_id,
            "subfolder_count": len(subfolders),
            "subfolders": subfolder_info
        }
    
    return safe_api_call(
        _get_subfolder_list,
        f"Error getting subfolder list for folder {folder_id}"
    ) 