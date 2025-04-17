# DaVinci Resolve MCP Agent Version History

## Version: 2.0.0.A
**Release Date:** 2025-04-17

### Overview
This release introduces a comprehensive parameter validation system to ensure proper alignment between function implementations and tool registrations in the MCP server. The new validation framework addresses a critical issue where function parameter names in implementations didn't match their registered counterparts, causing tool execution failures.

### Features
- **Parameter Validation System**: New validation framework to detect and fix mismatches between function signatures and tool registrations
- **Automatic Tool Registration Correction**: Command-line tools for automatically fixing parameter mismatches
- **Startup Validation**: Runtime validation on server startup to detect potential issues early
- **Cloud Project Functionality Fixed**: Corrected parameter mismatches in cloud project operations (`create_cloud_project`, `load_cloud_project`, `import_cloud_project`, `restore_cloud_project`)
- **Project Backup/Restore Fixed**: Corrected parameter mismatch in `restore_project` function

### Known Issues
- Existing tool registrations may still have minor parameter mismatches that aren't critical (extra parameters)
- Parameter validation doesn't check type compatibility beyond basic type inference