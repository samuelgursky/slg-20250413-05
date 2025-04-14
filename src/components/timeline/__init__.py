"""
Timeline Component for DaVinci Resolve API
Handles timeline-related operations
"""

import logging
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.timeline")

def get_current_timeline_helper():
    """Helper function to get the current timeline from the current project."""
    project = get_current_project()
    if not project:
        logger.error("No project is currently open")
        return None
    
    timeline = project.GetCurrentTimeline()
    if not timeline:
        logger.error("No timeline is currently open")
        return None
    
    return timeline

def get_timeline_details() -> Dict[str, Any]:
    """
    Get details about the current timeline
    
    Returns:
        Dictionary with timeline details or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        timeline = project.GetCurrentTimeline()
        if not timeline:
            return {"success": False, "error": "No timeline is currently open"}
            
        return {
            "success": True,
            "result": {
                "name": timeline.GetName(),
                "track_count": {
                    "video": timeline.GetTrackCount("video"),
                    "audio": timeline.GetTrackCount("audio"),
                    "subtitle": timeline.GetTrackCount("subtitle"),
                },
                "start_frame": timeline.GetStartFrame(),
                "end_frame": timeline.GetEndFrame(),
                "duration_frames": timeline.GetEndFrame() - timeline.GetStartFrame() + 1,
                "timecode": timeline.GetCurrentTimecode()
            }
        }
    except Exception as e:
        logger.error(f"Error getting timeline details: {str(e)}")
        return {"success": False, "error": str(e)}

def get_timeline_tracks() -> Dict[str, Any]:
    """
    Get details about all tracks in the current timeline
    
    Returns:
        Dictionary with track details or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        timeline = project.GetCurrentTimeline()
        if not timeline:
            return {"success": False, "error": "No timeline is currently open"}
        
        track_types = ["video", "audio", "subtitle"]
        tracks = {}
        
        for track_type in track_types:
            track_count = timeline.GetTrackCount(track_type)
            track_list = []
            
            for i in range(1, track_count + 1):
                # Try to get track-specific properties depending on type
                track_info = {
                    "index": i,
                    "name": f"{track_type.capitalize()} {i}",  # Default name if not available
                    "enabled": timeline.GetIsTrackEnabled(track_type, i)
                }
                
                # Add track specific info
                if track_type == "video":
                    track_info["items_count"] = len(timeline.GetItemListInTrack(track_type, i))
                elif track_type == "audio":
                    track_info["items_count"] = len(timeline.GetItemListInTrack(track_type, i))
                
                track_list.append(track_info)
                
            tracks[track_type] = {
                "count": track_count,
                "tracks": track_list
            }
            
        return {
            "success": True,
            "result": tracks
        }
    except Exception as e:
        logger.error(f"Error getting timeline tracks: {str(e)}")
        return {"success": False, "error": str(e)}

def get_timeline_items() -> Dict[str, Any]:
    """
    Get details about items in the current timeline
    
    This function includes a retry mechanism to handle the known issue with 
    'NoneType' object is not callable error from the Resolve API. It will attempt
    to refresh the timeline state before retrying.
    
    Returns:
        Dictionary with timeline items or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    # Maximum number of retry attempts
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            timeline = project.GetCurrentTimeline()
            if not timeline:
                return {"success": False, "error": "No timeline is currently open"}
            
            # Get all video items from all video tracks
            video_track_count = timeline.GetTrackCount("video")
            video_items = []
            
            for i in range(1, video_track_count + 1):
                try:
                    track_items = timeline.GetItemListInTrack("video", i)
                    
                    if track_items:
                        for item in track_items:
                            try:
                                video_items.append({
                                    "name": item.GetName(),
                                    "track": i,
                                    "start_frame": item.GetStart(),
                                    "end_frame": item.GetEnd(),
                                    "duration": item.GetDuration(),
                                    "type": item.GetType(),
                                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                                })
                            except Exception as e:
                                logger.warning(f"Error processing video item on track {i}: {str(e)}")
                except TypeError as e:
                    if "'NoneType' object is not callable" in str(e):
                        logger.warning(f"Encountered NoneType error on video track {i}, retrying...")
                        # Increment retry counter and try again
                        retry_count += 1
                        
                        # If we have more retries left, try to refresh timeline state
                        if retry_count < max_retries:
                            import time
                            time.sleep(0.5)  # Short delay before retrying
                            
                            # Try to refresh timeline state
                            current_timecode = timeline.GetCurrentTimecode()
                            timeline.SetCurrentTimecode(current_timecode)
                            
                            break  # Break the track loop to restart the whole process
                        else:
                            # If we've exceeded retries, return partial results with warning
                            return {
                                "success": True,
                                "warning": "Some timeline items couldn't be retrieved due to API limitations",
                                "result": {
                                    "video_items": video_items,
                                    "audio_items": [],  # Return empty for audio since we couldn't complete
                                    "partial_results": True
                                }
                            }
                    else:
                        # Re-raise other TypeError exceptions
                        raise
            
            # If we broke out of the loop due to retry, continue to next iteration
            if retry_count < max_retries and retry_count > 0:
                continue
                
            # Get all audio items from all audio tracks
            audio_track_count = timeline.GetTrackCount("audio")
            audio_items = []
            
            for i in range(1, audio_track_count + 1):
                try:
                    track_items = timeline.GetItemListInTrack("audio", i)
                    
                    if track_items:
                        for item in track_items:
                            try:
                                audio_items.append({
                                    "name": item.GetName(),
                                    "track": i,
                                    "start_frame": item.GetStart(),
                                    "end_frame": item.GetEnd(),
                                    "duration": item.GetDuration(),
                                    "type": item.GetType(),
                                    "id": item.GetUniqueId() if hasattr(item, "GetUniqueId") else "unknown"
                                })
                            except Exception as e:
                                logger.warning(f"Error processing audio item on track {i}: {str(e)}")
                except TypeError as e:
                    if "'NoneType' object is not callable" in str(e):
                        logger.warning(f"Encountered NoneType error on audio track {i}, retrying...")
                        retry_count += 1
                        
                        if retry_count < max_retries:
                            import time
                            time.sleep(0.5)  # Short delay before retrying
                            
                            # Try to refresh timeline state
                            current_timecode = timeline.GetCurrentTimecode()
                            timeline.SetCurrentTimecode(current_timecode)
                            
                            # Start over from video tracks
                            break
                        else:
                            # If we've exceeded retries, return partial results with warning
                            return {
                                "success": True,
                                "warning": "Some timeline items couldn't be retrieved due to API limitations",
                                "result": {
                                    "video_items": video_items,
                                    "audio_items": audio_items,
                                    "partial_results": True
                                }
                            }
                    else:
                        # Re-raise other TypeError exceptions
                        raise
                        
            # If we broke out of the loop due to retry, continue to next iteration
            if retry_count < max_retries and retry_count > 0:
                continue
                
            # If we get here, we've successfully retrieved all items
            return {
                "success": True,
                "result": {
                    "video_items": video_items,
                    "audio_items": audio_items
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting timeline items (attempt {retry_count + 1}): {str(e)}")
            retry_count += 1
            
            if retry_count >= max_retries:
                return {"success": False, "error": f"Failed to get timeline items after {max_retries} attempts: {str(e)}"}
            
            # Wait before retrying
            import time
            time.sleep(0.5)
    
    # Shouldn't reach here, but just in case
    return {"success": False, "error": "Failed to retrieve timeline items due to unexpected error"}

def add_track(track_type: str) -> Dict[str, Any]:
    """Add a track to the current timeline.
    
    Args:
        track_type: Type of track to add ('video', 'audio', or 'subtitle')
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_add_track(track_type)
        ),
        "Error adding track"
    )

def helper_add_track(track_type: str) -> Dict[str, Any]:
    """Helper function to add a track to the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    # Add the track
    result = timeline.AddTrack(track_type.lower())
    
    if not result:
        return {"success": False, "error": f"Failed to add {track_type} track"}
    
    return {"success": True, "result": {"added": True, "track_type": track_type}}

def delete_track(track_type: str, track_index: int) -> Dict[str, Any]:
    """Delete a track from the current timeline.
    
    Args:
        track_type: Type of track to delete ('video', 'audio', or 'subtitle')
        track_index: Index of the track to delete (1-based index)
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_track(track_type, track_index)
        ),
        "Error deleting track"
    )

def helper_delete_track(track_type: str, track_index: int) -> Dict[str, Any]:
    """Helper function to delete a track from the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    if track_index < 1:
        return {"success": False, "error": "Track index must be a positive integer (1-based index)"}
    
    # Delete the track
    result = timeline.DeleteTrack(track_type.lower(), track_index)
    
    if not result:
        return {"success": False, "error": f"Failed to delete {track_type} track at index {track_index}"}
    
    return {"success": True, "result": {"deleted": True, "track_type": track_type, "track_index": track_index}}

def delete_timeline_clips(clip_ids: List[str]) -> Dict[str, Any]:
    """Delete clips from the current timeline.
    
    Args:
        clip_ids: List of timeline clip IDs to delete
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_timeline_clips(clip_ids)
        ),
        "Error deleting timeline clips"
    )

def helper_delete_timeline_clips(clip_ids: List[str]) -> Dict[str, Any]:
    """Helper function to delete clips from the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not clip_ids or not isinstance(clip_ids, list):
        return {"success": False, "error": "clip_ids must be a non-empty list of clip IDs"}
    
    # Delete the clips
    result = timeline.DeleteClips(clip_ids)
    
    if not result:
        return {"success": False, "error": "Failed to delete clips from timeline"}
    
    return {"success": True, "result": {"deleted": True, "clip_count": len(clip_ids)}}

def set_current_timecode(timecode: str) -> Dict[str, Any]:
    """Set the current timecode for the timeline.
    
    Args:
        timecode: Timecode string to set (format: HH:MM:SS:FF)
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_current_timecode(timecode)
        ),
        "Error setting current timecode"
    )

def helper_set_current_timecode(timecode: str) -> Dict[str, Any]:
    """Helper function to set the current timecode for the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Validate timecode format
    import re
    if not re.match(r'^\d{2}:\d{2}:\d{2}:\d{2}$', timecode):
        return {"success": False, "error": "Invalid timecode format. Expected format: HH:MM:SS:FF"}
    
    # Set the timecode
    result = timeline.SetCurrentTimecode(timecode)
    
    if not result:
        return {"success": False, "error": f"Failed to set timecode to {timecode}"}
    
    return {"success": True, "result": {"set": True, "timecode": timecode}}

def set_track_enable(track_type: str, track_index: int, enable: bool) -> Dict[str, Any]:
    """Enable or disable a track in the current timeline.
    
    Args:
        track_type: Type of track ('video', 'audio', or 'subtitle')
        track_index: Index of the track (1-based index)
        enable: True to enable the track, False to disable
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_track_enable(track_type, track_index, enable)
        ),
        "Error setting track enable state"
    )

def helper_set_track_enable(track_type: str, track_index: int, enable: bool) -> Dict[str, Any]:
    """Helper function to enable or disable a track."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    if track_index < 1:
        return {"success": False, "error": "Track index must be a positive integer (1-based index)"}
    
    # Try to get track count
    track_count = timeline.GetTrackCount(track_type.lower())
    if track_index > track_count:
        return {"success": False, "error": f"Track index {track_index} is out of range (max: {track_count})"}
    
    # Set track enable/disable
    result = timeline.SetTrackEnable(track_type.lower(), track_index, enable)
    
    if not result:
        return {"success": False, "error": f"Failed to {'enable' if enable else 'disable'} {track_type} track at index {track_index}"}
    
    return {
        "success": True, 
        "result": {
            "track_type": track_type,
            "track_index": track_index,
            "enabled": enable
        }
    }

def set_track_lock(track_type: str, track_index: int, lock: bool) -> Dict[str, Any]:
    """Lock or unlock a track in the current timeline.
    
    Args:
        track_type: Type of track ('video', 'audio', or 'subtitle')
        track_index: Index of the track (1-based index)
        lock: True to lock the track, False to unlock
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_track_lock(track_type, track_index, lock)
        ),
        "Error setting track lock state"
    )

def helper_set_track_lock(track_type: str, track_index: int, lock: bool) -> Dict[str, Any]:
    """Helper function to lock or unlock a track."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    if track_index < 1:
        return {"success": False, "error": "Track index must be a positive integer (1-based index)"}
    
    # Try to get track count
    track_count = timeline.GetTrackCount(track_type.lower())
    if track_index > track_count:
        return {"success": False, "error": f"Track index {track_index} is out of range (max: {track_count})"}
    
    # Set track lock/unlock
    result = timeline.SetTrackLock(track_type.lower(), track_index, lock)
    
    if not result:
        return {"success": False, "error": f"Failed to {'lock' if lock else 'unlock'} {track_type} track at index {track_index}"}
    
    return {
        "success": True, 
        "result": {
            "track_type": track_type,
            "track_index": track_index,
            "locked": lock
        }
    }

def add_marker(frame_id: float, color: str, name: str, note: str, duration: float, custom_data: str = "") -> Dict[str, Any]:
    """Add a marker to the current timeline.
    
    Args:
        frame_id: Frame position for the marker
        color: Color name for the marker
        name: Name of the marker
        note: Note text for the marker
        duration: Duration of the marker in frames
        custom_data: Optional custom data to attach to the marker
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_add_marker(frame_id, color, name, note, duration, custom_data)
        ),
        "Error adding marker to timeline"
    )

def helper_add_marker(frame_id: float, color: str, name: str, note: str, duration: float, custom_data: str = "") -> Dict[str, Any]:
    """Helper function to add a marker to the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Validate marker color
    valid_colors = ["blue", "cyan", "green", "yellow", "red", "pink", "purple", "fuchsia", "rose", "lavender", "sky", "mint", "lemon", "sand", "cocoa", "cream"]
    if color.lower() not in valid_colors:
        return {"success": False, "error": f"Invalid marker color: {color}. Must be one of {', '.join(valid_colors)}"}
    
    # Add the marker
    result = timeline.AddMarker(frame_id, color, name, note, duration, custom_data)
    
    if not result:
        return {"success": False, "error": f"Failed to add marker at frame {frame_id}"}
    
    return {
        "success": True, 
        "result": {
            "added": True,
            "frame_id": frame_id,
            "color": color,
            "name": name,
            "note": note,
            "duration": duration,
            "custom_data": custom_data
        }
    }

def get_markers() -> Dict[str, Any]:
    """Get all markers from the current timeline.
    
    Returns:
        Dictionary with success status and markers
    """
    return safe_api_call(
        lambda: (
            helper_get_markers()
        ),
        "Error getting timeline markers"
    )

def helper_get_markers() -> Dict[str, Any]:
    """Helper function to get all markers from the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Get the markers
    markers = timeline.GetMarkers()
    
    # Convert to serializable format
    serialized_markers = {}
    for frame_id, marker_info in markers.items():
        serialized_markers[str(frame_id)] = {
            "color": marker_info.get("color", ""),
            "name": marker_info.get("name", ""),
            "note": marker_info.get("note", ""),
            "duration": marker_info.get("duration", 0),
            "custom_data": marker_info.get("customData", "")
        }
    
    return {
        "success": True, 
        "result": {
            "markers": serialized_markers,
            "count": len(serialized_markers)
        }
    }

def get_marker_by_custom_data(custom_data: str) -> Dict[str, Any]:
    """Get a marker by its custom data.
    
    Args:
        custom_data: Custom data string to search for
        
    Returns:
        Dictionary with success status and marker info if found
    """
    return safe_api_call(
        lambda: (
            helper_get_marker_by_custom_data(custom_data)
        ),
        "Error getting marker by custom data"
    )

def helper_get_marker_by_custom_data(custom_data: str) -> Dict[str, Any]:
    """Helper function to get a marker by its custom data."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Get the marker
    marker_info = timeline.GetMarkerByCustomData(custom_data)
    
    if not marker_info:
        return {"success": False, "error": f"No marker found with custom data: {custom_data}"}
    
    # Convert to serializable format
    serialized_marker = {
        "color": marker_info.get("color", ""),
        "name": marker_info.get("name", ""),
        "note": marker_info.get("note", ""),
        "duration": marker_info.get("duration", 0),
        "custom_data": marker_info.get("customData", "")
    }
    
    return {
        "success": True, 
        "result": serialized_marker
    }

def update_marker_custom_data(frame_id: float, custom_data: str) -> Dict[str, Any]:
    """Update custom data for a marker at a specific frame.
    
    Args:
        frame_id: Frame position of the marker
        custom_data: New custom data to set
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_update_marker_custom_data(frame_id, custom_data)
        ),
        "Error updating marker custom data"
    )

def helper_update_marker_custom_data(frame_id: float, custom_data: str) -> Dict[str, Any]:
    """Helper function to update custom data for a marker."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Update the marker
    result = timeline.UpdateMarkerCustomData(frame_id, custom_data)
    
    if not result:
        return {"success": False, "error": f"Failed to update marker at frame {frame_id}"}
    
    return {
        "success": True, 
        "result": {
            "updated": True,
            "frame_id": frame_id,
            "custom_data": custom_data
        }
    }

def get_marker_custom_data(frame_id: float) -> Dict[str, Any]:
    """Get custom data for a marker at a specific frame.
    
    Args:
        frame_id: Frame position of the marker
        
    Returns:
        Dictionary with success status and custom data
    """
    return safe_api_call(
        lambda: (
            helper_get_marker_custom_data(frame_id)
        ),
        "Error getting marker custom data"
    )

def helper_get_marker_custom_data(frame_id: float) -> Dict[str, Any]:
    """Helper function to get custom data for a marker."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Get the marker custom data
    custom_data = timeline.GetMarkerCustomData(frame_id)
    
    if custom_data is None:
        return {"success": False, "error": f"No marker found at frame {frame_id}"}
    
    return {
        "success": True, 
        "result": {
            "frame_id": frame_id,
            "custom_data": custom_data
        }
    }

def delete_markers_by_color(color: str) -> Dict[str, Any]:
    """Delete all markers of a specific color from the timeline.
    
    Args:
        color: Color of markers to delete, or 'All' to delete all markers
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_markers_by_color(color)
        ),
        "Error deleting markers by color"
    )

def helper_delete_markers_by_color(color: str) -> Dict[str, Any]:
    """Helper function to delete markers by color."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Validate marker color
    valid_colors = ["blue", "cyan", "green", "yellow", "red", "pink", "purple", "fuchsia", 
                    "rose", "lavender", "sky", "mint", "lemon", "sand", "cocoa", "cream", "all"]
    if color.lower() not in valid_colors:
        return {"success": False, "error": f"Invalid marker color: {color}. Must be one of {', '.join(valid_colors)}"}
    
    # Delete the markers
    result = timeline.DeleteMarkersByColor(color if color.lower() != "all" else "All")
    
    if not result:
        return {"success": False, "error": f"Failed to delete {color} markers"}
    
    return {
        "success": True, 
        "result": {
            "deleted": True,
            "color": color
        }
    }

def delete_marker_at_frame(frame_num: float) -> Dict[str, Any]:
    """Delete a marker at a specific frame.
    
    Args:
        frame_num: Frame number where the marker is located
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_marker_at_frame(frame_num)
        ),
        "Error deleting marker at frame"
    )

def helper_delete_marker_at_frame(frame_num: float) -> Dict[str, Any]:
    """Helper function to delete a marker at a specific frame."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Delete the marker
    result = timeline.DeleteMarkerAtFrame(frame_num)
    
    if not result:
        return {"success": False, "error": f"Failed to delete marker at frame {frame_num}"}
    
    return {
        "success": True, 
        "result": {
            "deleted": True,
            "frame_num": frame_num
        }
    }

def delete_marker_by_custom_data(custom_data: str) -> Dict[str, Any]:
    """Delete a marker by its custom data.
    
    Args:
        custom_data: Custom data string to search for
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_delete_marker_by_custom_data(custom_data)
        ),
        "Error deleting marker by custom data"
    )

def helper_delete_marker_by_custom_data(custom_data: str) -> Dict[str, Any]:
    """Helper function to delete a marker by its custom data."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Delete the marker
    result = timeline.DeleteMarkerByCustomData(custom_data)
    
    if not result:
        return {"success": False, "error": f"Failed to delete marker with custom data: {custom_data}"}
    
    return {
        "success": True, 
        "result": {
            "deleted": True,
            "custom_data": custom_data
        }
    }

def set_name(timeline_name: str) -> Dict[str, Any]:
    """Set the name of the current timeline.
    
    Args:
        timeline_name: New name for the timeline
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_name(timeline_name)
        ),
        "Error setting timeline name"
    )

def helper_set_name(timeline_name: str) -> Dict[str, Any]:
    """Helper function to set the name of the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not timeline_name or not isinstance(timeline_name, str):
        return {"success": False, "error": "Timeline name must be a non-empty string"}
    
    # Set the timeline name
    result = timeline.SetName(timeline_name)
    
    if not result:
        return {"success": False, "error": f"Failed to set timeline name to '{timeline_name}'. Name might be already in use."}
    
    return {
        "success": True, 
        "result": {
            "name": timeline_name
        }
    }

def get_track_name(track_type: str, track_index: int) -> Dict[str, Any]:
    """Get the name of a track in the current timeline.
    
    Args:
        track_type: Type of track ('video', 'audio', or 'subtitle')
        track_index: Index of the track (1-based index)
        
    Returns:
        Dictionary with success status and track name
    """
    return safe_api_call(
        lambda: (
            helper_get_track_name(track_type, track_index)
        ),
        "Error getting track name"
    )

def helper_get_track_name(track_type: str, track_index: int) -> Dict[str, Any]:
    """Helper function to get the name of a track."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    if track_index < 1:
        return {"success": False, "error": "Track index must be a positive integer (1-based index)"}
    
    # Try to get track count
    track_count = timeline.GetTrackCount(track_type.lower())
    if track_index > track_count:
        return {"success": False, "error": f"Track index {track_index} is out of range (max: {track_count})"}
    
    # Get the track name
    track_name = timeline.GetTrackName(track_type.lower(), track_index)
    
    return {
        "success": True, 
        "result": {
            "track_type": track_type,
            "track_index": track_index,
            "name": track_name
        }
    }

def set_track_name(track_type: str, track_index: int, name: str) -> Dict[str, Any]:
    """Set the name of a track in the current timeline.
    
    Args:
        track_type: Type of track ('video', 'audio', or 'subtitle')
        track_index: Index of the track (1-based index)
        name: New name for the track
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_track_name(track_type, track_index, name)
        ),
        "Error setting track name"
    )

def helper_set_track_name(track_type: str, track_index: int, name: str) -> Dict[str, Any]:
    """Helper function to set the name of a track."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if track_type.lower() not in ['video', 'audio', 'subtitle']:
        return {"success": False, "error": f"Invalid track type: {track_type}. Must be 'video', 'audio', or 'subtitle'"}
    
    if track_index < 1:
        return {"success": False, "error": "Track index must be a positive integer (1-based index)"}
    
    # Try to get track count
    track_count = timeline.GetTrackCount(track_type.lower())
    if track_index > track_count:
        return {"success": False, "error": f"Track index {track_index} is out of range (max: {track_count})"}
    
    # Set the track name
    result = timeline.SetTrackName(track_type.lower(), track_index, name)
    
    if not result:
        return {"success": False, "error": f"Failed to set track name to '{name}'"}
    
    return {
        "success": True, 
        "result": {
            "track_type": track_type,
            "track_index": track_index,
            "name": name
        }
    }

def create_compound_clip(timeline_items: List[str], clip_info: Dict[str, str] = None) -> Dict[str, Any]:
    """Create a compound clip from timeline items.
    
    Args:
        timeline_items: List of timeline item IDs to include in the compound clip
        clip_info: Optional dictionary with clip info (keys: 'startTimecode', 'name')
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_create_compound_clip(timeline_items, clip_info)
        ),
        "Error creating compound clip"
    )

def helper_create_compound_clip(timeline_items: List[str], clip_info: Dict[str, str] = None) -> Dict[str, Any]:
    """Helper function to create a compound clip."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not timeline_items or not isinstance(timeline_items, list):
        return {"success": False, "error": "timeline_items must be a non-empty list of timeline item IDs"}
    
    # Validate and prepare clip_info
    if clip_info is None:
        clip_info = {}
    
    # Get timeline items
    items = []
    for item_id in timeline_items:
        # Use the resolve_api utility to find timeline item by ID
        from ...resolve_api import get_timeline_item_by_id
        item = get_timeline_item_by_id(item_id)
        if not item:
            return {"success": False, "error": f"Timeline item with ID '{item_id}' not found"}
        items.append(item)
    
    # Create the compound clip
    result = timeline.CreateCompoundClip(items, clip_info)
    
    if not result:
        return {"success": False, "error": "Failed to create compound clip"}
    
    # Extract information about the created timeline item
    item_info = {
        "name": result.GetName() if hasattr(result, "GetName") else "Unknown",
        "id": result.GetUniqueId() if hasattr(result, "GetUniqueId") else "Unknown",
        "start_frame": result.GetStart() if hasattr(result, "GetStart") else 0,
        "end_frame": result.GetEnd() if hasattr(result, "GetEnd") else 0,
        "duration": result.GetDuration() if hasattr(result, "GetDuration") else 0
    }
    
    return {
        "success": True, 
        "result": {
            "created": True,
            "item": item_info
        }
    }

def get_current_timecode() -> Dict[str, Any]:
    """
    Get the current timecode of the timeline.
    
    Returns:
        Dictionary with current timecode or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.GetCurrentTimecode(),
        "Failed to get current timecode"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "timecode": result["result"]
    }

def duplicate_timeline(timeline_name: str = None) -> Dict[str, Any]:
    """
    Duplicates the current timeline and returns the created timeline.
    
    Args:
        timeline_name: Optional name for the duplicated timeline
        
    Returns:
        Dictionary with success status and duplicated timeline information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    # Call the duplicate timeline function
    args = []
    if timeline_name:
        args.append(timeline_name)
    
    result = safe_api_call(
        lambda: timeline.DuplicateTimeline(*args),
        "Failed to duplicate timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": "Failed to duplicate timeline"}
    
    # Get information about the duplicated timeline
    duplicated_timeline = result["result"]
    timeline_info = {
        "name": duplicated_timeline.GetName() if hasattr(duplicated_timeline, "GetName") else "Unknown",
        "start_frame": duplicated_timeline.GetStartFrame() if hasattr(duplicated_timeline, "GetStartFrame") else 0,
        "end_frame": duplicated_timeline.GetEndFrame() if hasattr(duplicated_timeline, "GetEndFrame") else 0,
        "start_timecode": duplicated_timeline.GetStartTimecode() if hasattr(duplicated_timeline, "GetStartTimecode") else "00:00:00:00"
    }
    
    return {
        "success": True,
        "timeline": timeline_info
    }

def export_timeline(file_path: str, export_type: str, export_subtype: str = None) -> Dict[str, Any]:
    """
    Exports the current timeline to a file in the specified format.
    
    Args:
        file_path: Path where the exported file will be saved
        export_type: Type of export (AAF, EDL, XML, etc.)
        export_subtype: Subtype of export (optional, used for certain export types)
        
    Returns:
        Dictionary with success status or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    # Validate export type
    valid_export_types = [
        "AAF", "DRT", "EDL", "FCP7XML", "FCPXML_1_8", "FCPXML_1_9", 
        "FCPXML_1_10", "HDR10_PROFILE_A", "HDR10_PROFILE_B", "CSV", 
        "TAB", "DOLBY_VISION_VER_2_9", "DOLBY_VISION_VER_4_0",
        "DOLBY_VISION_VER_5_1", "OTIO", "ALE", "ALE_CDL"
    ]
    
    if export_type.upper() not in valid_export_types:
        return {"success": False, "error": f"Invalid export type. Must be one of: {', '.join(valid_export_types)}"}
    
    # Handle subtypes for specific export types
    args = [file_path, export_type]
    if export_subtype:
        # Validate export subtype based on export type
        if export_type.upper() == "AAF" and export_subtype.upper() not in ["NEW", "EXISTING"]:
            return {"success": False, "error": "For AAF export, subtype must be either 'NEW' or 'EXISTING'"}
        if export_type.upper() == "EDL" and export_subtype.upper() not in ["CDL", "SDL", "MISSING_CLIPS", "NONE"]:
            return {"success": False, "error": "For EDL export, subtype must be one of: 'CDL', 'SDL', 'MISSING_CLIPS', 'NONE'"}
        
        args.append(export_subtype)
    
    result = safe_api_call(
        lambda: timeline.Export(*args),
        f"Failed to export timeline to {file_path}"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error")
    }

def get_timeline_setting(setting_name: str = None) -> Dict[str, Any]:
    """
    Get the value of a timeline setting, or all settings if no name is provided.
    
    Args:
        setting_name: Optional name of the setting to retrieve
        
    Returns:
        Dictionary with success status and setting value(s) or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    if setting_name:
        result = safe_api_call(
            lambda: timeline.GetSetting(setting_name),
            f"Failed to get timeline setting '{setting_name}'"
        )
        
        if not result["success"]:
            return result
        
        return {
            "success": True,
            "setting": {setting_name: result["result"]}
        }
    else:
        # Get all settings
        result = safe_api_call(
            lambda: timeline.GetSetting(),
            "Failed to get all timeline settings"
        )
        
        if not result["success"]:
            return result
        
        return {
            "success": True,
            "settings": result["result"]
        }

def set_timeline_setting(setting_name: str, setting_value: str) -> Dict[str, Any]:
    """
    Set the value of a timeline setting.
    
    Args:
        setting_name: Name of the setting to set
        setting_value: Value to set for the setting
        
    Returns:
        Dictionary with success status or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    if not setting_name:
        return {"success": False, "error": "Setting name must be provided"}
    
    result = safe_api_call(
        lambda: timeline.SetSetting(setting_name, setting_value),
        f"Failed to set timeline setting '{setting_name}' to '{setting_value}'"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error")
    }

def insert_generator_into_timeline(generator_name: str) -> Dict[str, Any]:
    """
    Inserts a generator into the current timeline.
    
    Args:
        generator_name: Name of the generator to insert
        
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertGeneratorIntoTimeline(generator_name),
        f"Failed to insert generator '{generator_name}' into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Failed to insert generator '{generator_name}' into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def insert_fusion_generator_into_timeline(generator_name: str) -> Dict[str, Any]:
    """
    Inserts a Fusion generator into the current timeline.
    
    Args:
        generator_name: Name of the Fusion generator to insert
        
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertFusionGeneratorIntoTimeline(generator_name),
        f"Failed to insert Fusion generator '{generator_name}' into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Failed to insert Fusion generator '{generator_name}' into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def insert_fusion_composition_into_timeline() -> Dict[str, Any]:
    """
    Inserts a Fusion composition into the current timeline.
    
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertFusionCompositionIntoTimeline(),
        "Failed to insert Fusion composition into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": "Failed to insert Fusion composition into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def insert_ofx_generator_into_timeline(generator_name: str) -> Dict[str, Any]:
    """
    Inserts an OFX generator into the current timeline.
    
    Args:
        generator_name: Name of the OFX generator to insert
        
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertOFXGeneratorIntoTimeline(generator_name),
        f"Failed to insert OFX generator '{generator_name}' into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Failed to insert OFX generator '{generator_name}' into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def insert_title_into_timeline(title_name: str) -> Dict[str, Any]:
    """
    Inserts a title into the current timeline.
    
    Args:
        title_name: Name of the title to insert
        
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertTitleIntoTimeline(title_name),
        f"Failed to insert title '{title_name}' into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Failed to insert title '{title_name}' into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def insert_fusion_title_into_timeline(title_name: str) -> Dict[str, Any]:
    """
    Inserts a Fusion title into the current timeline.
    
    Args:
        title_name: Name of the Fusion title to insert
        
    Returns:
        Dictionary with success status and inserted item information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.InsertFusionTitleIntoTimeline(title_name),
        f"Failed to insert Fusion title '{title_name}' into timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Failed to insert Fusion title '{title_name}' into timeline"}
    
    # Get information about the inserted item
    timeline_item = result["result"]
    item_info = {
        "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
        "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
        "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
        "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0
    }
    
    return {
        "success": True,
        "timeline_item": item_info
    }

def get_current_video_item() -> Dict[str, Any]:
    """
    Gets the current video item at the playhead position.
    This is a workaround for the lack of a direct "get selected items" function.
    
    Returns:
        Dictionary with success status and item info or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.GetCurrentVideoItem(),
        "Failed to get current video item"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": "No video item found at current playhead position"}
    
    # Get information about the current video item
    timeline_item = result["result"]
    
    try:
        item_info = {
            "id": timeline_item.GetUniqueId() if hasattr(timeline_item, "GetUniqueId") else None,
            "name": timeline_item.GetName() if hasattr(timeline_item, "GetName") else "Unknown",
            "start": timeline_item.GetStart() if hasattr(timeline_item, "GetStart") else 0,
            "end": timeline_item.GetEnd() if hasattr(timeline_item, "GetEnd") else 0,
            "duration": timeline_item.GetDuration() if hasattr(timeline_item, "GetDuration") else 0,
            "type": timeline_item.GetType() if hasattr(timeline_item, "GetType") else "Unknown"
        }
        
        return {
            "success": True,
            "result": item_info
        }
    except Exception as e:
        logger.error(f"Error extracting current video item properties: {str(e)}")
        return {"success": False, "error": f"Error getting current video item details: {str(e)}"}

def get_timeline_items_in_range(start_frame: int = None, end_frame: int = None) -> Dict[str, Any]:
    """
    Gets all timeline items that intersect with the specified frame range.
    This is a workaround for the lack of a direct "get selected items" function.
    
    If no frame range is specified, it will get all items in the timeline.
    
    Args:
        start_frame: Start frame of the range (inclusive)
        end_frame: End frame of the range (inclusive)
        
    Returns:
        Dictionary with success status and filtered items or error
    """
    # Get all timeline items first
    all_items_result = get_timeline_items()
    
    if not all_items_result["success"]:
        return all_items_result
    
    all_items = all_items_result["result"]
    video_items = all_items["video_items"]
    audio_items = all_items["audio_items"]
    
    # If no range specified, return all items
    if start_frame is None and end_frame is None:
        return all_items_result
    
    # Default values if only one bound is specified
    if start_frame is None:
        timeline = get_current_timeline_helper()
        if timeline:
            start_frame = timeline.GetStartFrame()
        else:
            start_frame = 0
            
    if end_frame is None:
        timeline = get_current_timeline_helper()
        if timeline:
            end_frame = timeline.GetEndFrame()
        else:
            end_frame = float('inf')
    
    # Filter items that intersect with the range
    filtered_video_items = []
    for item in video_items:
        item_start = item["start_frame"]
        item_end = item["end_frame"]
        
        # Check if the item intersects with the range
        if (item_start <= end_frame) and (item_end >= start_frame):
            filtered_video_items.append(item)
    
    filtered_audio_items = []
    for item in audio_items:
        item_start = item["start_frame"]
        item_end = item["end_frame"]
        
        # Check if the item intersects with the range
        if (item_start <= end_frame) and (item_end >= start_frame):
            filtered_audio_items.append(item)
    
    return {
        "success": True,
        "result": {
            "video_items": filtered_video_items,
            "audio_items": filtered_audio_items,
            "filter_applied": True,
            "filter_range": {
                "start_frame": start_frame,
                "end_frame": end_frame
            }
        }
    }

def grab_still() -> Dict[str, Any]:
    """
    Grabs a still from the current video clip in the timeline.
    
    Returns:
        Dictionary with success status and still information or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    result = safe_api_call(
        lambda: timeline.GrabStill(),
        "Failed to grab still from timeline"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": "Failed to grab still from timeline"}
    
    # Get information about the grabbed still
    gallery_still = result["result"]
    
    # Since GalleryStill doesn't have many accessible properties, we just return success
    return {
        "success": True,
        "message": "Successfully grabbed still from timeline"
    }

def grab_all_stills(still_frame_source: int) -> Dict[str, Any]:
    """
    Grabs stills from all clips in the timeline at the specified source frame.
    
    Args:
        still_frame_source: Source frame for stills (1 - First frame, 2 - Middle frame)
        
    Returns:
        Dictionary with success status and count of stills grabbed or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline is currently open"}
    
    # Validate still_frame_source
    if still_frame_source not in [1, 2]:
        return {"success": False, "error": "still_frame_source must be 1 (First frame) or 2 (Middle frame)"}
    
    result = safe_api_call(
        lambda: timeline.GrabAllStills(still_frame_source),
        "Failed to grab stills from all clips in timeline"
    )
    
    if not result["success"]:
        return result
    
    # Get the count of stills grabbed
    stills = result["result"] or []
    
    return {
        "success": True,
        "stills_count": len(stills),
        "message": f"Successfully grabbed {len(stills)} stills from timeline"
    }

def set_start_timecode(timecode: str) -> Dict[str, Any]:
    """Set the start timecode of the current timeline.
    
    Args:
        timecode: The timecode to set as the start timecode of the timeline (format: "HH:MM:SS:FF")
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_start_timecode(timecode)
        ),
        "Error setting start timecode"
    )

def helper_set_start_timecode(timecode: str) -> Dict[str, Any]:
    """Helper function to set the start timecode of the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Validate timecode format (simple check)
    import re
    if not re.match(r'^\d{2}:\d{2}:\d{2}:\d{2}$', timecode):
        return {"success": False, "error": f"Invalid timecode format: {timecode}. Expected format: 'HH:MM:SS:FF'"}
    
    # Set the start timecode
    result = timeline.SetStartTimecode(timecode)
    
    if not result:
        return {"success": False, "error": f"Failed to set start timecode to {timecode}"}
    
    return {"success": True, "result": {"timecode": timecode}}

def set_clips_linked(clip_ids: List[str], linked: bool) -> Dict[str, Any]:
    """Set clips to be linked or unlinked.
    
    Args:
        clip_ids: List of timeline item IDs to link/unlink
        linked: Whether to link (True) or unlink (False) the clips
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_set_clips_linked(clip_ids, linked)
        ),
        "Error setting clips linked state"
    )

def helper_set_clips_linked(clip_ids: List[str], linked: bool) -> Dict[str, Any]:
    """Helper function to set clips to be linked or unlinked."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not clip_ids or not isinstance(clip_ids, list):
        return {"success": False, "error": "clip_ids must be a non-empty list of timeline item IDs"}
    
    # Resolve API requires a list of TimelineItem objects, not IDs
    # We need to convert the IDs to TimelineItem objects
    timeline_items = []
    
    for clip_id in clip_ids:
        # Since we don't have a direct way to get TimelineItem by ID in this context,
        # we'll search through all tracks to find the item
        all_tracks = ["video", "audio", "subtitle"]
        item_found = False
        
        for track_type in all_tracks:
            track_count = timeline.GetTrackCount(track_type)
            
            for i in range(1, track_count + 1):
                items = timeline.GetItemListInTrack(track_type, i)
                
                for item in items:
                    # If we had a GetUniqueId method, we would compare with clip_id
                    # For now, we'll try to find it another way or report an error
                    try:
                        if str(item) == clip_id:  # This may not work depending on how items are represented
                            timeline_items.append(item)
                            item_found = True
                            break
                    except:
                        pass
    
    if not timeline_items:
        return {"success": False, "error": "Could not find any of the specified timeline items"}
    
    # Set clips linked status
    result = timeline.SetClipsLinked(timeline_items, linked)
    
    if not result:
        return {"success": False, "error": f"Failed to set clips linked state to {linked}"}
    
    return {
        "success": True, 
        "result": {
            "linked": linked, 
            "clips_count": len(timeline_items),
            "clips_found": len(timeline_items) == len(clip_ids)
        }
    }

def get_current_clip_thumbnail_image(width: int = 320, height: int = 180) -> Dict[str, Any]:
    """Get a thumbnail image of the current clip at the playhead position.
    
    Args:
        width: Width of the thumbnail in pixels (default: 320)
        height: Height of the thumbnail in pixels (default: 180)
        
    Returns:
        Dictionary with success status and thumbnail data (if supported by the API)
    """
    return safe_api_call(
        lambda: (
            helper_get_current_clip_thumbnail_image(width, height)
        ),
        "Error getting current clip thumbnail image"
    )

def helper_get_current_clip_thumbnail_image(width: int, height: int) -> Dict[str, Any]:
    """Helper function to get a thumbnail image of the current clip."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    # Validate dimensions
    if width <= 0 or height <= 0:
        return {"success": False, "error": "Width and height must be positive integers"}
    
    try:
        # Note: The DaVinci Resolve API might return the thumbnail in different ways depending on the version
        # This is a generic approach that may need adaptation based on the actual API behavior
        thumbnail = timeline.GetCurrentClipThumbnailImage(width, height)
        
        if not thumbnail:
            return {"success": False, "error": "Failed to get thumbnail for the current clip"}
        
        # The actual return format depends on how DaVinci Resolve API implements this
        # It might be a file path, a binary blob, base64 data, etc.
        return {
            "success": True,
            "result": {
                "thumbnail": thumbnail,
                "width": width,
                "height": height
            }
        }
    except Exception as e:
        return {"success": False, "error": f"Error getting thumbnail: {str(e)}"}

def create_fusion_clip(timeline_items: List[str], clip_info: Dict[str, str] = None) -> Dict[str, Any]:
    """Create a Fusion clip from the specified timeline items.
    
    Args:
        timeline_items: List of timeline item IDs to include in the Fusion clip
        clip_info: Optional dictionary with additional clip information (e.g., name)
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_create_fusion_clip(timeline_items, clip_info)
        ),
        "Error creating Fusion clip"
    )

def helper_create_fusion_clip(timeline_items: List[str], clip_info: Dict[str, str] = None) -> Dict[str, Any]:
    """Helper function to create a Fusion clip from timeline items."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not timeline_items or not isinstance(timeline_items, list):
        return {"success": False, "error": "timeline_items must be a non-empty list of timeline item IDs"}
    
    # Initialize clip_info if not provided
    if clip_info is None:
        clip_info = {}
    
    # Resolve API requires a list of TimelineItem objects, not IDs
    # Similar to set_clips_linked, we need to convert IDs to TimelineItem objects
    resolved_items = []
    
    for clip_id in timeline_items:
        # Similar approach as in set_clips_linked
        all_tracks = ["video", "audio", "subtitle"]
        item_found = False
        
        for track_type in all_tracks:
            track_count = timeline.GetTrackCount(track_type)
            
            for i in range(1, track_count + 1):
                items = timeline.GetItemListInTrack(track_type, i)
                
                for item in items:
                    try:
                        if str(item) == clip_id:
                            resolved_items.append(item)
                            item_found = True
                            break
                    except:
                        pass
    
    if not resolved_items:
        return {"success": False, "error": "Could not find any of the specified timeline items"}
    
    # Create the Fusion clip
    result = timeline.CreateFusionClip(resolved_items)
    
    if not result:
        return {"success": False, "error": "Failed to create Fusion clip"}
    
    # The API might return the created clip or just a boolean
    # Adjust this part based on the actual behavior of the Resolve API
    if isinstance(result, bool):
        return {
            "success": True,
            "result": {
                "created": True,
                "items_count": len(resolved_items),
                "all_items_found": len(resolved_items) == len(timeline_items)
            }
        }
    else:
        # Assuming result is the created clip object
        return {
            "success": True,
            "result": {
                "name": result.GetName() if hasattr(result, "GetName") else "Fusion Clip",
                "start": result.GetStart() if hasattr(result, "GetStart") else None,
                "end": result.GetEnd() if hasattr(result, "GetEnd") else None,
                "duration": result.GetDuration() if hasattr(result, "GetDuration") else None
            }
        }

def import_into_timeline(file_path: str, import_options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Import media or AAF/XML/EDL/etc. into the current timeline.
    
    Args:
        file_path: Path to the file to import
        import_options: Optional dictionary with import options specific to the file type
        
    Returns:
        Dictionary with success status and result
    """
    return safe_api_call(
        lambda: (
            helper_import_into_timeline(file_path, import_options)
        ),
        "Error importing into timeline"
    )

def helper_import_into_timeline(file_path: str, import_options: Dict[str, Any] = None) -> Dict[str, Any]:
    """Helper function to import media or project files into the timeline."""
    timeline = get_current_timeline_helper()
    
    if not timeline:
        return {"success": False, "error": "Failed to get current timeline"}
    
    if not file_path:
        return {"success": False, "error": "file_path must be provided"}
    
    # Verify file exists
    import os
    if not os.path.exists(file_path):
        return {"success": False, "error": f"File not found: {file_path}"}
    
    # Initialize import_options if not provided
    if import_options is None:
        import_options = {}
    
    # Import into timeline
    # Note: The actual ImportIntoTimeline method in DaVinci Resolve API might have different parameters
    # This is a generic approach that may need adaptation based on the actual API
    try:
        result = timeline.ImportIntoTimeline(file_path, **import_options)
        
        if not result:
            return {"success": False, "error": f"Failed to import {file_path} into timeline"}
        
        # The API might return information about the imported items
        return {
            "success": True,
            "result": {
                "imported": True,
                "file_path": file_path
            }
        }
    except Exception as e:
        return {"success": False, "error": f"Error importing into timeline: {str(e)}"} 