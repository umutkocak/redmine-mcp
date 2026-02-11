#!/usr/bin/env python3
"""
Redmine Project Memberships management MCP tools.

This module provides Redmine project membership management:
- List project members
- Get membership details
- Add members to projects
- Update member roles
- Remove members from projects
"""

from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_memberships_tool() -> types.Tool:
    """Creates tool for listing project memberships."""
    return types.Tool(
        name="list_memberships",
        description="Lists all members of a specific project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to list members for"
                }
            },
            "required": ["project_id"]
        }
    )


def create_get_membership_tool() -> types.Tool:
    """Creates tool for getting membership details."""
    return types.Tool(
        name="get_membership",
        description="Gets details of a specific membership.",
        inputSchema={
            "type": "object",
            "properties": {
                "membership_id": {
                    "type": "integer",
                    "description": "Membership ID"
                }
            },
            "required": ["membership_id"]
        }
    )


def create_create_membership_tool() -> types.Tool:
    """Creates tool for adding members to projects."""
    return types.Tool(
        name="create_membership",
        description=(
            "Adds a user or group to a project with specified roles. "
            "Either user_id or group_id must be provided, along with role_ids."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                },
                "user_id": {
                    "type": "integer",
                    "description": "User ID to add to project"
                },
                "group_id": {
                    "type": "integer",
                    "description": "Group ID to add to project"
                },
                "role_ids": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "List of role IDs to assign"
                }
            },
            "required": ["project_id"],
            "oneOf": [
                {"required": ["user_id", "role_ids"]},
                {"required": ["group_id", "role_ids"]}
            ]
        }
    )


def create_update_membership_tool() -> types.Tool:
    """Creates tool for updating membership roles."""
    return types.Tool(
        name="update_membership",
        description="Updates roles for an existing membership.",
        inputSchema={
            "type": "object",
            "properties": {
                "membership_id": {
                    "type": "integer",
                    "description": "Membership ID to update"
                },
                "role_ids": {
                    "type": "array",
                    "items": {
                        "type": "integer"
                    },
                    "description": "New list of role IDs"
                }
            },
            "required": ["membership_id", "role_ids"]
        }
    )


def create_delete_membership_tool() -> types.Tool:
    """Creates tool for removing members from projects."""
    return types.Tool(
        name="delete_membership",
        description="Removes a member from a project.",
        inputSchema={
            "type": "object",
            "properties": {
                "membership_id": {
                    "type": "integer",
                    "description": "Membership ID to remove"
                }
            },
            "required": ["membership_id"]
        }
    )


# Handler functions

async def handle_list_memberships(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists project memberships."""
    project_id = arguments["project_id"]
    
    memberships = client.list_memberships(project_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Found {len(memberships)} member(s) for Project '{project_id}':\n\n{format_memberships(memberships)}"
        )
    ]


async def handle_get_membership(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets membership details."""
    membership_id = arguments["membership_id"]
    
    membership = client.get_membership(membership_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Membership Details (ID: {membership_id}):\n\n{format_membership(membership)}"
        )
    ]


async def handle_create_membership(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates a new membership."""
    project_id = arguments["project_id"]
    membership_data = {
        k: v for k, v in arguments.items() 
        if k in ["user_id", "group_id", "role_ids"] and v is not None
    }
    
    membership = client.create_membership(project_id, membership_data)
    
    return [
        types.TextContent(
            type="text",
            text=f"✅ Membership created successfully!\n\nID: {membership['id']}\n{format_membership(membership)}"
        )
    ]


async def handle_update_membership(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates a membership."""
    membership_id = arguments["membership_id"]
    role_ids = arguments["role_ids"]
    
    success = client.update_membership(membership_id, role_ids)
    
    if success:
        updated_membership = client.get_membership(membership_id)
        return [
            types.TextContent(
                type="text",
                text=f"✅ Membership #{membership_id} updated successfully!\n\n{format_membership(updated_membership)}"
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to update membership #{membership_id}."
            )
        ]


async def handle_delete_membership(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes a membership."""
    membership_id = arguments["membership_id"]
    
    success = client.delete_membership(membership_id)
    
    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Membership #{membership_id} removed successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to remove membership #{membership_id}."
            )
        ]


# Helper formatters

def format_membership(membership: Dict[str, Any]) -> str:
    """Formats a single membership."""
    user_info = membership.get('user') or membership.get('group', {})
    user_name = user_info.get('name', 'Unknown')
    user_type = 'User' if 'user' in membership else 'Group'
    
    roles = [role.get('name', str(role.get('id', 'N/A'))) for role in membership.get('roles', [])]
    
    parts = [
        f"Member: {user_name} ({user_type})",
        f"Project: {membership.get('project', {}).get('name', 'N/A')}",
        f"Roles: {', '.join(roles) if roles else 'None'}"
    ]
    
    return "\n".join(parts)


def format_memberships(memberships: List[Dict[str, Any]]) -> str:
    """Formats a list of memberships."""
    if not memberships:
        return "No members found."
    
    formatted = []
    for i, member in enumerate(memberships, 1):
        formatted.append(f"{i}. ID: {member.get('id', 'N/A')}")
        formatted.append(f"   {format_membership(member)}")
        formatted.append("")
    
    return "\n".join(formatted)