"""
Redmine MCP Server - Version Management

This module manages the project version.
"""

__version__ = "1.0.4"
__version_info__ = (1, 0, 4)

# Changelog
CHANGELOG = {
    "1.0.3": {
        "date": "2025-08-04",
        "changes": [
            "✨ create_time_entry tool added for creating new time entries",
            "🕒 Enhanced time tracking capabilities with full CRUD operations",
            "🔧 Support for custom fields in time entry creation",
            "📋 Flexible time entry assignment to issues or projects",
            "🛠️ Improved RedmineClient with create_time_entry method"
        ],
        "breaking_changes": [],
        "migration_notes": []
    },
    "1.0.2": {
        "date": "2025-08-02",
        "changes": [
            "🐛 create_issue double-wrapping bug fixed",
            "✅ Issue creation validation improved (project_id and subject validation)",
            "🔧 Format compatibility issue between RedmineClient and tool handler resolved",
            "📋 create_issue bug fix test script added"
        ],
        "breaking_changes": [],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
    "1.0.1": {
        "date": "2025-08-02",
        "changes": [
            "🔧 MCP version check error fixed",
            "✅ Issue validation error messages improved",
            "✅ Claude Desktop compatibility enhanced",
            "📋 Validation test script added"
        ],
        "breaking_changes": [],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
    "1.0.0": {
        "date": "2025-08-02",
        "changes": [
            "✅ First stable release",
            "✅ Full integration with standard MCP library",
            "✅ 10 core tools completed (projects, issues, users, time_entries, enumerations)",
            "✅ Issue tools updated with {'issue': {...}} wrapper format",
            "✅ Custom field values support added",
            "✅ Parent issue ID, start_date, due_date support",
            "✅ Claude Desktop integration ready",
            "✅ Comprehensive error handling and logging",
            "✅ Environment-based configuration",
            "✅ Production-ready documentation"
        ],
        "breaking_changes": [
            "⚠️ Migration from FastMCP to Standard MCP",
            "⚠️ create_issue and update_issue tools require wrapper format"
        ],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    }
}

def get_version() -> str:
    """Returns the current version number."""
    return __version__

def get_version_info() -> tuple:
    """Returns the version info tuple (major, minor, patch)."""
    return __version_info__

def get_changelog(version: str = None) -> dict:
    """Returns the changelog for the specified version or all versions."""
    if version:
        return CHANGELOG.get(version, {})
    return CHANGELOG

def print_version_info():
    """Prints version information."""
    print(f"Redmine MCP Server v{__version__}")
    print(f"Release Date: {CHANGELOG[__version__]['date']}")
    print(f"MCP Library: Standard MCP >= 1.0.0")
    print(f"Python: 3.9+")
