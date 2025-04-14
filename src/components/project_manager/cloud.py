"""
Cloud Project Management Functions
Implements cloud project operations from the ProjectManager component
"""

import logging
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_resolve, get_project_manager, safe_api_call

logger = logging.getLogger("resolve_api.components.project_manager.cloud")

def create_cloud_project(cloud_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Creates a new cloud project with the given settings
    
    Args:
        cloud_settings: Dictionary with cloud settings
            Required keys:
            - 'project_name': String
            - 'project_media_path': String
            Optional keys:
            - 'is_collab': Bool (default False)
            - 'sync_mode': String ('none', 'proxy_only', 'proxy_and_orig') (default 'proxy_only')
            - 'is_camera_access': Bool (default False)
        
    Returns:
        Dictionary with success status and project info or error
    """
    def _create_cloud_project():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get Resolve object")
            
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Validate required fields
        if 'project_name' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_name'")
            
        if 'project_media_path' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_media_path'")
            
        # Prepare cloud settings in format expected by the API
        api_cloud_settings = {
            resolve.CLOUD_SETTING_PROJECT_NAME: cloud_settings['project_name'],
            resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH: cloud_settings['project_media_path'],
            resolve.CLOUD_SETTING_IS_COLLAB: cloud_settings.get('is_collab', False)
        }
        
        # Handle sync mode
        sync_mode = cloud_settings.get('sync_mode', 'proxy_only').lower()
        if sync_mode == 'none':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_NONE
        elif sync_mode == 'proxy_and_orig':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_AND_ORIG
        else:  # Default to 'proxy_only'
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_ONLY
            
        # Handle camera access
        api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS] = cloud_settings.get('is_camera_access', False)
        
        # Create the cloud project
        project = project_manager.CreateCloudProject(api_cloud_settings)
        
        if not project:
            raise RuntimeError(f"Failed to create cloud project '{cloud_settings['project_name']}'")
            
        # Return basic project info
        return {
            "name": project.GetName(),
            "created": True,
            "cloud_settings": {
                "project_name": cloud_settings['project_name'],
                "project_media_path": cloud_settings['project_media_path'],
                "is_collab": api_cloud_settings[resolve.CLOUD_SETTING_IS_COLLAB],
                "sync_mode": sync_mode,
                "is_camera_access": api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS]
            }
        }
        
    return safe_api_call(
        _create_cloud_project,
        f"Error creating cloud project '{cloud_settings.get('project_name', 'unknown')}'"
    )

def load_cloud_project(cloud_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Loads an existing cloud project with the given settings
    
    Args:
        cloud_settings: Dictionary with cloud settings
            Required keys:
            - 'project_name': String
            - 'project_media_path': String
            Optional keys:
            - 'sync_mode': String ('none', 'proxy_only', 'proxy_and_orig') (default 'proxy_only')
        
    Returns:
        Dictionary with success status and project info or error
    """
    def _load_cloud_project():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get Resolve object")
            
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Validate required fields
        if 'project_name' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_name'")
            
        if 'project_media_path' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_media_path'")
            
        # Prepare cloud settings in format expected by the API
        api_cloud_settings = {
            resolve.CLOUD_SETTING_PROJECT_NAME: cloud_settings['project_name'],
            resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH: cloud_settings['project_media_path']
        }
        
        # Handle sync mode
        sync_mode = cloud_settings.get('sync_mode', 'proxy_only').lower()
        if sync_mode == 'none':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_NONE
        elif sync_mode == 'proxy_and_orig':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_AND_ORIG
        else:  # Default to 'proxy_only'
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_ONLY
        
        # Load the cloud project
        project = project_manager.LoadCloudProject(api_cloud_settings)
        
        if not project:
            raise RuntimeError(f"Failed to load cloud project '{cloud_settings['project_name']}'")
            
        # Return basic project info
        return {
            "name": project.GetName(),
            "loaded": True,
            "cloud_settings": {
                "project_name": cloud_settings['project_name'],
                "project_media_path": cloud_settings['project_media_path'],
                "sync_mode": sync_mode
            }
        }
        
    return safe_api_call(
        _load_cloud_project,
        f"Error loading cloud project '{cloud_settings.get('project_name', 'unknown')}'"
    )

def import_cloud_project(file_path: str, cloud_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Imports a project as a cloud project from the specified file path
    
    Args:
        file_path: Path to the project file to import
        cloud_settings: Dictionary with cloud settings
            Required keys:
            - 'project_name': String
            - 'project_media_path': String
            Optional keys:
            - 'is_collab': Bool (default False)
            - 'sync_mode': String ('none', 'proxy_only', 'proxy_and_orig') (default 'proxy_only')
            - 'is_camera_access': Bool (default False)
        
    Returns:
        Dictionary with success status or error
    """
    def _import_cloud_project():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get Resolve object")
            
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Validate required fields
        if 'project_name' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_name'")
            
        if 'project_media_path' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_media_path'")
            
        # Prepare cloud settings in format expected by the API
        api_cloud_settings = {
            resolve.CLOUD_SETTING_PROJECT_NAME: cloud_settings['project_name'],
            resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH: cloud_settings['project_media_path'],
            resolve.CLOUD_SETTING_IS_COLLAB: cloud_settings.get('is_collab', False)
        }
        
        # Handle sync mode
        sync_mode = cloud_settings.get('sync_mode', 'proxy_only').lower()
        if sync_mode == 'none':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_NONE
        elif sync_mode == 'proxy_and_orig':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_AND_ORIG
        else:  # Default to 'proxy_only'
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_ONLY
            
        # Handle camera access
        api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS] = cloud_settings.get('is_camera_access', False)
        
        # Import the cloud project
        result = project_manager.ImportCloudProject(file_path, api_cloud_settings)
        
        if not result:
            raise RuntimeError(f"Failed to import cloud project from '{file_path}'")
            
        return {
            "imported": True,
            "file_path": file_path,
            "cloud_settings": {
                "project_name": cloud_settings['project_name'],
                "project_media_path": cloud_settings['project_media_path'],
                "is_collab": api_cloud_settings[resolve.CLOUD_SETTING_IS_COLLAB],
                "sync_mode": sync_mode,
                "is_camera_access": api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS]
            }
        }
        
    return safe_api_call(
        _import_cloud_project,
        f"Error importing cloud project from '{file_path}'"
    )

def restore_cloud_project(folder_path: str, cloud_settings: Dict[str, Any]) -> Dict[str, Any]:
    """
    Restores a project as a cloud project from the specified folder path
    
    Args:
        folder_path: Path to the folder containing the project archive
        cloud_settings: Dictionary with cloud settings
            Required keys:
            - 'project_name': String
            - 'project_media_path': String
            Optional keys:
            - 'is_collab': Bool (default False)
            - 'sync_mode': String ('none', 'proxy_only', 'proxy_and_orig') (default 'proxy_only')
            - 'is_camera_access': Bool (default False)
        
    Returns:
        Dictionary with success status or error
    """
    def _restore_cloud_project():
        resolve = get_resolve()
        if not resolve:
            raise RuntimeError("Failed to get Resolve object")
            
        project_manager = get_project_manager()
        if not project_manager:
            raise RuntimeError("Failed to get Project Manager")
            
        # Validate required fields
        if 'project_name' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_name'")
            
        if 'project_media_path' not in cloud_settings:
            raise ValueError("Cloud settings must include 'project_media_path'")
            
        # Prepare cloud settings in format expected by the API
        api_cloud_settings = {
            resolve.CLOUD_SETTING_PROJECT_NAME: cloud_settings['project_name'],
            resolve.CLOUD_SETTING_PROJECT_MEDIA_PATH: cloud_settings['project_media_path'],
            resolve.CLOUD_SETTING_IS_COLLAB: cloud_settings.get('is_collab', False)
        }
        
        # Handle sync mode
        sync_mode = cloud_settings.get('sync_mode', 'proxy_only').lower()
        if sync_mode == 'none':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_NONE
        elif sync_mode == 'proxy_and_orig':
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_AND_ORIG
        else:  # Default to 'proxy_only'
            api_cloud_settings[resolve.CLOUD_SETTING_SYNC_MODE] = resolve.CLOUD_SYNC_PROXY_ONLY
            
        # Handle camera access
        api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS] = cloud_settings.get('is_camera_access', False)
        
        # Restore the cloud project
        result = project_manager.RestoreCloudProject(folder_path, api_cloud_settings)
        
        if not result:
            raise RuntimeError(f"Failed to restore cloud project from '{folder_path}'")
            
        return {
            "restored": True,
            "folder_path": folder_path,
            "cloud_settings": {
                "project_name": cloud_settings['project_name'],
                "project_media_path": cloud_settings['project_media_path'],
                "is_collab": api_cloud_settings[resolve.CLOUD_SETTING_IS_COLLAB],
                "sync_mode": sync_mode,
                "is_camera_access": api_cloud_settings[resolve.CLOUD_SETTING_IS_CAMERA_ACCESS]
            }
        }
        
    return safe_api_call(
        _restore_cloud_project,
        f"Error restoring cloud project from '{folder_path}'"
    ) 