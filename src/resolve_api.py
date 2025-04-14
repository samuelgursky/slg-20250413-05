"""
DaVinci Resolve API Wrapper
Contains common functions and utilities for interacting with the DaVinci Resolve API
"""

import logging
import os
import sys
import functools
from typing import Any, Dict, Callable, Optional, List, TypeVar, cast

logger = logging.getLogger("resolve_api")

# Helper function return type
T = TypeVar('T')

def get_resolve_api_module() -> Any:
    """
    Get the DaVinci Resolve API module based on the current platform
    
    Returns:
        The DaVinci Resolve API module
    """
    resolve_api = None
    
    try:
        if sys.platform.startswith("darwin"):
            # macOS path
            script_dir = "/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules"
            
            if not os.path.exists(script_dir):
                raise ImportError(f"DaVinci Resolve Scripting Modules directory not found: {script_dir}")
                
            if script_dir not in sys.path:
                sys.path.append(script_dir)
                
            import DaVinciResolveScript as dvr_script
            resolve_api = dvr_script
        elif sys.platform.startswith("win") or sys.platform.startswith("cygwin"):
            # Windows path
            script_dir = os.path.join(
                os.environ.get("PROGRAMDATA", "C:\\ProgramData"),
                "Blackmagic Design\\DaVinci Resolve\\Support\\Developer\\Scripting\\Modules"
            )
            
            if not os.path.exists(script_dir):
                raise ImportError(f"DaVinci Resolve Scripting Modules directory not found: {script_dir}")
                
            if script_dir not in sys.path:
                sys.path.append(script_dir)
                
            import DaVinciResolveScript as dvr_script
            resolve_api = dvr_script
        else:
            # Linux
            script_dir = "/opt/resolve/Developer/Scripting/Modules"
            
            if not os.path.exists(script_dir):
                raise ImportError(f"DaVinci Resolve Scripting Modules directory not found: {script_dir}")
                
            if script_dir not in sys.path:
                sys.path.append(script_dir)
                
            import DaVinciResolveScript as dvr_script
            resolve_api = dvr_script
    except ImportError as e:
        logger.error(f"Error loading DaVinci Resolve API module: {str(e)}")
        resolve_api = None
        
    return resolve_api

def get_resolve() -> Any:
    """
    Get the DaVinci Resolve application object
    
    Returns:
        The DaVinci Resolve application object or None if not available
    """
    resolve_api = get_resolve_api_module()
    
    if not resolve_api:
        logger.error("Failed to load DaVinci Resolve API module")
        return None
        
    try:
        resolve = resolve_api.scriptapp("Resolve")
        if not resolve:
            logger.error("Failed to connect to DaVinci Resolve application")
            return None
            
        return resolve
    except Exception as e:
        logger.error(f"Error connecting to DaVinci Resolve: {str(e)}")
        return None

def get_project_manager() -> Any:
    """
    Get the Project Manager instance
    
    Returns:
        The Project Manager object or None if not available
    """
    resolve = get_resolve()
    
    if not resolve:
        logger.error("Could not connect to DaVinci Resolve")
        return None
        
    return resolve.GetProjectManager()

def get_current_project() -> Any:
    """
    Get the current DaVinci Resolve project
    
    Returns:
        The current DaVinci Resolve project or None if not available
    """
    resolve = get_resolve()
    
    if not resolve:
        logger.error("Failed to connect to DaVinci Resolve")
        return None
        
    try:
        project_manager = resolve.GetProjectManager()
        if not project_manager:
            logger.error("Failed to get project manager")
            return None
            
        project = project_manager.GetCurrentProject()
        if not project:
            logger.error("No project is currently open")
            return None
            
        return project
    except Exception as e:
        logger.error(f"Error getting current project: {str(e)}")
        return None

def safe_api_call(func: Callable[[], T], error_message: str) -> Dict[str, Any]:
    """
    Safely call a function and handle exceptions
    
    Args:
        func: Function to call
        error_message: Error message to log if an exception occurs
        
    Returns:
        Dictionary with result or error
    """
    try:
        result = func()
        return {
            "success": True,
            "result": result
        }
    except NotImplementedError as e:
        logger.warning(f"{error_message}: {str(e)}")
        return {
            "success": False, 
            "error": str(e)
        }
    except Exception as e:
        logger.error(f"{error_message}: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

# TODO: Helper functions needed for object lookup by ID
# These functions need to be implemented to support various component operations

def get_media_pool_item_by_id(item_id: str) -> Optional[Any]:
    """
    Find a MediaPoolItem object by its unique ID
    
    This is a critical helper function needed by:
    - append_to_timeline
    - create_timeline_from_clips
    - delete_clips
    - add_clip_mattes_to_media_pool
    
    Args:
        item_id: Unique ID of the media pool item
        
    Returns:
        MediaPoolItem object or None if not found
    """
    # Get the current project
    project = get_current_project()
    if not project:
        logger.error(f"Failed to get current project while looking for media item {item_id}")
        return None
        
    # Get the media pool
    media_pool = project.GetMediaPool()
    if not media_pool:
        logger.error(f"Failed to get media pool while looking for media item {item_id}")
        return None
        
    # Alternative approach: If the above search doesn't work, use the current folder directly
    # and try to get all current clips
    current_folder = media_pool.GetCurrentFolder()
    if current_folder:
        try:
            # Try to get clips from the current folder
            clips = current_folder.GetClipList() or []
            
            # Check each clip for the matching ID
            for clip in clips:
                try:
                    if hasattr(clip, "GetUniqueId") and clip.GetUniqueId() == item_id:
                        return clip
                except Exception as e:
                    logger.debug(f"Error getting clip ID: {str(e)}")
                    continue
        except Exception as e:
            logger.debug(f"Error getting clips from current folder: {str(e)}")
    
    # Get the root folder
    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        logger.error(f"Failed to get root folder while looking for media item {item_id}")
        return None
        
    # Define a recursive function to search through folders
    def search_folder_for_clip(folder):
        # Get all clips in this folder
        clips = folder.GetClipList() or []
        
        # Check each clip for the matching ID
        for clip in clips:
            try:
                if hasattr(clip, "GetUniqueId") and clip.GetUniqueId() == item_id:
                    logger.debug(f"Found clip with ID {item_id} in folder {folder.GetName()}")
                    return clip
            except Exception as e:
                logger.debug(f"Error getting clip ID: {str(e)}")
                continue
                
        # If not found, search in subfolders
        subfolders = folder.GetSubFolderList() or []
        for subfolder in subfolders:
            result = search_folder_for_clip(subfolder)
            if result:
                return result
                
        # Not found in this folder or its subfolders
        return None
        
    # Start the search from the root folder
    found_clip = search_folder_for_clip(root_folder)
    if found_clip:
        return found_clip
    
    # Fall back to an alternative approach - try to iterate through all subfolders and manually look for clips
    # This is a workaround for potential issues with the recursion approach
    try:
        # Try a manual approach - sometimes GetClipList() might not return all clips
        # Try importing the media again to get a direct reference
        current_timeline = project.GetCurrentTimeline()
        if current_timeline:
            # Get all items in the current timeline
            track_count = current_timeline.GetTrackCount("video")
            for i in range(1, track_count + 1):
                items = current_timeline.GetItemListInTrack("video", i) or []
                for item in items:
                    try:
                        if hasattr(item, "GetMediaPoolItem"):
                            clip = item.GetMediaPoolItem()
                            if clip and hasattr(clip, "GetUniqueId") and clip.GetUniqueId() == item_id:
                                return clip
                    except Exception as e:
                        logger.debug(f"Error getting media pool item: {str(e)}")
    except Exception as e:
        logger.debug(f"Error in fallback approach: {str(e)}")
    
    # Last resort - try to import the clip again to get a direct reference
    # This can be used if we have a mapping of IDs to file paths (not implemented here)
    
    logger.error(f"Could not find MediaPoolItem with ID: {item_id}")
    return None

def get_folder_by_id(folder_id: str) -> Optional[Any]:
    """
    Find a Folder object by its unique ID
    
    This is a critical helper function needed by:
    - set_current_folder
    - add_subfolder with parent folder ID
    - add_timeline_mattes_to_media_pool
    
    Args:
        folder_id: Unique ID of the folder
        
    Returns:
        Folder object or None if not found
    """
    # Get the current project
    project = get_current_project()
    if not project:
        logger.error(f"Failed to get current project while looking for folder {folder_id}")
        return None
        
    # Get the media pool
    media_pool = project.GetMediaPool()
    if not media_pool:
        logger.error(f"Failed to get media pool while looking for folder {folder_id}")
        return None
        
    # Get the root folder
    root_folder = media_pool.GetRootFolder()
    if not root_folder:
        logger.error(f"Failed to get root folder while looking for folder {folder_id}")
        return None
        
    # Check if the root folder matches the ID
    try:
        if hasattr(root_folder, "GetUniqueId") and root_folder.GetUniqueId() == folder_id:
            return root_folder
    except Exception as e:
        logger.debug(f"Error getting root folder ID: {str(e)}")
        
    # Define a recursive function to search through folders
    def search_for_folder(folder):
        # Get all subfolders
        subfolders = folder.GetSubFolderList() or []
        
        # Check each subfolder for the matching ID
        for subfolder in subfolders:
            try:
                if hasattr(subfolder, "GetUniqueId") and subfolder.GetUniqueId() == folder_id:
                    return subfolder
            except Exception as e:
                logger.debug(f"Error getting subfolder ID: {str(e)}")
                continue
                
            # If not found, search in this subfolder's subfolders
            result = search_for_folder(subfolder)
            if result:
                return result
                
        # Not found in this folder or its subfolders
        return None
        
    # Start the search from the root folder
    return search_for_folder(root_folder)

def get_timeline_by_id(timeline_id: str) -> Optional[Any]:
    """
    Find a Timeline object by its unique ID
    
    This helper function will be needed for future timeline operations
    
    Args:
        timeline_id: Unique ID of the timeline
        
    Returns:
        Timeline object or None if not found
    """
    # Get the current project
    project = get_current_project()
    if not project:
        logger.error(f"Failed to get current project while looking for timeline {timeline_id}")
        return None
        
    # Get the number of timelines
    timeline_count = project.GetTimelineCount()
    
    # Iterate through all timelines and check their IDs
    for i in range(1, timeline_count + 1):
        timeline = project.GetTimelineByIndex(i)
        if not timeline:
            continue
            
        try:
            if hasattr(timeline, "GetUniqueId") and timeline.GetUniqueId() == timeline_id:
                return timeline
        except Exception as e:
            logger.debug(f"Error getting timeline ID: {str(e)}")
            continue
            
    # Timeline not found
    return None

def get_timeline_item_by_id(item_id: str) -> Optional[Any]:
    """
    Find a TimelineItem object by its unique ID
    
    This helper function will be needed for future timeline item operations
    
    Args:
        item_id: Unique ID of the timeline item
        
    Returns:
        TimelineItem object or None if not found
    """
    # Get the current project
    project = get_current_project()
    if not project:
        logger.error(f"Failed to get current project while looking for timeline item {item_id}")
        return None
        
    # Get the current timeline
    timeline = project.GetCurrentTimeline()
    if not timeline:
        logger.error(f"Failed to get current timeline while looking for timeline item {item_id}")
        return None
        
    # Get all track types
    track_types = ["video", "audio", "subtitle"]
    
    # Iterate through track types and all tracks
    for track_type in track_types:
        # Get number of tracks for this type
        track_count = timeline.GetTrackCount(track_type)
        
        # Check all tracks
        for track_index in range(1, track_count + 1):
            # Get items in this track
            items = timeline.GetItemListInTrack(track_type, track_index) or []
            
            # Check each item for matching ID
            for item in items:
                try:
                    if hasattr(item, "GetUniqueId") and item.GetUniqueId() == item_id:
                        return item
                except Exception as e:
                    logger.debug(f"Error getting timeline item ID: {str(e)}")
                    continue
                    
    # If not found in current timeline, try to check all timelines
    # This is a more thorough search but may be slower
    timeline_count = project.GetTimelineCount()
    current_timeline = timeline  # Save current timeline to restore later
    
    for i in range(1, timeline_count + 1):
        # Skip the current timeline as we already checked it
        timeline_to_check = project.GetTimelineByIndex(i)
        if timeline_to_check == current_timeline:
            continue
            
        # Set as current timeline to access its items
        if not project.SetCurrentTimeline(timeline_to_check):
            continue
            
        # Now check this timeline
        for track_type in track_types:
            track_count = timeline_to_check.GetTrackCount(track_type)
            
            for track_index in range(1, track_count + 1):
                items = timeline_to_check.GetItemListInTrack(track_type, track_index) or []
                
                for item in items:
                    try:
                        if hasattr(item, "GetUniqueId") and item.GetUniqueId() == item_id:
                            # Restore original timeline
                            project.SetCurrentTimeline(current_timeline)
                            return item
                    except Exception as e:
                        logger.debug(f"Error getting timeline item ID: {str(e)}")
                        continue
    
    # Restore original timeline
    project.SetCurrentTimeline(current_timeline)
    
    # Item not found
    return None 