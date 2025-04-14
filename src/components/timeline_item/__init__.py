"""
TimelineItem Component for DaVinci Resolve API
Handles timeline item operations (clips in a timeline)
"""

import logging
import os
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_current_project, get_timeline_item_by_id, safe_api_call
from src.components.timeline import get_current_timeline_helper

logger = logging.getLogger("resolve_api.timeline_item")

def get_timeline_item(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get a timeline item by its ID and return its basic details.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and timeline item details or error
    """
    timeline = get_current_timeline_helper()
    if not timeline:
        return {"success": False, "error": "No timeline open"}
    
    result = safe_api_call(
        lambda: timeline.GetItemById(timeline_item_id),
        "Failed to get timeline item by ID"
    )
    
    if not result["success"] or not result["result"]:
        return {"success": False, "error": f"Timeline item with ID {timeline_item_id} not found"}
    
    return {"success": True, "result": result["result"]}

def get_name(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the name of a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and name or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    return {
        "success": True,
        "name": timeline_item.GetName(),
        "timeline_item_id": timeline_item_id
    }

def get_duration(timeline_item_id: str, subframe_precision: bool = False) -> Dict[str, Any]:
    """
    Get the duration of a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        subframe_precision: Whether to return fractional frames
        
    Returns:
        Dictionary with success status and duration or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    duration = timeline_item.GetDuration(subframe_precision)
    return {
        "success": True,
        "duration": duration,
        "timeline_item_id": timeline_item_id,
        "subframe_precision": subframe_precision
    }

def get_start(timeline_item_id: str, subframe_precision: bool = False) -> Dict[str, Any]:
    """
    Get the start frame position of a timeline item on the timeline.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        subframe_precision: Whether to return fractional frames
        
    Returns:
        Dictionary with success status and start position or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    start = timeline_item.GetStart(subframe_precision)
    return {
        "success": True,
        "start": start,
        "timeline_item_id": timeline_item_id,
        "subframe_precision": subframe_precision
    }

def get_end(timeline_item_id: str, subframe_precision: bool = False) -> Dict[str, Any]:
    """
    Get the end frame position of a timeline item on the timeline.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        subframe_precision: Whether to return fractional frames
        
    Returns:
        Dictionary with success status and end position or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    end = timeline_item.GetEnd(subframe_precision)
    return {
        "success": True,
        "end": end,
        "timeline_item_id": timeline_item_id,
        "subframe_precision": subframe_precision
    }

def get_left_offset(timeline_item_id: str, subframe_precision: bool = False) -> Dict[str, Any]:
    """
    Get the maximum extension by frame for clip from left side.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        subframe_precision: Whether to return fractional frames
        
    Returns:
        Dictionary with success status and left offset or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    offset = timeline_item.GetLeftOffset(subframe_precision)
    return {
        "success": True,
        "left_offset": offset,
        "timeline_item_id": timeline_item_id,
        "subframe_precision": subframe_precision
    }

def get_right_offset(timeline_item_id: str, subframe_precision: bool = False) -> Dict[str, Any]:
    """
    Get the maximum extension by frame for clip from right side.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        subframe_precision: Whether to return fractional frames
        
    Returns:
        Dictionary with success status and right offset or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    offset = timeline_item.GetRightOffset(subframe_precision)
    return {
        "success": True,
        "right_offset": offset,
        "timeline_item_id": timeline_item_id,
        "subframe_precision": subframe_precision
    }

def get_source_start_frame(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the start frame of the source media in the timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and source start frame or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    start_frame = timeline_item.GetSourceStartFrame()
    return {
        "success": True,
        "source_start_frame": start_frame,
        "timeline_item_id": timeline_item_id
    }

def get_source_end_frame(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the end frame of the source media in the timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and source end frame or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    end_frame = timeline_item.GetSourceEndFrame()
    return {
        "success": True,
        "source_end_frame": end_frame,
        "timeline_item_id": timeline_item_id
    }

def get_source_start_time(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the start time position of the media pool clip in the timeline clip.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and source start time or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    start_time = timeline_item.GetSourceStartTime()
    return {
        "success": True,
        "source_start_time": start_time,
        "timeline_item_id": timeline_item_id
    }

def get_source_end_time(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the end time position of the media pool clip in the timeline clip.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and source end time or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    end_time = timeline_item.GetSourceEndTime()
    return {
        "success": True,
        "source_end_time": end_time,
        "timeline_item_id": timeline_item_id
    }

def get_property(timeline_item_id: str, property_key: str) -> Dict[str, Any]:
    """
    Gets a specific property from the timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        property_key: The name of the property to retrieve
        
    Returns:
        Dictionary with success status and property value or error
    """
    def _get_property():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            # Try to get the property
            value = timeline_item.GetProperty(property_key)
            
            # DaVinci Resolve returns None for invalid properties
            if value is None:
                return {
                    "success": False, 
                    "error": f"Property '{property_key}' not found or has no value",
                    "timeline_item_id": timeline_item_id
                }
            
            return {
                "success": True,
                "property_key": property_key,
                "property_value": value,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error getting timeline item property: {str(e)}")
            return {"success": False, "error": f"Failed to get property '{property_key}': {str(e)}"}
    
    return safe_api_call(
        _get_property,
        f"Error getting property '{property_key}' for timeline item ID: {timeline_item_id}"
    )

def set_property(timeline_item_id: str, property_key: str, property_value: Any) -> Dict[str, Any]:
    """
    Sets a specific property on the timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        property_key: The name of the property to set
        property_value: The value to set the property to
        
    Returns:
        Dictionary with success status or error
    """
    def _set_property():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            # Try to set the property
            result = timeline_item.SetProperty(property_key, property_value)
            if not result:
                return {
                    "success": False, 
                    "error": f"Failed to set property '{property_key}' to '{property_value}'",
                    "timeline_item_id": timeline_item_id
                }
            
            # Get the property to confirm it was set
            new_value = timeline_item.GetProperty(property_key)
            
            return {
                "success": True,
                "property_key": property_key,
                "previous_value": None,  # We don't have previous value information
                "new_value": new_value,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error setting timeline item property: {str(e)}")
            return {"success": False, "error": f"Failed to set property '{property_key}': {str(e)}"}
    
    return safe_api_call(
        _set_property,
        f"Error setting property '{property_key}' for timeline item ID: {timeline_item_id}"
    )

def set_start(timeline_item_id: str, frame_num: int) -> Dict[str, Any]:
    """
    Sets the start frame of the specified timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_num: Frame number for the new start position
        
    Returns:
        Dictionary with success status or error
    """
    def _set_start():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.SetStart(frame_num)
            if not result:
                return {"success": False, "error": f"Failed to set start frame to {frame_num}"}
            
            # Get the updated start value to confirm change
            new_start = timeline_item.GetStart()
            
            return {
                "success": True,
                "new_start": new_start,
                "requested_frame": frame_num,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error setting timeline item start frame: {str(e)}")
            return {"success": False, "error": f"Failed to set start frame: {str(e)}"}
    
    return safe_api_call(
        _set_start,
        f"Error setting start frame for timeline item ID: {timeline_item_id}"
    )

def set_end(timeline_item_id: str, frame_num: int) -> Dict[str, Any]:
    """
    Sets the end frame of the specified timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_num: Frame number for the new end position
        
    Returns:
        Dictionary with success status or error
    """
    def _set_end():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.SetEnd(frame_num)
            if not result:
                return {"success": False, "error": f"Failed to set end frame to {frame_num}"}
            
            # Get the updated end value to confirm change
            new_end = timeline_item.GetEnd()
            
            return {
                "success": True,
                "new_end": new_end,
                "requested_frame": frame_num,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error setting timeline item end frame: {str(e)}")
            return {"success": False, "error": f"Failed to set end frame: {str(e)}"}
    
    return safe_api_call(
        _set_end,
        f"Error setting end frame for timeline item ID: {timeline_item_id}"
    )

def set_left_offset(timeline_item_id: str, frame_num: int) -> Dict[str, Any]:
    """
    Sets the left offset (handle) of the specified timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_num: Frame number for the new left offset position
        
    Returns:
        Dictionary with success status or error
    """
    def _set_left_offset():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.SetLeftOffset(frame_num)
            if not result:
                return {"success": False, "error": f"Failed to set left offset to {frame_num}"}
            
            # Get the updated left offset value to confirm change
            new_offset = timeline_item.GetLeftOffset()
            
            return {
                "success": True,
                "new_left_offset": new_offset,
                "requested_offset": frame_num,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error setting timeline item left offset: {str(e)}")
            return {"success": False, "error": f"Failed to set left offset: {str(e)}"}
    
    return safe_api_call(
        _set_left_offset,
        f"Error setting left offset for timeline item ID: {timeline_item_id}"
    )

def set_right_offset(timeline_item_id: str, frame_num: int) -> Dict[str, Any]:
    """
    Sets the right offset (handle) of the specified timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_num: Frame number for the new right offset position
        
    Returns:
        Dictionary with success status or error
    """
    def _set_right_offset():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.SetRightOffset(frame_num)
            if not result:
                return {"success": False, "error": f"Failed to set right offset to {frame_num}"}
            
            # Get the updated right offset value to confirm change
            new_offset = timeline_item.GetRightOffset()
            
            return {
                "success": True,
                "new_right_offset": new_offset,
                "requested_offset": frame_num,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error setting timeline item right offset: {str(e)}")
            return {"success": False, "error": f"Failed to set right offset: {str(e)}"}
    
    return safe_api_call(
        _set_right_offset,
        f"Error setting right offset for timeline item ID: {timeline_item_id}"
    )

def add_marker(timeline_item_id: str, frame_id: int, color: str = "blue", 
               name: str = None, note: str = None, duration: int = 1, 
               custom_data: str = None) -> Dict[str, Any]:
    """
    Add a marker to a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_id: Frame position for the marker (timeline position)
        color: Marker color (blue, cyan, green, yellow, red, pink, purple, fuchsia, rose, lavender, sky, mint, lemon, sand, cocoa, cream)
        name: Marker name
        note: Marker note
        duration: Marker duration in frames
        custom_data: Custom data to associate with the marker
        
    Returns:
        Dictionary with success status or error
    """
    def _add_marker():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            # Create marker data dictionary
            marker_data = {}
            
            if color:
                marker_data["color"] = color
            if name:
                marker_data["name"] = name
            if note:
                marker_data["note"] = note
            if duration:
                marker_data["duration"] = duration
            if custom_data:
                marker_data["customData"] = custom_data
            
            result = timeline_item.AddMarker(frame_id, marker_data)
            if not result:
                return {"success": False, "error": f"Failed to add marker at frame {frame_id}"}
            
            return {
                "success": True,
                "frame_id": frame_id,
                "marker_data": marker_data,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error adding timeline item marker: {str(e)}")
            return {"success": False, "error": f"Failed to add timeline item marker: {str(e)}"}
    
    return safe_api_call(
        _add_marker,
        f"Error adding timeline item marker for ID: {timeline_item_id}"
    )

def get_markers(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get all markers from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and markers or error
    """
    def _get_markers():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            markers = timeline_item.GetMarkers()
            # Markers are returned as a dict with frame numbers as keys
            # Convert to a list for easier handling
            marker_list = []
            for frame, marker_data in markers.items():
                marker_data["frame"] = int(frame)
                marker_list.append(marker_data)
            
            return {
                "success": True,
                "markers": marker_list,
                "count": len(marker_list),
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error getting timeline item markers: {str(e)}")
            return {"success": False, "error": f"Failed to get timeline item markers: {str(e)}"}
    
    return safe_api_call(
        _get_markers,
        f"Error getting timeline item markers for ID: {timeline_item_id}"
    )

def get_marker_by_custom_data(timeline_item_id: str, custom_data: str) -> Dict[str, Any]:
    """
    Get a marker by its custom data from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        custom_data: Custom data associated with the marker
        
    Returns:
        Dictionary with success status and marker data or error
    """
    def _get_marker_by_custom_data():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            marker = timeline_item.GetMarkerByCustomData(custom_data)
            if not marker:
                return {"success": False, "error": f"No marker found with custom data '{custom_data}'"}
            
            return {
                "success": True,
                "marker": marker,
                "timeline_item_id": timeline_item_id,
                "custom_data": custom_data
            }
        except Exception as e:
            logger.error(f"Error getting timeline item marker by custom data: {str(e)}")
            return {"success": False, "error": f"Failed to get timeline item marker by custom data: {str(e)}"}
    
    return safe_api_call(
        _get_marker_by_custom_data,
        f"Error getting timeline item marker by custom data for ID: {timeline_item_id}"
    )

def update_marker_custom_data(timeline_item_id: str, frame_id: int, custom_data: str) -> Dict[str, Any]:
    """
    Update custom data for a marker at the specified frame in a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_id: Frame position of the marker (timeline position)
        custom_data: New custom data to set for the marker
        
    Returns:
        Dictionary with success status or error
    """
    def _update_marker_custom_data():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.UpdateMarkerCustomData(frame_id, custom_data)
            if not result:
                return {"success": False, "error": f"Failed to update marker custom data at frame {frame_id}"}
            
            return {
                "success": True,
                "frame_id": frame_id,
                "custom_data": custom_data,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error updating timeline item marker custom data: {str(e)}")
            return {"success": False, "error": f"Failed to update timeline item marker custom data: {str(e)}"}
    
    return safe_api_call(
        _update_marker_custom_data,
        f"Error updating timeline item marker custom data for ID: {timeline_item_id}"
    )

def get_marker_custom_data(timeline_item_id: str, frame_id: int) -> Dict[str, Any]:
    """
    Get custom data from a marker at the specified frame in a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_id: Frame position of the marker (timeline position)
        
    Returns:
        Dictionary with success status and custom data or error
    """
    def _get_marker_custom_data():
        # Get the timeline item
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            custom_data = timeline_item.GetMarkerCustomData(frame_id)
            if custom_data is None:
                return {"success": False, "error": f"No marker found at frame {frame_id} or no custom data"}
            
            return {
                "success": True,
                "custom_data": custom_data,
                "frame_id": frame_id,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error getting marker custom data: {str(e)}")
            return {"success": False, "error": f"Failed to get marker custom data: {str(e)}"}
    
    return safe_api_call(
        _get_marker_custom_data,
        f"Error getting marker custom data for timeline item ID: {timeline_item_id}"
    )

def delete_markers_by_color(timeline_item_id: str, color: str) -> Dict[str, Any]:
    """
    Delete all markers of a specific color from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        color: Color of markers to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_markers_by_color():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.DeleteMarkersByColor(color)
            if not result:
                return {"success": False, "error": f"Failed to delete markers with color '{color}'"}
            
            return {
                "success": True,
                "color": color,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error deleting timeline item markers by color: {str(e)}")
            return {"success": False, "error": f"Failed to delete timeline item markers by color: {str(e)}"}
    
    return safe_api_call(
        _delete_markers_by_color,
        f"Error deleting timeline item markers by color for ID: {timeline_item_id}"
    )

def delete_marker_at_frame(timeline_item_id: str, frame_id: int) -> Dict[str, Any]:
    """
    Delete a marker at the specified frame from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        frame_id: Frame position of the marker to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_marker_at_frame():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.DeleteMarkerAtFrame(frame_id)
            if not result:
                return {"success": False, "error": f"Failed to delete marker at frame {frame_id}"}
            
            return {
                "success": True,
                "frame_id": frame_id,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error deleting timeline item marker: {str(e)}")
            return {"success": False, "error": f"Failed to delete timeline item marker: {str(e)}"}
    
    return safe_api_call(
        _delete_marker_at_frame,
        f"Error deleting timeline item marker for ID: {timeline_item_id}"
    )

def delete_marker_by_custom_data(timeline_item_id: str, custom_data: str) -> Dict[str, Any]:
    """
    Delete a marker by its custom data from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        custom_data: Custom data associated with the marker to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_marker_by_custom_data():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            result = timeline_item.DeleteMarkerByCustomData(custom_data)
            if not result:
                return {"success": False, "error": f"No marker found with custom data '{custom_data}'"}
            
            return {
                "success": True,
                "custom_data": custom_data,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error deleting timeline item marker by custom data: {str(e)}")
            return {"success": False, "error": f"Failed to delete timeline item marker by custom data: {str(e)}"}
    
    return safe_api_call(
        _delete_marker_by_custom_data,
        f"Error deleting timeline item marker by custom data for ID: {timeline_item_id}"
    )

def add_flag(timeline_item_id, color):
    """
    Adds a flag of specified color to a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        color (str): Color of the flag to add
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.AddFlag(color),
        f"Failed to add {color} flag to timeline item"
    )
    return result

def get_flags(timeline_item_id):
    """
    Gets the flags attached to a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': list of flags or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    result = safe_api_call(
        lambda: item.GetFlags(),
        "Failed to get flags for timeline item"
    )
    return result

def clear_flags(timeline_item_id, color=None):
    """
    Clears flags from a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        color (str, optional): Specific flag color to clear. If None, clears all flags.
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    if color:
        result = safe_api_call(
            lambda: item.ClearFlags(color),
            f"Failed to clear {color} flags from timeline item"
        )
    else:
        result = safe_api_call(
            lambda: item.ClearFlags(),
            "Failed to clear all flags from timeline item"
        )
    
    return result

def set_clip_color(timeline_item_id, color_name):
    """
    Sets the color of a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        color_name (str): Name of the color to set
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.SetClipColor(color_name),
        f"Failed to set clip color to {color_name} for timeline item"
    )
    return result

def get_clip_color(timeline_item_id):
    """
    Gets the color of a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': color name (str) or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.GetClipColor(),
        "Failed to get clip color for timeline item"
    )
    return result

def clear_clip_color(timeline_item_id):
    """
    Clears the color of a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.ClearClipColor(),
        "Failed to clear clip color for timeline item"
    )
    return result

def get_fusion_comp_count(timeline_item_id):
    """
    Gets the number of Fusion compositions in a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': number of Fusion compositions or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.GetFusionCompCount(),
        "Failed to get Fusion composition count for timeline item"
    )
    return result

def get_fusion_comp_name_list(timeline_item_id):
    """
    Gets the names of all Fusion compositions in a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': list of Fusion composition names or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.GetFusionCompNameList(),
        "Failed to get Fusion composition name list for timeline item"
    )
    return result

def get_fusion_comp_by_name(timeline_item_id, comp_name):
    """
    Gets a Fusion composition by name from a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_name (str): Name of the Fusion composition
        
    Returns:
        dict: {'success': bool, 'result': Fusion composition object or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.GetFusionCompByName(comp_name),
        f"Failed to get Fusion composition '{comp_name}' for timeline item"
    )
    return result

def add_fusion_comp(timeline_item_id, comp_name=None):
    """
    Adds a new Fusion composition to a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_name (str, optional): Name for the new Fusion composition
        
    Returns:
        dict: {'success': bool, 'result': Fusion composition or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    if comp_name:
        result = safe_api_call(
            lambda: item.AddFusionComp(comp_name),
            f"Failed to add Fusion composition '{comp_name}' to timeline item"
        )
    else:
        result = safe_api_call(
            lambda: item.AddFusionComp(),
            "Failed to add Fusion composition to timeline item"
        )
    return result

def rename_fusion_comp(timeline_item_id, old_name, new_name):
    """
    Renames a Fusion composition in a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        old_name (str): Current name of the Fusion composition
        new_name (str): New name for the Fusion composition
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    result = safe_api_call(
        lambda: item.RenameFusionComp(old_name, new_name),
        f"Failed to rename Fusion composition from '{old_name}' to '{new_name}'"
    )
    return result

def import_fusion_comp(timeline_item_id, comp_file, comp_name=None):
    """
    Imports a Fusion composition to a timeline item from a file.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_file (str): Path to the Fusion composition file
        comp_name (str, optional): Name for the imported Fusion composition
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    # Ensure the composition file exists
    if not os.path.exists(comp_file):
        return {'success': False, 'error': f"Fusion composition file not found: {comp_file}"}
    
    if comp_name:
        result = safe_api_call(
            lambda: item.ImportFusionComp(comp_file, comp_name),
            f"Failed to import Fusion composition from '{comp_file}'"
        )
    else:
        result = safe_api_call(
            lambda: item.ImportFusionComp(comp_file),
            f"Failed to import Fusion composition from '{comp_file}'"
        )
    return result

def export_fusion_comp(timeline_item_id, comp_name, comp_file):
    """
    Exports a Fusion composition from a timeline item to a file.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_name (str): Name of the Fusion composition to export
        comp_file (str): Path where the Fusion composition will be saved
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    # Ensure the parent directory exists
    parent_dir = os.path.dirname(comp_file)
    if parent_dir and not os.path.exists(parent_dir):
        try:
            os.makedirs(parent_dir, exist_ok=True)
        except OSError as e:
            return {'success': False, 'error': f"Failed to create directory for export: {str(e)}"}
    
    result = safe_api_call(
        lambda: item.ExportFusionComp(comp_name, comp_file),
        f"Failed to export Fusion composition '{comp_name}' to '{comp_file}'"
    )
    return result

def delete_fusion_comp_by_name(timeline_item_id, comp_name):
    """
    Deletes a Fusion composition from a timeline item by name.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_name (str): Name of the Fusion composition to delete
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    result = safe_api_call(
        lambda: item.DeleteFusionCompByName(comp_name),
        f"Failed to delete Fusion composition '{comp_name}'"
    )
    return result

def get_fusion_comp_names(timeline_item_id):
    """
    Gets the names of all Fusion compositions in a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': list of Fusion composition names or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    result = safe_api_call(
        lambda: item.GetFusionCompNames(),
        f"Failed to get Fusion composition names"
    )
    return result

def load_fusion_comp_by_name(timeline_item_id, comp_name):
    """
    Loads a Fusion composition by name in a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        comp_name (str): Name of the Fusion composition to load
        
    Returns:
        dict: {'success': bool, 'result': True/False or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    
    result = safe_api_call(
        lambda: item.LoadFusionCompByName(comp_name),
        f"Failed to load Fusion composition '{comp_name}'"
    )
    return result

def set_scale(timeline_item_id, scale):
    """
    Sets the scale (playback speed) of a timeline item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        scale (float): Scale value (e.g., 0.5 for 50%, 2.0 for 200%)
        
    Returns:
        dict: {'success': bool, 'result': success message or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['item']
    try:
        scale_value = float(scale)
    except ValueError:
        return {"success": False, "result": f"Invalid scale value: {scale}. Must be a number."}
    
    result = safe_api_call(
        lambda: item.SetScale(scale_value),
        f"Failed to set scale to {scale_value} for timeline item"
    )
    return result

def get_scale(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the scale (playback speed) of a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and scale value or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.GetScale(),
        "Failed to get timeline item scale"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "scale": result["result"],
        "timeline_item_id": timeline_item_id
    }

def get_media_pool_item(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the media pool item that a timeline item is created from.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and media pool item or error
    """
    def _get_media_pool_item():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            media_pool_item = timeline_item.GetMediaPoolItem()
            if not media_pool_item:
                return {"success": False, "error": f"No media pool item found for timeline item ID '{timeline_item_id}'"}
            
            # Get some basic info about the media pool item
            name = media_pool_item.GetName()
            clip_color = media_pool_item.GetClipColor()
            
            return {
                "success": True,
                "media_pool_item": media_pool_item,
                "name": name,
                "clip_color": clip_color,
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error getting media pool item: {str(e)}")
            return {"success": False, "error": f"Failed to get media pool item: {str(e)}"}
    
    return safe_api_call(
        _get_media_pool_item,
        f"Error getting media pool item for timeline item ID: {timeline_item_id}"
    )

def get_fusion_comp_names(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get all Fusion composition names from a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and Fusion composition names or error
    """
    def _get_fusion_comp_names():
        # Get the timeline item using the helper function
        timeline_item = get_timeline_item_by_id(timeline_item_id)
        if not timeline_item:
            return {"success": False, "error": f"Timeline item with ID '{timeline_item_id}' not found"}
        
        try:
            comp_names = timeline_item.GetFusionCompNames()
            if not comp_names:
                return {
                    "success": True, 
                    "comp_names": [],
                    "count": 0,
                    "timeline_item_id": timeline_item_id
                }
            
            return {
                "success": True,
                "comp_names": comp_names,
                "count": len(comp_names),
                "timeline_item_id": timeline_item_id
            }
        except Exception as e:
            logger.error(f"Error getting Fusion composition names: {str(e)}")
            return {"success": False, "error": f"Failed to get Fusion composition names: {str(e)}"}

def has_video_effect(timeline_item_id):
    """
    Check if a timeline item has a video effect applied.
    
    Args:
        timeline_item_id (str): The ID of the timeline item to check.
    
    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the operation was successful.
            - result (bool): True if the timeline item has a video effect, False otherwise.
            - error (str, optional): Error message if the operation failed.
    """
    def _has_video_effect(resolve, project, timeline, timeline_item_id):
        item_result = get_timeline_item(timeline_item_id)
        if not item_result['success']:
            return item_result
        
        item = item_result['result']
        has_effect = item.GetFusionCompCount() > 0 or item.GetVideoEffectList()
        
        return {
            'success': True,
            'result': has_effect
        }
    
    return safe_api_call(_has_video_effect, timeline_item_id=timeline_item_id)

def get_is_filler(timeline_item_id):
    """
    Checks if a timeline item is a filler item.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': True/False or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    result = safe_api_call(
        lambda: item.GetIsFiller(),
        "Failed to check if timeline item is a filler item"
    )
    return result

def has_audio_effect(timeline_item_id):
    """
    Check if a timeline item has an audio effect applied.
    
    Args:
        timeline_item_id (str): The ID of the timeline item to check.
    
    Returns:
        dict: A dictionary containing:
            - success (bool): Whether the operation was successful.
            - result (bool): True if the timeline item has an audio effect, False otherwise.
            - error (str, optional): Error message if the operation failed.
    """
    def _has_audio_effect(resolve, project, timeline, timeline_item_id):
        item_result = get_timeline_item(timeline_item_id)
        if not item_result['success']:
            return item_result
        
        item = item_result['result']
        has_effect = item.GetAudioEffectList()
        
        return {
            'success': True,
            'result': bool(has_effect)
        }
    
    return safe_api_call(_has_audio_effect, timeline_item_id=timeline_item_id)

def has_video_effect_at_offset(timeline_item_id, frame_offset):
    """
    Checks if a timeline item has a video effect at the specified frame offset.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        frame_offset (int): Frame offset to check for video effect
        
    Returns:
        dict: {'success': bool, 'result': True/False or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        frame_offset = int(frame_offset)
    except ValueError:
        return {"success": False, "result": f"Invalid frame offset: {frame_offset}. Must be an integer."}
    
    result = safe_api_call(
        lambda: item.HasVideoEffectAtOffset(frame_offset),
        f"Failed to check if timeline item has video effect at offset {frame_offset}"
    )
    return result

def has_audio_effect_at_offset(timeline_item_id, frame_offset):
    """
    Checks if a timeline item has an audio effect at the specified frame offset.
    
    Args:
        timeline_item_id (str): ID of the timeline item
        frame_offset (int): Frame offset to check for audio effect
        
    Returns:
        dict: {'success': bool, 'result': True/False or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        frame_offset = int(frame_offset)
    except ValueError:
        return {"success": False, "result": f"Invalid frame offset: {frame_offset}. Must be an integer."}
    
    result = safe_api_call(
        lambda: item.HasAudioEffectAtOffset(frame_offset),
        f"Failed to check if timeline item has audio effect at offset {frame_offset}"
    )
    return result

# Adding an alias for get_flags to ensure compatibility
def get_flag_list(timeline_item_id):
    """
    Gets the flags attached to a timeline item (alias for get_flags).
    
    Args:
        timeline_item_id (str): ID of the timeline item
        
    Returns:
        dict: {'success': bool, 'result': list of flags or error message}
    """
    return get_flags(timeline_item_id)

def add_video_effect(timeline_item_id, effect_name):
    """
    Adds a video effect to a timeline item
    
    Args:
        timeline_item_id (str): ID of the timeline item
        effect_name (str): Name of the effect to add
        
    Returns:
        dict: {'success': bool, 'result': True or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        resolve = bmd.scriptapp("Resolve")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        
        if not timeline:
            return {'success': False, 'error': 'No timeline is open'}
        
        # Get timeline item
        timeline_item = timeline.FindItemById(timeline_item_id)
        if not timeline_item:
            return {'success': False, 'error': f'Timeline item with ID {timeline_item_id} not found'}
        
        # Add video effect
        result = timeline_item.AddVideoEffect(effect_name)
        return {'success': True, 'result': result}
    
    except Exception as e:
        logger.error(f"Error adding video effect to timeline item {timeline_item_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def add_audio_effect(timeline_item_id, effect_name):
    """
    Adds an audio effect to a timeline item
    
    Args:
        timeline_item_id (str): ID of the timeline item
        effect_name (str): Name of the effect to add
        
    Returns:
        dict: {'success': bool, 'result': True or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        resolve = bmd.scriptapp("Resolve")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        
        if not timeline:
            return {'success': False, 'error': 'No timeline is open'}
        
        # Get timeline item
        timeline_item = timeline.FindItemById(timeline_item_id)
        if not timeline_item:
            return {'success': False, 'error': f'Timeline item with ID {timeline_item_id} not found'}
        
        # Add audio effect
        result = timeline_item.AddAudioEffect(effect_name)
        return {'success': True, 'result': result}
    
    except Exception as e:
        logger.error(f"Error adding audio effect to timeline item {timeline_item_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def remove_video_effect(timeline_item_id, effect_name):
    """
    Removes a video effect from a timeline item
    
    Args:
        timeline_item_id (str): ID of the timeline item
        effect_name (str): Name of the effect to remove
        
    Returns:
        dict: {'success': bool, 'result': True or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        resolve = bmd.scriptapp("Resolve")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        
        if not timeline:
            return {'success': False, 'error': 'No timeline is open'}
        
        # Get timeline item
        timeline_item = timeline.FindItemById(timeline_item_id)
        if not timeline_item:
            return {'success': False, 'error': f'Timeline item with ID {timeline_item_id} not found'}
        
        # Remove video effect
        result = timeline_item.RemoveVideoEffect(effect_name)
        return {'success': True, 'result': result}
    
    except Exception as e:
        logger.error(f"Error removing video effect from timeline item {timeline_item_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def remove_audio_effect(timeline_item_id, effect_name):
    """
    Removes an audio effect from a timeline item
    
    Args:
        timeline_item_id (str): ID of the timeline item
        effect_name (str): Name of the effect to remove
        
    Returns:
        dict: {'success': bool, 'result': True or error message}
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result['success']:
        return item_result
    
    item = item_result['result']
    
    try:
        resolve = bmd.scriptapp("Resolve")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()
        timeline = project.GetCurrentTimeline()
        
        if not timeline:
            return {'success': False, 'error': 'No timeline is open'}
        
        # Get timeline item
        timeline_item = timeline.FindItemById(timeline_item_id)
        if not timeline_item:
            return {'success': False, 'error': f'Timeline item with ID {timeline_item_id} not found'}
        
        # Remove audio effect
        result = timeline_item.RemoveAudioEffect(effect_name)
        return {'success': True, 'result': result}
    
    except Exception as e:
        logger.error(f"Error removing audio effect from timeline item {timeline_item_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def add_take(timeline_item_id: str, media_pool_item_id: str, start_frame: int = None, end_frame: int = None) -> Dict[str, Any]:
    """
    Adds a media pool item as a new take to the timeline item.
    Initializes a take selector for the timeline item if needed.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        media_pool_item_id: ID of the media pool item to add as a take
        start_frame: Optional start frame to specify clip extents
        end_frame: Optional end frame to specify clip extents
        
    Returns:
        Dictionary with success status or error
    """
    # Get timeline item
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    # Get media pool item
    from ...resolve_api import get_media_pool_item_by_id
    media_pool_item = get_media_pool_item_by_id(media_pool_item_id)
    if not media_pool_item:
        return {"success": False, "error": f"Media pool item with ID {media_pool_item_id} not found"}
    
    # Call the API to add take
    args = [media_pool_item]
    if start_frame is not None:
        args.append(start_frame)
    if end_frame is not None:
        args.append(end_frame)
    
    result = safe_api_call(
        lambda: timeline_item.AddTake(*args),
        "Failed to add take to timeline item"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def get_selected_take_index(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the index of the currently selected take in the timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and selected take index or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.GetSelectedTakeIndex(),
        "Failed to get selected take index"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "selected_take_index": result["result"],
        "timeline_item_id": timeline_item_id
    }

def get_takes_count(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the number of takes in a take selector timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and takes count or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.GetTakesCount(),
        "Failed to get takes count"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "takes_count": result["result"],
        "timeline_item_id": timeline_item_id
    }

def get_take_by_index(timeline_item_id: str, take_index: int) -> Dict[str, Any]:
    """
    Get information about a take by its index.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        take_index: Index of the take to retrieve (1-based index)
        
    Returns:
        Dictionary with success status and take information or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    # Validate take index
    if not isinstance(take_index, int) or take_index < 1:
        return {"success": False, "error": "Take index must be a positive integer"}
    
    result = safe_api_call(
        lambda: timeline_item.GetTakeByIndex(take_index),
        f"Failed to get take at index {take_index}"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "take_info": result["result"],
        "timeline_item_id": timeline_item_id
    }

def delete_take_by_index(timeline_item_id: str, take_index: int) -> Dict[str, Any]:
    """
    Delete a take by its index.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        take_index: Index of the take to delete (1-based index)
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    # Validate take index
    if not isinstance(take_index, int) or take_index < 1:
        return {"success": False, "error": "Take index must be a positive integer"}
    
    result = safe_api_call(
        lambda: timeline_item.DeleteTakeByIndex(take_index),
        f"Failed to delete take at index {take_index}"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def select_take_by_index(timeline_item_id: str, take_index: int) -> Dict[str, Any]:
    """
    Select a take by its index.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        take_index: Index of the take to select (1-based index)
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    # Validate take index
    if not isinstance(take_index, int) or take_index < 1:
        return {"success": False, "error": "Take index must be a positive integer"}
    
    result = safe_api_call(
        lambda: timeline_item.SelectTakeByIndex(take_index),
        f"Failed to select take at index {take_index}"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def finalize_take(timeline_item_id: str) -> Dict[str, Any]:
    """
    Finalize the take selection for a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.FinalizeTake(),
        "Failed to finalize take"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def set_clip_enabled(timeline_item_id: str, enabled: bool) -> Dict[str, Any]:
    """
    Enable or disable a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        enabled: Boolean value to set clip enabled state
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    # Validate enabled parameter
    if not isinstance(enabled, bool):
        return {"success": False, "error": "Enabled parameter must be a boolean"}
    
    result = safe_api_call(
        lambda: timeline_item.SetClipEnabled(enabled),
        f"Failed to {'enable' if enabled else 'disable'} clip"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def get_clip_enabled(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the enabled status of a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and enabled status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.GetClipEnabled(),
        "Failed to get clip enabled status"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "enabled": result["result"],
        "timeline_item_id": timeline_item_id
    }

def update_sidecar(timeline_item_id: str) -> Dict[str, Any]:
    """
    Updates sidecar file for BRAW clips or RMD file for R3D clips.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.UpdateSidecar(),
        "Failed to update sidecar file"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    }

def get_unique_id(timeline_item_id: str) -> Dict[str, Any]:
    """
    Get the unique ID of a timeline item.
    
    Args:
        timeline_item_id: Unique ID for the timeline item
        
    Returns:
        Dictionary with success status and unique ID or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    timeline_item = item_result["result"]
    
    result = safe_api_call(
        lambda: timeline_item.GetUniqueId(),
        "Failed to get timeline item unique ID"
    )
    
    if not result["success"]:
        return result
    
    return {
        "success": True,
        "unique_id": result["result"],
        "timeline_item_id": timeline_item_id
    }

def copy_grades(timeline_item_id: str, target_timeline_items: List[str]) -> Dict[str, Any]:
    """
    Copies the current node stack layer grade to the same layer for each item in target_timeline_items.
    
    Args:
        timeline_item_id: Unique ID for the source timeline item
        target_timeline_items: List of timeline item IDs to copy grades to
        
    Returns:
        Dictionary with success status or error
    """
    item_result = get_timeline_item(timeline_item_id)
    if not item_result["success"]:
        return item_result
    
    source_timeline_item = item_result["result"]
    
    # Get target timeline items
    target_items = []
    for target_id in target_timeline_items:
        target_result = get_timeline_item(target_id)
        if not target_result["success"]:
            return {"success": False, "error": f"Target timeline item with ID {target_id} not found"}
        target_items.append(target_result["result"])
    
    result = safe_api_call(
        lambda: source_timeline_item.CopyGrades(target_items),
        "Failed to copy grades to target timeline items"
    )
    
    return {
        "success": result["success"],
        "error": result.get("error"),
        "timeline_item_id": timeline_item_id
    } 