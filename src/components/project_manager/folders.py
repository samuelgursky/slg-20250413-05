"""
Folder and Database Management Functions
Implements folder and database operations from the ProjectManager component
"""

import logging
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_resolve, get_project_manager, safe_api_call

logger = logging.getLogger("resolve_api.components.project_manager.folders")

def create_folder(folder_name: str) -> Dict[str, Any]:
    """
    Creates a new folder in the current location
    
    Args:
        folder_name: Name for the new folder
        
    Returns:
        Dictionary with success status or error
    """
    def _create_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Create the folder
        result = project_manager.CreateFolder(folder_name)
        
        if not result:
            raise RuntimeError(f"Failed to create folder '{folder_name}', may already exist")
            
        return {
            "created": True,
            "folder_name": folder_name,
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _create_folder,
        f"Error creating folder '{folder_name}'"
    )

def delete_folder(folder_name: str) -> Dict[str, Any]:
    """
    Deletes a folder in the current location
    
    Args:
        folder_name: Name of the folder to delete
        
    Returns:
        Dictionary with success status or error
    """
    def _delete_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Delete the folder
        result = project_manager.DeleteFolder(folder_name)
        
        if not result:
            raise RuntimeError(f"Failed to delete folder '{folder_name}', may not exist or contains projects")
            
        return {
            "deleted": True,
            "folder_name": folder_name,
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _delete_folder,
        f"Error deleting folder '{folder_name}'"
    )

def get_project_list() -> Dict[str, Any]:
    """
    Gets the list of projects in the current folder
    
    Returns:
        Dictionary with list of projects or error
    """
    def _get_project_list():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get the project list
        projects = project_manager.GetProjectListInCurrentFolder()
        
        return {
            "projects": projects,
            "count": len(projects),
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _get_project_list,
        "Error getting project list"
    )

def get_folder_list() -> Dict[str, Any]:
    """
    Gets the list of folders in the current folder
    
    Returns:
        Dictionary with list of folders or error
    """
    def _get_folder_list():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get the folder list
        folders = project_manager.GetFolderListInCurrentFolder()
        
        return {
            "folders": folders,
            "count": len(folders),
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _get_folder_list,
        "Error getting folder list"
    )

def goto_root_folder() -> Dict[str, Any]:
    """
    Navigates to the root folder in the database
    
    Returns:
        Dictionary with success status or error
    """
    def _goto_root_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Go to root folder
        result = project_manager.GotoRootFolder()
        
        if not result:
            raise RuntimeError("Failed to navigate to root folder")
            
        return {
            "success": True,
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _goto_root_folder,
        "Error navigating to root folder"
    )

def goto_parent_folder() -> Dict[str, Any]:
    """
    Navigates to the parent folder of the current folder
    
    Returns:
        Dictionary with success status or error
    """
    def _goto_parent_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Save current folder name before navigating
        current_folder = project_manager.GetCurrentFolder()
            
        # Go to parent folder
        result = project_manager.GotoParentFolder()
        
        if not result:
            raise RuntimeError("Failed to navigate to parent folder, may already be at root")
            
        return {
            "success": True,
            "previous_folder": current_folder,
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _goto_parent_folder,
        "Error navigating to parent folder"
    )

def get_current_folder() -> Dict[str, Any]:
    """
    Gets the current folder name
    
    Returns:
        Dictionary with current folder name or error
    """
    def _get_current_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get current folder
        folder_name = project_manager.GetCurrentFolder()
        
        return {
            "current_folder": folder_name
        }
        
    return safe_api_call(
        _get_current_folder,
        "Error getting current folder"
    )

def open_folder(folder_name: str) -> Dict[str, Any]:
    """
    Opens a folder with the given name
    
    Args:
        folder_name: Name of the folder to open
        
    Returns:
        Dictionary with success status or error
    """
    def _open_folder():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Save current folder name before opening
        previous_folder = project_manager.GetCurrentFolder()
            
        # Open the folder
        result = project_manager.OpenFolder(folder_name)
        
        if not result:
            raise RuntimeError(f"Failed to open folder '{folder_name}', may not exist")
            
        return {
            "success": True,
            "previous_folder": previous_folder,
            "current_folder": project_manager.GetCurrentFolder()
        }
        
    return safe_api_call(
        _open_folder,
        f"Error opening folder '{folder_name}'"
    )

def get_current_database() -> Dict[str, Any]:
    """
    Gets the current database information
    
    Returns:
        Dictionary with database information or error
    """
    def _get_current_database():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get current database
        db_info = project_manager.GetCurrentDatabase()
        
        return {
            "database": db_info
        }
        
    return safe_api_call(
        _get_current_database,
        "Error getting current database"
    )

def get_database_list() -> Dict[str, Any]:
    """
    Gets the list of available databases
    
    Returns:
        Dictionary with list of databases or error
    """
    def _get_database_list():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Get database list
        databases = project_manager.GetDatabaseList()
        
        return {
            "databases": databases,
            "count": len(databases)
        }
        
    return safe_api_call(
        _get_database_list,
        "Error getting database list"
    )

def set_current_database(db_info: Dict[str, str]) -> Dict[str, Any]:
    """
    Sets the current database
    
    Args:
        db_info: Dictionary with database information
               Required keys: 'DbType' ('Disk' or 'PostgreSQL'), 'DbName'
               Optional key: 'IpAddress' (defaults to '127.0.0.1' for PostgreSQL)
        
    Returns:
        Dictionary with success status or error
    """
    def _set_current_database():
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
        
        # Validate database info
        if 'DbType' not in db_info:
            raise ValueError("Database info must include 'DbType' key ('Disk' or 'PostgreSQL')")
        
        if db_info['DbType'] not in ['Disk', 'PostgreSQL']:
            raise ValueError("DbType must be 'Disk' or 'PostgreSQL'")
            
        if 'DbName' not in db_info:
            raise ValueError("Database info must include 'DbName' key")
            
        # Set current database
        result = project_manager.SetCurrentDatabase(db_info)
        
        if not result:
            raise RuntimeError(f"Failed to set current database to {db_info}")
            
        # Get the new current database info
        current_db = project_manager.GetCurrentDatabase()
            
        return {
            "success": True,
            "database": current_db
        }
        
    return safe_api_call(
        _set_current_database,
        "Error setting current database"
    ) 