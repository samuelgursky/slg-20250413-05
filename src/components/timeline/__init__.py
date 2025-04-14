"""
Timeline Component for DaVinci Resolve API
Handles timeline-related operations
"""

import logging
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.timeline")

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
    
    Returns:
        Dictionary with timeline items or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        timeline = project.GetCurrentTimeline()
        if not timeline:
            return {"success": False, "error": "No timeline is currently open"}
        
        # Get all video items from all video tracks
        video_track_count = timeline.GetTrackCount("video")
        video_items = []
        
        for i in range(1, video_track_count + 1):
            track_items = timeline.GetItemListInTrack("video", i)
            
            for item in track_items:
                video_items.append({
                    "name": item.GetName(),
                    "track": i,
                    "start_frame": item.GetStart(),
                    "end_frame": item.GetEnd(),
                    "duration": item.GetDuration(),
                    "type": item.GetType()
                })
        
        # Get all audio items from all audio tracks
        audio_track_count = timeline.GetTrackCount("audio")
        audio_items = []
        
        for i in range(1, audio_track_count + 1):
            track_items = timeline.GetItemListInTrack("audio", i)
            
            for item in track_items:
                audio_items.append({
                    "name": item.GetName(),
                    "track": i,
                    "start_frame": item.GetStart(),
                    "end_frame": item.GetEnd(),
                    "duration": item.GetDuration(),
                    "type": item.GetType()
                })
        
        return {
            "success": True,
            "result": {
                "video_items": video_items,
                "audio_items": audio_items
            }
        }
    except Exception as e:
        logger.error(f"Error getting timeline items: {str(e)}")
        return {"success": False, "error": str(e)} 