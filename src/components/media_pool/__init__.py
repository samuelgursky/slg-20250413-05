"""
Media Pool Component for DaVinci Resolve API
Handles media pool-related operations
"""

import logging
import os
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_current_project, safe_api_call, get_media_pool_item_by_id, get_folder_by_id

logger = logging.getLogger("resolve_api.media_pool")

def get_media_pool() -> Any:
    """Get the media pool from the current project"""
    project = get_current_project()
    if not project:
        return None
        
    return project.GetMediaPool()

def list_media_pool_items() -> Dict[str, Any]:
    """
    List items in the current media pool folder
    
    Returns:
        Dictionary with media pool items or error
    """
    def _list_media_pool_items():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        current_folder = media_pool.GetCurrentFolder()
        if not current_folder:
            raise RuntimeError("Failed to get current folder")
            
        clips = current_folder.GetClipList() or []
        clip_info = []
        
        for clip in clips:
            clip_info.append({
                "name": clip.GetName(),
                "duration": clip.GetDuration(),
                "fps": clip.GetClipProperty("FPS"),
                "resolution": clip.GetClipProperty("Resolution"),
                "file_path": clip.GetClipProperty("File Path"),
                "type": clip.GetClipProperty("Type"),
                "format": clip.GetClipProperty("Format"),
                "id": clip.GetUniqueId() if hasattr(clip, "GetUniqueId") else "unknown"
            })
            
        return {
            "folder_name": current_folder.GetName(),
            "clip_count": len(clips),
            "clips": clip_info
        }
    
    return safe_api_call(
        _list_media_pool_items,
        "Error listing media pool items"
    )

def get_folder_structure() -> Dict[str, Any]:
    """
    Get the media pool folder structure
    
    Returns:
        Dictionary with folder structure or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        media_pool = project.GetMediaPool()
        if not media_pool:
            return {"success": False, "error": "Could not access media pool"}
            
        root_folder = media_pool.GetRootFolder()
        if not root_folder:
            return {"success": False, "error": "Could not access root folder"}
        
        def get_folder_info(folder):
            """Recursively get folder information"""
            subfolders = folder.GetSubFolderList()
            clips = folder.GetClipList()
            
            subfolder_info = []
            for subfolder in subfolders:
                subfolder_info.append(get_folder_info(subfolder))
                
            return {
                "name": folder.GetName(),
                "clip_count": len(clips) if clips else 0,
                "subfolders": subfolder_info
            }
            
        folder_structure = get_folder_info(root_folder)
        
        return {
            "success": True,
            "result": folder_structure
        }
    except Exception as e:
        logger.error(f"Error getting folder structure: {str(e)}")
        return {"success": False, "error": str(e)}

def get_root_folder() -> Dict[str, Any]:
    """
    Get the root folder of the media pool
    
    Returns:
        Dictionary with root folder information or error
    """
    def _get_root_folder():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        root_folder = media_pool.GetRootFolder()
        if not root_folder:
            raise RuntimeError("Failed to get root folder")
            
        clips = root_folder.GetClipList() or []
        subfolders = root_folder.GetSubFolderList() or []
            
        return {
            "name": root_folder.GetName(),
            "clip_count": len(clips),
            "subfolder_count": len(subfolders)
        }
    
    return safe_api_call(
        _get_root_folder,
        "Error getting root folder"
    )

def add_subfolder(folder_name: str, parent_folder_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a subfolder to the media pool
    
    Args:
        folder_name: Name of the new subfolder
        parent_folder_id: Optional ID of the parent folder. If not provided, 
                         the current folder will be used as parent.
        
    Returns:
        Dictionary with folder information or error
    """
    def _add_subfolder():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        parent_folder = None
        
        # If parent folder ID is provided, find that folder
        if parent_folder_id:
            parent_folder = get_folder_by_id(parent_folder_id)
            if not parent_folder:
                raise RuntimeError(f"Failed to find parent folder with ID: {parent_folder_id}")
        else:
            # Otherwise use the current folder as parent
            parent_folder = media_pool.GetCurrentFolder()
            if not parent_folder:
                raise RuntimeError("Failed to get current folder")
        
        # Create the subfolder
        folder = media_pool.AddSubFolder(parent_folder, folder_name)
        if not folder:
            raise RuntimeError(f"Failed to create subfolder '{folder_name}'")
            
        # Get info about the new folder
        return {
            "name": folder.GetName(),
            "parent_name": parent_folder.GetName(),
            "success": True
        }
        
    return safe_api_call(
        _add_subfolder,
        f"Error adding subfolder '{folder_name}'"
    )

def delete_folders(folder_names: List[str]) -> Dict[str, Any]:
    """
    Delete folders from the media pool
    
    Args:
        folder_names: List of folder names to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_folders():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the folders by name
        current_folder = media_pool.GetCurrentFolder()
        if not current_folder:
            raise RuntimeError("Failed to get current folder")
            
        subfolders = current_folder.GetSubFolderList() or []
        
        # Find folders that match the provided names
        folders_to_delete = []
        found_names = []
        for subfolder in subfolders:
            if subfolder.GetName() in folder_names:
                folders_to_delete.append(subfolder)
                found_names.append(subfolder.GetName())
        
        # Check if we found all requested folders
        missing_names = [name for name in folder_names if name not in found_names]
        if missing_names:
            raise RuntimeError(f"Could not find folder(s): {', '.join(missing_names)}")
            
        # Delete the folders
        result = media_pool.DeleteFolders(folders_to_delete)
        if not result:
            raise RuntimeError("Failed to delete folders")
            
        return {
            "success": True,
            "deleted_count": len(folders_to_delete),
            "deleted_folders": found_names
        }
        
    return safe_api_call(
        _delete_folders,
        "Error deleting folders from media pool"
    )

def refresh_folders() -> Dict[str, Any]:
    """
    Refresh folders in the media pool (useful in collaboration mode)
    
    Returns:
        Dictionary with success status or error
    """
    def _refresh_folders():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        result = media_pool.RefreshFolders()
        if not result:
            raise RuntimeError("Failed to refresh folders")
            
        return {
            "success": True
        }
    
    return safe_api_call(
        _refresh_folders,
        "Error refreshing folders"
    )

def create_empty_timeline(timeline_name: str) -> Dict[str, Any]:
    """
    Create a new empty timeline
    
    Args:
        timeline_name: Name for the new timeline
        
    Returns:
        Dictionary with timeline information or error
    """
    def _create_empty_timeline():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        timeline = media_pool.CreateEmptyTimeline(timeline_name)
        if not timeline:
            raise RuntimeError(f"Failed to create timeline '{timeline_name}'")
            
        return {
            "name": timeline.GetName(),
            "success": True,
            "start_timecode": timeline.GetStartTimecode(),
            "frame_count": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
            "track_count": timeline.GetTrackCount("video") + timeline.GetTrackCount("audio")
        }
    
    return safe_api_call(
        _create_empty_timeline,
        f"Error creating timeline '{timeline_name}'"
    )

def append_to_timeline(clips: Union[List[Dict[str, Any]], List[str]]) -> Dict[str, Any]:
    """
    Append clips to the current timeline
    
    Args:
        clips: List of media pool item IDs or clip info dictionaries
        
    Returns:
        Dictionary with appended timeline items or error
    """
    def _append_to_timeline():
        # Get the current project
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
            
        # Verify we have a current timeline
        current_timeline = project.GetCurrentTimeline()
        if not current_timeline:
            raise RuntimeError("No timeline is currently active")
        
        # Get the media pool
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Special case handling for "all" clips
        if len(clips) == 1 and clips[0] == "all":
            logger.info("Appending all clips from current folder")
            current_folder = media_pool.GetCurrentFolder()
            if not current_folder:
                raise RuntimeError("Failed to get current folder")
                
            all_clips = current_folder.GetClipList() or []
            if not all_clips:
                raise RuntimeError("No clips found in current folder")
                
            # Directly append all clips
            timeline_items = media_pool.AppendToTimeline(all_clips)
            if not timeline_items:
                raise RuntimeError("Failed to append all clips to timeline")
                
            # Convert timeline items to serializable format
            item_info = []
            for item in timeline_items:
                if item:
                    item_info.append({
                        "name": item.GetName(),
                        "start_frame": item.GetStart(),
                        "end_frame": item.GetEnd(),
                        "duration": item.GetDuration(),
                        "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                    })
                    
            return {
                "success": True,
                "count": len(item_info),
                "items": item_info
            }
        
        # Process clips to ensure they're in the right format
        processed_clips = []
        failed_clip_ids = []
        
        for clip in clips:
            if isinstance(clip, str):
                # This is a clip ID - try to get the MediaPoolItem
                # First try to find in current folder (faster)
                current_folder = media_pool.GetCurrentFolder()
                folder_clips = current_folder.GetClipList() or [] if current_folder else []
                
                found_clip = None
                for folder_clip in folder_clips:
                    try:
                        if hasattr(folder_clip, "GetUniqueId") and folder_clip.GetUniqueId() == clip:
                            found_clip = folder_clip
                            break
                    except Exception as e:
                        logger.debug(f"Error getting clip ID: {str(e)}")
                
                if not found_clip:
                    # Try the helper function as fallback
                    found_clip = get_media_pool_item_by_id(clip)
                    
                if found_clip:
                    processed_clips.append(found_clip)
                else:
                    failed_clip_ids.append(clip)
                    logger.warning(f"Failed to find MediaPoolItem with ID: {clip} - will try fallback approaches")
            elif isinstance(clip, dict):
                # This is a clip info dictionary
                if "mediaPoolItem" not in clip:
                    raise RuntimeError(f"Missing required 'mediaPoolItem' field in clip info: {clip}")
                    
                # If mediaPoolItem is a string ID, convert it to an actual MediaPoolItem
                if isinstance(clip["mediaPoolItem"], str):
                    # First try to find in current folder (faster)
                    current_folder = media_pool.GetCurrentFolder()
                    folder_clips = current_folder.GetClipList() or [] if current_folder else []
                    
                    found_clip = None
                    for folder_clip in folder_clips:
                        try:
                            if hasattr(folder_clip, "GetUniqueId") and folder_clip.GetUniqueId() == clip["mediaPoolItem"]:
                                found_clip = folder_clip
                                break
                        except Exception as e:
                            logger.debug(f"Error getting clip ID: {str(e)}")
                    
                    if not found_clip:
                        # Try the helper function as fallback
                        found_clip = get_media_pool_item_by_id(clip["mediaPoolItem"])
                        
                    if found_clip:
                        # Create a new dict with the actual MediaPoolItem
                        processed_clip_info = clip.copy()
                        processed_clip_info["mediaPoolItem"] = found_clip
                        processed_clips.append(processed_clip_info)
                    else:
                        failed_clip_ids.append(clip["mediaPoolItem"])
                        logger.warning(f"Failed to find MediaPoolItem with ID: {clip['mediaPoolItem']} - will try fallback approaches")
                else:
                    # Assume it's already a MediaPoolItem object
                    processed_clips.append(clip)
            else:
                # Unknown format
                raise RuntimeError(f"Unsupported clip format: {clip}")
        
        # If we couldn't process any clips by ID but have IDs to find,
        # try a fallback approach using current folder clips
        if not processed_clips and failed_clip_ids:
            logger.info("Using fallback approach to find clips by ID")
            try:
                # Get the current folder and all its clips
                current_folder = media_pool.GetCurrentFolder()
                if current_folder:
                    folder_clips = current_folder.GetClipList() or []
                    
                    # If we have exactly one clip in the folder and one ID to match,
                    # just use that clip (assuming it's what the user wants)
                    if len(folder_clips) == 1 and len(failed_clip_ids) == 1:
                        logger.info(f"Using the only clip in folder as a fallback")
                        processed_clips.append(folder_clips[0])
                    else:
                        # Otherwise, just use all clips in the folder
                        logger.info(f"Using all {len(folder_clips)} clips from the current folder")
                        processed_clips.extend(folder_clips)
            except Exception as e:
                logger.error(f"Fallback approach failed: {str(e)}")
        
        # If we still don't have any clips processed, raise an error
        if not processed_clips:
            raise RuntimeError("No valid clips found to append to timeline")
            
        # Append to timeline
        logger.info(f"Appending {len(processed_clips)} clips to timeline")
        timeline_items = media_pool.AppendToTimeline(processed_clips)
        
        if not timeline_items:
            raise RuntimeError("Failed to append clips to timeline - this may be due to DaVinci Resolve API limitations or the clips not being compatible with the timeline")
            
        # Convert timeline items to serializable format
        item_info = []
        for item in timeline_items:
            if item:
                item_info.append({
                    "name": item.GetName(),
                    "start_frame": item.GetStart(),
                    "end_frame": item.GetEnd(),
                    "duration": item.GetDuration(),
                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                })
                
        return {
            "success": True,
            "count": len(item_info),
            "items": item_info
        }
    
    return safe_api_call(
        _append_to_timeline,
        "Error appending clips to timeline"
    )

def import_media(paths: List[str]) -> Dict[str, Any]:
    """
    Import media files into the current media pool folder
    
    Args:
        paths: List of file or folder paths to import
        
    Returns:
        Dictionary with imported media items or error
    """
    def _import_media():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
        
        # Normalize all paths
        normalized_paths = [os.path.normpath(path) for path in paths]
        
        # Verify all paths exist
        for path in normalized_paths:
            if not os.path.exists(path):
                raise RuntimeError(f"Path does not exist: {path}")
        
        # Import media
        imported_items = media_pool.ImportMedia(normalized_paths)
        if imported_items is None:
            raise RuntimeError("Failed to import media")
        
        # Convert imported items to serializable format
        item_info = []
        for item in imported_items:
            if item:
                item_info.append({
                    "name": item.GetName(),
                    "type": item.GetClipProperty("Type") if hasattr(item, "GetClipProperty") else "unknown",
                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                })
                
        return {
            "success": True,
            "count": len(item_info),
            "items": item_info
        }
    
    return safe_api_call(
        _import_media,
        "Error importing media"
    )

def delete_clips(clip_ids: List[str]) -> Dict[str, Any]:
    """
    Delete clips from the media pool
    
    Args:
        clip_ids: List of clip IDs to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_clips():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Convert clip IDs to actual MediaPoolItem objects
        clips_to_delete = []
        for clip_id in clip_ids:
            clip = get_media_pool_item_by_id(clip_id)
            if not clip:
                raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            clips_to_delete.append(clip)
            
        # Delete the clips
        if not clips_to_delete:
            raise RuntimeError("No clips to delete")
            
        result = media_pool.DeleteClips(clips_to_delete)
        if not result:
            raise RuntimeError("Failed to delete clips")
            
        return {
            "success": True,
            "deleted_count": len(clips_to_delete)
        }
        
    return safe_api_call(
        _delete_clips,
        "Error deleting clips from media pool"
    )

def get_current_folder() -> Dict[str, Any]:
    """
    Get the current folder in the media pool
    
    Returns:
        Dictionary with current folder information or error
    """
    def _get_current_folder():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        current_folder = media_pool.GetCurrentFolder()
        if not current_folder:
            raise RuntimeError("Failed to get current folder")
            
        clips = current_folder.GetClipList() or []
        subfolders = current_folder.GetSubFolderList() or []
            
        return {
            "name": current_folder.GetName(),
            "clip_count": len(clips),
            "subfolder_count": len(subfolders)
        }
    
    return safe_api_call(
        _get_current_folder,
        "Error getting current folder"
    )

def set_media_pool_current_folder(folder_id: str) -> Dict[str, Any]:
    """
    Set the current folder in the media pool
    
    Args:
        folder_id: ID of the folder to set as current
        
    Returns:
        Dictionary with success status or error
    """
    def _set_current_folder():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the folder by ID
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        # Set as current folder
        result = media_pool.SetCurrentFolder(folder)
        if not result:
            raise RuntimeError(f"Failed to set folder with ID '{folder_id}' as current folder")
            
        return {
            "success": True,
            "folder_name": folder.GetName(),
            "folder_id": folder_id
        }
        
    return safe_api_call(
        _set_current_folder,
        "Error setting current folder in media pool"
    )

def import_timeline_from_file(file_path: str, import_options: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Import a timeline from a file (AAF, EDL, XML, etc.)
    
    Args:
        file_path: Path to the timeline file to import
        import_options: Optional dictionary of import options
            - timelineName: Name for the imported timeline
            - importSourceClips: Whether to import source clips (default True)
            - sourceClipsPath: Path to search for source clips
            - sourceClipsFolders: List of Media Pool folder objects to search for source clips
            - interlaceProcessing: Whether to enable interlace processing (AAF only)
            
    Returns:
        Dictionary with imported timeline information or error
    """
    def _import_timeline_from_file():
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
        
        # Normalize file path
        normalized_path = os.path.normpath(file_path)
        
        # Verify the file exists
        if not os.path.exists(normalized_path):
            raise RuntimeError(f"File does not exist: {normalized_path}")
        
        # Verify the file type
        valid_extensions = ['.aaf', '.edl', '.xml', '.fcpxml', '.drt', '.adl', '.otio']
        file_ext = os.path.splitext(normalized_path)[1].lower()
        if file_ext not in valid_extensions:
            raise RuntimeError(f"Unsupported file format: {file_ext}. Supported formats: {', '.join(valid_extensions)}")
        
        # Set default import options if none provided
        options = import_options or {}
        
        # Import the timeline
        timeline = media_pool.ImportTimelineFromFile(normalized_path, options)
        
        if not timeline:
            raise RuntimeError(f"Failed to import timeline from '{normalized_path}'")
        
        # Get timeline details
        return {
            "name": timeline.GetName(),
            "success": True,
            "start_timecode": timeline.GetStartTimecode(),
            "frame_count": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
            "track_count": timeline.GetTrackCount("video") + timeline.GetTrackCount("audio")
        }
    
    return safe_api_call(
        _import_timeline_from_file,
        f"Error importing timeline from '{file_path}'"
    )

def create_timeline_from_clips(timeline_name: str, clips: List[Union[Dict[str, Any], str]]) -> Dict[str, Any]:
    """
    Create a new timeline with specified name and append the specified clips
    
    Args:
        timeline_name: Name for the new timeline
        clips: List of media pool item IDs or clip info dictionaries
            Each clip info dict can contain:
            - mediaPoolItem: Media pool item object or ID
            - startFrame: Start frame of the clip (optional)
            - endFrame: End frame of the clip (optional)
            - recordFrame: Record frame position on the timeline (optional)
            
    Returns:
        Dictionary with timeline information or error
    """
    def _create_timeline_from_clips():
        # Get the current project
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")

        # Get the media pool
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
        
        # Special case handling for "all" clips
        if len(clips) == 1 and clips[0] == "all":
            logger.info("Creating timeline with all clips from current folder")
            current_folder = media_pool.GetCurrentFolder()
            if not current_folder:
                raise RuntimeError("Failed to get current folder")
                
            clip_list = current_folder.GetClipList()
            if not clip_list:
                raise RuntimeError("No clips found in current folder")
                
            timeline = media_pool.CreateTimelineFromClips(timeline_name, clip_list)
        else:
            # Process clips list
            processed_clips = []
            
            for clip_info in clips:
                if isinstance(clip_info, str):
                    # Just a media pool item ID
                    media_pool_item = get_media_pool_item_by_id(clip_info)
                    if not media_pool_item:
                        raise RuntimeError(f"Failed to find clip with ID: {clip_info}")
                    processed_clips.append({
                        "mediaPoolItem": media_pool_item
                    })
                else:
                    # A clip info dict
                    media_pool_item_id = clip_info.get("mediaPoolItem")
                    if not media_pool_item_id:
                        raise RuntimeError("Missing mediaPoolItem in clip info")
                        
                    media_pool_item = get_media_pool_item_by_id(media_pool_item_id)
                    if not media_pool_item:
                        raise RuntimeError(f"Failed to find clip with ID: {media_pool_item_id}")
                        
                    processed_clip_info = {
                        "mediaPoolItem": media_pool_item
                    }
                    
                    # Add optional parameters if present
                    for param in ["startFrame", "endFrame", "recordFrame"]:
                        if param in clip_info:
                            processed_clip_info[param] = clip_info[param]
                            
                    processed_clips.append(processed_clip_info)
            
            if not processed_clips:
                raise RuntimeError("No valid clips to add to timeline")
                
            timeline = media_pool.CreateTimelineFromClips(timeline_name, processed_clips)
            
        if not timeline:
            raise RuntimeError(f"Failed to create timeline '{timeline_name}'")
            
        return {
            "name": timeline.GetName(),
            "success": True,
            "start_timecode": timeline.GetStartTimecode(),
            "frame_count": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
            "track_count": timeline.GetTrackCount("video") + timeline.GetTrackCount("audio")
        }
    
    return safe_api_call(
        _create_timeline_from_clips,
        f"Error creating timeline '{timeline_name}' from clips"
    )

def delete_timelines(timeline_names: List[str]) -> Dict[str, Any]:
    """
    Delete timelines from the current project
    
    Args:
        timeline_names: List of timeline names to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_timelines():
        # Get the current project
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")

        # Get the media pool
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the timelines by name
        all_timelines = []
        timeline_count = project.GetTimelineCount()
        for i in range(1, timeline_count + 1):
            timeline = project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() in timeline_names:
                all_timelines.append(timeline)
                
        # Check if we found all requested timelines
        found_names = [timeline.GetName() for timeline in all_timelines]
        missing_names = [name for name in timeline_names if name not in found_names]
        
        if missing_names:
            raise RuntimeError(f"Could not find timeline(s): {', '.join(missing_names)}")
            
        # Delete the timelines
        result = media_pool.DeleteTimelines(all_timelines)
        if not result:
            raise RuntimeError("Failed to delete timelines")
            
        return {
            "success": True,
            "deleted_count": len(all_timelines),
            "deleted_timelines": found_names
        }
        
    return safe_api_call(
        _delete_timelines,
        "Error deleting timelines from project"
    )

def append_all_clips_to_timeline() -> Dict[str, Any]:
    """
    Append all clips from the current media pool folder to the current timeline
    
    Returns:
        Dictionary with appended timeline items or error
    """
    def _append_all_clips_to_timeline():
        # Get the current project
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
            
        # Verify we have a current timeline
        current_timeline = project.GetCurrentTimeline()
        if not current_timeline:
            raise RuntimeError("No timeline is currently active")
        
        # Get the media pool
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Get the current folder
        current_folder = media_pool.GetCurrentFolder()
        if not current_folder:
            raise RuntimeError("Failed to get current folder")
            
        # Get all clips in the current folder
        clips = current_folder.GetClipList() or []
        if not clips:
            raise RuntimeError("No clips found in current folder")
            
        logger.info(f"Found {len(clips)} clips in current folder, attempting to append to timeline")
        
        # Append the clips directly to the timeline
        # Note: We pass the actual MediaPoolItem objects, not their IDs
        timeline_items = media_pool.AppendToTimeline(clips)
        
        if not timeline_items:
            raise RuntimeError(f"Failed to append clips to timeline, check if timeline is active and clips are valid")
            
        # Convert timeline items to serializable format
        item_info = []
        for item in timeline_items:
            if item:
                item_info.append({
                    "name": item.GetName(),
                    "start_frame": item.GetStart(),
                    "end_frame": item.GetEnd(),
                    "duration": item.GetDuration(),
                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                })
                
        return {
            "success": True,
            "count": len(item_info),
            "items": item_info
        }
    
    return safe_api_call(
        _append_all_clips_to_timeline,
        "Error appending all clips to timeline"
    )

# Alias for backward compatibility
set_current_folder = set_media_pool_current_folder 

def move_clips(clip_ids: List[str], target_folder_id: str) -> Dict[str, Any]:
    """
    Move specified clips to a target folder
    
    Args:
        clip_ids: List of clip IDs to move
        target_folder_id: ID of the target folder
        
    Returns:
        Dictionary with success status or error
    """
    def _move_clips():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the target folder
        target_folder = get_folder_by_id(target_folder_id)
        if not target_folder:
            raise RuntimeError(f"Failed to find target folder with ID: {target_folder_id}")
            
        # Convert clip IDs to MediaPoolItem objects
        clips_to_move = []
        for clip_id in clip_ids:
            clip = get_media_pool_item_by_id(clip_id)
            if not clip:
                raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            clips_to_move.append(clip)
            
        # Move the clips
        if not clips_to_move:
            raise RuntimeError("No clips to move")
            
        result = media_pool.MoveClips(clips_to_move, target_folder)
        if not result:
            raise RuntimeError("Failed to move clips")
            
        return {
            "success": True,
            "moved_count": len(clips_to_move),
            "target_folder": target_folder.GetName()
        }
        
    return safe_api_call(
        _move_clips,
        "Error moving clips to target folder"
    )

def move_folders(folder_ids: List[str], target_folder_id: str) -> Dict[str, Any]:
    """
    Move specified folders to a target folder
    
    Args:
        folder_ids: List of folder IDs to move
        target_folder_id: ID of the target folder
        
    Returns:
        Dictionary with success status or error
    """
    def _move_folders():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the target folder
        target_folder = get_folder_by_id(target_folder_id)
        if not target_folder:
            raise RuntimeError(f"Failed to find target folder with ID: {target_folder_id}")
            
        # Convert folder IDs to Folder objects
        folders_to_move = []
        folder_names = []
        for folder_id in folder_ids:
            folder = get_folder_by_id(folder_id)
            if not folder:
                raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            folders_to_move.append(folder)
            folder_names.append(folder.GetName())
            
        # Move the folders
        if not folders_to_move:
            raise RuntimeError("No folders to move")
            
        result = media_pool.MoveFolders(folders_to_move, target_folder)
        if not result:
            raise RuntimeError("Failed to move folders")
            
        return {
            "success": True,
            "moved_count": len(folders_to_move),
            "moved_folders": folder_names,
            "target_folder": target_folder.GetName()
        }
        
    return safe_api_call(
        _move_folders,
        "Error moving folders to target folder"
    )

def get_clip_matte_list(clip_id: str) -> Dict[str, Any]:
    """
    Get the list of mattes for a specified clip
    
    Args:
        clip_id: ID of the clip to get mattes for
        
    Returns:
        Dictionary with matte paths or error
    """
    def _get_clip_matte_list():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the clip
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Get the mattes
        mattes = media_pool.GetClipMatteList(clip)
        if mattes is None:  # Check if None, as empty list is valid
            raise RuntimeError("Failed to get matte list")
            
        return {
            "success": True,
            "clip_name": clip.GetName(),
            "clip_id": clip_id,
            "matte_count": len(mattes),
            "matte_paths": mattes
        }
        
    return safe_api_call(
        _get_clip_matte_list,
        f"Error getting matte list for clip with ID: {clip_id}"
    )

def get_timeline_matte_list(folder_id: str) -> Dict[str, Any]:
    """
    Get the list of timeline mattes in a specified folder
    
    Args:
        folder_id: ID of the folder to get mattes from
        
    Returns:
        Dictionary with matte MediaPoolItems or error
    """
    def _get_timeline_matte_list():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the folder
        folder = get_folder_by_id(folder_id)
        if not folder:
            raise RuntimeError(f"Failed to find folder with ID: {folder_id}")
            
        # Get the mattes
        mattes = media_pool.GetTimelineMatteList(folder)
        if mattes is None:  # Check if None, as empty list is valid
            raise RuntimeError("Failed to get timeline matte list")
            
        # Convert mattes to serializable format
        matte_info = []
        for matte in mattes:
            if matte:
                matte_info.append({
                    "name": matte.GetName(),
                    "id": matte.GetUniqueId() if hasattr(matte, "GetUniqueId") else "unknown",
                    "type": matte.GetClipProperty("Type") if hasattr(matte, "GetClipProperty") else "unknown"
                })
                
        return {
            "success": True,
            "folder_name": folder.GetName(),
            "folder_id": folder_id,
            "matte_count": len(matte_info),
            "mattes": matte_info
        }
        
    return safe_api_call(
        _get_timeline_matte_list,
        f"Error getting timeline matte list for folder with ID: {folder_id}"
    )

def delete_clip_mattes(clip_id: str, matte_paths: List[str]) -> Dict[str, Any]:
    """
    Delete mattes for a specified clip
    
    Args:
        clip_id: ID of the clip to delete mattes from
        matte_paths: List of paths to the matte files to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_clip_mattes():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the clip
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Delete the mattes
        result = media_pool.DeleteClipMattes(clip, matte_paths)
        if not result:
            raise RuntimeError("Failed to delete clip mattes")
            
        return {
            "success": True,
            "clip_name": clip.GetName(),
            "clip_id": clip_id,
            "deleted_count": len(matte_paths)
        }
        
    return safe_api_call(
        _delete_clip_mattes,
        f"Error deleting mattes for clip with ID: {clip_id}"
    )

def relink_clips(clip_ids: List[str], folder_path: str) -> Dict[str, Any]:
    """
    Update the folder location of specified media pool clips
    
    Args:
        clip_ids: List of clip IDs to relink
        folder_path: Path to the folder where the media is located
        
    Returns:
        Dictionary with success status or error
    """
    def _relink_clips():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Convert clip IDs to MediaPoolItem objects
        clips_to_relink = []
        for clip_id in clip_ids:
            clip = get_media_pool_item_by_id(clip_id)
            if not clip:
                raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            clips_to_relink.append(clip)
            
        # Relink the clips
        if not clips_to_relink:
            raise RuntimeError("No clips to relink")
            
        # Ensure the folder path exists
        if not os.path.isdir(folder_path):
            raise RuntimeError(f"Folder path does not exist or is not a directory: {folder_path}")
            
        # Normalize folder path
        normalized_path = os.path.normpath(folder_path)
        
        result = media_pool.RelinkClips(clips_to_relink, normalized_path)
        if not result:
            raise RuntimeError("Failed to relink clips")
            
        return {
            "success": True,
            "relinked_count": len(clips_to_relink),
            "folder_path": normalized_path
        }
        
    return safe_api_call(
        _relink_clips,
        "Error relinking clips"
    )

def unlink_clips(clip_ids: List[str]) -> Dict[str, Any]:
    """
    Unlink specified media pool clips
    
    Args:
        clip_ids: List of clip IDs to unlink
        
    Returns:
        Dictionary with success status or error
    """
    def _unlink_clips():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Convert clip IDs to MediaPoolItem objects
        clips_to_unlink = []
        for clip_id in clip_ids:
            clip = get_media_pool_item_by_id(clip_id)
            if not clip:
                raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            clips_to_unlink.append(clip)
            
        # Unlink the clips
        if not clips_to_unlink:
            raise RuntimeError("No clips to unlink")
            
        result = media_pool.UnlinkClips(clips_to_unlink)
        if not result:
            raise RuntimeError("Failed to unlink clips")
            
        return {
            "success": True,
            "unlinked_count": len(clips_to_unlink)
        }
        
    return safe_api_call(
        _unlink_clips,
        "Error unlinking clips"
    )

def export_metadata(file_path: str, clip_ids: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Export metadata of clips to CSV format
    
    Args:
        file_path: Path to save the CSV file
        clip_ids: Optional list of clip IDs to export metadata for
                 If not provided, metadata for all clips in the media pool will be exported
        
    Returns:
        Dictionary with success status or error
    """
    def _export_metadata():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Normalize file path
        normalized_path = os.path.normpath(file_path)
        
        # Ensure the directory exists
        directory = os.path.dirname(normalized_path)
        if directory and not os.path.isdir(directory):
            raise RuntimeError(f"Directory does not exist: {directory}")
            
        # If clip IDs are provided, convert to MediaPoolItem objects
        clips = None
        if clip_ids:
            clips = []
            for clip_id in clip_ids:
                clip = get_media_pool_item_by_id(clip_id)
                if not clip:
                    raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
                clips.append(clip)
                
        # Export the metadata
        result = media_pool.ExportMetadata(normalized_path, clips)
        if not result:
            raise RuntimeError("Failed to export metadata")
            
        return {
            "success": True,
            "file_path": normalized_path,
            "clip_count": len(clips) if clips else "all"
        }
        
    return safe_api_call(
        _export_metadata,
        "Error exporting metadata"
    )

def get_unique_id() -> Dict[str, Any]:
    """
    Get a unique ID for the media pool
    
    Returns:
        Dictionary with the unique ID or error
    """
    def _get_unique_id():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Get the unique ID
        unique_id = media_pool.GetUniqueId()
        if not unique_id:
            raise RuntimeError("Failed to get unique ID for media pool")
            
        return {
            "success": True,
            "unique_id": unique_id
        }
        
    return safe_api_call(
        _get_unique_id,
        "Error getting unique ID for media pool"
    )

def create_stereo_clip(left_clip_id: str, right_clip_id: str) -> Dict[str, Any]:
    """
    Creates a new 3D stereoscopic media pool entry from two existing media pool items
    
    Args:
        left_clip_id: ID of the clip to use for the left eye
        right_clip_id: ID of the clip to use for the right eye
        
    Returns:
        Dictionary with the created stereo clip or error
    """
    def _create_stereo_clip():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the left and right clips
        left_clip = get_media_pool_item_by_id(left_clip_id)
        if not left_clip:
            raise RuntimeError(f"Failed to find left clip with ID: {left_clip_id}")
            
        right_clip = get_media_pool_item_by_id(right_clip_id)
        if not right_clip:
            raise RuntimeError(f"Failed to find right clip with ID: {right_clip_id}")
            
        # Create the stereo clip
        stereo_clip = media_pool.CreateStereoClip(left_clip, right_clip)
        if not stereo_clip:
            raise RuntimeError("Failed to create stereo clip")
            
        return {
            "success": True,
            "stereo_clip_name": stereo_clip.GetName(),
            "stereo_clip_id": stereo_clip.GetUniqueId() if hasattr(stereo_clip, "GetUniqueId") else "unknown",
            "left_clip_name": left_clip.GetName(),
            "right_clip_name": right_clip.GetName()
        }
        
    return safe_api_call(
        _create_stereo_clip,
        "Error creating stereo clip"
    )

def auto_sync_audio(clip_ids: List[str], audio_sync_settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Syncs audio for specified media pool items
    
    Args:
        clip_ids: List of clip IDs to sync audio for (minimum 2 clips, at least one video and one audio)
        audio_sync_settings: Optional dictionary with audio sync settings
                            Valid keys include:
                            - timecodeAccuracy: accuracy in frames (default: 1)
                            - audioSyncAccuracy: options include "frame", "sample", "10ms", and "sub-sample" (default: "frame")
                            - handleLength: handle length in frames (default: 0)
                            - appendSyncedAudio: whether to append the synced audio (default: False)
    
    Returns:
        Dictionary with success status or error
    """
    def _auto_sync_audio():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Convert clip IDs to MediaPoolItem objects
        clips_to_sync = []
        for clip_id in clip_ids:
            clip = get_media_pool_item_by_id(clip_id)
            if not clip:
                raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            clips_to_sync.append(clip)
            
        # Check if we have at least 2 clips
        if len(clips_to_sync) < 2:
            raise RuntimeError("Need at least 2 clips for audio syncing (at least one video and one audio clip)")
        
        # Set default settings if none provided
        settings = audio_sync_settings or {}
        
        # Auto sync the audio
        result = media_pool.AutoSyncAudio(clips_to_sync, settings)
        if not result:
            raise RuntimeError("Failed to auto sync audio")
            
        return {
            "success": True,
            "synced_count": len(clips_to_sync),
            "settings_used": settings
        }
        
    return safe_api_call(
        _auto_sync_audio,
        "Error syncing audio"
    )

def get_selected_clips() -> Dict[str, Any]:
    """
    Get the currently selected clips in the media pool
    
    Returns:
        Dictionary with selected clips or error
    """
    def _get_selected_clips():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Get the selected clips
        selected_clips = media_pool.GetSelectedClips()
        if selected_clips is None:  # Check if None specifically, empty list is valid
            raise RuntimeError("Failed to get selected clips")
            
        # Convert clips to serializable format
        clip_info = []
        for clip in selected_clips:
            if clip:
                clip_info.append({
                    "name": clip.GetName(),
                    "id": clip.GetUniqueId() if hasattr(clip, "GetUniqueId") else "unknown",
                    "type": clip.GetClipProperty("Type") if hasattr(clip, "GetClipProperty") else "unknown"
                })
                
        return {
            "success": True,
            "selected_count": len(clip_info),
            "clips": clip_info
        }
        
    return safe_api_call(
        _get_selected_clips,
        "Error getting selected clips"
    )

def set_selected_clip(clip_id: str) -> Dict[str, Any]:
    """
    Set a clip as selected in the media pool
    
    Args:
        clip_id: ID of the clip to select
        
    Returns:
        Dictionary with success status or error
    """
    def _set_selected_clip():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Find the clip
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Set the clip as selected
        result = media_pool.SetSelectedClip(clip)
        if not result:
            raise RuntimeError("Failed to set selected clip")
            
        return {
            "success": True,
            "clip_name": clip.GetName(),
            "clip_id": clip_id
        }
        
    return safe_api_call(
        _set_selected_clip,
        f"Error setting clip with ID: {clip_id} as selected"
    )

def import_folder_from_file(file_path: str, source_clips_path: str = "") -> Dict[str, Any]:
    """
    Import a folder from a DRB file
    
    Args:
        file_path: Path to the DRB file to import
        source_clips_path: Optional path to search for source clips if they're not in their original location
        
    Returns:
        Dictionary with success status or error
    """
    def _import_folder_from_file():
        # Get the media pool
        media_pool = get_media_pool()
        if not media_pool:
            raise RuntimeError("Failed to get media pool")
            
        # Normalize the file path
        normalized_path = os.path.normpath(file_path)
        
        # Check if the file exists
        if not os.path.isfile(normalized_path):
            raise RuntimeError(f"File does not exist: {normalized_path}")
            
        # Check if the file is a DRB file
        if not normalized_path.lower().endswith('.drb'):
            raise RuntimeError(f"File is not a DRB file: {normalized_path}")
            
        # Normalize the source clips path if provided
        normalized_source_clips_path = ""
        if source_clips_path:
            normalized_source_clips_path = os.path.normpath(source_clips_path)
            
            # Check if the directory exists
            if not os.path.isdir(normalized_source_clips_path):
                raise RuntimeError(f"Source clips path does not exist or is not a directory: {normalized_source_clips_path}")
        
        # Import the folder
        result = media_pool.ImportFolderFromFile(normalized_path, normalized_source_clips_path)
        if not result:
            raise RuntimeError(f"Failed to import folder from file: {normalized_path}")
            
        return {
            "success": True,
            "file_path": normalized_path,
            "source_clips_path": normalized_source_clips_path if normalized_source_clips_path else "Not specified"
        }
        
    return safe_api_call(
        _import_folder_from_file,
        f"Error importing folder from file: {file_path}"
    ) 