#!/usr/bin/env python3
"""
Redmine Groups management MCP tools.

This module provides Redmine group management:
- List groups
- Get group details
- Create groups
- Update groups
- Delete groups
- Add/remove users from groups
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_groups_tool() -> types.Tool:
    """Creates tool for listing groups."""
    return types.Tool(
        name="list_groups",
        description="Lists all groups in Redmine. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )


def create_get_group_tool() -> types.Tool:
    """Creates tool for getting group details."""
    return types.Tool(
        name="get_group",
        description="Gets details of a specific group, optionally including its members.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "Group ID"
                },
                "include_users": {
                    "type": "boolean",
                    "description": "Whether to include group members in the response (default: false)"
                }
            },
            "required": ["group_id"]
        }
    )


def create_create_group_tool() -> types.Tool:
    """Creates tool for creating groups."""
    return types.Tool(
        name="create_group",
        description="Creates a new group. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Group name"
                },
                "user_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "List of user IDs to add to the group (optional)"
                }
            },
            "required": ["name"]
        }
    )


def create_update_group_tool() -> types.Tool:
    """Creates tool for updating groups."""
    return types.Tool(
        name="update_group",
        description="Updates an existing group. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "Group ID to update"
                },
                "name": {
                    "type": "string",
                    "description": "New group name"
                },
                "user_ids": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "New list of user IDs (replaces existing members)"
                }
            },
            "required": ["group_id"]
        }
    )


def create_delete_group_tool() -> types.Tool:
    """Creates tool for deleting groups."""
    return types.Tool(
        name="delete_group",
        description="Deletes a specific group. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "Group ID to delete"
                }
            },
            "required": ["group_id"]
        }
    )


def create_add_user_to_group_tool() -> types.Tool:
    """Creates tool for adding a user to a group."""
    return types.Tool(
        name="add_user_to_group",
        description="Adds a user to a group. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "Group ID"
                },
                "user_id": {
                    "type": "integer",
                    "description": "User ID to add to the group"
                }
            },
            "required": ["group_id", "user_id"]
        }
    )


def create_remove_user_from_group_tool() -> types.Tool:
    """Creates tool for removing a user from a group."""
    return types.Tool(
        name="remove_user_from_group",
        description="Removes a user from a group. Requires admin privileges.",
        inputSchema={
            "type": "object",
            "properties": {
                "group_id": {
                    "type": "integer",
                    "description": "Group ID"
                },
                "user_id": {
                    "type": "integer",
                    "description": "User ID to remove from the group"
                }
            },
            "required": ["group_id", "user_id"]
        }
    )


# Handler functions

async def handle_list_groups(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists all groups."""
    groups = client.list_groups()

    return [
        types.TextContent(
            type="text",
            text=f"Found {len(groups)} group(s):\n\n{format_groups(groups)}"
        )
    ]


async def handle_get_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets group details."""
    group_id = arguments["group_id"]
    include_users = arguments.get("include_users", False)

    group = client.get_group(group_id, include_users=include_users)

    return [
        types.TextContent(
            type="text",
            text=f"Group Details (ID: {group_id}):\n\n{format_group(group)}"
        )
    ]


async def handle_create_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates a new group."""
    group_data = {k: v for k, v in arguments.items() if v is not None}

    group = client.create_group(group_data)

    return [
        types.TextContent(
            type="text",
            text=f"✅ Group created successfully!\n\n{format_group(group)}"
        )
    ]


async def handle_update_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates a group."""
    group_id = arguments.pop("group_id")
    group_data = {k: v for k, v in arguments.items() if v is not None}

    success = client.update_group(group_id, group_data)

    if success:
        updated_group = client.get_group(group_id)
        return [
            types.TextContent(
                type="text",
                text=f"✅ Group #{group_id} updated successfully!\n\n{format_group(updated_group)}"
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to update group #{group_id}."
            )
        ]


async def handle_delete_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes a group."""
    group_id = arguments["group_id"]

    success = client.delete_group(group_id)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Group #{group_id} deleted successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to delete group #{group_id}."
            )
        ]


async def handle_add_user_to_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Adds a user to a group."""
    group_id = arguments["group_id"]
    user_id = arguments["user_id"]

    success = client.add_user_to_group(group_id, user_id)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ User #{user_id} added to group #{group_id} successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to add user #{user_id} to group #{group_id}."
            )
        ]


async def handle_remove_user_from_group(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Removes a user from a group."""
    group_id = arguments["group_id"]
    user_id = arguments["user_id"]

    success = client.remove_user_from_group(group_id, user_id)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ User #{user_id} removed from group #{group_id} successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to remove user #{user_id} from group #{group_id}."
            )
        ]


# Helper formatters

def format_group(group: Dict[str, Any]) -> str:
    """Formats a single group."""
    parts = [
        f"ID: {group.get('id', 'N/A')}",
        f"Name: {group.get('name', 'N/A')}",
    ]

    if group.get('users'):
        users = group['users']
        parts.append(f"Members ({len(users)}):")
        for user in users:
            parts.append(f"  - {user.get('name', 'N/A')} (ID: {user.get('id', 'N/A')})")

    if group.get('memberships'):
        memberships = group['memberships']
        parts.append(f"Project Memberships ({len(memberships)}):")
        for m in memberships:
            project = m.get('project', {})
            roles = [r.get('name', '') for r in m.get('roles', [])]
            parts.append(f"  - {project.get('name', 'N/A')}: {', '.join(roles)}")

    return "\n".join(parts)


def format_groups(groups: List[Dict[str, Any]]) -> str:
    """Formats a list of groups."""
    if not groups:
        return "No groups found."

    formatted = []
    for i, group in enumerate(groups, 1):
        formatted.append(f"{i}. ID: {group.get('id', 'N/A')} - {group.get('name', 'N/A')}")

    return "\n".join(formatted)
