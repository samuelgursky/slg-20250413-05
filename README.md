# DaVinci Resolve MCP Agent

This project implements a Model Context Protocol (MCP) agent setup for interacting with DaVinci Resolve. The system allows external agents (like Claude or other LLMs) to discover and execute tools to control DaVinci Resolve through a component-based MCP server.

## Architecture

The implementation follows a component-based architecture:

1. **Core API Layer**
   - `resolve_api.py`: Core connectivity to DaVinci Resolve's API
   - Provides utility functions for safe API calls and environment configuration

2. **Component Layer**
   - Organizes functionality by DaVinci Resolve API components
   - Each component (Resolve, Project, Timeline, etc.) is implemented in a separate module
   - Components are structured according to Resolve's API hierarchy

3. **Tools Registry**
   - `tools/registration.py`: Centralized registration of all available tools
   - Provides tool discovery and execution mechanisms

4. **MCP Server**
   - `main.py`: Entry point that sets up the environment and starts the MCP server
   - Responds to search and execute commands from client applications

## Prerequisites

- **DaVinci Resolve Studio**: Installed and running
- **Python 3.7+**: Required for running the server
- **MCP SDK**: Install via pip:
  ```bash
  pip install mcp[cli]
  ```
  
## Setup

1. Make sure DaVinci Resolve is correctly installed on your system.
2. Ensure the Python SDK for DaVinci Resolve is properly configured:
   - On macOS: Files should be in `/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting`
   - On Windows: Files should be in `C:\ProgramData\Blackmagic Design\DaVinci Resolve\Support\Developer\Scripting`
3. Clone this repository or download the scripts to a local directory.
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the MCP Server

1. Open DaVinci Resolve and create or open a project.
2. In your terminal, navigate to the project directory.
3. Run the server:
   ```bash
   python src/main.py
   ```
   or use the provided script:
   ```bash
   ./scripts/run_mcp_server.sh
   ```

### Using with Claude or Other LLMs

To use this MCP agent setup with Claude:

1. Start the MCP server:
   ```bash
   python src/main.py
   ```

2. Use the MCP CLI to register the server with Claude:
   ```bash
   mcp install src/main.py --name "DaVinci Resolve Tools"
   ```

3. Claude can then discover and execute tools using the MCP interface.

## Available Tools

The implementation organizes tools by component, following the structure of the DaVinci Resolve API:

### Resolve (General)
- **get_product_info**: Get DaVinci Resolve product information (name and version)
- **get_current_page**: Get the current page displayed in DaVinci Resolve
- **open_page**: Switch to the specified page in DaVinci Resolve
- **get_keyframe_mode**: Get the current keyframe mode
- **set_keyframe_mode**: Set the keyframe mode
- **manage_layout_preset**: Manage layout presets (load, save, update, delete, import, export)
- **manage_render_preset**: Manage render presets (import, export)
- **manage_burn_in_preset**: Manage burn-in presets (import, export)
- **quit_resolve**: Quit DaVinci Resolve application

### ProjectManager
- **create_project**: Create a new project with the specified name
- **load_project**: Load an existing project with the specified name
- **save_project**: Save the currently loaded project
- **close_project**: Close the currently loaded project without saving
- **delete_project**: Delete a project with the specified name
- **archive_project**: Archive a project to a file
- **import_project**: Import a project from a file
- **export_project**: Export a project to a file
- **restore_project**: Restore a project from a backup
- **create_folder**: Create a new folder in the current location
- **delete_folder**: Delete a folder with the specified name
- **get_project_list**: Get a list of all projects in the current folder
- **get_folder_list**: Get a list of all folders in the current folder
- **get_current_folder**: Get the name of the current folder in the project manager
- **open_folder**: Open a folder with the specified name
- **goto_root_folder**: Navigate to the root folder in the database
- **goto_parent_folder**: Navigate to the parent folder of the current folder
- **get_current_database**: Get the name of the current database
- **get_database_list**: Get a list of all available databases
- **set_current_database**: Set the current database by name
- **create_cloud_project**: Create a new project in DaVinci Resolve cloud database
- **load_cloud_project**: Load a project from DaVinci Resolve cloud database
- **import_cloud_project**: Import a project from DaVinci Resolve cloud database to local database
- **restore_cloud_project**: Restore a project from DaVinci Resolve cloud database

### Project
- **get_project_info**: Get information about the current project
- **get_project_settings**: Get all settings for the current project
- **get_all_timelines**: Get a list of all timelines in the current project

### Media Pool
- **list_media_pool_items**: List items in the current media pool folder
- **get_folder_structure**: Get the media pool folder structure

### Timeline
- **get_timeline_details**: Get details about the current timeline
- **get_timeline_tracks**: Get details about all tracks in the current timeline
- **get_timeline_items**: Get details about items in the current timeline

## Implementation and Testing Status

The project is being developed component by component, with testing done as components are completed:

- **ProjectManager**: 100% implemented (24/24 functions) and extensively tested
- **Resolve**: 89% implemented (17/19 functions), partially tested
- **Project**: 12% implemented (5/42 functions), partially tested
- **MediaPool**: 9% implemented (2/23 functions), partially tested
- **Timeline**: 14% implemented (8/56 functions), partially tested
- **Other Components**: Implementation in progress

During testing, we identified and fixed several parameter mismatches between function implementations and their tool registrations. This ensures consistent parameter naming across the API and improves reliability of the tools.

See the full tracking document (`API_IMPLEMENTATION_TRACKING.md`) for detailed implementation status.

## Extending the Tools

To add new tools to interact with DaVinci Resolve:

1. **Identify the Component**:
   - Determine which component the tool belongs to (Resolve, Project, Timeline, etc.)
   - Create a new file in the appropriate component directory if needed

2. **Implement the Tool Function**:
   ```python
   def your_new_tool(param1, param2) -> Dict[str, Any]:
       """
       Description of what your tool does
       
       Args:
           param1: Description
           param2: Description
           
       Returns:
           Dictionary with success status and result data
       """
       return safe_api_call(
           lambda: {"your_result_key": your_actual_function_logic()},
           "Error message if it fails"
       )
   ```

3. **Register the Tool**:
   - Add your tool to `tools/registration.py`:
   ```python
   "your_new_tool": {
       "name": "your_new_tool",
       "description": "Description of what your tool does",
       "component": "component_name",
       "function": your_new_tool,
       "parameters": [
           {"name": "param1", "type": "string", "description": "Description", "required": True},
           {"name": "param2", "type": "integer", "description": "Description", "required": False}
       ]
   }
   ```

4. **Export the Tool**:
   - Update the component's `__init__.py` to export your tool

5. **Restart the MCP Server** to make the new tool available

## Troubleshooting

- **ImportError for DaVinciResolveScript**: Ensure your environment variables are correctly set and DaVinci Resolve's Python API is installed correctly
- **No tools found**: Make sure DaVinci Resolve is running with an open project
- **Connection errors**: Check if any other process is using the same port
- **Parameter mismatches**: If a tool fails with an unexpected keyword argument error, check the parameter names in the implementation versus registration

## Component Structure

The project follows the component structure of the DaVinci Resolve API:
- **Resolve**: General API functions directly available from the Resolve object
- **ProjectManager**: Project database and management functions
- **Project**: Current project functions
- **MediaStorage**: Media and file system navigation
- **MediaPool**: Media organization within a project
- **Timeline**: Timeline operations and editing
- **TimelineItem**: Individual clip functions in a timeline
- **Gallery**: Still image management
- **Graph**: Node-based effects and color grading
- **ColorGroup**: Color group management

## License

MIT

## Acknowledgements

This project is built using the Model Context Protocol (MCP) SDK, which enables standardized interaction between language models and external tools. 