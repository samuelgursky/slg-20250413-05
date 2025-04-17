"""
Startup Validation Module

This module provides validation functions that can be run at MCP server startup
to ensure tool registrations match function signatures.
"""

import logging
import os
import sys
from typing import Dict, Any, List, Optional, Tuple

from .validation import validate_tool_parameters
from .registration import TOOLS_REGISTRY

logger = logging.getLogger("resolve_api.tools.startup_validation")

def validate_tools_on_startup(strict: bool = False) -> bool:
    """
    Validate all tool registrations against function signatures on startup
    
    Args:
        strict: If True, raise an exception for critical errors, otherwise just log warnings
        
    Returns:
        True if validation passed with no critical errors, False otherwise
    """
    validation_errors = validate_tool_parameters(TOOLS_REGISTRY)
    
    if not validation_errors:
        logger.info("Tool validation passed: All tool registrations match function signatures")
        return True
    
    # Group errors by severity
    critical_errors = []
    non_critical_errors = []
    
    for error in validation_errors:
        if error.get("severity") in ["error", "critical"]:
            critical_errors.append(error)
        else:
            non_critical_errors.append(error)
    
    # Log information about the errors
    if critical_errors:
        logger.error(f"Tool validation failed: Found {len(critical_errors)} critical parameter mismatches")
        for idx, error in enumerate(critical_errors, 1):
            tool_name = error.get("tool_name", "Unknown tool")
            function_name = error.get("function_name", "Unknown function")
            
            if "missing_params" in error and error["missing_params"]:
                logger.error(f"{idx}. {tool_name} ({function_name}): Missing parameters: {', '.join(error['missing_params'])}")
            
            if "extra_params" in error and error["extra_params"]:
                logger.error(f"{idx}. {tool_name} ({function_name}): Extra parameters: {', '.join(error['extra_params'])}")
            
            if "error" in error:
                logger.error(f"{idx}. {tool_name} ({function_name}): {error['error']}")
    
    if non_critical_errors:
        logger.warning(f"Tool validation warning: Found {len(non_critical_errors)} non-critical parameter mismatches")
        for idx, error in enumerate(non_critical_errors, 1):
            tool_name = error.get("tool_name", "Unknown tool")
            function_name = error.get("function_name", "Unknown function")
            
            if "extra_params" in error and error["extra_params"]:
                logger.warning(f"{idx}. {tool_name} ({function_name}): Extra parameters: {', '.join(error['extra_params'])}")
            
            if "error" in error:
                logger.warning(f"{idx}. {tool_name} ({function_name}): {error['error']}")
    
    if strict and critical_errors:
        error_details = "\n".join([
            f"{e.get('tool_name', 'Unknown')}: {', '.join(e.get('missing_params', []))}" 
            for e in critical_errors if 'missing_params' in e and e['missing_params']
        ])
        error_message = f"Tool validation failed with {len(critical_errors)} critical errors. Please run the parameter validation script to fix these issues.\n{error_details}"
        raise ValueError(error_message)
    
    return len(critical_errors) == 0

def get_validation_summary() -> Dict[str, Any]:
    """
    Get a summary of validation errors for health check endpoints
    
    Returns:
        Dict with validation summary information
    """
    validation_errors = validate_tool_parameters(TOOLS_REGISTRY)
    
    critical_errors = [e for e in validation_errors if e.get("severity") in ["error", "critical"]]
    non_critical_errors = [e for e in validation_errors if e.get("severity") not in ["error", "critical"]]
    
    return {
        "passed": len(critical_errors) == 0,
        "critical_error_count": len(critical_errors),
        "warning_count": len(non_critical_errors),
        "critical_errors": [
            {
                "tool_name": e.get("tool_name", "Unknown"),
                "function_name": e.get("function_name", "Unknown"),
                "missing_params": e.get("missing_params", []),
                "extra_params": e.get("extra_params", [])
            }
            for e in critical_errors
        ],
        "warnings": [
            {
                "tool_name": e.get("tool_name", "Unknown"),
                "function_name": e.get("function_name", "Unknown"),
                "missing_params": e.get("missing_params", []),
                "extra_params": e.get("extra_params", [])
            }
            for e in non_critical_errors
        ]
    } 