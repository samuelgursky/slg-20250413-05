"""
MediaPoolItem Component for DaVinci Resolve API
Handles operations on individual media pool items
"""

import logging
import os
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_current_project, safe_api_call, get_media_pool_item_by_id

logger = logging.getLogger("resolve_api.media_pool_item")

def get_metadata(clip_id: str, metadata_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get metadata for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        metadata_type: Optional specific metadata type to retrieve
        
    Returns:
        Dictionary with metadata or error
    """
    def _get_metadata():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # If a specific metadata type is requested, return only that
        if metadata_type:
            return clip.GetMetadata(metadata_type)
        
        # Otherwise return all metadata
        return clip.GetMetadata()
    
    return safe_api_call(
        _get_metadata,
        f"Error getting metadata for clip {clip_id}"
    )

def set_metadata(clip_id: str, metadata: Union[Dict[str, str], str], metadata_value: Optional[str] = None) -> Dict[str, Any]:
    """
    Set metadata for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        metadata: Either a dictionary of metadata key-value pairs or a single metadata key
        metadata_value: Value to set if metadata is a single key (ignored if metadata is a dictionary)
        
    Returns:
        Dictionary with success status or error
    """
    def _set_metadata():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Handle both dictionary and key-value formats
        if isinstance(metadata, dict):
            result = clip.SetMetadata(metadata)
        else:
            if metadata_value is None:
                raise ValueError("metadata_value must be provided when metadata is a string")
            result = clip.SetMetadata(metadata, metadata_value)
            
        if not result:
            raise RuntimeError("Failed to set metadata")
            
        return True
    
    return safe_api_call(
        _set_metadata,
        f"Error setting metadata for clip {clip_id}"
    )

def get_clip_property(clip_id: str, property_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get clip properties for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        property_name: Optional specific property to retrieve
        
    Returns:
        Dictionary with properties or error
    """
    def _get_clip_property():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # If a specific property is requested, return only that
        if property_name:
            return clip.GetClipProperty(property_name)
        
        # Otherwise return all properties
        return clip.GetClipProperty()
    
    return safe_api_call(
        _get_clip_property,
        f"Error getting properties for clip {clip_id}"
    )

def set_clip_property(clip_id: str, property_name: str, property_value: str) -> Dict[str, Any]:
    """
    Set a clip property for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        property_name: Name of the property to set
        property_value: Value to set for the property
        
    Returns:
        Dictionary with success status or error
    """
    def _set_clip_property():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.SetClipProperty(property_name, property_value)
        if not result:
            raise RuntimeError(f"Failed to set property '{property_name}'")
            
        return True
    
    return safe_api_call(
        _set_clip_property,
        f"Error setting property for clip {clip_id}"
    )

def get_clip_color(clip_id: str) -> Dict[str, Any]:
    """
    Get the color assigned to a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with color information or error
    """
    def _get_clip_color():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetClipColor()
    
    return safe_api_call(
        _get_clip_color,
        f"Error getting color for clip {clip_id}"
    )

def set_clip_color(clip_id: str, color_name: str) -> Dict[str, Any]:
    """
    Set the color for a clip
    
    Args:
        clip_id: ID of the media pool item
        color_name: Name of the color to set
        
    Returns:
        Dictionary with success status or error
    """
    def _set_clip_color():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.SetClipColor(color_name)
        if not result:
            raise RuntimeError(f"Failed to set color '{color_name}'")
            
        return True
    
    return safe_api_call(
        _set_clip_color,
        f"Error setting color for clip {clip_id}"
    )

def clear_clip_color(clip_id: str) -> Dict[str, Any]:
    """
    Clear the color assigned to a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with success status or error
    """
    def _clear_clip_color():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.ClearClipColor()
        if not result:
            raise RuntimeError("Failed to clear clip color")
            
        return True
    
    return safe_api_call(
        _clear_clip_color,
        f"Error clearing color for clip {clip_id}"
    )

def add_marker(clip_id: str, frame_id: float, color: str, name: str, note: str, 
              duration: float, custom_data: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a marker to a clip
    
    Args:
        clip_id: ID of the media pool item
        frame_id: Frame position for the marker
        color: Color name for the marker
        name: Name of the marker
        note: Note text for the marker
        duration: Duration of the marker in frames
        custom_data: Optional custom data to attach to the marker
        
    Returns:
        Dictionary with success status or error
    """
    def _add_marker():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Add the marker
        custom_data = custom_data or ""
        result = clip.AddMarker(frame_id, color, name, note, duration, custom_data)
        if not result:
            raise RuntimeError("Failed to add marker")
            
        return True
    
    return safe_api_call(
        _add_marker,
        f"Error adding marker to clip {clip_id}"
    )

def get_markers(clip_id: str) -> Dict[str, Any]:
    """
    Get all markers for a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with markers information or error
    """
    def _get_markers():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetMarkers()
    
    return safe_api_call(
        _get_markers,
        f"Error getting markers for clip {clip_id}"
    )

def delete_marker_at_frame(clip_id: str, frame_num: float) -> Dict[str, Any]:
    """
    Delete a marker at a specific frame
    
    Args:
        clip_id: ID of the media pool item
        frame_num: Frame number where the marker is located
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_marker_at_frame():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.DeleteMarkerAtFrame(frame_num)
        if not result:
            raise RuntimeError(f"Failed to delete marker at frame {frame_num}")
            
        return True
    
    return safe_api_call(
        _delete_marker_at_frame,
        f"Error deleting marker for clip {clip_id}"
    )

def delete_markers_by_color(clip_id: str, color: str) -> Dict[str, Any]:
    """
    Delete all markers of a specific color
    
    Args:
        clip_id: ID of the media pool item
        color: Color of markers to delete, or "All" to delete all markers
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_markers_by_color():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.DeleteMarkersByColor(color)
        if not result:
            raise RuntimeError(f"Failed to delete markers with color '{color}'")
            
        return True
    
    return safe_api_call(
        _delete_markers_by_color,
        f"Error deleting markers for clip {clip_id}"
    )

def add_flag(clip_id: str, color: str) -> Dict[str, Any]:
    """
    Add a flag to a clip
    
    Args:
        clip_id: ID of the media pool item
        color: Color name for the flag
        
    Returns:
        Dictionary with success status or error
    """
    def _add_flag():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.AddFlag(color)
        if not result:
            raise RuntimeError(f"Failed to add flag with color '{color}'")
            
        return True
    
    return safe_api_call(
        _add_flag,
        f"Error adding flag to clip {clip_id}"
    )

def get_flag_list(clip_id: str) -> Dict[str, Any]:
    """
    Get all flags for a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with flag information or error
    """
    def _get_flag_list():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetFlagList()
    
    return safe_api_call(
        _get_flag_list,
        f"Error getting flags for clip {clip_id}"
    )

def clear_flags(clip_id: str, color: str) -> Dict[str, Any]:
    """
    Clear flags from a clip
    
    Args:
        clip_id: ID of the media pool item
        color: Color of flags to clear, or "All" to clear all flags
        
    Returns:
        Dictionary with success status or error
    """
    def _clear_flags():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.ClearFlags(color)
        if not result:
            raise RuntimeError(f"Failed to clear flags with color '{color}'")
            
        return True
    
    return safe_api_call(
        _clear_flags,
        f"Error clearing flags for clip {clip_id}"
    )

def get_media_id(clip_id: str) -> Dict[str, Any]:
    """
    Get the media ID for a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with media ID information or error
    """
    def _get_media_id():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetMediaId()
    
    return safe_api_call(
        _get_media_id,
        f"Error getting media ID for clip {clip_id}"
    )

def get_name(clip_id: str) -> Dict[str, Any]:
    """
    Get the name of a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with clip name or error
    """
    def _get_name():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetName()
    
    return safe_api_call(
        _get_name,
        f"Error getting name for clip {clip_id}"
    )

def get_unique_id(clip_id: str) -> Dict[str, Any]:
    """
    Get the unique ID of a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with unique ID or error
    """
    def _get_unique_id():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetUniqueId()
    
    return safe_api_call(
        _get_unique_id,
        f"Error getting unique ID for clip {clip_id}"
    )

def get_third_party_metadata(clip_id: str, metadata_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get third-party metadata for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        metadata_type: Optional specific metadata type to retrieve
        
    Returns:
        Dictionary with metadata or error
    """
    def _get_third_party_metadata():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # If a specific metadata type is requested, return only that
        if metadata_type:
            return clip.GetThirdPartyMetadata(metadata_type)
        
        # Otherwise return all metadata
        return clip.GetThirdPartyMetadata()
    
    return safe_api_call(
        _get_third_party_metadata,
        f"Error getting third-party metadata for clip {clip_id}"
    )

def set_third_party_metadata(clip_id: str, metadata: Union[Dict[str, str], str], metadata_value: Optional[str] = None) -> Dict[str, Any]:
    """
    Set third-party metadata for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        metadata: Either a dictionary of metadata key-value pairs or a single metadata key
        metadata_value: Value to set if metadata is a single key (ignored if metadata is a dictionary)
        
    Returns:
        Dictionary with success status or error
    """
    def _set_third_party_metadata():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Handle both dictionary and key-value formats
        if isinstance(metadata, dict):
            result = clip.SetThirdPartyMetadata(metadata)
        else:
            if metadata_value is None:
                raise ValueError("metadata_value must be provided when metadata is a string")
            result = clip.SetThirdPartyMetadata(metadata, metadata_value)
            
        if not result:
            raise RuntimeError("Failed to set third-party metadata")
            
        return True
    
    return safe_api_call(
        _set_third_party_metadata,
        f"Error setting third-party metadata for clip {clip_id}"
    )

def link_proxy_media(clip_id: str, proxy_media_file_path: str) -> Dict[str, Any]:
    """
    Link proxy media to a clip
    
    Args:
        clip_id: ID of the media pool item
        proxy_media_file_path: Absolute path to the proxy media file
        
    Returns:
        Dictionary with success status or error
    """
    def _link_proxy_media():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Check if the proxy media file exists
        if not os.path.exists(proxy_media_file_path):
            raise FileNotFoundError(f"Proxy media file not found: {proxy_media_file_path}")
            
        result = clip.LinkProxyMedia(proxy_media_file_path)
        if not result:
            raise RuntimeError(f"Failed to link proxy media: {proxy_media_file_path}")
            
        return True
    
    return safe_api_call(
        _link_proxy_media,
        f"Error linking proxy media for clip {clip_id}"
    )

def unlink_proxy_media(clip_id: str) -> Dict[str, Any]:
    """
    Unlink proxy media from a clip
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with success status or error
    """
    def _unlink_proxy_media():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.UnlinkProxyMedia()
        if not result:
            raise RuntimeError("Failed to unlink proxy media")
            
        return True
    
    return safe_api_call(
        _unlink_proxy_media,
        f"Error unlinking proxy media for clip {clip_id}"
    )

def replace_clip(clip_id: str, file_path: str) -> Dict[str, Any]:
    """
    Replace a clip with another file
    
    Args:
        clip_id: ID of the media pool item to replace
        file_path: Absolute path to the new media file
        
    Returns:
        Dictionary with success status or error
    """
    def _replace_clip():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Check if the new media file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Replacement media file not found: {file_path}")
            
        result = clip.ReplaceClip(file_path)
        if not result:
            raise RuntimeError(f"Failed to replace clip with file: {file_path}")
            
        return True
    
    return safe_api_call(
        _replace_clip,
        f"Error replacing clip {clip_id}"
    )

def get_marker_by_custom_data(clip_id: str, custom_data: str) -> Dict[str, Any]:
    """
    Get marker information by custom data
    
    Args:
        clip_id: ID of the media pool item
        custom_data: Custom data string to search for
        
    Returns:
        Dictionary with marker information or error
    """
    def _get_marker_by_custom_data():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        marker_info = clip.GetMarkerByCustomData(custom_data)
        if not marker_info:
            raise RuntimeError(f"No marker found with custom data: {custom_data}")
            
        return marker_info
    
    return safe_api_call(
        _get_marker_by_custom_data,
        f"Error getting marker by custom data for clip {clip_id}"
    )

def update_marker_custom_data(clip_id: str, frame_id: float, custom_data: str) -> Dict[str, Any]:
    """
    Update custom data for a marker at a specific frame
    
    Args:
        clip_id: ID of the media pool item
        frame_id: Frame position of the marker
        custom_data: New custom data to set
        
    Returns:
        Dictionary with success status or error
    """
    def _update_marker_custom_data():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.UpdateMarkerCustomData(frame_id, custom_data)
        if not result:
            raise RuntimeError(f"Failed to update marker custom data at frame {frame_id}")
            
        return True
    
    return safe_api_call(
        _update_marker_custom_data,
        f"Error updating marker custom data for clip {clip_id}"
    )

def get_marker_custom_data(clip_id: str, frame_id: float) -> Dict[str, Any]:
    """
    Get custom data for a marker at a specific frame
    
    Args:
        clip_id: ID of the media pool item
        frame_id: Frame position of the marker
        
    Returns:
        Dictionary with custom data or error
    """
    def _get_marker_custom_data():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetMarkerCustomData(frame_id)
    
    return safe_api_call(
        _get_marker_custom_data,
        f"Error getting marker custom data for clip {clip_id}"
    )

def delete_marker_by_custom_data(clip_id: str, custom_data: str) -> Dict[str, Any]:
    """
    Delete a marker by its custom data
    
    Args:
        clip_id: ID of the media pool item
        custom_data: Custom data string to search for
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_marker_by_custom_data():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.DeleteMarkerByCustomData(custom_data)
        if not result:
            raise RuntimeError(f"Failed to delete marker with custom data: {custom_data}")
            
        return True
    
    return safe_api_call(
        _delete_marker_by_custom_data,
        f"Error deleting marker by custom data for clip {clip_id}"
    )

def transcribe_audio(clip_id: str) -> Dict[str, Any]:
    """
    Transcribe audio for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with success status or error
    """
    def _transcribe_audio():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.TranscribeAudio()
        if not result:
            raise RuntimeError("Failed to transcribe audio")
            
        return True
    
    return safe_api_call(
        _transcribe_audio,
        f"Error transcribing audio for clip {clip_id}"
    )

def clear_transcription(clip_id: str) -> Dict[str, Any]:
    """
    Clear audio transcription for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with success status or error
    """
    def _clear_transcription():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        result = clip.ClearTranscription()
        if not result:
            raise RuntimeError("Failed to clear transcription")
            
        return True
    
    return safe_api_call(
        _clear_transcription,
        f"Error clearing transcription for clip {clip_id}"
    )

def get_audio_mapping(clip_id: str) -> Dict[str, Any]:
    """
    Get audio mapping information for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with audio mapping information or error
    """
    def _get_audio_mapping():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetAudioMapping()
    
    return safe_api_call(
        _get_audio_mapping,
        f"Error getting audio mapping for clip {clip_id}"
    )

def get_mark_in_out(clip_id: str) -> Dict[str, Any]:
    """
    Get in and out point information for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        
    Returns:
        Dictionary with mark in/out information or error
    """
    def _get_mark_in_out():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        return clip.GetMarkInOut()
    
    return safe_api_call(
        _get_mark_in_out,
        f"Error getting mark in/out for clip {clip_id}"
    )

def set_mark_in_out(clip_id: str, mark_in: int, mark_out: int, mark_type: str = "all") -> Dict[str, Any]:
    """
    Set in and out points for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        mark_in: Frame number for the in point
        mark_out: Frame number for the out point
        mark_type: Type of mark in/out to set ("video", "audio", or "all")
        
    Returns:
        Dictionary with success status or error
    """
    def _set_mark_in_out():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Validate mark type
        if mark_type not in ["video", "audio", "all"]:
            raise ValueError(f"Invalid mark type: {mark_type}. Must be 'video', 'audio', or 'all'")
            
        result = clip.SetMarkInOut(mark_in, mark_out, mark_type)
        if not result:
            raise RuntimeError(f"Failed to set {mark_type} mark in/out to {mark_in}/{mark_out}")
            
        return True
    
    return safe_api_call(
        _set_mark_in_out,
        f"Error setting mark in/out for clip {clip_id}"
    )

def clear_mark_in_out(clip_id: str, mark_type: str = "all") -> Dict[str, Any]:
    """
    Clear in and out points for a media pool item
    
    Args:
        clip_id: ID of the media pool item
        mark_type: Type of mark in/out to clear ("video", "audio", or "all")
        
    Returns:
        Dictionary with success status or error
    """
    def _clear_mark_in_out():
        # Get the media pool item
        clip = get_media_pool_item_by_id(clip_id)
        if not clip:
            raise RuntimeError(f"Failed to find clip with ID: {clip_id}")
            
        # Validate mark type
        if mark_type not in ["video", "audio", "all"]:
            raise ValueError(f"Invalid mark type: {mark_type}. Must be 'video', 'audio', or 'all'")
            
        result = clip.ClearMarkInOut(mark_type)
        if not result:
            raise RuntimeError(f"Failed to clear {mark_type} mark in/out")
            
        return True
    
    return safe_api_call(
        _clear_mark_in_out,
        f"Error clearing mark in/out for clip {clip_id}"
    ) 