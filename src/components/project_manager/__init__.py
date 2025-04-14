"""
ProjectManager Component
Implements functions for project and database management
"""

import logging
from typing import Dict, Any, List, Optional, Union

from ...resolve_api import get_resolve, get_project_manager, safe_api_call

# Import all functions from the component modules
from .projects import (
    create_project,
    delete_project,
    load_project,
    save_project,
    close_project,
    archive_project,
    import_project,
    export_project,
    restore_project
)

from .folders import (
    create_folder,
    delete_folder,
    get_project_list,
    get_folder_list,
    goto_root_folder,
    goto_parent_folder,
    get_current_folder,
    open_folder,
    get_current_database,
    get_database_list,
    set_current_database
)

from .cloud import (
    create_cloud_project,
    load_cloud_project,
    import_cloud_project,
    restore_cloud_project
)

# Export all functions
__all__ = [
    # Project functions
    'create_project',
    'delete_project',
    'load_project',
    'save_project',
    'close_project',
    'archive_project',
    'import_project',
    'export_project',
    'restore_project',
    
    # Folder functions
    'create_folder',
    'delete_folder',
    'get_project_list',
    'get_folder_list',
    'goto_root_folder',
    'goto_parent_folder',
    'get_current_folder',
    'open_folder',
    
    # Database functions
    'get_current_database',
    'get_database_list',
    'set_current_database',
    
    # Cloud project functions
    'create_cloud_project',
    'load_cloud_project',
    'import_cloud_project',
    'restore_cloud_project'
]

logger = logging.getLogger("resolve_api.components.project_manager") 