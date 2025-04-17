#!/usr/bin/env python3
"""
Tool Registration Update Script

This script updates the tool registrations in the MCP server to match their
actual function implementations.
"""

import os
import sys
import argparse
import logging
import re
from typing import Dict, Any, List, Optional, Tuple

# Add parent directory to path so we can import modules
script_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.dirname(script_dir)
if src_dir not in sys.path:
    sys.path.append(src_dir)

from tools.validation import validate_tool_parameters, print_validation_errors, fix_tool_parameters
from tools.registration import TOOLS_REGISTRY

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("update_tool_registrations")

def format_parameter_entry(param: Dict[str, Any]) -> str:
    """
    Format a parameter entry for insertion into the registration file
    
    Args:
        param: Parameter dictionary
        
    Returns:
        Formatted string representation of the parameter entry
    """
    lines = ["            {"]
    
    # Add each key-value pair
    for key, value in param.items():
        if isinstance(value, str):
            lines.append(f'                "{key}": "{value}",')
        else:
            lines.append(f'                "{key}": {value},')
    
    lines.append("            }")
    return "\n".join(lines)

def update_registration_file(registration_file: str, tool_fixes: Dict[str, List[Dict[str, Any]]]) -> bool:
    """
    Update the registration file with fixed parameter entries
    
    Args:
        registration_file: Path to the registration file
        tool_fixes: Dictionary mapping tool names to lists of corrected parameter dictionaries
        
    Returns:
        True if updates were made, False otherwise
    """
    # Read the file
    with open(registration_file, 'r') as f:
        content = f.read()
        
    # Make a copy for comparison
    original_content = content
    
    # For each tool with fixes
    for tool_name, fixed_params in tool_fixes.items():
        # Find the tool entry
        tool_pattern = re.compile(rf'"{tool_name}":\s*{{\s*.*?"parameters":\s*\[\s*.*?\],', re.DOTALL)
        match = tool_pattern.search(content)
        
        if match:
            # Extract the tool entry
            tool_entry = match.group(0)
            
            # Find the parameters section
            params_pattern = re.compile(r'"parameters":\s*\[\s*.*?\],', re.DOTALL)
            params_match = params_pattern.search(tool_entry)
            
            if params_match:
                # Create new parameters section
                new_params = '"parameters": [\n'
                for i, param in enumerate(fixed_params):
                    new_params += format_parameter_entry(param)
                    if i < len(fixed_params) - 1:
                        new_params += ",\n"
                    else:
                        new_params += "\n        "
                new_params += "],"
                
                # Replace the parameters section in the tool entry
                new_tool_entry = tool_entry.replace(params_match.group(0), new_params)
                
                # Replace the tool entry in the content
                content = content.replace(tool_entry, new_tool_entry)
    
    # If changes were made, write the file
    if content != original_content:
        with open(registration_file, 'w') as f:
            f.write(content)
        return True
    
    return False

def generate_fixes(validation_errors: List[Dict[str, Any]], current_registry: Dict[str, Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    Generate improved parameter fixes that preserve descriptions and other metadata
    
    Args:
        validation_errors: List of validation error dictionaries
        current_registry: The current tool registry
        
    Returns:
        Dictionary mapping tool names to lists of corrected parameter dictionaries
    """
    fixes = {}
    
    for error in validation_errors:
        tool_name = error.get("tool_name")
        if not tool_name or tool_name not in current_registry:
            continue
            
        # Get function parameter information
        missing_params = set(error.get("missing_params", []))
        extra_params = set(error.get("extra_params", []))
        param_types = error.get("param_types", {})
        
        # Get current parameters
        current_tool = current_registry[tool_name]
        current_params = current_tool.get("parameters", [])
        
        # Keep track of parameter names for duplicate detection
        param_names_seen = set()
        
        # Create corrected parameters list
        corrected_params = []
        
        # First, include all function parameters (removing extras)
        for param_name in sorted(param_types.keys()):
            type_info = param_types[param_name]
            
            # Find if this parameter already exists in the current registration
            existing_param = None
            for p in current_params:
                if isinstance(p, dict) and p.get("name") == param_name:
                    existing_param = p
                    break
            
            # Create new parameter entry, preserving metadata if possible
            if existing_param:
                # Use existing parameter but ensure required field is accurate
                is_required = "Optional" not in type_info
                new_param = existing_param.copy()
                new_param["required"] = is_required
            else:
                # Create new parameter entry
                is_required = "Optional" not in type_info
                new_param = {
                    "name": param_name,
                    "type": "object" if "Dict" in type_info else "string",
                    "description": f"Parameter {param_name} ({type_info})",
                    "required": is_required
                }
            
            corrected_params.append(new_param)
            param_names_seen.add(param_name)
        
        # Only save if there were actually changes
        if missing_params or extra_params:
            fixes[tool_name] = corrected_params
    
    return fixes

def main():
    parser = argparse.ArgumentParser(description='Update tool parameter registrations to match function signatures.')
    parser.add_argument('--registration-file', type=str, default='src/tools/registration.py',
                      help='Path to the registration file (default: src/tools/registration.py)')
    parser.add_argument('--dry-run', action='store_true', 
                      help='Show what would be updated without making changes')
    args = parser.parse_args()
    
    # Validate all tools
    logger.info("Validating tool registrations against function signatures...")
    validation_errors = validate_tool_parameters(TOOLS_REGISTRY)
    
    # Print errors
    if validation_errors:
        print_validation_errors(validation_errors)
        logger.info(f"Found {len(validation_errors)} validation issues.")
        
        error_count = sum(1 for e in validation_errors if e.get("severity") in ["error", "critical"])
        warning_count = len(validation_errors) - error_count
        
        logger.info(f"Errors: {error_count}, Warnings: {warning_count}")
        
        # Generate improved fixes
        fixes = generate_fixes(validation_errors, TOOLS_REGISTRY)
        logger.info(f"Generated fixes for {len(fixes)} tools")
        
        # Update registration file
        if not args.dry_run:
            if update_registration_file(args.registration_file, fixes):
                logger.info(f"Successfully updated {len(fixes)} tool registrations in {args.registration_file}")
            else:
                logger.info("No updates were made to the registration file")
        else:
            logger.info("Dry run, no changes made. The following tools would be updated:")
            for tool_name in fixes:
                logger.info(f"  - {tool_name}")
    else:
        logger.info("No validation issues found. All tool registrations match function signatures.")
    
    # Return error count for shell scripting
    return 1 if validation_errors else 0

if __name__ == "__main__":
    sys.exit(main()) 