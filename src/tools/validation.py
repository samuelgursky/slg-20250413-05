"""
Tool Registration Validation Module

This module provides functions to validate that tool registrations match their actual function implementations.
"""

import inspect
import logging
from typing import Dict, Any, List, Callable, Tuple, Set, Optional

logger = logging.getLogger("resolve_api.tools.validation")

def validate_tool_parameters(tool_registry: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Validates that all registered tool parameters match their function implementations.
    
    Args:
        tool_registry: The complete tool registry dictionary
        
    Returns:
        A list of dictionaries containing validation errors with details:
        {
            "tool_name": str,
            "function_name": str,
            "missing_params": list,
            "extra_params": list,
            "param_types": dict,
            "severity": str
        }
    """
    validation_errors = []
    
    for tool_id, tool_info in tool_registry.items():
        if "function" not in tool_info:
            validation_errors.append({
                "tool_name": tool_id,
                "function_name": None,
                "error": "No function reference in tool registration",
                "severity": "critical"
            })
            continue
            
        function = tool_info["function"]
        function_name = function.__name__
        
        try:
            # Get function signature
            sig = inspect.signature(function)
            function_params = sig.parameters
            
            # Get registered parameters
            registered_params = {
                param_info["name"]: param_info 
                for param_info in tool_info.get("parameters", []) 
                if isinstance(param_info, dict) and "name" in param_info
            }
            
            # Check for missing or extra parameters
            function_param_names = set(function_params.keys())
            registered_param_names = set(registered_params.keys())
            
            # Skip 'self' for class methods
            if "self" in function_param_names:
                function_param_names.remove("self")
            
            missing_params = function_param_names - registered_param_names
            extra_params = registered_param_names - function_param_names
            
            # Gather parameter type information for comparison
            param_types = {}
            for param_name, param in function_params.items():
                if param_name != "self":  # Skip 'self' for class methods
                    annotation = param.annotation
                    if annotation != inspect.Parameter.empty:
                        param_types[param_name] = str(annotation)
            
            if missing_params or extra_params:
                validation_errors.append({
                    "tool_name": tool_id,
                    "function_name": function_name,
                    "missing_params": list(missing_params),
                    "extra_params": list(extra_params),
                    "param_types": param_types,
                    "severity": "error" if missing_params else "warning"
                })
                
        except Exception as e:
            validation_errors.append({
                "tool_name": tool_id,
                "function_name": function_name,
                "error": f"Failed to validate parameters: {str(e)}",
                "severity": "error"
            })
    
    return validation_errors

def print_validation_errors(validation_errors: List[Dict[str, Any]]) -> None:
    """
    Print validation errors in a readable format
    
    Args:
        validation_errors: List of validation error dictionaries
    """
    if not validation_errors:
        print("No validation errors found!")
        return
        
    print(f"\n\033[1mFound {len(validation_errors)} parameter validation issues:\033[0m\n")
    
    for idx, error in enumerate(validation_errors, 1):
        severity_color = "\033[31m" if error.get("severity") == "error" or error.get("severity") == "critical" else "\033[33m"
        print(f"{idx}. {severity_color}{error.get('tool_name', 'Unknown tool')}\033[0m - Function: {error.get('function_name', 'Unknown')}")
        
        if "error" in error:
            print(f"   Error: {error['error']}")
        
        if "missing_params" in error and error["missing_params"]:
            print(f"   Missing parameters in registration: {', '.join(error['missing_params'])}")
            
        if "extra_params" in error and error["extra_params"]:
            print(f"   Extra parameters in registration: {', '.join(error['extra_params'])}")
            
        if "param_types" in error and error["param_types"]:
            print("   Parameter types from function:")
            for param, type_str in error["param_types"].items():
                print(f"     - {param}: {type_str}")
                
        print()  # Empty line between errors

def generate_parameter_fixes(validation_errors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate parameter fixes for tools with validation errors
    
    Args:
        validation_errors: List of validation error dictionaries
        
    Returns:
        Dictionary mapping tool names to lists of corrected parameter dictionaries
    """
    fixes = {}
    
    for error in validation_errors:
        tool_name = error.get("tool_name")
        if not tool_name or "missing_params" not in error or "extra_params" not in error:
            continue
            
        # Get param types from function signature
        param_types = error.get("param_types", {})
        
        # For each tool, suggest a corrected parameters list
        # This would need the original registry entry to be complete
        # For now just generate placeholder entries
        corrected_params = []
        
        for param_name in sorted(list(param_types.keys())):
            type_info = param_types[param_name]
            is_required = "Optional" not in type_info
            
            corrected_params.append({
                "name": param_name,
                "type": "object" if "Dict" in type_info else "string",
                "description": f"Parameter {param_name} ({type_info})",
                "required": is_required
            })
            
        fixes[tool_name] = corrected_params
        
    return fixes

def fix_tool_parameters(tool_registry: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Automatically fix tool parameters to match function signatures
    
    Args:
        tool_registry: The complete tool registry dictionary
        
    Returns:
        A new tool registry with corrected parameters
    """
    # Create a deep copy of the registry
    import copy
    fixed_registry = copy.deepcopy(tool_registry)
    
    # Get validation errors
    validation_errors = validate_tool_parameters(tool_registry)
    
    # Generate fixes
    fixes = generate_parameter_fixes(validation_errors)
    
    # Apply fixes to the registry copy
    for tool_name, corrected_params in fixes.items():
        if tool_name in fixed_registry:
            fixed_registry[tool_name]["parameters"] = corrected_params
            
    return fixed_registry 