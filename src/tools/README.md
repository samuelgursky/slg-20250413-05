# DaVinci Resolve MCP Tool Validation

This directory contains the DaVinci Resolve MCP tool registration system and validation tools.

## Parameter Validation

The MCP server uses a validation system to ensure that tool registrations match their function implementations. This helps prevent errors where a tool is registered with incorrect parameter names or types.

### Key Components

- `validation.py`: Core validation functions that check function signatures against tool registrations
- `startup_validation.py`: Functions for validating tools at server startup
- `validate_tools.py`: Command-line script for validating tools and reporting issues
- `update_tool_registrations.py`: Command-line script for automatically fixing parameter mismatches

### Using the Validation Tools

#### Check for Parameter Mismatches

```bash
python -m src.tools.validate_tools
```

This will check all tool registrations against their function implementations and report any mismatches.

#### Automatically Fix Parameter Mismatches

```bash
python -m src.tools.update_tool_registrations
```

This will automatically update the tool registrations to match their function implementations.

#### Dry Run (Show What Would Be Fixed)

```bash
python -m src.tools.update_tool_registrations --dry-run
```

This will show what would be fixed without making any changes.

### Common Issues

Parameter mismatches typically occur when:

1. A function's parameters are renamed but the tool registration isn't updated
2. A function is updated to use a dictionary parameter instead of individual parameters
3. New parameters are added to a function but not to the tool registration

### Fixing Parameter Mismatches

The automatic fix script handles most cases, but you may need to manually update complex cases:

1. Run the validation script to identify issues
2. For each issue, check the function implementation and update the tool registration
3. Use the official DaVinci Resolve API documentation as reference for parameter names and types
4. Re-run the validation script to ensure all issues are fixed

## API Implementation Tracking

When implementing new API functions:

1. Update the function implementation in the appropriate component file
2. Register the function in `registration.py` with the correct parameters
3. Run the validation script to ensure the registration is correct
4. Update the API_IMPLEMENTATION_TRACKING.md file with the implementation status 