"""
Redmine MCP Server - Version Management

This module manages the project version.
"""

__version__ = "2.0.0"
__version_info__ = (2, 0, 0)

# Changelog
CHANGELOG = {
    "2.0.0": {
        "date": "2026-02-11",
        "changes": [
            "🎉 Full API coverage: 11 → 55+ operations (Phase 1-4 complete)",
            "✨ Phase 3: Wiki Pages (list, get, create/update, delete)",
            "✨ Phase 3: Groups (list, get, create, update, delete, add/remove users)",
            "✨ Phase 3: Roles Detail (list with details, get with permissions)",
            "✨ Phase 3: Custom Fields (list all custom field definitions)",
            "✨ Phase 3: Journals (list issue history, update journal notes)",
            "✨ Phase 4: News (list, get news entries)",
            "✨ Phase 4: Queries (list saved/custom queries)",
            "✨ Phase 4: Search (global search across all Redmine resources)",
            "✨ Phase 4: Files (list project files)",
            "✨ Phase 4: My Account (get/update authenticated user account)",
            "🔧 Extended RedmineClient with 20+ new API methods",
            "📝 All code and documentation in English",
            "✅ Consistent error handling across all new modules"
        ],
        "breaking_changes": [],
        "migration_notes": [
            "Requires Python >= 3.10 (MCP >= 1.0.0 dependency)",
            "No breaking changes from v1.0.4",
            "New tools are additive - existing tools unchanged"
        ],
        "dependencies": {
            "mcp": ">=1.0.0 (requires Python 3.10+)",
            "requests": ">=2.31.0",
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
    "1.0.4": {
        "date": "2026-02-11",
        "changes": [
            "🎉 Major API expansion: 11 → 29 operations (+164% increase)",
            "✨ Projects: create, update, delete, archive, unarchive",
            "✨ Issues: delete, add_watcher, remove_watcher, list_watchers",
            "✨ Users: create, update, delete, get_current",
            "✨ Time Entries: get, update, delete (full CRUD)",
            "✨ Attachments: upload, get, download",
            "🌍 Full UTF-8 support for Turkish and international content",
            "📝 English-only documentation (README, CHANGELOG)",
            "🔧 Enhanced REST API client with comprehensive method coverage",
            "✅ Improved error handling and logging"
        ],
        "breaking_changes": [],
        "migration_notes": [
            "Requires Python >= 3.10 (MCP >= 1.0.0 dependency)",
            "No breaking changes from v1.0.3"
        ],
        "dependencies": {
            "mcp": ">=1.0.0 (requires Python 3.10+)",
            "requests": ">=2.31.0",
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
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
    print(f"Python: 3.10+")
