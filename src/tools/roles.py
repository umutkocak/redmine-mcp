#!/usr/bin/env python3
"""
Redmine Roles management MCP tools.

This module provides Redmine role management:
- List all roles
- Get role details with permissions
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_roles_detail_tool() -> types.Tool:
    """Creates tool for listing roles with details."""
    return types.Tool(
        name="list_roles_detail",
        description="Lists all available roles in Redmine with their IDs and names.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )


def create_get_role_tool() -> types.Tool:
    """Creates tool for getting role details."""
    return types.Tool(
        name="get_role",
        description="Gets details of a specific role, including its permissions.",
        inputSchema={
            "type": "object",
            "properties": {
                "role_id": {
                    "type": "integer",
                    "description": "Role ID"
                }
            },
            "required": ["role_id"]
        }
    )


# Handler functions

async def handle_list_roles_detail(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists all roles with details."""
    roles = client.list_roles()

    result = {
        "roles": roles,
        "total_count": len(roles)
    }

    return [
        types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )
    ]


async def handle_get_role(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets role details with permissions."""
    role_id = arguments["role_id"]

    role = client.get_role(role_id)

    return [
        types.TextContent(
            type="text",
            text=f"Role Details (ID: {role_id}):\n\n{format_role(role)}"
        )
    ]


# Helper formatters

def format_role(role: Dict[str, Any]) -> str:
    """Formats a single role with permissions."""
    parts = [
        f"ID: {role.get('id', 'N/A')}",
        f"Name: {role.get('name', 'N/A')}",
    ]

    if role.get('assignable') is not None:
        parts.append(f"Assignable: {role['assignable']}")

    if role.get('issues_visibility'):
        parts.append(f"Issues Visibility: {role['issues_visibility']}")

    if role.get('time_entries_visibility'):
        parts.append(f"Time Entries Visibility: {role['time_entries_visibility']}")

    if role.get('users_visibility'):
        parts.append(f"Users Visibility: {role['users_visibility']}")

    if role.get('permissions'):
        permissions = role['permissions']
        parts.append(f"\nPermissions ({len(permissions)}):")
        for perm in permissions:
            parts.append(f"  - {perm}")

    return "\n".join(parts)
