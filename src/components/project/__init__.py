"""
Project Component for DaVinci Resolve API
Handles project-related operations
"""

import logging
from typing import Dict, Any, List, Optional

from ...resolve_api import get_current_project, safe_api_call

logger = logging.getLogger("resolve_api.project")

__all__ = [
    'get_project_info',
    'get_project_settings',
    'get_all_timelines',
    'set_current_timeline',
    'get_media_pool',
    'get_gallery',
    'set_project_name',
    'save_project_as',
    'get_preset_list',
    'set_preset',
    'add_render_job',
    'delete_render_job',
    'delete_all_render_jobs',
    'get_render_job_list',
    'get_render_preset_list',
    'start_rendering',
    'stop_rendering',
    'is_rendering_in_progress',
    'load_render_preset',
    'save_as_new_render_preset',
    'delete_render_preset',
    'set_render_settings',
    'get_render_job_status',
    'get_render_formats',
    'get_render_codecs',
    'get_current_render_format_and_codec',
    'set_current_render_format_and_codec',
    'get_current_render_mode',
    'set_current_render_mode',
    'get_render_resolutions',
    'refresh_lut_list',
    'get_unique_id',
    'get_quick_export_render_presets',
    'render_with_quick_export',
    'insert_audio_to_current_track_at_playhead',
    'load_burn_in_preset',
    'export_current_frame_as_still',
    'get_color_groups_list',
    'add_color_group',
    'delete_color_group',
    'set_setting'
]

def get_project_info() -> Dict[str, Any]:
    """
    Get information about the current project
    
    Returns:
        Dictionary with project information or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        return {"success": True, "result": {
            "name": project.GetName(),
            "timeline_count": project.GetTimelineCount(),
            "current_timeline": project.GetCurrentTimeline().GetName() if project.GetCurrentTimeline() else None,
            "fps": project.GetSetting("timelineFrameRate"),
            "width": project.GetSetting("timelineResolutionWidth"),
            "height": project.GetSetting("timelineResolutionHeight"),
        }}
    except Exception as e:
        logger.error(f"Error getting project info: {str(e)}")
        return {"success": False, "error": str(e)}

def get_project_settings() -> Dict[str, Any]:
    """
    Get all available settings for the current project
    
    Returns:
        Dictionary with project settings or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        # Common settings to retrieve
        common_settings = [
            "timelineFrameRate",
            "timelineResolutionWidth",
            "timelineResolutionHeight",
            "timelineOutputResolutionWidth",
            "timelineOutputResolutionHeight",
            "videoMonitorFormat",
            "colorScienceMode",
            "timelinePlaybackFrameRate"
        ]
        
        settings = {}
        for setting in common_settings:
            settings[setting] = project.GetSetting(setting)
        
        return {"success": True, "result": settings}
    except Exception as e:
        logger.error(f"Error getting project settings: {str(e)}")
        return {"success": False, "error": str(e)}

def set_setting(setting_name: str, setting_value: str) -> Dict[str, Any]:
    """
    Set a project setting value
    
    Args:
        setting_name: Name of the setting to change
        setting_value: New value for the setting
        
    Returns:
        Dictionary with success status or error
    """
    def _set_setting():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Get the current value for comparison
        old_value = project.GetSetting(setting_name)
        
        # Set the new value
        result = project.SetSetting(setting_name, setting_value)
        if not result:
            raise RuntimeError(f"Failed to set setting '{setting_name}' to '{setting_value}'")
        
        # Read the value back to confirm it was set
        new_value = project.GetSetting(setting_name)
        
        return {
            "success": True,
            "setting_name": setting_name,
            "old_value": old_value,
            "new_value": new_value
        }
    
    return safe_api_call(
        _set_setting,
        f"Error setting project setting '{setting_name}' to '{setting_value}'"
    )

def get_all_timelines() -> Dict[str, Any]:
    """
    Get all timelines in the current project
    
    Returns:
        Dictionary with timeline list or error
    """
    project = get_current_project()
    if not project:
        return {"success": False, "error": "No project is currently open"}
    
    try:
        timeline_count = project.GetTimelineCount()
        timelines = []
        
        for i in range(1, timeline_count + 1):
            timeline = project.GetTimelineByIndex(i)
            if timeline:
                timelines.append({
                    "name": timeline.GetName(),
                    "index": i,
                    "is_current": timeline == project.GetCurrentTimeline()
                })
        
        return {
            "success": True,
            "result": {
                "count": timeline_count,
                "timelines": timelines
            }
        }
    except Exception as e:
        logger.error(f"Error getting timelines: {str(e)}")
        return {"success": False, "error": str(e)}

def get_media_pool() -> Dict[str, Any]:
    """
    Get the media pool object for the current project
    
    Returns:
        Dictionary with media pool info or error
    """
    def _get_media_pool():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
            
        media_pool = project.GetMediaPool()
        if not media_pool:
            raise RuntimeError("Failed to get Media Pool")
        
        # Since we can't return the actual object through MCP, 
        # just return a confirmation that we got it
        return {
            "available": True,
            "root_folder": media_pool.GetRootFolder().GetName() if media_pool.GetRootFolder() else None
        }
    
    return safe_api_call(
        _get_media_pool,
        "Error getting Media Pool"
    )

def set_current_timeline(timeline_name: str) -> Dict[str, Any]:
    """
    Set a timeline as the current timeline by name
    
    Args:
        timeline_name: Name of the timeline to set as current
        
    Returns:
        Dictionary with success status or error
    """
    def _set_current_timeline():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # First get all timelines to find the one with matching name
        timeline_count = project.GetTimelineCount()
        target_timeline = None
        
        for i in range(1, timeline_count + 1):
            timeline = project.GetTimelineByIndex(i)
            if timeline and timeline.GetName() == timeline_name:
                target_timeline = timeline
                break
        
        if not target_timeline:
            raise RuntimeError(f"Timeline '{timeline_name}' not found")
        
        # Set as current timeline
        result = project.SetCurrentTimeline(target_timeline)
        if not result:
            raise RuntimeError(f"Failed to set '{timeline_name}' as current timeline")
        
        return {
            "success": True,
            "timeline_name": timeline_name
        }
    
    return safe_api_call(
        _set_current_timeline,
        f"Error setting timeline '{timeline_name}' as current"
    )

def get_gallery() -> Dict[str, Any]:
    """
    Get the gallery for the current project
    
    Returns:
        Dictionary with gallery information or error
    """
    def _get_gallery():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        gallery = project.GetGallery()
        if not gallery:
            raise RuntimeError("Failed to get Gallery")
        
        # Since we can't return the actual gallery object through MCP,
        # just return confirmation that we got it
        return {
            "available": True
        }
    
    return safe_api_call(
        _get_gallery,
        "Error getting Gallery"
    )

def set_project_name(project_name: str) -> Dict[str, Any]:
    """
    Set the name of the current project
    
    Args:
        project_name: New name for the project
        
    Returns:
        Dictionary with success status or error
    """
    def _set_project_name():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        old_name = project.GetName()
        result = project.SetName(project_name)
        
        if not result:
            raise RuntimeError(f"Failed to set project name to '{project_name}'")
        
        return {
            "success": True,
            "old_name": old_name,
            "new_name": project_name
        }
    
    return safe_api_call(
        _set_project_name,
        f"Error setting project name to '{project_name}'"
    )

def save_project_as(project_name: str) -> Dict[str, Any]:
    """
    Save the current project with a new name (SaveAs)
    
    Args:
        project_name: New name to save the project as
        
    Returns:
        Dictionary with success status or error
    """
    def _save_project_as():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        old_name = project.GetName()
        result = project.SaveAs(project_name)
        
        if not result:
            raise RuntimeError(f"Failed to save project as '{project_name}'")
        
        return {
            "success": True,
            "old_name": old_name,
            "new_name": project_name
        }
    
    return safe_api_call(
        _save_project_as,
        f"Error saving project as '{project_name}'"
    )

def get_preset_list() -> Dict[str, Any]:
    """
    Get the list of available presets for the current project
    
    Returns:
        Dictionary with preset list or error
    """
    def _get_preset_list():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        presets = project.GetPresetList()
        if presets is None:
            raise RuntimeError("Failed to get preset list")
        
        return {
            "presets": presets,
            "count": len(presets)
        }
    
    return safe_api_call(
        _get_preset_list,
        "Error getting preset list"
    )

def set_preset(preset_name: str) -> Dict[str, Any]:
    """
    Apply a preset to the current project
    
    Args:
        preset_name: Name of the preset to apply
        
    Returns:
        Dictionary with success status or error
    """
    def _set_preset():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Verify preset exists
        presets = project.GetPresetList()
        if preset_name not in presets:
            raise RuntimeError(f"Preset '{preset_name}' not found")
        
        result = project.SetPreset(preset_name)
        if not result:
            raise RuntimeError(f"Failed to apply preset '{preset_name}'")
        
        return {
            "success": True,
            "preset_name": preset_name
        }
    
    return safe_api_call(
        _set_preset,
        f"Error applying preset '{preset_name}'"
    )

def add_render_job() -> Dict[str, Any]:
    """
    Add a render job to the render queue based on current render settings
    
    Returns:
        Dictionary with job ID or error
    """
    def _add_render_job():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        job_id = project.AddRenderJob()
        if not job_id:
            raise RuntimeError("Failed to add render job")
        
        return {
            "job_id": job_id,
            "added": True
        }
    
    return safe_api_call(
        _add_render_job,
        "Error adding render job"
    )

def delete_render_job(job_id: str) -> Dict[str, Any]:
    """
    Delete a render job from the render queue
    
    Args:
        job_id: ID of the render job to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_render_job():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.DeleteRenderJob(job_id)
        if not result:
            raise RuntimeError(f"Failed to delete render job '{job_id}'")
        
        return {
            "success": True,
            "job_id": job_id
        }
    
    return safe_api_call(
        _delete_render_job,
        f"Error deleting render job '{job_id}'"
    )

def delete_all_render_jobs() -> Dict[str, Any]:
    """
    Delete all render jobs from the render queue
    
    Returns:
        Dictionary with success status or error
    """
    def _delete_all_render_jobs():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.DeleteAllRenderJobs()
        if not result:
            raise RuntimeError("Failed to delete all render jobs")
        
        return {
            "success": True
        }
    
    return safe_api_call(
        _delete_all_render_jobs,
        "Error deleting all render jobs"
    )

def get_render_job_list() -> Dict[str, Any]:
    """
    Get list of render jobs in the render queue
    
    Returns:
        Dictionary with render job list or error
    """
    def _get_render_job_list():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        jobs = project.GetRenderJobList()
        if jobs is None:
            raise RuntimeError("Failed to get render job list")
        
        return {
            "jobs": jobs,
            "count": len(jobs)
        }
    
    return safe_api_call(
        _get_render_job_list,
        "Error getting render job list"
    )

def get_render_preset_list() -> Dict[str, Any]:
    """
    Get list of available render presets
    
    Returns:
        Dictionary with render preset list or error
    """
    def _get_render_preset_list():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        presets = project.GetRenderPresetList()
        if presets is None:
            raise RuntimeError("Failed to get render preset list")
        
        return {
            "presets": presets,
            "count": len(presets)
        }
    
    return safe_api_call(
        _get_render_preset_list,
        "Error getting render preset list"
    )

def start_rendering(job_ids: Optional[List[str]] = None, is_interactive_mode: bool = False) -> Dict[str, Any]:
    """
    Start rendering specified jobs or all jobs if none specified
    
    Args:
        job_ids: List of job IDs to render (optional)
        is_interactive_mode: Enable error feedback in UI during rendering
        
    Returns:
        Dictionary with success status or error
    """
    def _start_rendering():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = False
        if job_ids:
            # Start specified render jobs
            if len(job_ids) == 1:
                # Handle single job ID case
                result = project.StartRendering(job_ids[0], is_interactive_mode=is_interactive_mode)
            else:
                # Handle multiple job IDs
                result = project.StartRendering(job_ids, is_interactive_mode=is_interactive_mode)
        else:
            # Start all render jobs
            result = project.StartRendering(is_interactive_mode=is_interactive_mode)
        
        if not result:
            raise RuntimeError("Failed to start rendering")
        
        return {
            "success": True,
            "job_ids": job_ids if job_ids else "all",
            "interactive_mode": is_interactive_mode
        }
    
    return safe_api_call(
        _start_rendering,
        "Error starting rendering"
    )

def stop_rendering() -> Dict[str, Any]:
    """
    Stop any current rendering processes
    
    Returns:
        Dictionary with success status or error
    """
    def _stop_rendering():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        project.StopRendering()
        
        return {
            "success": True
        }
    
    return safe_api_call(
        _stop_rendering,
        "Error stopping rendering"
    )

def is_rendering_in_progress() -> Dict[str, Any]:
    """
    Check if rendering is currently in progress
    
    Returns:
        Dictionary with rendering status or error
    """
    def _is_rendering_in_progress():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        status = project.IsRenderingInProgress()
        
        return {
            "in_progress": status
        }
    
    return safe_api_call(
        _is_rendering_in_progress,
        "Error checking rendering status"
    )

def load_render_preset(preset_name: str) -> Dict[str, Any]:
    """
    Load a render preset as the current render preset
    
    Args:
        preset_name: Name of the render preset to load
        
    Returns:
        Dictionary with success status or error
    """
    def _load_render_preset():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.LoadRenderPreset(preset_name)
        if not result:
            raise RuntimeError(f"Failed to load render preset '{preset_name}'")
        
        return {
            "success": True,
            "preset_name": preset_name
        }
    
    return safe_api_call(
        _load_render_preset,
        f"Error loading render preset '{preset_name}'"
    )

def save_as_new_render_preset(preset_name: str) -> Dict[str, Any]:
    """
    Save current render settings as a new render preset
    
    Args:
        preset_name: Name for the new render preset
        
    Returns:
        Dictionary with success status or error
    """
    def _save_as_new_render_preset():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.SaveAsNewRenderPreset(preset_name)
        if not result:
            raise RuntimeError(f"Failed to save render preset '{preset_name}'")
        
        return {
            "success": True,
            "preset_name": preset_name
        }
    
    return safe_api_call(
        _save_as_new_render_preset,
        f"Error saving render preset '{preset_name}'"
    )

def delete_render_preset(preset_name: str) -> Dict[str, Any]:
    """
    Delete a render preset
    
    Args:
        preset_name: Name of the render preset to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_render_preset():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.DeleteRenderPreset(preset_name)
        if not result:
            raise RuntimeError(f"Failed to delete render preset '{preset_name}'")
        
        return {
            "success": True,
            "preset_name": preset_name
        }
    
    return safe_api_call(
        _delete_render_preset,
        f"Error deleting render preset '{preset_name}'"
    )

def set_render_settings(settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Set render settings for the current project
    
    Args:
        settings: Dictionary of render settings to apply
        
    Returns:
        Dictionary with success status or error
    """
    def _set_render_settings():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.SetRenderSettings(settings)
        if not result:
            raise RuntimeError("Failed to set render settings")
        
        return {
            "success": True,
            "settings": settings
        }
    
    return safe_api_call(
        _set_render_settings,
        "Error setting render settings"
    )

def get_render_job_status(job_id: str) -> Dict[str, Any]:
    """
    Get the status of a render job
    
    Args:
        job_id: ID of the render job to check
        
    Returns:
        Dictionary with job status or error
    """
    def _get_render_job_status():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        status = project.GetRenderJobStatus(job_id)
        if status is None:
            raise RuntimeError(f"Failed to get status for render job '{job_id}'")
        
        return status
    
    return safe_api_call(
        _get_render_job_status,
        f"Error getting status for render job '{job_id}'"
    )

def get_quick_export_render_presets() -> Dict[str, Any]:
    """
    Get list of available quick export render presets
    
    Returns:
        Dictionary with quick export render preset list or error
    """
    def _get_quick_export_render_presets():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        presets = project.GetQuickExportRenderPresets()
        if presets is None:
            raise RuntimeError("Failed to get quick export render presets")
        
        return {
            "presets": presets,
            "count": len(presets)
        }
    
    return safe_api_call(
        _get_quick_export_render_presets,
        "Error getting quick export render presets"
    )

def render_with_quick_export(preset_name: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Render current timeline using quick export with specified preset
    
    Args:
        preset_name: Name of the quick export preset to use
        params: Optional parameters for the quick export (TargetDir, CustomName, VideoQuality, EnableUpload)
        
    Returns:
        Dictionary with render result or error
    """
    def _render_with_quick_export():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Default empty params dict if none provided
        if params is None:
            params = {}
        
        result = project.RenderWithQuickExport(preset_name, params)
        if not result:
            raise RuntimeError(f"Failed to render with quick export preset '{preset_name}'")
        
        return result
    
    return safe_api_call(
        _render_with_quick_export,
        f"Error rendering with quick export preset '{preset_name}'"
    )

def get_render_formats() -> Dict[str, Any]:
    """
    Get list of available render formats
    
    Returns:
        Dictionary with render formats or error
    """
    def _get_render_formats():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        formats = project.GetRenderFormats()
        if formats is None:
            raise RuntimeError("Failed to get render formats")
        
        return {
            "formats": formats,
            "count": len(formats)
        }
    
    return safe_api_call(
        _get_render_formats,
        "Error getting render formats"
    )

def get_render_codecs(render_format: str) -> Dict[str, Any]:
    """
    Get list of available render codecs for the specified format
    
    Args:
        render_format: Render format to get codecs for
        
    Returns:
        Dictionary with render codecs or error
    """
    def _get_render_codecs():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        codecs = project.GetRenderCodecs(render_format)
        if codecs is None:
            raise RuntimeError(f"Failed to get render codecs for format '{render_format}'")
        
        return {
            "format": render_format,
            "codecs": codecs,
            "count": len(codecs)
        }
    
    return safe_api_call(
        _get_render_codecs,
        f"Error getting render codecs for format '{render_format}'"
    )

def get_current_render_format_and_codec() -> Dict[str, Any]:
    """
    Get currently selected render format and codec
    
    Returns:
        Dictionary with current render format and codec or error
    """
    def _get_current_render_format_and_codec():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        format_codec = project.GetCurrentRenderFormatAndCodec()
        if format_codec is None:
            raise RuntimeError("Failed to get current render format and codec")
        
        return format_codec
    
    return safe_api_call(
        _get_current_render_format_and_codec,
        "Error getting current render format and codec"
    )

def set_current_render_format_and_codec(format_name: str, codec_name: str) -> Dict[str, Any]:
    """
    Set render format and codec
    
    Args:
        format_name: Name of the render format
        codec_name: Name of the render codec
        
    Returns:
        Dictionary with success status or error
    """
    def _set_current_render_format_and_codec():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.SetCurrentRenderFormatAndCodec(format_name, codec_name)
        if not result:
            raise RuntimeError(f"Failed to set render format '{format_name}' and codec '{codec_name}'")
        
        return {
            "success": True,
            "format": format_name,
            "codec": codec_name
        }
    
    return safe_api_call(
        _set_current_render_format_and_codec,
        f"Error setting render format '{format_name}' and codec '{codec_name}'"
    )

def get_current_render_mode() -> Dict[str, Any]:
    """
    Get current render mode (0 for Individual clips, 1 for Single clip)
    
    Returns:
        Dictionary with render mode or error
    """
    def _get_current_render_mode():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        mode = project.GetCurrentRenderMode()
        
        # Convert numeric mode to descriptive value
        mode_description = "Individual clips" if mode == 0 else "Single clip"
        
        return {
            "mode": mode,
            "description": mode_description
        }
    
    return safe_api_call(
        _get_current_render_mode,
        "Error getting current render mode"
    )

def set_current_render_mode(render_mode: int) -> Dict[str, Any]:
    """
    Set render mode
    
    Args:
        render_mode: 0 for Individual clips, 1 for Single clip
        
    Returns:
        Dictionary with success status or error
    """
    def _set_current_render_mode():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Validate render mode
        if render_mode not in [0, 1]:
            raise ValueError("Render mode must be 0 (Individual clips) or 1 (Single clip)")
        
        result = project.SetCurrentRenderMode(render_mode)
        if not result:
            raise RuntimeError(f"Failed to set render mode to {render_mode}")
        
        # Convert numeric mode to descriptive value
        mode_description = "Individual clips" if render_mode == 0 else "Single clip"
        
        return {
            "success": True,
            "mode": render_mode,
            "description": mode_description
        }
    
    return safe_api_call(
        _set_current_render_mode,
        f"Error setting render mode to {render_mode}"
    )

def get_render_resolutions(format_name: Optional[str] = None, codec_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Get available render resolutions for the specified format and codec
    
    Args:
        format_name: Render format (optional)
        codec_name: Render codec (optional)
        
    Returns:
        Dictionary with render resolutions or error
    """
    def _get_render_resolutions():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # Get resolutions based on provided parameters
        if format_name and codec_name:
            resolutions = project.GetRenderResolutions(format_name, codec_name)
        else:
            resolutions = project.GetRenderResolutions()
        
        if resolutions is None:
            raise RuntimeError("Failed to get render resolutions")
        
        return {
            "format": format_name,
            "codec": codec_name,
            "resolutions": resolutions,
            "count": len(resolutions)
        }
    
    return safe_api_call(
        _get_render_resolutions,
        "Error getting render resolutions"
    )

def refresh_lut_list() -> Dict[str, Any]:
    """
    Refresh the LUT list
    
    Returns:
        Dictionary with success status or error
    """
    def _refresh_lut_list():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.RefreshLUTList()
        if not result:
            raise RuntimeError("Failed to refresh LUT list")
        
        return {
            "success": True
        }
    
    return safe_api_call(
        _refresh_lut_list,
        "Error refreshing LUT list"
    )

def get_unique_id() -> Dict[str, Any]:
    """
    Get unique ID for the project
    
    Returns:
        Dictionary with project ID or error
    """
    def _get_unique_id():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        project_id = project.GetUniqueId()
        if not project_id:
            raise RuntimeError("Failed to get project unique ID")
        
        return {
            "id": project_id
        }
    
    return safe_api_call(
        _get_unique_id,
        "Error getting project unique ID"
    )

def insert_audio_to_current_track_at_playhead(
    media_path: str,
    start_offset_in_samples: int,
    duration_in_samples: int
) -> Dict[str, Any]:
    """
    Insert audio file to current track at playhead on Fairlight page
    
    Args:
        media_path: Path to the audio file
        start_offset_in_samples: Start offset in samples
        duration_in_samples: Duration in samples
        
    Returns:
        Dictionary with success status or error
    """
    def _insert_audio():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.InsertAudioToCurrentTrackAtPlayhead(
            media_path,
            start_offset_in_samples,
            duration_in_samples
        )
        if not result:
            raise RuntimeError("Failed to insert audio")
        
        return {
            "success": True,
            "media_path": media_path,
            "start_offset": start_offset_in_samples,
            "duration": duration_in_samples
        }
    
    return safe_api_call(
        _insert_audio,
        "Error inserting audio"
    )

def load_burn_in_preset(preset_name: str) -> Dict[str, Any]:
    """
    Load burn-in preset for the project
    
    Args:
        preset_name: Name of the burn-in preset to load
        
    Returns:
        Dictionary with success status or error
    """
    def _load_burn_in_preset():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.LoadBurnInPreset(preset_name)
        if not result:
            raise RuntimeError(f"Failed to load burn-in preset '{preset_name}'")
        
        return {
            "success": True,
            "preset_name": preset_name
        }
    
    return safe_api_call(
        _load_burn_in_preset,
        f"Error loading burn-in preset '{preset_name}'"
    )

def export_current_frame_as_still(file_path: str) -> Dict[str, Any]:
    """
    Export current frame as still image
    
    Args:
        file_path: Path to save the still image
        
    Returns:
        Dictionary with success status or error
    """
    def _export_current_frame_as_still():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        result = project.ExportCurrentFrameAsStill(file_path)
        if not result:
            raise RuntimeError(f"Failed to export current frame to '{file_path}'")
        
        return {
            "success": True,
            "file_path": file_path
        }
    
    return safe_api_call(
        _export_current_frame_as_still,
        f"Error exporting current frame to '{file_path}'"
    )

def get_color_groups_list() -> Dict[str, Any]:
    """
    Get list of color groups in the project
    
    Returns:
        Dictionary with color groups or error
    """
    def _get_color_groups_list():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        groups = project.GetColorGroupsList()
        if groups is None:
            raise RuntimeError("Failed to get color groups list")
        
        # Since we can't return the actual group objects through MCP,
        # just return the count
        return {
            "count": len(groups),
            "groups_available": True
        }
    
    return safe_api_call(
        _get_color_groups_list,
        "Error getting color groups list"
    )

def add_color_group(group_name: str) -> Dict[str, Any]:
    """
    Add a new color group to the project
    
    Args:
        group_name: Name for the new color group
        
    Returns:
        Dictionary with success status or error
    """
    def _add_color_group():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        group = project.AddColorGroup(group_name)
        if not group:
            raise RuntimeError(f"Failed to add color group '{group_name}'")
        
        return {
            "success": True,
            "group_name": group_name
        }
    
    return safe_api_call(
        _add_color_group,
        f"Error adding color group '{group_name}'"
    )

def delete_color_group(group_name: str) -> Dict[str, Any]:
    """
    Delete a color group by name
    
    Args:
        group_name: Name of the color group to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_color_group():
        project = get_current_project()
        if not project:
            raise RuntimeError("No project is currently open")
        
        # We need to find the group object by name first
        groups = project.GetColorGroupsList()
        target_group = None
        
        # Find the group with the matching name
        for group in groups:
            if group.GetName() == group_name:
                target_group = group
                break
        
        if not target_group:
            raise RuntimeError(f"Color group '{group_name}' not found")
        
        result = project.DeleteColorGroup(target_group)
        if not result:
            raise RuntimeError(f"Failed to delete color group '{group_name}'")
        
        return {
            "success": True,
            "group_name": group_name
        }
    
    return safe_api_call(
        _delete_color_group,
        f"Error deleting color group '{group_name}'"
    ) 