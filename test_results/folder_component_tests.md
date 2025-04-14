# Folder Component Function Tests

## Test Requirements

To test the Folder component functions, we need:
1. A valid folder ID from the Media Pool
2. A properly functioning MCP server connected to DaVinci Resolve

## Functions to Test

1. **get_is_folder_stale** - Check if a folder's content is stale and needs refreshing
2. **get_folder_unique_id** - Get the unique ID of a folder
3. **export_folder** - Export a folder to a file path
4. **transcribe_folder_audio** - Transcribe audio content in a folder
5. **clear_folder_transcription** - Clear transcription data for a folder

## Test Procedure

### Test Setup

1. Ensure DaVinci Resolve is running
2. Ensure the MCP server is running (`bash run_mcp_server.sh`)
3. Create a test project with folders and media
4. Get a valid folder ID to use for testing:
   ```python
   # Get root folder and its ID
   root_folder_result = get_media_pool_root_folder()
   root_folder_id = root_folder_result["id"]
   ```

### Individual Function Tests

#### 1. get_is_folder_stale

**Function Purpose**: Check if a folder's content is stale and needs refreshing

**Test Procedure**:
1. Call function with valid folder ID
2. Verify return structure includes folder_id and is_stale keys

**Expected Result**: 
- Returns a dictionary with folder_id and is_stale (boolean) keys
- The is_stale value should indicate if folder content is stale

#### 2. get_folder_unique_id

**Function Purpose**: Get the unique ID of a folder

**Test Procedure**:
1. Call function with valid folder ID
2. Verify return structure includes folder_id and unique_id keys

**Expected Result**:
- Returns a dictionary with folder_id and unique_id keys
- The unique_id should match the input folder_id if using a folder's own ID

#### 3. export_folder

**Function Purpose**: Export a folder to a file path

**Test Procedure**:
1. Call function with valid folder ID and file path
2. Verify file is created at specified location

**Expected Result**:
- Returns a dictionary with success, folder_id, and export_path keys
- Should create a file at the specified path

#### 4. transcribe_folder_audio

**Function Purpose**: Transcribe audio content in a folder

**Test Procedure**:
1. Create folder with audio clips
2. Call function with valid folder ID
3. Verify transcription operation begins

**Expected Result**:
- Returns a dictionary with success, folder_id, and transcription_started keys
- Should start the transcription process for audio in the folder

#### 5. clear_folder_transcription

**Function Purpose**: Clear transcription data for a folder

**Test Procedure**:
1. Use folder with existing transcription data
2. Call function with valid folder ID
3. Verify transcription data is cleared

**Expected Result**:
- Returns a dictionary with success, folder_id, and transcription_cleared keys
- Should clear any existing transcription data for the folder

## Testing Notes

- These folder functions all require a valid folder ID to work properly
- Without a properly connected MCP server, we cannot obtain valid folder IDs to test
- Once the MCP server is running, we should:
  1. Get a valid folder ID from the Media Pool
  2. Create test folders with appropriate content (audio for transcription tests)
  3. Test each function with proper parameters
  4. Document results and any issues found

## Issues Encountered During Testing

1. **MCP Server Connection**: The MCP server needs to be properly running and connected to DaVinci Resolve for testing.
2. **Folder ID Requirement**: All folder functions require a valid folder ID, which must be obtained through the MediaPool.
3. **Test Content Requirements**: Functions like transcribe_folder_audio require specific content types to test properly.

## Recommendations for Implementation

1. Add better error handling for cases when invalid folder IDs are provided
2. Provide clear documentation on how to obtain valid folder IDs
3. Consider adding helper functions to simplify working with folders 