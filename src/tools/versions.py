#!/usr/bin/env python3
"""
Redmine Versions management MCP tools.

This module provides Redmine version (milestone) management:
- List project versions
- Get version details
- Create new versions
- Update versions
- Delete versions
"""

from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_versions_tool() -> types.Tool:
    """Creates tool for listing project versions."""
    return types.Tool(
        name="list_versions",
        description="Lists all versions for a specific project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to list versions for"
                }
            },
            "required": ["project_id"]
        }
    )


def create_get_version_tool() -> types.Tool:
    """Creates tool for getting version details."""
    return types.Tool(
        name="get_version",
        description="Gets details of a specific version.",
        inputSchema={
            "type": "object",
            "properties": {
                "version_id": {
                    "type": "integer",
                    "description": "Version ID"
                }
            },
            "required": ["version_id"]
        }
    )


def create_create_version_tool() -> types.Tool:
    """Creates tool for creating new versions."""
    return types.Tool(
        name="create_version",
        description=(
            "Creates a new version (milestone) in a project. "
            "Common properties: name, description, status, due_date, sharing"
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                },
                "name": {
                    "type": "string",
                    "description": "Version name"
                },
                "description": {
                    "type": "string",
                    "description": "Version description"
                },
                "status": {
                    "type": "string",
                    "description": "Version status",
                    "enum": ["open", "locked", "closed"]
                },
                "due_date": {
                    "type": "string",
                    "description": "Due date in YYYY-MM-DD format"
                },
                "sharing": {
                    "type": "string",
                    "description": "Sharing level",
                    "enum": [
                        "none",           # Not shared
                        "descendants",    # With subprojects
                        "hierarchy",      # With project hierarchy
                        "tree",           # With project tree
                        "system"          # With all projects
                    ]
                }
            },
            "required": ["project_id", "name"]
        }
    )


def create_update_version_tool() -> types.Tool:
    """Creates tool for updating versions."""
    return types.Tool(
        name="update_version",
        description="Updates an existing version.",
        inputSchema={
            "type": "object",
            "properties": {
                "version_id": {
                    "type": "integer",
                    "description": "Version ID to update"
                },
                "name": {
                    "type": "string",
                    "description": "New version name"
                },
                "description": {
                    "type": "string",
                    "description": "New version description"
                },
                "status": {
                    "type": "string",
                    "description": "New version status",
                    "enum": ["open", "locked", "closed"]
                },
                "due_date": {
                    "type": "string",
                    "description": "New due date in YYYY-MM-DD format"
                },
                "sharing": {
                    "type": "string",
                    "description": "New sharing level",
                    "enum": [
                        "none",           # Not shared
                        "descendants",    # With subprojects
                        "hierarchy",      # With project hierarchy
                        "tree",           # With project tree
                        "system"          # With all projects
                    ]
                }
            },
            "required": ["version_id"]
        }
    )


def create_delete_version_tool() -> types.Tool:
    """Creates tool for deleting versions."""
    return types.Tool(
        name="delete_version",
        description="Deletes a specific version.",
        inputSchema={
            "type": "object",
            "properties": {
                "version_id": {
                    "type": "integer",
                    "description": "Version ID to delete"
                }
            },
            "required": ["version_id"]
        }
    )


# Handler functions

async def handle_list_versions(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists project versions."""
    project_id = arguments["project_id"]
    
    versions = client.list_versions(project_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Found {len(versions)} version(s) for Project '{project_id}':\n\n{format_versions(versions)}"
        )
    ]


async def handle_get_version(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets version details."""
    version_id = arguments["version_id"]
    
    version = client.get_version(version_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Version Details (ID: {version_id}):\n\n{format_version(version)}"
        )
    ]


async def handle_create_version(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates a new version."""
    # Remove project_id from version data since it's handled separately
    project_id = arguments.pop("project_id")
    version_data = {k: v for k, v in arguments.items() if v is not None}
    
    version = client.create_version(project_id, version_data)
    
    return [
        types.TextContent(
            type="text",
            text=f"✅ Version created successfully!\n\nID: {version['id']}\n{format_version(version)}"
        )
    ]


async def handle_update_version(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates a version."""
    version_id = arguments.pop("version_id")
    version_data = {k: v for k, v in arguments.items() if v is not None}
    
    success = client.update_version(version_id, version_data)
    
    if success:
        updated_version = client.get_version(version_id)
        return [
            types.TextContent(
                type="text",
                text=f"✅ Version #{version_id} updated successfully!\n\n{format_version(updated_version)}"
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to update version #{version_id}."
            )
        ]


async def handle_delete_version(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes a version."""
    version_id = arguments["version_id"]
    
    success = client.delete_version(version_id)
    
    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Version #{version_id} deleted successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to delete version #{version_id}."
            )
        ]


# Helper formatters

def format_version(version: Dict[str, Any]) -> str:
    """Formats a single version."""
    parts = [
        f"Name: {version.get('name', 'N/A')}",
        f"Status: {version.get('status', 'N/A')}",
        f"Project ID: {version.get('project', {}).get('id', version.get('project_id', 'N/A'))}"
    ]
    
    if version.get('description'):
        parts.append(f"Description: {version['description'][:100]}{'...' if len(version['description']) > 100 else ''}")
    
    if version.get('due_date'):
        parts.append(f"Due Date: {version['due_date']}")
    
    if version.get('sharing'):
        parts.append(f"Sharing: {version['sharing']}")
    
    return "\n".join(parts)


def format_versions(versions: List[Dict[str, Any]]) -> str:
    """Formats a list of versions."""
    if not versions:
        return "No versions found."
    
    formatted = []
    for i, ver in enumerate(versions, 1):
        formatted.append(f"{i}. ID: {ver.get('id', 'N/A')}")
        formatted.append(f"   {format_version(ver)}")
        formatted.append("")
    
    return "\n".join(formatted)