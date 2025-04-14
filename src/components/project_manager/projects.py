"""
Project Management Functions
Implements project-specific operations from the ProjectManager component
"""

import logging
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_resolve, get_project_manager, safe_api_call

logger = logging.getLogger("resolve_api.components.project_manager.projects")

def create_project(project_name: str) -> Dict[str, Any]:
    """
    Creates a new project with the given name
    
    Args:
        project_name: Name for the new project
        
    Returns:
        Dictionary with success status and project info or error
    """
    def _create_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Create the project
        project = project_manager.CreateProject(project_name)
        
        if not project:
            raise RuntimeError(f"Failed to create project '{project_name}', may already exist")
            
        # Return basic project info
        return {
            "name": project.GetName(),
            "created": True
        }
        
    return safe_api_call(
        _create_project,
        f"Error creating project '{project_name}'"
    )

def delete_project(project_name: str) -> Dict[str, Any]:
    """
    Deletes a project with the given name from the current folder
    
    Args:
        project_name: Name of the project to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Delete the project
        result = project_manager.DeleteProject(project_name)
        
        if not result:
            raise RuntimeError(f"Failed to delete project '{project_name}', may not exist or is currently loaded")
            
        return {
            "deleted": True,
            "project_name": project_name
        }
        
    return safe_api_call(
        _delete_project,
        f"Error deleting project '{project_name}'"
    )

def load_project(project_name: str) -> Dict[str, Any]:
    """
    Loads an existing project with the given name
    
    Args:
        project_name: Name of the project to load
        
    Returns:
        Dictionary with success status and project info or error
    """
    def _load_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Load the project
        project = project_manager.LoadProject(project_name)
        
        if not project:
            raise RuntimeError(f"Failed to load project '{project_name}', may not exist")
            
        # Return basic project info
        return {
            "name": project.GetName(),
            "loaded": True
        }
        
    return safe_api_call(
        _load_project,
        f"Error loading project '{project_name}'"
    )

def save_project() -> Dict[str, Any]:
    """
    Saves the currently loaded project
    
    Returns:
        Dictionary with success status or error
    """
    def _save_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get current project
        project = project_manager.GetCurrentProject()
        if not project:
            raise RuntimeError("No project is currently loaded")
            
        # Save the project
        result = project_manager.SaveProject()
        
        if not result:
            raise RuntimeError("Failed to save project")
            
        return {
            "saved": True,
            "project_name": project.GetName()
        }
        
    return safe_api_call(
        _save_project,
        "Error saving project"
    )

def close_project() -> Dict[str, Any]:
    """
    Closes the currently loaded project without saving
    
    Returns:
        Dictionary with success status or error
    """
    def _close_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get current project
        project = project_manager.GetCurrentProject()
        if not project:
            raise RuntimeError("No project is currently loaded")
            
        # Save the project name before closing
        project_name = project.GetName()
        
        # Close the project
        result = project_manager.CloseProject(project)
        
        if not result:
            raise RuntimeError("Failed to close project")
            
        return {
            "closed": True,
            "project_name": project_name
        }
        
    return safe_api_call(
        _close_project,
        "Error closing project"
    )

def archive_project(
    project_name: str, 
    file_path: str, 
    archive_src_media: bool = True, 
    archive_render_cache: bool = True, 
    archive_proxy_media: bool = False
) -> Dict[str, Any]:
    """
    Archives a project to the specified file path with the given configuration
    
    Args:
        project_name: Name of the project to archive
        file_path: Path where the archive will be saved
        archive_src_media: Whether to include source media in the archive
        archive_render_cache: Whether to include render cache in the archive
        archive_proxy_media: Whether to include proxy media in the archive
        
    Returns:
        Dictionary with success status or error
    """
    def _archive_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Archive the project
        result = project_manager.ArchiveProject(
            project_name,
            file_path,
            archive_src_media,
            archive_render_cache,
            archive_proxy_media
        )
        
        if not result:
            raise RuntimeError(f"Failed to archive project '{project_name}'")
            
        return {
            "archived": True,
            "project_name": project_name,
            "archive_path": file_path,
            "configuration": {
                "archive_src_media": archive_src_media,
                "archive_render_cache": archive_render_cache,
                "archive_proxy_media": archive_proxy_media
            }
        }
        
    return safe_api_call(
        _archive_project,
        f"Error archiving project '{project_name}'"
    )

def import_project(file_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Imports a project from the specified file path
    
    Args:
        file_path: Path to the project file to import
        project_name: Optional name to give the imported project
        
    Returns:
        Dictionary with success status or error
    """
    def _import_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Import the project
        if project_name:
            result = project_manager.ImportProject(file_path, project_name)
        else:
            result = project_manager.ImportProject(file_path)
        
        if not result:
            raise RuntimeError(f"Failed to import project from '{file_path}'")
            
        return {
            "imported": True,
            "file_path": file_path,
            "project_name": project_name if project_name else "Default name from file"
        }
        
    return safe_api_call(
        _import_project,
        f"Error importing project from '{file_path}'"
    )

def export_project(
    project_name: str, 
    file_path: str, 
    with_stills_and_luts: bool = True
) -> Dict[str, Any]:
    """
    Exports a project to the specified file path
    
    Args:
        project_name: Name of the project to export
        file_path: Path where the project will be exported
        with_stills_and_luts: Whether to include stills and LUTs in the export
        
    Returns:
        Dictionary with success status or error
    """
    def _export_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Export the project
        result = project_manager.ExportProject(project_name, file_path, with_stills_and_luts)
        
        if not result:
            raise RuntimeError(f"Failed to export project '{project_name}'")
            
        return {
            "exported": True,
            "project_name": project_name,
            "export_path": file_path,
            "with_stills_and_luts": with_stills_and_luts
        }
        
    return safe_api_call(
        _export_project,
        f"Error exporting project '{project_name}'"
    )

def restore_project(file_path: str, project_name: Optional[str] = None) -> Dict[str, Any]:
    """
    Restores a project from the specified archive file path
    
    Args:
        file_path: Path to the archive file
        project_name: Optional name to give the restored project
        
    Returns:
        Dictionary with success status or error
    """
    def _restore_project():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Restore the project
        if project_name:
            result = project_manager.RestoreProject(file_path, project_name)
        else:
            result = project_manager.RestoreProject(file_path)
        
        if not result:
            raise RuntimeError(f"Failed to restore project from '{file_path}'")
            
        return {
            "restored": True,
            "file_path": file_path,
            "project_name": project_name if project_name else "Default name from archive"
        }
        
    return safe_api_call(
        _restore_project,
        f"Error restoring project from '{file_path}'"
    ) 