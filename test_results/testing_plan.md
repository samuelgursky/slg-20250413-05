# DaVinci Resolve MCP Testing Plan

This document outlines the plan for testing all untested functions in the DaVinci Resolve MCP project.

## Testing Environment Setup

1. **Project Setup**:
   - Create a test project with multiple timelines
   - Import various media types (video, audio, images)
   - Create compound clips and apply effects
   - Set up color groups and grades

2. **Testing Tools**:
   - DaVinci Resolve (latest version)
   - Sample media files (video, audio, images)
   - Test scripts to execute functions

## Functions to Test by Component

### 1. Timeline Component (7 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| SetStartTimecode | set_start_timecode | Set a new start timecode on current timeline | Active timeline |
| SetClipsLinked | set_clips_linked | Select clips and set linked state | Timeline with multiple clips |
| GetCurrentVideoItem | get_current_video_item | Get clip at playhead position | Timeline with clips |
| GetCurrentClipThumbnailImage | get_current_clip_thumbnail_image | Get thumbnail of clip at playhead | Timeline with video clips |
| CreateFusionClip | create_fusion_clip | Create Fusion clip from selected items | Timeline with multiple clips |
| ImportIntoTimeline | import_into_timeline | Import media into timeline | Media files ready |
| GrabAllStills | grab_all_stills | Grab stills from all timeline clips | Timeline with multiple clips |

### 2. Folder Component (5 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| GetIsFolderStale | get_is_folder_stale | Check folder stale status | Media pool with folders |
| GetUniqueId | get_folder_unique_id | Get folder unique ID | Media pool with folders |
| Export | export_folder | Export folder to file | Media pool with folders and clips |
| TranscribeAudio | transcribe_folder_audio | Transcribe audio content | Folder with audio clips |
| ClearTranscription | clear_folder_transcription | Clear folder transcription | Folder with transcribed audio |

### 3. Gallery Component (8 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| GetAlbumName | get_album_name | Get name of a gallery album | Create test gallery album |
| SetAlbumName | set_album_name | Set name of a gallery album | Existing gallery album |
| GetCurrentStillAlbum | get_current_still_album | Get current still album info | Gallery with stills |
| SetCurrentStillAlbum | set_current_still_album | Set current still album | Multiple gallery albums |
| GetGalleryStillAlbums | get_gallery_still_albums | Get all still albums | Gallery with albums |
| GetGalleryPowerGradeAlbums | get_gallery_power_grade_albums | Get power grade albums | Gallery with power grades |
| CreateGalleryStillAlbum | create_gallery_still_album | Create new still album | Gallery access |
| CreateGalleryPowerGradeAlbum | create_gallery_power_grade_album | Create power grade album | Gallery access |

### 4. GalleryStillAlbum Component (6 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| GetStills | get_stills | Get all stills from album | Album with stills |
| GetLabel | get_album_label | Get album label | Existing album |
| SetLabel | set_album_label | Set album label | Existing album |
| ImportStills | import_stills | Import stills to album | Image files ready |
| ExportStills | export_stills | Export stills from album | Album with stills |
| DeleteStills | delete_stills | Delete stills from album | Album with stills |

### 5. Graph Component (11 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| GetNumNodes | get_num_nodes | Get node count | Color page with nodes |
| SetLUT | set_lut | Set LUT for a node | Color page with nodes |
| GetLUT | get_lut | Get LUT information | Node with LUT applied |
| SetNodeCacheMode | set_node_cache_mode | Set node cache mode | Color page with nodes |
| GetNodeCacheMode | get_node_cache_mode | Get node cache mode | Color page with nodes |
| GetNodeLabel | get_node_label | Get node label | Color page with nodes |
| GetToolsInNode | get_tools_in_node | Get tools in node | Color page with nodes |
| SetNodeEnabled | set_node_enabled | Enable/disable node | Color page with nodes |
| ApplyGradeFromDRX | apply_grade_from_drx | Apply DRX grade | DRX file ready |
| ApplyArriCdlLut | apply_arri_cdl_lut | Apply ARRI CDL LUT | ARRI CDL file ready |
| ResetAllGrades | reset_all_grades | Reset all grades | Color page with grades |

### 6. ColorGroup Component (5 untested functions)

| Function | Tool Name | Test Procedure | Prerequisites |
|----------|-----------|---------------|---------------|
| GetName | get_color_group_name | Get color group name | Project with color groups |
| SetName | set_color_group_name | Set color group name | Existing color group |
| GetClipsInTimeline | get_color_group_clips_in_timeline | Get clips in a color group | Timeline with grouped clips |
| GetPreClipNodeGraph | get_color_group_pre_clip_node_graph | Get pre-clip graph | Color group with nodes |
| GetPostClipNodeGraph | get_color_group_post_clip_node_graph | Get post-clip graph | Color group with nodes |

## Testing Workflow

1. **Preparation**:
   - Ensure DaVinci Resolve is running
   - Set up test project with required media
   - Set active page appropriate for the test

2. **Testing Process**:
   - Test each function with both valid and invalid parameters
   - Document success/failure for each test
   - For failures, note specific error messages and conditions
   - Update API_IMPLEMENTATION_TRACKING.md with test results

3. **Documentation**:
   - Update each function's status in API_IMPLEMENTATION_TRACKING.md
   - Add notes about any workarounds required
   - Update the implementation percentage statistics

## Priority Order

1. Timeline Component functions - these are core to editing operations
2. Folder Component functions - these are frequently used in media management
3. Graph Component functions - important for color grading
4. ColorGroup Component functions - important for organized grading
5. Gallery Component functions - useful for still management
6. GalleryStillAlbum Component functions - useful for still organization

## Expected Outcomes

After completing this testing plan, all implemented functions should be marked as tested in the API_IMPLEMENTATION_TRACKING.md file, with clear notes about any limitations or special requirements. The overall testing percentage should increase to 100% of implemented functions. 