"""
Tools Registration Module
Registers all tool functions and makes them available to the MCP server
"""

import logging
from typing import Dict, Any, List, Callable

# Import tool modules
from .resolve import (
    get_product_info,
    get_current_page,
    open_page,
    get_keyframe_mode,
    set_keyframe_mode,
    manage_layout_preset,
    manage_render_preset,
    manage_burn_in_preset,
    quit_resolve
)

# Import component functions
from ..components.project_manager import (
    create_project,
    delete_project,
    load_project,
    save_project,
    close_project,
    archive_project,
    import_project,
    export_project,
    restore_project,
    get_project_list,
    get_folder_list,
    get_current_folder,
    create_folder,
    delete_folder,
    open_folder,
    goto_root_folder,
    goto_parent_folder,
    get_current_database,
    get_database_list,
    set_current_database,
    create_cloud_project,
    load_cloud_project,
    import_cloud_project,
    restore_cloud_project
)

# Import component functions - Project component
from ..components.project import (
    get_project_info,
    get_project_settings,
    get_all_timelines,
    get_media_pool,
    set_current_timeline,
    get_gallery,
    set_project_name,
    get_preset_list,
    set_preset,
    save_project_as,
    add_render_job,
    delete_render_job,
    delete_all_render_jobs,
    get_render_job_list,
    get_render_preset_list,
    start_rendering,
    stop_rendering,
    is_rendering_in_progress,
    load_render_preset,
    save_as_new_render_preset,
    delete_render_preset,
    set_render_settings,
    get_render_job_status,
    get_quick_export_render_presets,
    render_with_quick_export,
    get_render_formats,
    get_render_codecs,
    get_current_render_format_and_codec,
    set_current_render_format_and_codec,
    get_current_render_mode,
    set_current_render_mode,
    get_render_resolutions,
    refresh_lut_list,
    get_unique_id,
    insert_audio_to_current_track_at_playhead,
    load_burn_in_preset,
    export_current_frame_as_still,
    get_color_groups_list,
    add_color_group,
    delete_color_group,
    set_setting
)

# Import component functions - MediaStorage component
from ..components.media_storage import (
    get_mounted_volumes,
    get_subfolder_list,
    get_file_list,
    reveal_in_storage,
    add_items_to_media_pool,
    add_clip_mattes_to_media_pool,
    add_timeline_mattes_to_media_pool
)

# Import component functions - MediaPool component
from ..components.media_pool import (
    list_media_pool_items,
    get_folder_structure,
    get_root_folder,
    add_subfolder,
    refresh_folders,
    create_empty_timeline,
    import_media,
    delete_clips,
    get_current_folder as get_media_pool_current_folder,
    set_current_folder as set_media_pool_current_folder,
    import_timeline_from_file,
    create_timeline_from_clips,
    append_to_timeline,
    append_all_clips_to_timeline,
    delete_timelines,
    delete_folders,
    auto_sync_audio,
    get_selected_clips,
    set_selected_clip,
    import_folder_from_file,
    move_clips,
    move_folders,
    get_clip_matte_list,
    get_timeline_matte_list,
    delete_clip_mattes,
    relink_clips,
    unlink_clips,
    export_metadata,
    create_stereo_clip
)

# Import component functions - MediaPoolItem component
from ..components.media_pool_item import (
    get_name,
    get_metadata,
    set_metadata,
    get_third_party_metadata,
    set_third_party_metadata,
    get_media_id,
    add_marker,
    get_markers,
    get_marker_by_custom_data,
    update_marker_custom_data,
    get_marker_custom_data,
    delete_markers_by_color,
    delete_marker_at_frame,
    delete_marker_by_custom_data,
    add_flag,
    get_flag_list,
    clear_flags,
    get_clip_color,
    set_clip_color,
    clear_clip_color,
    get_clip_property,
    set_clip_property,
    link_proxy_media,
    unlink_proxy_media,
    replace_clip,
    get_unique_id,
    transcribe_audio,
    clear_transcription,
    get_audio_mapping,
    get_mark_in_out,
    set_mark_in_out,
    clear_mark_in_out
)

# Import Timeline component functions
from ..components.timeline import (
    get_timeline_details,
    get_timeline_tracks,
    get_timeline_items,
    get_current_video_item,
    get_timeline_items_in_range,
    add_track,
    delete_track,
    delete_timeline_clips,
    set_current_timecode,
    set_track_enable,
    set_track_lock,
    add_marker,
    get_markers,
    get_marker_by_custom_data,
    update_marker_custom_data,
    get_marker_custom_data,
    delete_markers_by_color,
    delete_marker_at_frame,
    delete_marker_by_custom_data,
    set_name,
    get_track_name,
    set_track_name,
    create_compound_clip,
    get_current_timecode,
    duplicate_timeline,
    export_timeline,
    get_timeline_setting,
    set_timeline_setting,
    insert_generator_into_timeline,
    insert_fusion_generator_into_timeline,
    insert_fusion_composition_into_timeline,
    insert_ofx_generator_into_timeline,
    insert_title_into_timeline,
    insert_fusion_title_into_timeline,
    grab_still,
    grab_all_stills,
    # New functions
    set_start_timecode,
    set_clips_linked,
    get_current_video_item,
    get_current_clip_thumbnail_image,
    create_fusion_clip,
    import_into_timeline,
    get_timeline_items_in_range
)

# Import the timeline_item component functions
from ..components.timeline_item import (
    get_timeline_item,
    get_duration,
    get_start,
    get_end,
    get_left_offset,
    get_right_offset,
    get_source_start_frame,
    get_source_end_frame,
    get_source_start_time,
    get_source_end_time,
    get_property,
    set_property,
    set_start,
    set_end,
    set_left_offset,
    set_right_offset,
    add_flag,
    get_flags,
    clear_flags,
    get_clip_color,
    set_clip_color,
    clear_clip_color,
    add_fusion_comp,
    rename_fusion_comp,
    get_scale,
    get_is_filler,
    has_video_effect,
    has_audio_effect,
    has_video_effect_at_offset,
    has_audio_effect_at_offset,
    add_take,
    get_selected_take_index,
    get_takes_count,
    get_take_by_index,
    delete_take_by_index,
    select_take_by_index,
    finalize_take,
    set_clip_enabled,
    get_clip_enabled,
    update_sidecar,
    get_unique_id,
    copy_grades
)

# Add import for Gallery component functions
from ..components.gallery import (
    get_album_name,
    set_album_name,
    get_current_still_album,
    set_current_still_album,
    get_gallery_still_albums,
    get_gallery_power_grade_albums,
    create_gallery_still_album,
    create_gallery_power_grade_album
)

# Add import for GalleryStillAlbum component functions
from ..components.gallery_still_album import (
    get_stills,
    get_label,
    set_label,
    import_stills,
    export_stills,
    delete_stills
)
from ..components.graph import (
    get_num_nodes, set_lut, get_lut, set_node_cache_mode, get_node_cache_mode,
    get_node_label, get_tools_in_node, set_node_enabled, apply_grade_from_drx,
    apply_arri_cdl_lut, reset_all_grades
)
from ..components.color_group import (
    get_name, set_name, get_clips_in_timeline, get_pre_clip_node_graph, get_post_clip_node_graph
)
from ..components.folder import (
    get_clip_list, get_name, get_subfolder_list, get_is_folder_stale,
    get_unique_id, export_folder, transcribe_audio, clear_transcription
)

logger = logging.getLogger("resolve_api.tools.registration")

# Tool registry dictionary
# Maps tool IDs to function references and metadata
TOOLS_REGISTRY = {
    # Resolve general tools
    "get_product_info": {
        "name": "get_product_info",
        "description": "Get DaVinci Resolve product information (name and version)",
        "component": "resolve",
        "function": get_product_info,
        "parameters": []
    },
    "get_current_page": {
        "name": "get_current_page",
        "description": "Get the current page displayed in DaVinci Resolve",
        "component": "resolve",
        "function": get_current_page,
        "parameters": []
    },
    "open_page": {
        "name": "open_page",
        "description": "Switch to the specified page in DaVinci Resolve",
        "component": "resolve",
        "function": open_page,
        "parameters": [
            {"name": "page_name", "type": "string", "description": "Page name (media, cut, edit, fusion, color, fairlight, deliver)", "required": True}
        ]
    },
    "get_keyframe_mode": {
        "name": "get_keyframe_mode",
        "description": "Get the current keyframe mode",
        "component": "resolve",
        "function": get_keyframe_mode,
        "parameters": []
    },
    "set_keyframe_mode": {
        "name": "set_keyframe_mode",
        "description": "Set the keyframe mode",
        "component": "resolve",
        "function": set_keyframe_mode,
        "parameters": [
            {"name": "mode", "type": "string or integer", "description": "Keyframe mode (0-3 or 'All', 'All+Dynamic', 'Selected', 'Selected+Dynamic')", "required": True}
        ]
    },
    "manage_layout_preset": {
        "name": "manage_layout_preset",
        "description": "Manage layout presets (load, save, update, delete, import, export)",
        "component": "resolve",
        "function": manage_layout_preset,
        "parameters": [
            {"name": "action", "type": "string", "description": "Action to perform (load, save, update, delete, import, export)", "required": True},
            {"name": "preset_name", "type": "string", "description": "Name of the preset", "required": True},
            {"name": "file_path", "type": "string", "description": "File path for import/export operations", "required": False}
        ]
    },
    "manage_render_preset": {
        "name": "manage_render_preset",
        "description": "Manage render presets (import, export)",
        "component": "resolve",
        "function": manage_render_preset,
        "parameters": [
            {"name": "action", "type": "string", "description": "Action to perform (import, export)", "required": True},
            {"name": "preset_path", "type": "string", "description": "Path for import operation", "required": False},
            {"name": "preset_name", "type": "string", "description": "Name of the preset for export", "required": False},
            {"name": "export_path", "type": "string", "description": "Path for export operation", "required": False}
        ]
    },
    "manage_burn_in_preset": {
        "name": "manage_burn_in_preset",
        "description": "Manage burn-in presets (import, export)",
        "component": "resolve",
        "function": manage_burn_in_preset,
        "parameters": [
            {"name": "action", "type": "string", "description": "Action to perform (import, export)", "required": True},
            {"name": "preset_path", "type": "string", "description": "Path for import operation", "required": False},
            {"name": "preset_name", "type": "string", "description": "Name of the preset for export", "required": False},
            {"name": "export_path", "type": "string", "description": "Path for export operation", "required": False}
        ]
    },
    "quit_resolve": {
        "name": "quit_resolve",
        "description": "Quit DaVinci Resolve application",
        "component": "resolve",
        "function": quit_resolve,
        "parameters": []
    },
    
    # ProjectManager tools
    "create_project": {
        "name": "create_project",
        "description": "Create a new project with the specified name",
        "component": "project_manager",
        "function": create_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name for the new project", "required": True}
        ]
    },
    "load_project": {
        "name": "load_project",
        "description": "Load an existing project with the specified name",
        "component": "project_manager",
        "function": load_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the project to load", "required": True}
        ]
    },
    "save_project": {
        "name": "save_project",
        "description": "Save the currently loaded project",
        "component": "project_manager",
        "function": save_project,
        "parameters": []
    },
    "close_project": {
        "name": "close_project",
        "description": "Close the currently loaded project without saving",
        "component": "project_manager",
        "function": close_project,
        "parameters": []
    },
    "get_project_list": {
        "name": "get_project_list",
        "description": "Get a list of all projects in the current folder",
        "component": "project_manager",
        "function": get_project_list,
        "parameters": []
    },
    "get_folder_list": {
        "name": "get_folder_list",
        "description": "Get a list of all folders in the current folder",
        "component": "project_manager",
        "function": get_folder_list,
        "parameters": []
    },
    "get_current_folder": {
        "name": "get_current_folder",
        "description": "Get the name of the current folder in the project manager",
        "component": "project_manager",
        "function": get_current_folder,
        "parameters": []
    },
    "create_folder": {
        "name": "create_folder",
        "description": "Create a new folder in the current location",
        "component": "project_manager",
        "function": create_folder,
        "parameters": [
            {"name": "folder_name", "type": "string", "description": "Name for the new folder", "required": True}
        ]
    },
    "open_folder": {
        "name": "open_folder",
        "description": "Open a folder with the specified name",
        "component": "project_manager",
        "function": open_folder,
        "parameters": [
            {"name": "folder_name", "type": "string", "description": "Name of the folder to open", "required": True}
        ]
    },
    "goto_root_folder": {
        "name": "goto_root_folder",
        "description": "Navigate to the root folder in the database",
        "component": "project_manager",
        "function": goto_root_folder,
        "parameters": []
    },
    "goto_parent_folder": {
        "name": "goto_parent_folder",
        "description": "Navigate to the parent folder of the current folder",
        "component": "project_manager",
        "function": goto_parent_folder,
        "parameters": []
    },
    
    # Additional ProjectManager tools
    "delete_project": {
        "name": "delete_project",
        "description": "Delete a project with the specified name",
        "component": "project_manager",
        "function": delete_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the project to delete", "required": True}
        ]
    },
    "archive_project": {
        "name": "archive_project",
        "description": "Archive a project to a file",
        "component": "project_manager",
        "function": archive_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the project to archive", "required": True},
            {"name": "file_path", "type": "string", "description": "Path to save the archive", "required": True},
            {"name": "archive_src_media", "type": "boolean", "description": "Include source media", "required": False},
            {"name": "archive_render_cache", "type": "boolean", "description": "Include render cache", "required": False},
            {"name": "archive_proxy_media", "type": "boolean", "description": "Include proxy media", "required": False}
        ]
    },
    "delete_folder": {
        "name": "delete_folder",
        "description": "Delete a folder with the specified name",
        "component": "project_manager",
        "function": delete_folder,
        "parameters": [
            {"name": "folder_name", "type": "string", "description": "Name of the folder to delete", "required": True}
        ]
    },
    "import_project": {
        "name": "import_project",
        "description": "Import a project from a file",
        "component": "project_manager",
        "function": import_project,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to the project file", "required": True},
            {"name": "project_name", "type": "string", "description": "New name for the imported project", "required": False}
        ]
    },
    "export_project": {
        "name": "export_project",
        "description": "Export a project to a file",
        "component": "project_manager",
        "function": export_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the project to export", "required": True},
            {"name": "file_path", "type": "string", "description": "Path to save the exported project", "required": True},
            {"name": "with_stills_and_luts", "type": "boolean", "description": "Include stills and LUTs", "required": False}
        ]
    },
    "restore_project": {
        "name": "restore_project",
        "description": "Restore a project from a backup",
        "component": "project_manager",
        "function": restore_project,
        "parameters": [
            {"name": "backup_path", "type": "string", "description": "Path to the backup file", "required": True},
            {"name": "project_name", "type": "string", "description": "Name for the restored project", "required": False}
        ]
    },
    "get_current_database": {
        "name": "get_current_database",
        "description": "Get the name of the current database",
        "component": "project_manager",
        "function": get_current_database,
        "parameters": []
    },
    "get_database_list": {
        "name": "get_database_list",
        "description": "Get a list of all available databases",
        "component": "project_manager",
        "function": get_database_list,
        "parameters": []
    },
    "set_current_database": {
        "name": "set_current_database",
        "description": "Set the current database by name",
        "component": "project_manager",
        "function": set_current_database,
        "parameters": [
            {"name": "db_info", "type": "object", "description": "Database info object with DbType and DbName keys", "required": True}
        ]
    },
    "create_cloud_project": {
        "name": "create_cloud_project",
        "description": "Create a new project in DaVinci Resolve cloud database",
        "component": "project_manager",
        "function": create_cloud_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name for the new cloud project", "required": True},
            {"name": "location_path", "type": "string", "description": "Cloud location path", "required": True}
        ]
    },
    "load_cloud_project": {
        "name": "load_cloud_project",
        "description": "Load a project from DaVinci Resolve cloud database",
        "component": "project_manager",
        "function": load_cloud_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the cloud project to load", "required": True},
            {"name": "location_path", "type": "string", "description": "Cloud location path", "required": True}
        ]
    },
    "import_cloud_project": {
        "name": "import_cloud_project",
        "description": "Import a project from DaVinci Resolve cloud database to local database",
        "component": "project_manager",
        "function": import_cloud_project,
        "parameters": [
            {"name": "project_name", "type": "string", "description": "Name of the cloud project to import", "required": True},
            {"name": "location_path", "type": "string", "description": "Cloud location path", "required": True},
            {"name": "local_folder_path", "type": "string", "description": "Local folder path", "required": True}
        ]
    },
    "restore_cloud_project": {
        "name": "restore_cloud_project",
        "description": "Restore a project from DaVinci Resolve cloud database",
        "component": "project_manager",
        "function": restore_cloud_project,
        "parameters": [
            {"name": "backup_id", "type": "string", "description": "ID of the backup to restore", "required": True},
            {"name": "location_path", "type": "string", "description": "Cloud location path", "required": True}
        ]
    },

    # Project tools
    "get_project_info": {
        "name": "get_project_info",
        "description": "Get information about the current project",
        "component": "project",
        "function": get_project_info,
        "parameters": []
    },
    "get_project_settings": {
        "name": "get_project_settings",
        "description": "Get all settings for the current project",
        "component": "project",
        "function": get_project_settings,
        "parameters": {}
    },
    "get_all_timelines": {
        "name": "get_all_timelines",
        "description": "Get a list of all timelines in the current project",
        "component": "project",
        "function": get_all_timelines,
        "parameters": []
    },
    "get_media_pool": {
        "name": "get_media_pool",
        "description": "Get the media pool for the current project",
        "component": "project",
        "function": get_media_pool,
        "parameters": []
    },
    "set_current_timeline": {
        "name": "set_current_timeline",
        "description": "Set a timeline as the current timeline",
        "component": "project",
        "function": set_current_timeline,
        "parameters": [
            {"name": "timeline_name", "type": "string", "description": "Name of the timeline to set as current", "required": True}
        ]
    },
    "get_gallery": {
        "name": "get_gallery",
        "description": "Get the gallery for the current project",
        "component": "project",
        "function": get_gallery,
        "parameters": []
    },
    "set_project_name": {
        "name": "set_project_name",
        "description": "Set the name of the current project",
        "component": "project",
        "function": set_project_name,
        "parameters": {
            "project_name": {
                "type": "string",
                "description": "New name for the project",
                "required": True
            }
        }
    },
    "save_project_as": {
        "name": "save_project_as",
        "description": "Save the current project with a new name",
        "component": "project",
        "function": save_project_as,
        "parameters": {
            "project_name": {
                "type": "string",
                "description": "New name to save the project as",
                "required": True
            }
        }
    },
    "get_preset_list": {
        "name": "get_preset_list",
        "description": "Get the list of available presets for the current project",
        "component": "project",
        "function": get_preset_list,
        "parameters": []
    },
    "set_preset": {
        "name": "set_preset",
        "description": "Apply a preset to the current project",
        "component": "project",
        "function": set_preset,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name of the preset to apply", "required": True}
        ]
    },
    "add_render_job": {
        "name": "add_render_job",
        "description": "Add a render job to the render queue",
        "component": "project",
        "function": add_render_job,
        "parameters": []
    },
    "delete_render_job": {
        "name": "delete_render_job",
        "description": "Delete a render job from the render queue",
        "component": "project",
        "function": delete_render_job,
        "parameters": [
            {"name": "job_id", "type": "string", "description": "ID of the render job to delete", "required": True}
        ]
    },
    "delete_all_render_jobs": {
        "name": "delete_all_render_jobs",
        "description": "Delete all render jobs from the render queue",
        "component": "project",
        "function": delete_all_render_jobs,
        "parameters": []
    },
    "get_render_job_list": {
        "name": "get_render_job_list",
        "description": "Get list of render jobs in the render queue",
        "component": "project",
        "function": get_render_job_list,
        "parameters": []
    },
    "get_render_preset_list": {
        "name": "get_render_preset_list",
        "description": "Get list of available render presets",
        "component": "project",
        "function": get_render_preset_list,
        "parameters": []
    },
    "start_rendering": {
        "name": "start_rendering",
        "description": "Start rendering specified jobs or all jobs",
        "component": "project",
        "function": start_rendering,
        "parameters": [
            {"name": "job_ids", "type": "array", "description": "List of job IDs to render (optional)", "required": False},
            {"name": "is_interactive_mode", "type": "boolean", "description": "Enable error feedback in UI during rendering", "required": False}
        ]
    },
    "stop_rendering": {
        "name": "stop_rendering",
        "description": "Stop any current rendering processes",
        "component": "project",
        "function": stop_rendering,
        "parameters": []
    },
    "is_rendering_in_progress": {
        "name": "is_rendering_in_progress",
        "description": "Check if rendering is currently in progress",
        "component": "project",
        "function": is_rendering_in_progress,
        "parameters": []
    },
    "load_render_preset": {
        "name": "load_render_preset",
        "description": "Load a render preset as the current render preset",
        "component": "project",
        "function": load_render_preset,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name of the render preset to load", "required": True}
        ]
    },
    "save_as_new_render_preset": {
        "name": "save_as_new_render_preset",
        "description": "Save current render settings as a new render preset",
        "component": "project",
        "function": save_as_new_render_preset,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name for the new render preset", "required": True}
        ]
    },
    "delete_render_preset": {
        "name": "delete_render_preset",
        "description": "Delete a render preset",
        "component": "project",
        "function": delete_render_preset,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name of the render preset to delete", "required": True}
        ]
    },
    "set_render_settings": {
        "name": "set_render_settings",
        "description": "Set render settings for the current project",
        "component": "project",
        "function": set_render_settings,
        "parameters": [
            {"name": "settings", "type": "object", "description": "Dictionary of render settings to apply", "required": True}
        ]
    },
    "get_render_job_status": {
        "name": "get_render_job_status",
        "description": "Get the status of a render job",
        "component": "project",
        "function": get_render_job_status,
        "parameters": [
            {"name": "job_id", "type": "string", "description": "ID of the render job to check", "required": True}
        ]
    },
    "get_quick_export_render_presets": {
        "name": "get_quick_export_render_presets",
        "description": "Get list of available quick export render presets",
        "component": "project",
        "function": get_quick_export_render_presets,
        "parameters": []
    },
    "render_with_quick_export": {
        "name": "render_with_quick_export",
        "description": "Render current timeline using quick export with specified preset",
        "component": "project",
        "function": render_with_quick_export,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name of the quick export preset to use", "required": True},
            {"name": "params", "type": "object", "description": "Parameters for the quick export (TargetDir, CustomName, VideoQuality, EnableUpload)", "required": False}
        ]
    },
    "get_render_formats": {
        "name": "get_render_formats",
        "description": "Get list of available render formats",
        "component": "project",
        "function": get_render_formats,
        "parameters": []
    },
    "get_render_codecs": {
        "name": "get_render_codecs",
        "description": "Get list of available render codecs for the specified format",
        "component": "project",
        "function": get_render_codecs,
        "parameters": [
            {"name": "render_format", "type": "string", "description": "Render format to get codecs for", "required": True}
        ]
    },
    "get_current_render_format_and_codec": {
        "name": "get_current_render_format_and_codec",
        "description": "Get currently selected render format and codec",
        "component": "project",
        "function": get_current_render_format_and_codec,
        "parameters": []
    },
    "set_current_render_format_and_codec": {
        "name": "set_current_render_format_and_codec",
        "description": "Set render format and codec",
        "component": "project",
        "function": set_current_render_format_and_codec,
        "parameters": [
            {"name": "format_name", "type": "string", "description": "Name of the render format", "required": True},
            {"name": "codec_name", "type": "string", "description": "Name of the render codec", "required": True}
        ]
    },
    "get_current_render_mode": {
        "name": "get_current_render_mode",
        "description": "Get current render mode (0 for Individual clips, 1 for Single clip)",
        "component": "project",
        "function": get_current_render_mode,
        "parameters": []
    },
    "set_current_render_mode": {
        "name": "set_current_render_mode",
        "description": "Set render mode (0 for Individual clips, 1 for Single clip)",
        "component": "project",
        "function": set_current_render_mode,
        "parameters": [
            {"name": "render_mode", "type": "integer", "description": "Render mode (0 for Individual clips, 1 for Single clip)", "required": True}
        ]
    },
    "get_render_resolutions": {
        "name": "get_render_resolutions",
        "description": "Get available render resolutions for the specified format and codec",
        "component": "project",
        "function": get_render_resolutions,
        "parameters": [
            {"name": "format_name", "type": "string", "description": "Render format (optional)", "required": False},
            {"name": "codec_name", "type": "string", "description": "Render codec (optional)", "required": False}
        ]
    },
    "refresh_lut_list": {
        "name": "refresh_lut_list",
        "description": "Refresh the LUT list",
        "component": "project",
        "function": refresh_lut_list,
        "parameters": []
    },
    "insert_audio_to_current_track_at_playhead": {
        "name": "insert_audio_to_current_track_at_playhead",
        "description": "Insert audio file to current track at playhead on Fairlight page",
        "component": "project",
        "function": insert_audio_to_current_track_at_playhead,
        "parameters": [
            {"name": "media_path", "type": "string", "description": "Path to the audio file", "required": True},
            {"name": "start_offset_in_samples", "type": "integer", "description": "Start offset in samples", "required": True},
            {"name": "duration_in_samples", "type": "integer", "description": "Duration in samples", "required": True}
        ]
    },
    "load_burn_in_preset": {
        "name": "load_burn_in_preset",
        "description": "Load burn-in preset for the project",
        "component": "project",
        "function": load_burn_in_preset,
        "parameters": [
            {"name": "preset_name", "type": "string", "description": "Name of the burn-in preset to load", "required": True}
        ]
    },
    "export_current_frame_as_still": {
        "name": "export_current_frame_as_still",
        "description": "Export current frame as still image",
        "component": "project",
        "function": export_current_frame_as_still,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to save the still image", "required": True}
        ]
    },
    "get_color_groups_list": {
        "name": "get_color_groups_list",
        "description": "Get list of color groups in the project",
        "component": "project",
        "function": get_color_groups_list,
        "parameters": []
    },
    "add_color_group": {
        "name": "add_color_group",
        "description": "Add a new color group to the project",
        "component": "project",
        "function": add_color_group,
        "parameters": [
            {"name": "group_name", "type": "string", "description": "Name for the new color group", "required": True}
        ]
    },
    "delete_color_group": {
        "name": "delete_color_group",
        "description": "Delete a color group by name",
        "component": "project",
        "function": delete_color_group,
        "parameters": [
            {"name": "group_name", "type": "string", "description": "Name of the color group to delete", "required": True}
        ]
    },
    "set_setting": {
        "name": "set_setting",
        "description": "Set a project setting value",
        "component": "project",
        "function": set_setting,
        "parameters": {
            "setting_name": {
                "type": "string",
                "description": "Name of the setting to change",
                "required": True
            },
            "setting_value": {
                "type": "string",
                "description": "New value for the setting",
                "required": True
            }
        }
    },

    # MediaStorage tools
    "get_mounted_volumes": {
        "name": "get_mounted_volumes",
        "description": "Get a list of mounted volumes/drives",
        "component": "media_storage",
        "function": get_mounted_volumes,
        "parameters": []
    },
    "get_subfolder_list": {
        "name": "get_subfolder_list",
        "description": "Get a list of subfolders in the specified folder",
        "component": "media_storage",
        "function": get_subfolder_list,
        "parameters": [
            {"name": "folder_path", "type": "string", "description": "Path to folder to list subfolders from", "required": True}
        ]
    },
    "get_file_list": {
        "name": "get_file_list",
        "description": "Get a list of files in the specified folder",
        "component": "media_storage",
        "function": get_file_list,
        "parameters": [
            {"name": "folder_path", "type": "string", "description": "Path to folder to list files from", "required": True}
        ]
    },
    "reveal_in_storage": {
        "name": "reveal_in_storage",
        "description": "Reveal a file or folder in the OS file browser",
        "component": "media_storage",
        "function": reveal_in_storage,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to file or folder to reveal", "required": True}
        ]
    },
    "add_items_to_media_pool": {
        "name": "add_items_to_media_pool",
        "description": "Add items to media pool",
        "component": "media_storage",
        "function": add_items_to_media_pool,
        "parameters": [
            {"name": "file_paths", "type": "array", "description": "List of file paths to add", "required": True},
            {"name": "folder_id", "type": "string", "description": "Optional ID of folder to add items to", "required": False}
        ]
    },
    "add_clip_mattes_to_media_pool": {
        "name": "add_clip_mattes_to_media_pool",
        "description": "Add clip mattes to a media pool item",
        "component": "media_storage",
        "function": add_clip_mattes_to_media_pool,
        "parameters": [
            {"name": "media_pool_item_id", "type": "string", "description": "ID of the media pool item to add mattes to", "required": True},
            {"name": "file_paths", "type": "array", "description": "List of matte file paths to add", "required": True}
        ]
    },
    "add_timeline_mattes_to_media_pool": {
        "name": "add_timeline_mattes_to_media_pool",
        "description": "Add timeline mattes to media pool",
        "component": "media_storage",
        "function": add_timeline_mattes_to_media_pool,
        "parameters": [
            {"name": "file_paths", "type": "array", "description": "List of matte file paths to add", "required": True},
            {"name": "folder_id", "type": "string", "description": "Optional ID of folder to add mattes to", "required": False}
        ]
    },
    
    # MediaPool tools
    "list_media_pool_items": {
        "name": "list_media_pool_items",
        "description": "List items in the current media pool folder",
        "component": "media_pool",
        "function": list_media_pool_items,
        "parameters": []
    },
    "get_folder_structure": {
        "name": "get_folder_structure",
        "description": "Get the media pool folder structure",
        "component": "media_pool",
        "function": get_folder_structure,
        "parameters": []
    },
    "get_media_pool_root_folder": {
        "name": "get_media_pool_root_folder",
        "description": "Get the root folder of the media pool",
        "component": "media_pool",
        "function": get_root_folder,
        "parameters": []
    },
    "add_subfolder": {
        "name": "add_subfolder",
        "description": "Add a new subfolder to the media pool",
        "component": "media_pool",
        "function": add_subfolder,
        "parameters": [
            {"name": "folder_name", "type": "string", "description": "Name of the new folder", "required": True},
            {"name": "parent_folder_id", "type": "string", "description": "Optional ID of parent folder", "required": False}
        ]
    },
    "refresh_folders": {
        "name": "refresh_folders",
        "description": "Refresh folders in the media pool (useful in collaboration mode)",
        "component": "media_pool",
        "function": refresh_folders,
        "parameters": []
    },
    "create_empty_timeline": {
        "name": "create_empty_timeline",
        "description": "Create a new empty timeline",
        "component": "media_pool",
        "function": create_empty_timeline,
        "parameters": [
            {"name": "timeline_name", "type": "string", "description": "Name for the new timeline", "required": True}
        ]
    },
    "append_to_timeline": {
        "name": "append_to_timeline",
        "description": "Append clips to the current timeline",
        "component": "media_pool",
        "function": append_to_timeline,
        "parameters": [
            {"name": "clips", "type": "array", "description": "List of clip IDs or clip info dictionaries", "required": True}
        ]
    },
    "append_all_clips_to_timeline": {
        "name": "append_all_clips_to_timeline",
        "description": "Append all clips from the current media pool folder to the current timeline",
        "component": "media_pool",
        "function": append_all_clips_to_timeline,
        "parameters": []
    },
    "create_timeline_from_clips": {
        "name": "create_timeline_from_clips",
        "description": "Create a new timeline and add the specified clips to it",
        "component": "media_pool",
        "function": create_timeline_from_clips,
        "parameters": [
            {"name": "timeline_name", "type": "string", "description": "Name for the new timeline", "required": True},
            {"name": "clips", "type": "array", "description": "List of clip IDs or clip info dictionaries", "required": True}
        ]
    },
    "import_timeline_from_file": {
        "name": "import_timeline_from_file",
        "description": "Import a timeline from a file (AAF, EDL, XML, etc.)",
        "component": "media_pool",
        "function": import_timeline_from_file,
        "parameters": {
            "file_path": {
                "type": "string",
                "description": "Path to the timeline file to import",
                "required": True
            },
            "import_options": {
                "type": "object",
                "description": "Optional dictionary of import options",
                "required": False
            }
        }
    },
    "import_media": {
        "name": "import_media",
        "description": "Import media files into the current media pool folder",
        "component": "media_pool",
        "function": import_media,
        "parameters": [
            {"name": "paths", "type": "array", "description": "List of file or folder paths to import", "required": True}
        ]
    },
    "delete_clips": {
        "name": "delete_clips",
        "description": "Delete clips from the media pool",
        "component": "media_pool",
        "function": delete_clips,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of clip IDs to delete", "required": True}
        ]
    },
    "get_media_pool_current_folder": {
        "name": "get_media_pool_current_folder",
        "description": "Get the current folder in the media pool",
        "component": "media_pool",
        "function": get_media_pool_current_folder,
        "parameters": []
    },
    "set_media_pool_current_folder": {
        "name": "set_media_pool_current_folder",
        "description": "Set the current folder in the media pool",
        "component": "media_pool",
        "function": set_media_pool_current_folder,
        "parameters": [
            {"name": "folder_id", "type": "string", "description": "ID of the folder to set as current", "required": True}
        ]
    },
    "delete_timelines": {
        "name": "delete_timelines",
        "description": "Delete timelines from the current project",
        "component": "media_pool",
        "function": delete_timelines,
        "parameters": {
            "timeline_names": {
                "type": "array",
                "description": "List of timeline names to delete",
                "required": True
            }
        }
    },
    "delete_folders": {
        "name": "delete_folders",
        "description": "Delete folders from the media pool",
        "component": "media_pool",
        "function": delete_folders,
        "parameters": {
            "folder_names": {
                "type": "array",
                "description": "List of folder names to delete",
                "required": True
            }
        }
    },
    "auto_sync_audio": {
        "name": "auto_sync_audio",
        "description": "Sync audio for specified media pool items",
        "component": "media_pool",
        "function": auto_sync_audio,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of clip IDs to sync (at least one video and one audio clip)", "required": True},
            {"name": "audio_sync_settings", "type": "object", "description": "Optional dictionary with audio sync settings (timecodeAccuracy, audioSyncAccuracy, handleLength, appendSyncedAudio)", "required": False}
        ]
    },
    "get_selected_clips": {
        "name": "get_selected_clips",
        "description": "Get currently selected clips in the media pool",
        "component": "media_pool",
        "function": get_selected_clips,
        "parameters": []
    },
    "set_selected_clip": {
        "name": "set_selected_clip",
        "description": "Set a specified clip as selected in the media pool",
        "component": "media_pool",
        "function": set_selected_clip,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the clip to set as selected", "required": True}
        ]
    },
    "import_folder_from_file": {
        "name": "import_folder_from_file",
        "description": "Import a folder from a DRB file",
        "component": "media_pool",
        "function": import_folder_from_file,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to the DRB file to import", "required": True},
            {"name": "source_clips_path", "type": "string", "description": "Optional path to search for source clips if they're not in their original location", "required": False}
        ]
    },
    "move_clips": {
        "name": "move_clips",
        "description": "Move specified clips to a target folder",
        "component": "media_pool",
        "function": move_clips,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of clip IDs to move", "required": True},
            {"name": "target_folder_id", "type": "string", "description": "ID of the target folder", "required": True}
        ]
    },
    "move_folders": {
        "name": "move_folders",
        "description": "Move specified folders to a target folder",
        "component": "media_pool",
        "function": move_folders,
        "parameters": [
            {"name": "folder_ids", "type": "array", "description": "List of folder IDs to move", "required": True},
            {"name": "target_folder_id", "type": "string", "description": "ID of the target folder", "required": True}
        ]
    },
    "get_clip_matte_list": {
        "name": "get_clip_matte_list",
        "description": "Get the list of mattes for a specified clip",
        "component": "media_pool",
        "function": get_clip_matte_list,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the clip to get mattes for", "required": True}
        ]
    },
    "get_timeline_matte_list": {
        "name": "get_timeline_matte_list",
        "description": "Get the list of timeline mattes in a specified folder",
        "component": "media_pool",
        "function": get_timeline_matte_list,
        "parameters": [
            {"name": "folder_id", "type": "string", "description": "ID of the folder to get mattes from", "required": True}
        ]
    },
    "delete_clip_mattes": {
        "name": "delete_clip_mattes",
        "description": "Delete mattes for a specified clip",
        "component": "media_pool",
        "function": delete_clip_mattes,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the clip to delete mattes from", "required": True},
            {"name": "matte_paths", "type": "array", "description": "List of paths to the matte files to delete", "required": True}
        ]
    },
    "relink_clips": {
        "name": "relink_clips",
        "description": "Update the folder location of specified media pool clips",
        "component": "media_pool",
        "function": relink_clips,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of clip IDs to relink", "required": True},
            {"name": "folder_path", "type": "string", "description": "Path to the folder where the media is located", "required": True}
        ]
    },
    "unlink_clips": {
        "name": "unlink_clips",
        "description": "Unlink specified media pool clips",
        "component": "media_pool",
        "function": unlink_clips,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of clip IDs to unlink", "required": True}
        ]
    },
    "export_metadata": {
        "name": "export_metadata",
        "description": "Export metadata of clips to CSV format",
        "component": "media_pool",
        "function": export_metadata,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to save the CSV file", "required": True},
            {"name": "clip_ids", "type": "array", "description": "Optional list of clip IDs to export metadata for", "required": False}
        ]
    },
    "get_media_pool_unique_id": {
        "name": "get_media_pool_unique_id",
        "description": "Get a unique ID for the media pool",
        "component": "media_pool",
        "function": get_unique_id,
        "parameters": []
    },
    "create_stereo_clip": {
        "name": "create_stereo_clip",
        "description": "Creates a new 3D stereoscopic media pool entry from two existing media pool items",
        "component": "media_pool",
        "function": create_stereo_clip,
        "parameters": [
            {"name": "left_clip_id", "type": "string", "description": "ID of the clip to use for the left eye", "required": True},
            {"name": "right_clip_id", "type": "string", "description": "ID of the clip to use for the right eye", "required": True}
        ]
    },

    # Timeline tools
    "add_track": {
        "name": "add_track",
        "description": "Add a track to the current timeline",
        "component": "timeline",
        "function": add_track,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track to add ('video', 'audio', or 'subtitle')", "required": True}
        ]
    },
    "delete_track": {
        "name": "delete_track",
        "description": "Delete a track from the current timeline",
        "component": "timeline",
        "function": delete_track,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track to delete ('video', 'audio', or 'subtitle')", "required": True},
            {"name": "track_index", "type": "integer", "description": "Index of the track to delete (1-based index)", "required": True}
        ]
    },
    "delete_timeline_clips": {
        "name": "delete_timeline_clips",
        "description": "Delete clips from the current timeline",
        "component": "timeline",
        "function": delete_timeline_clips,
        "parameters": [
            {"name": "clip_ids", "type": "array", "description": "List of timeline clip IDs to delete", "required": True}
        ]
    },
    "set_current_timecode": {
        "name": "set_current_timecode",
        "description": "Set the current timecode for the timeline",
        "component": "timeline",
        "function": set_current_timecode,
        "parameters": [
            {"name": "timecode", "type": "string", "description": "Timecode string to set (format: HH:MM:SS:FF)", "required": True}
        ]
    },
    "set_track_enable": {
        "name": "set_track_enable",
        "description": "Enable or disable a track in the timeline",
        "component": "timeline",
        "function": set_track_enable,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track ('video', 'audio', or 'subtitle')", "required": True},
            {"name": "track_index", "type": "integer", "description": "Index of the track (1-based index)", "required": True},
            {"name": "enable", "type": "boolean", "description": "True to enable the track, False to disable", "required": True}
        ]
    },
    "set_track_lock": {
        "name": "set_track_lock",
        "description": "Lock or unlock a track in the timeline",
        "component": "timeline",
        "function": set_track_lock,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track ('video', 'audio', or 'subtitle')", "required": True},
            {"name": "track_index", "type": "integer", "description": "Index of the track (1-based index)", "required": True},
            {"name": "lock", "type": "boolean", "description": "True to lock the track, False to unlock", "required": True}
        ]
    },
    "add_marker": {
        "name": "add_marker",
        "description": "Add a marker to the timeline",
        "component": "timeline",
        "function": add_marker,
        "parameters": [
            {"name": "frame_id", "type": "number", "description": "Frame position for the marker", "required": True},
            {"name": "color", "type": "string", "description": "Color name for the marker", "required": True},
            {"name": "name", "type": "string", "description": "Name of the marker", "required": True},
            {"name": "note", "type": "string", "description": "Note text for the marker", "required": True},
            {"name": "duration", "type": "number", "description": "Duration of the marker in frames", "required": True},
            {"name": "custom_data", "type": "string", "description": "Custom data to attach to the marker", "required": False}
        ]
    },
    "get_markers": {
        "name": "get_markers",
        "description": "Get all markers from the timeline",
        "component": "timeline",
        "function": get_markers,
        "parameters": []
    },
    "get_marker_by_custom_data": {
        "name": "get_marker_by_custom_data",
        "description": "Get a marker by its custom data",
        "component": "timeline",
        "function": get_marker_by_custom_data,
        "parameters": [
            {"name": "custom_data", "type": "string", "description": "Custom data string to search for", "required": True}
        ]
    },
    "update_marker_custom_data": {
        "name": "update_marker_custom_data",
        "description": "Update custom data for a marker at a specific frame",
        "component": "timeline",
        "function": update_marker_custom_data,
        "parameters": [
            {"name": "frame_id", "type": "number", "description": "Frame position of the marker", "required": True},
            {"name": "custom_data", "type": "string", "description": "New custom data to set", "required": True}
        ]
    },
    "get_marker_custom_data": {
        "name": "get_marker_custom_data",
        "description": "Get custom data for a marker at a specific frame",
        "component": "timeline",
        "function": get_marker_custom_data,
        "parameters": [
            {"name": "frame_id", "type": "number", "description": "Frame position of the marker", "required": True}
        ]
    },
    "delete_markers_by_color": {
        "name": "delete_markers_by_color",
        "description": "Delete all markers of a specific color from the timeline",
        "component": "timeline",
        "function": delete_markers_by_color,
        "parameters": [
            {"name": "color", "type": "string", "description": "Color of markers to delete, or 'All' to delete all markers", "required": True}
        ]
    },
    "delete_marker_at_frame": {
        "name": "delete_marker_at_frame",
        "description": "Delete a marker at a specific frame",
        "component": "timeline",
        "function": delete_marker_at_frame,
        "parameters": [
            {"name": "frame_num", "type": "number", "description": "Frame number where the marker is located", "required": True}
        ]
    },
    "delete_marker_by_custom_data": {
        "name": "delete_marker_by_custom_data",
        "description": "Delete a marker by its custom data",
        "component": "timeline",
        "function": delete_marker_by_custom_data,
        "parameters": [
            {"name": "custom_data", "type": "string", "description": "Custom data string to search for", "required": True}
        ]
    },
    "set_timeline_name": {
        "name": "set_timeline_name",
        "description": "Set the name of the current timeline",
        "component": "timeline",
        "function": set_name,
        "parameters": [
            {"name": "timeline_name", "type": "string", "description": "New name for the timeline", "required": True}
        ]
    },
    "get_track_name": {
        "name": "get_track_name",
        "description": "Get the name of a track in the timeline",
        "component": "timeline",
        "function": get_track_name,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track ('video', 'audio', or 'subtitle')", "required": True},
            {"name": "track_index", "type": "integer", "description": "Index of the track (1-based index)", "required": True}
        ]
    },
    "set_track_name": {
        "name": "set_track_name",
        "description": "Set the name of a track in the timeline",
        "component": "timeline",
        "function": set_track_name,
        "parameters": [
            {"name": "track_type", "type": "string", "description": "Type of track ('video', 'audio', or 'subtitle')", "required": True},
            {"name": "track_index", "type": "integer", "description": "Index of the track (1-based index)", "required": True},
            {"name": "name", "type": "string", "description": "New name for the track", "required": True}
        ]
    },
    "create_compound_clip": {
        "name": "create_compound_clip",
        "description": "Create a compound clip from timeline items",
        "component": "timeline",
        "function": create_compound_clip,
        "parameters": [
            {"name": "timeline_items", "type": "array", "description": "List of timeline item IDs to include in the compound clip", "required": True},
            {"name": "clip_info", "type": "object", "description": "Optional dictionary with clip info (keys: 'startTimecode', 'name')", "required": False}
        ]
    },
    "get_current_timecode": {
        "name": "get_current_timecode",
        "description": "Get the current timecode of the timeline",
        "component": "timeline",
        "function": get_current_timecode,
        "parameters": []
    },
    "duplicate_timeline": {
        "name": "duplicate_timeline",
        "description": "Duplicate the current timeline with an optional new name",
        "component": "timeline",
        "function": duplicate_timeline,
        "parameters": [
            {"name": "timeline_name", "type": "string", "description": "Optional name for the duplicated timeline", "required": False}
        ]
    },
    "export_timeline": {
        "name": "export_timeline",
        "description": "Export the current timeline to a file in the specified format",
        "component": "timeline",
        "function": export_timeline,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path where the exported file will be saved", "required": True},
            {"name": "export_type", "type": "string", "description": "Type of export (AAF, DRT, EDL, etc.)", "required": True},
            {"name": "export_subtype", "type": "string", "description": "Subtype of export (optional, used for certain export types)", "required": False}
        ]
    },
    "get_timeline_setting": {
        "name": "get_timeline_setting",
        "description": "Get the value of a timeline setting or all settings",
        "component": "timeline",
        "function": get_timeline_setting,
        "parameters": [
            {"name": "setting_name", "type": "string", "description": "Optional name of the setting to retrieve", "required": False}
        ]
    },
    "set_timeline_setting": {
        "name": "set_timeline_setting",
        "description": "Set the value of a timeline setting",
        "component": "timeline",
        "function": set_timeline_setting,
        "parameters": [
            {"name": "setting_name", "type": "string", "description": "Name of the setting to set", "required": True},
            {"name": "setting_value", "type": "string", "description": "Value to set for the setting", "required": True}
        ]
    },
    "insert_generator_into_timeline": {
        "name": "insert_generator_into_timeline",
        "description": "Insert a generator into the current timeline",
        "component": "timeline",
        "function": insert_generator_into_timeline,
        "parameters": [
            {"name": "generator_name", "type": "string", "description": "Name of the generator to insert", "required": True}
        ]
    },
    "insert_fusion_generator_into_timeline": {
        "name": "insert_fusion_generator_into_timeline",
        "description": "Insert a Fusion generator into the current timeline",
        "component": "timeline",
        "function": insert_fusion_generator_into_timeline,
        "parameters": [
            {"name": "generator_name", "type": "string", "description": "Name of the Fusion generator to insert", "required": True}
        ]
    },
    "insert_fusion_composition_into_timeline": {
        "name": "insert_fusion_composition_into_timeline",
        "description": "Insert a Fusion composition into the current timeline",
        "component": "timeline",
        "function": insert_fusion_composition_into_timeline,
        "parameters": []
    },
    "insert_ofx_generator_into_timeline": {
        "name": "insert_ofx_generator_into_timeline",
        "description": "Insert an OFX generator into the current timeline",
        "component": "timeline",
        "function": insert_ofx_generator_into_timeline,
        "parameters": [
            {"name": "generator_name", "type": "string", "description": "Name of the OFX generator to insert", "required": True}
        ]
    },
    "insert_title_into_timeline": {
        "name": "insert_title_into_timeline",
        "description": "Insert a title into the current timeline",
        "component": "timeline",
        "function": insert_title_into_timeline,
        "parameters": [
            {"name": "title_name", "type": "string", "description": "Name of the title to insert", "required": True}
        ]
    },
    "insert_fusion_title_into_timeline": {
        "name": "insert_fusion_title_into_timeline",
        "description": "Insert a Fusion title into the current timeline",
        "component": "timeline",
        "function": insert_fusion_title_into_timeline,
        "parameters": [
            {"name": "title_name", "type": "string", "description": "Name of the Fusion title to insert", "required": True}
        ]
    },
    "grab_still": {
        "name": "grab_still",
        "description": "Grab a still from the current video clip in the timeline",
        "component": "timeline",
        "function": grab_still,
        "parameters": []
    },
    "grab_all_stills": {
        "name": "grab_all_stills",
        "description": "Grab stills from all clips in the timeline at the specified source frame",
        "component": "timeline",
        "function": grab_all_stills,
        "parameters": [
            {"name": "still_frame_source", "type": "integer", "description": "Source frame for stills (1 - First frame, 2 - Middle frame)", "required": True}
        ]
    },

    # MediaPoolItem tools
    "get_media_pool_item_name": {
        "name": "get_media_pool_item_name",
        "description": "Get the name of a media pool item",
        "component": "media_pool_item",
        "function": get_name,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "get_media_pool_item_metadata": {
        "name": "get_media_pool_item_metadata",
        "description": "Get metadata for a media pool item",
        "component": "media_pool_item",
        "function": get_metadata,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "metadata_type", "type": "string", "description": "Specific metadata type to retrieve", "required": False}
        ]
    },
    "set_media_pool_item_metadata": {
        "name": "set_media_pool_item_metadata",
        "description": "Set metadata for a media pool item",
        "component": "media_pool_item",
        "function": set_metadata,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "metadata", "type": "object or string", "description": "Metadata dictionary or key", "required": True},
            {"name": "metadata_value", "type": "string", "description": "Metadata value (only used if metadata is a string key)", "required": False}
        ]
    },
    "get_media_pool_item_third_party_metadata": {
        "name": "get_media_pool_item_third_party_metadata",
        "description": "Get third-party metadata for a media pool item",
        "component": "media_pool_item",
        "function": get_third_party_metadata,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "metadata_type", "type": "string", "description": "Specific metadata type to retrieve", "required": False}
        ]
    },
    "set_media_pool_item_third_party_metadata": {
        "name": "set_media_pool_item_third_party_metadata",
        "description": "Set third-party metadata for a media pool item",
        "component": "media_pool_item",
        "function": set_third_party_metadata,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "metadata", "type": "object or string", "description": "Metadata dictionary or key", "required": True},
            {"name": "metadata_value", "type": "string", "description": "Metadata value (only used if metadata is a string key)", "required": False}
        ]
    },
    "get_media_pool_item_media_id": {
        "name": "get_media_pool_item_media_id",
        "description": "Get the media ID for a media pool item",
        "component": "media_pool_item",
        "function": get_media_id,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "add_media_pool_item_marker": {
        "name": "add_media_pool_item_marker",
        "description": "Add a marker to a media pool item",
        "component": "media_pool_item",
        "function": add_marker,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "frame_id", "type": "number", "description": "Frame position for the marker", "required": True},
            {"name": "color", "type": "string", "description": "Color name for the marker", "required": True},
            {"name": "name", "type": "string", "description": "Name of the marker", "required": True},
            {"name": "note", "type": "string", "description": "Note text for the marker", "required": True},
            {"name": "duration", "type": "number", "description": "Duration of the marker in frames", "required": True},
            {"name": "custom_data", "type": "string", "description": "Custom data to attach to the marker", "required": False}
        ]
    },
    "get_media_pool_item_markers": {
        "name": "get_media_pool_item_markers",
        "description": "Get all markers for a media pool item",
        "component": "media_pool_item",
        "function": get_markers,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "get_media_pool_item_marker_by_custom_data": {
        "name": "get_media_pool_item_marker_by_custom_data",
        "description": "Get marker information by custom data",
        "component": "media_pool_item",
        "function": get_marker_by_custom_data,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "custom_data", "type": "string", "description": "Custom data string to search for", "required": True}
        ]
    },
    "update_media_pool_item_marker_custom_data": {
        "name": "update_media_pool_item_marker_custom_data",
        "description": "Update custom data for a marker at a specific frame",
        "component": "media_pool_item",
        "function": update_marker_custom_data,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "frame_id", "type": "number", "description": "Frame position of the marker", "required": True},
            {"name": "custom_data", "type": "string", "description": "New custom data to set", "required": True}
        ]
    },
    "get_media_pool_item_marker_custom_data": {
        "name": "get_media_pool_item_marker_custom_data",
        "description": "Get custom data for a marker at a specific frame",
        "component": "media_pool_item",
        "function": get_marker_custom_data,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "frame_id", "type": "number", "description": "Frame position of the marker", "required": True}
        ]
    },
    "delete_media_pool_item_markers_by_color": {
        "name": "delete_media_pool_item_markers_by_color",
        "description": "Delete all markers of a specific color",
        "component": "media_pool_item",
        "function": delete_markers_by_color,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "color", "type": "string", "description": "Color of markers to delete, or 'All' to delete all markers", "required": True}
        ]
    },
    "delete_media_pool_item_marker_at_frame": {
        "name": "delete_media_pool_item_marker_at_frame",
        "description": "Delete a marker at a specific frame",
        "component": "media_pool_item",
        "function": delete_marker_at_frame,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "frame_num", "type": "number", "description": "Frame number where the marker is located", "required": True}
        ]
    },
    "delete_media_pool_item_marker_by_custom_data": {
        "name": "delete_media_pool_item_marker_by_custom_data",
        "description": "Delete a marker by its custom data",
        "component": "media_pool_item",
        "function": delete_marker_by_custom_data,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "custom_data", "type": "string", "description": "Custom data string to search for", "required": True}
        ]
    },
    "add_media_pool_item_flag": {
        "name": "add_media_pool_item_flag",
        "description": "Add a flag to a media pool item",
        "component": "media_pool_item",
        "function": add_flag,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "color", "type": "string", "description": "Color name for the flag", "required": True}
        ]
    },
    "get_media_pool_item_flag_list": {
        "name": "get_media_pool_item_flag_list",
        "description": "Get all flags for a media pool item",
        "component": "media_pool_item",
        "function": get_flag_list,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "clear_media_pool_item_flags": {
        "name": "clear_media_pool_item_flags",
        "description": "Clear flags from a media pool item",
        "component": "media_pool_item",
        "function": clear_flags,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "color", "type": "string", "description": "Color of flags to clear, or 'All' to clear all flags", "required": True}
        ]
    },
    "get_media_pool_item_color": {
        "name": "get_media_pool_item_color",
        "description": "Get the color assigned to a media pool item",
        "component": "media_pool_item",
        "function": get_clip_color,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "set_media_pool_item_color": {
        "name": "set_media_pool_item_color",
        "description": "Set the color for a media pool item",
        "component": "media_pool_item",
        "function": set_clip_color,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "color_name", "type": "string", "description": "Name of the color to set", "required": True}
        ]
    },
    "clear_media_pool_item_color": {
        "name": "clear_media_pool_item_color",
        "description": "Clear the color assigned to a media pool item",
        "component": "media_pool_item",
        "function": clear_clip_color,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "get_media_pool_item_property": {
        "name": "get_media_pool_item_property",
        "description": "Get clip properties for a media pool item",
        "component": "media_pool_item",
        "function": get_clip_property,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "property_name", "type": "string", "description": "Specific property to retrieve", "required": False}
        ]
    },
    "set_media_pool_item_property": {
        "name": "set_media_pool_item_property",
        "description": "Set a clip property for a media pool item",
        "component": "media_pool_item",
        "function": set_clip_property,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "property_name", "type": "string", "description": "Name of the property to set", "required": True},
            {"name": "property_value", "type": "string", "description": "Value to set for the property", "required": True}
        ]
    },
    "link_media_pool_item_proxy_media": {
        "name": "link_media_pool_item_proxy_media",
        "description": "Link proxy media to a media pool item",
        "component": "media_pool_item",
        "function": link_proxy_media,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "proxy_media_file_path", "type": "string", "description": "Absolute path to the proxy media file", "required": True}
        ]
    },
    "unlink_media_pool_item_proxy_media": {
        "name": "unlink_media_pool_item_proxy_media",
        "description": "Unlink proxy media from a media pool item",
        "component": "media_pool_item",
        "function": unlink_proxy_media,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "replace_media_pool_item": {
        "name": "replace_media_pool_item",
        "description": "Replace a media pool item with another file",
        "component": "media_pool_item",
        "function": replace_clip,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item to replace", "required": True},
            {"name": "file_path", "type": "string", "description": "Absolute path to the new media file", "required": True}
        ]
    },
    "get_media_pool_item_unique_id": {
        "name": "get_media_pool_item_unique_id",
        "description": "Get the unique ID of a media pool item",
        "component": "media_pool_item",
        "function": get_unique_id,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "transcribe_media_pool_item_audio": {
        "name": "transcribe_media_pool_item_audio",
        "description": "Transcribe audio for a media pool item",
        "component": "media_pool_item",
        "function": transcribe_audio,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "clear_media_pool_item_transcription": {
        "name": "clear_media_pool_item_transcription",
        "description": "Clear audio transcription for a media pool item",
        "component": "media_pool_item",
        "function": clear_transcription,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "get_media_pool_item_audio_mapping": {
        "name": "get_media_pool_item_audio_mapping",
        "description": "Get audio mapping information for a media pool item",
        "component": "media_pool_item",
        "function": get_audio_mapping,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "get_media_pool_item_mark_in_out": {
        "name": "get_media_pool_item_mark_in_out",
        "description": "Get in and out point information for a media pool item",
        "component": "media_pool_item",
        "function": get_mark_in_out,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True}
        ]
    },
    "set_media_pool_item_mark_in_out": {
        "name": "set_media_pool_item_mark_in_out",
        "description": "Set in and out points for a media pool item",
        "component": "media_pool_item",
        "function": set_mark_in_out,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "mark_in", "type": "integer", "description": "Frame number for the in point", "required": True},
            {"name": "mark_out", "type": "integer", "description": "Frame number for the out point", "required": True},
            {"name": "mark_type", "type": "string", "description": "Type of mark in/out to set ('video', 'audio', or 'all')", "required": False}
        ]
    },
    "clear_media_pool_item_mark_in_out": {
        "name": "clear_media_pool_item_mark_in_out",
        "description": "Clear in and out points for a media pool item",
        "component": "media_pool_item",
        "function": clear_mark_in_out,
        "parameters": [
            {"name": "clip_id", "type": "string", "description": "ID of the media pool item", "required": True},
            {"name": "mark_type", "type": "string", "description": "Type of mark in/out to clear ('video', 'audio', or 'all')", "required": False}
        ]
    },

    # Timeline Item Tools
    "get_timeline_item": {
        "description": "Retrieve a timeline item by its ID",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            }
        },
        "function": get_timeline_item
    },
    "set_property": {
        "description": "Set a property on a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "property_key": {
                "description": "Property key name",
                "type": "string"
            },
            "property_value": {
                "description": "Property value to set (can be string, number, boolean)",
                "type": "string"
            }
        },
        "function": set_property
    },
    "get_property": {
        "description": "Get the value of a property from a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "property_key": {
                "description": "Property key name",
                "type": "string"
            }
        },
        "function": get_property
    },
    "set_start": {
        "description": "Set the start frame of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "frame_num": {
                "description": "Frame number for the new start position",
                "type": "integer"
            }
        },
        "function": set_start
    },
    "set_end": {
        "description": "Set the end frame of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "frame_num": {
                "description": "Frame number for the new end position",
                "type": "integer"
            }
        },
        "function": set_end
    },
    "set_left_offset": {
        "description": "Set the left offset of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "offset": {
                "description": "New left offset value in frames",
                "type": "integer"
            }
        },
        "function": set_left_offset
    },
    "set_right_offset": {
        "description": "Set the right offset of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "offset": {
                "description": "New right offset value in frames",
                "type": "integer"
            }
        },
        "function": set_right_offset
    },
    "add_fusion_comp": {
        "description": "Add a new Fusion composition to a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "comp_name": {
                "description": "Name for the new Fusion composition",
                "type": "string"
            }
        },
        "function": add_fusion_comp
    },
    "rename_fusion_comp": {
        "description": "Rename a Fusion composition in a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "Unique ID of the timeline item",
                "type": "string"
            },
            "old_name": {
                "description": "Current name of the Fusion composition",
                "type": "string"
            },
            "new_name": {
                "description": "New name for the Fusion composition",
                "type": "string"
            }
        },
        "function": rename_fusion_comp
    },
    "get_timeline_item_scale": {
        "description": "Gets the scale (playback speed) of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            }
        },
        "function": get_scale
    },
    "get_timeline_item_is_filler": {
        "description": "Checks if a timeline item is a filler item",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            }
        },
        "function": get_is_filler
    },
    "has_video_effect": {
        "description": "Checks if a timeline item has a video effect",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            }
        },
        "function": has_video_effect
    },
    "has_audio_effect": {
        "description": "Checks if a timeline item has an audio effect",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            }
        },
        "function": has_audio_effect
    },
    "has_video_effect_at_offset": {
        "description": "Checks if a timeline item has a video effect at a specific offset",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            },
            "offset": {
                "type": "number",
                "description": "Offset in seconds",
                "required": True
            }
        },
        "function": has_video_effect_at_offset
    },
    "has_audio_effect_at_offset": {
        "description": "Checks if a timeline item has an audio effect at a specific offset",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "ID of the timeline item",
                "required": True
            },
            "offset": {
                "type": "number",
                "description": "Offset in seconds",
                "required": True
            }
        },
        "function": has_audio_effect_at_offset
    },
    "get_timeline_item_has_video_effect": {
        "function": has_video_effect,
        "description": "Check if a timeline item has a video effect applied.",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "The ID of the timeline item to check.",
                "required": True
            }
        }
    },
    "get_timeline_item_has_audio_effect": {
        "function": has_audio_effect,
        "description": "Check if a timeline item has an audio effect applied.",
        "parameters": {
            "timeline_item_id": {
                "type": "string",
                "description": "The ID of the timeline item to check.",
                "required": True
            }
        }
    },
    "get_timeline_item_flag_list": {
        "description": "Get flags assigned to a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string"
            }
        },
        "function": get_flags
    },
    "add_timeline_item_take": {
        "description": "Add a media pool item as a new take to a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            },
            "media_pool_item_id": {
                "description": "ID of the media pool item to add as a take",
                "type": "string",
                "required": True
            },
            "start_frame": {
                "description": "Optional start frame to specify clip extents",
                "type": "integer",
                "required": False
            },
            "end_frame": {
                "description": "Optional end frame to specify clip extents",
                "type": "integer",
                "required": False
            }
        },
        "function": add_take
    },
    "get_timeline_item_selected_take_index": {
        "description": "Get the index of the currently selected take",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": get_selected_take_index
    },
    "get_timeline_item_takes_count": {
        "description": "Get the number of takes in a take selector",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": get_takes_count
    },
    "get_timeline_item_take_by_index": {
        "description": "Get information about a take by its index",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            },
            "take_index": {
                "description": "Index of the take to retrieve (1-based index)",
                "type": "integer",
                "required": True
            }
        },
        "function": get_take_by_index
    },
    "delete_timeline_item_take_by_index": {
        "description": "Delete a take by its index",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            },
            "take_index": {
                "description": "Index of the take to delete (1-based index)",
                "type": "integer",
                "required": True
            }
        },
        "function": delete_take_by_index
    },
    "select_timeline_item_take_by_index": {
        "description": "Select a take by its index",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            },
            "take_index": {
                "description": "Index of the take to select (1-based index)",
                "type": "integer",
                "required": True
            }
        },
        "function": select_take_by_index
    },
    "finalize_timeline_item_take": {
        "description": "Finalize take selection for a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": finalize_take
    },
    "set_timeline_item_enabled": {
        "description": "Enable or disable a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            },
            "enabled": {
                "description": "Boolean value to set clip enabled state",
                "type": "boolean",
                "required": True
            }
        },
        "function": set_clip_enabled
    },
    "get_timeline_item_enabled": {
        "description": "Get the enabled status of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": get_clip_enabled
    },
    "update_timeline_item_sidecar": {
        "description": "Update sidecar file for BRAW clips or RMD file for R3D clips",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": update_sidecar
    },
    "get_timeline_item_unique_id": {
        "description": "Get the unique ID of a timeline item",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the timeline item",
                "type": "string",
                "required": True
            }
        },
        "function": get_unique_id
    },
    "copy_timeline_item_grades": {
        "description": "Copy grades from one timeline item to others",
        "parameters": {
            "timeline_item_id": {
                "description": "ID of the source timeline item",
                "type": "string",
                "required": True
            },
            "target_timeline_items": {
                "description": "List of timeline item IDs to copy grades to",
                "type": "array",
                "required": True
            }
        },
        "function": copy_grades
    },
    "set_start_timecode": {
        "function": set_start_timecode,
        "description": "Set the start timecode of the current timeline",
        "parameters": {
            "timecode": {
                "type": "string",
                "description": "The timecode to set as the start timecode (format: 'HH:MM:SS:FF')"
            }
        }
    },
    "set_clips_linked": {
        "function": set_clips_linked,
        "description": "Set clips to be linked or unlinked",
        "parameters": {
            "clip_ids": {
                "type": "array",
                "description": "List of timeline item IDs to link/unlink"
            },
            "linked": {
                "type": "boolean",
                "description": "Whether to link (True) or unlink (False) the clips"
            }
        }
    },
    "get_current_video_item": {
        "name": "get_current_video_item",
        "description": "Get the current video item at the playhead position (workaround for selection)",
        "component": "timeline",
        "function": get_current_video_item,
        "parameters": []
    },
    "get_timeline_items_in_range": {
        "name": "get_timeline_items_in_range",
        "description": "Get all timeline items within a frame range (workaround for selection)",
        "component": "timeline",
        "function": get_timeline_items_in_range,
        "parameters": [
            {"name": "start_frame", "type": "integer", "description": "Start frame of the range (inclusive)", "required": False},
            {"name": "end_frame", "type": "integer", "description": "End frame of the range (inclusive)", "required": False}
        ]
    },
    "get_current_clip_thumbnail_image": {
        "name": "get_current_clip_thumbnail_image",
        "description": "Get a thumbnail image of the current clip at the playhead position",
        "component": "timeline",
        "function": get_current_clip_thumbnail_image,
        "parameters": [
            {"name": "width", "type": "integer", "description": "Width of the thumbnail in pixels (default: 320)", "required": False},
            {"name": "height", "type": "integer", "description": "Height of the thumbnail in pixels (default: 180)", "required": False}
        ]
    },
    "create_fusion_clip": {
        "name": "create_fusion_clip",
        "description": "Create a Fusion clip from the specified timeline items",
        "component": "timeline",
        "function": create_fusion_clip,
        "parameters": [
            {"name": "timeline_items", "type": "array", "description": "List of timeline item IDs to include in the Fusion clip", "required": True},
            {"name": "clip_info", "type": "object", "description": "Optional dictionary with additional clip information (e.g., name)", "required": False}
        ]
    },
    "import_into_timeline": {
        "name": "import_into_timeline",
        "description": "Import media or AAF/XML/EDL/etc. into the current timeline",
        "component": "timeline",
        "function": import_into_timeline,
        "parameters": [
            {"name": "file_path", "type": "string", "description": "Path to the file to import", "required": True},
            {"name": "import_options", "type": "object", "description": "Optional dictionary with import options specific to the file type", "required": False}
        ]
    },

    # Add Gallery component function entries
    
    "get_album_name": {
        "function": get_album_name,
        "description": "Get the name of a gallery album",
        "parameters": {
            "album_name": {
                "type": "string",
                "description": "Name of the album to get information about",
                "required": True
            }
        }
    },
    
    "set_album_name": {
        "function": set_album_name,
        "description": "Set the name of a gallery album",
        "parameters": {
            "album_name": {
                "type": "string",
                "description": "Current name of the album",
                "required": True
            },
            "new_name": {
                "type": "string",
                "description": "New name for the album",
                "required": True
            }
        }
    },
    
    "get_current_still_album": {
        "function": get_current_still_album,
        "description": "Get information about the current still album",
        "parameters": {}
    },
    
    "set_current_still_album": {
        "function": set_current_still_album,
        "description": "Set the current still album",
        "parameters": {
            "album_name": {
                "type": "string",
                "description": "Name of the album to set as current",
                "required": True
            }
        }
    },
    
    "get_gallery_still_albums": {
        "function": get_gallery_still_albums,
        "description": "Get a list of all gallery still albums",
        "parameters": {}
    },
    
    "get_gallery_power_grade_albums": {
        "function": get_gallery_power_grade_albums,
        "description": "Get a list of all gallery power grade albums",
        "parameters": {}
    },
    
    "create_gallery_still_album": {
        "function": create_gallery_still_album,
        "description": "Create a new gallery still album",
        "parameters": {
            "album_name": {
                "type": "string",
                "description": "Name for the new album",
                "required": True
            }
        }
    },
    
    "create_gallery_power_grade_album": {
        "function": create_gallery_power_grade_album,
        "description": "Create a new gallery power grade album",
        "parameters": {
            "album_name": {
                "type": "string",
                "description": "Name for the new power grade album",
                "required": True
            }
        }
    },
    
    # Add entries to TOOLS_REGISTRY for GalleryStillAlbum component functions
    "get_stills": {
        "description": "Get all stills from a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"}
        ]
    },
    "get_label": {
        "description": "Get label for a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"}
        ]
    },
    "set_label": {
        "description": "Set label for a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"},
            {"name": "label", "description": "New label for the album", "required": True, "type": "str"}
        ]
    },
    "import_stills": {
        "description": "Import stills into a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"},
            {"name": "still_paths", "description": "List of paths to still files to import", "required": True, "type": "List[str]"}
        ]
    },
    "export_stills": {
        "description": "Export stills from a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"},
            {"name": "still_indices", "description": "List of indices of stills to export", "required": True, "type": "List[int]"},
            {"name": "export_dir", "description": "Directory to export stills to", "required": True, "type": "str"},
            {"name": "file_prefix", "description": "Prefix for exported still filenames", "required": False, "type": "str"}
        ]
    },
    "delete_stills": {
        "description": "Delete stills from a gallery still album",
        "parameters": [
            {"name": "album_name", "description": "Name of the gallery still album", "required": True, "type": "str"},
            {"name": "still_indices", "description": "List of indices of stills to delete", "required": True, "type": "List[int]"}
        ]
    },
    
    # Graph
    "get_num_nodes": {
        "function": get_num_nodes,
        "description": "Get the number of nodes in the current node graph",
        "parameters": {}
    },
    "set_lut": {
        "function": set_lut,
        "description": "Set LUT for a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            },
            "lut_path": {
                "type": "string",
                "description": "Path to the LUT file",
                "required": True
            }
        }
    },
    "get_lut": {
        "function": get_lut,
        "description": "Get LUT information for a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            }
        }
    },
    "set_node_cache_mode": {
        "function": set_node_cache_mode,
        "description": "Set cache mode for a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            },
            "cache_mode": {
                "type": "string",
                "description": "Cache mode to set ('auto', 'on', or 'off')",
                "required": True
            }
        }
    },
    "get_node_cache_mode": {
        "function": get_node_cache_mode,
        "description": "Get cache mode for a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            }
        }
    },
    "get_node_label": {
        "function": get_node_label,
        "description": "Get the label of a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            }
        }
    },
    "get_tools_in_node": {
        "function": get_tools_in_node,
        "description": "Get the list of tools in a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            }
        }
    },
    "set_node_enabled": {
        "function": set_node_enabled,
        "description": "Enable or disable a specific node in the current node graph",
        "parameters": {
            "node_index": {
                "type": "integer",
                "description": "Index of the node",
                "required": True
            },
            "enabled": {
                "type": "boolean",
                "description": "Whether the node should be enabled",
                "required": True
            }
        }
    },
    "apply_grade_from_drx": {
        "function": apply_grade_from_drx,
        "description": "Apply a grade from a DRX file to the current node graph",
        "parameters": {
            "drx_path": {
                "type": "string",
                "description": "Path to the DRX file",
                "required": True
            },
            "node_index": {
                "type": "integer",
                "description": "Index of the node to apply the grade to",
                "required": False
            },
            "still_offset": {
                "type": "integer",
                "description": "Still offset for the grade",
                "required": False
            }
        }
    },
    "apply_arri_cdl_lut": {
        "function": apply_arri_cdl_lut,
        "description": "Apply an ARRI CDL LUT to the current node graph",
        "parameters": {
            "cdl_path": {
                "type": "string",
                "description": "Path to the CDL file",
                "required": True
            }
        }
    },
    "reset_all_grades": {
        "function": reset_all_grades,
        "description": "Reset all grades in the current node graph",
        "parameters": {}
    },
    
    # ColorGroup tools
    "get_color_group_name": {
        "function": get_name,
        "category": "ColorGroup",
        "description": "Get the name of a color group",
        "parameters": [
            {
                "name": "group_name",
                "type": "str",
                "description": "Name of the color group",
                "required": True,
            },
        ],
    },
    "set_color_group_name": {
        "function": set_name,
        "category": "ColorGroup",
        "description": "Set the name of a color group",
        "parameters": [
            {
                "name": "group_name",
                "type": "str",
                "description": "Current name of the color group",
                "required": True,
            },
            {
                "name": "new_name",
                "type": "str",
                "description": "New name for the color group",
                "required": True,
            },
        ],
    },
    "get_color_group_clips_in_timeline": {
        "function": get_clips_in_timeline,
        "category": "ColorGroup",
        "description": "Get the clips in the timeline that belong to a color group",
        "parameters": [
            {
                "name": "group_name",
                "type": "str",
                "description": "Name of the color group",
                "required": True,
            },
        ],
    },
    "get_color_group_pre_clip_node_graph": {
        "function": get_pre_clip_node_graph,
        "category": "ColorGroup",
        "description": "Get the pre-clip node graph of a color group",
        "parameters": [
            {
                "name": "group_name",
                "type": "str",
                "description": "Name of the color group",
                "required": True,
            },
        ],
    },
    "get_color_group_post_clip_node_graph": {
        "function": get_post_clip_node_graph,
        "category": "ColorGroup",
        "description": "Get the post-clip node graph of a color group",
        "parameters": [
            {
                "name": "group_name",
                "type": "str",
                "description": "Name of the color group",
                "required": True,
            },
        ],
    },
    # Folder tools
    "list_media_pool_items": {
        "function": get_clip_list,
        "category": "Folder",
        "description": "Get the list of clips in a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "get_folder_name": {
        "function": get_name,
        "category": "Folder",
        "description": "Get the name of a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "get_folder_subfolders": {
        "function": get_subfolder_list,
        "category": "Folder",
        "description": "Get the list of subfolders in a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "get_is_folder_stale": {
        "function": get_is_folder_stale,
        "category": "Folder",
        "description": "Check if a folder's content is stale and needs to be refreshed",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "get_folder_unique_id": {
        "function": get_unique_id,
        "category": "Folder",
        "description": "Get the unique ID of a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "export_folder": {
        "function": export_folder,
        "category": "Folder",
        "description": "Export a folder to a specified file path",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
            {
                "name": "file_path",
                "type": "str",
                "description": "Path where the folder will be exported",
                "required": True,
            },
        ],
    },
    "transcribe_folder_audio": {
        "function": transcribe_audio,
        "category": "Folder",
        "description": "Transcribe audio content in a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
    "clear_folder_transcription": {
        "function": clear_transcription,
        "category": "Folder",
        "description": "Clear transcription data for a folder",
        "parameters": [
            {
                "name": "folder_id",
                "type": "str",
                "description": "ID of the folder",
                "required": True,
            },
        ],
    },
}

def get_all_tools() -> List[Dict[str, Any]]:
    """
    Get all available tools
    
    Returns:
        List of tools with their descriptions and parameters
    """
    tools = []
    
    for tool_id, tool_info in TOOLS_REGISTRY.items():
        tools.append({
            "name": tool_id,  # Use the tool_id as the name
            "description": tool_info.get("description", ""),
            "component": "timeline_item",  # Add a default component
            "parameters": tool_info.get("parameters", {})
        })
    
    return tools

def get_tools_by_component() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get tools organized by component
    
    Returns:
        Dictionary mapping component names to lists of tools
    """
    tools_by_component = {}
    
    for tool_id, tool_info in TOOLS_REGISTRY.items():
        component = "timeline_item"  # Default component
        
        if component not in tools_by_component:
            tools_by_component[component] = []
            
        tools_by_component[component].append({
            "name": tool_id,  # Use the tool_id as the name
            "description": tool_info.get("description", ""),
            "parameters": tool_info.get("parameters", {})
        })
    
    return tools_by_component

def execute_tool(tool_name: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Execute a tool by name with the provided parameters
    
    Args:
        tool_name: Name of the tool to execute
        parameters: Parameters to pass to the tool
        
    Returns:
        Result of the tool execution
    """
    if parameters is None:
        parameters = {}
    
    if tool_name not in TOOLS_REGISTRY:
        return {
            "success": False,
            "error": f"Tool not found: {tool_name}",
            "message": "Use 'search' to see available tools"
        }
    
    try:
        tool_info = TOOLS_REGISTRY[tool_name]
        tool_function = tool_info["function"]
        
        logger.info(f"Executing tool: {tool_name} with parameters: {parameters}")
        result = tool_function(**parameters)
        
        return {
            "success": True,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error executing tool {tool_name}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Tool execution failed"
        } 