#!/usr/bin/env python3
"""
Redmine Issue Categories management MCP tools.

This module provides Redmine issue category management:
- List issue categories for a project
- Get category details
- Create new categories
- Update categories
- Delete categories
"""

from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_issue_categories_tool() -> types.Tool:
    """Creates tool for listing issue categories."""
    return types.Tool(
        name="list_issue_categories",
        description="Lists all issue categories for a specific project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to list categories for"
                }
            },
            "required": ["project_id"]
        }
    )


def create_get_issue_category_tool() -> types.Tool:
    """Creates tool for getting issue category details."""
    return types.Tool(
        name="get_issue_category",
        description="Gets details of a specific issue category.",
        inputSchema={
            "type": "object",
            "properties": {
                "category_id": {
                    "type": "integer",
                    "description": "Category ID"
                }
            },
            "required": ["category_id"]
        }
    )


def create_create_issue_category_tool() -> types.Tool:
    """Creates tool for creating issue categories."""
    return types.Tool(
        name="create_issue_category",
        description=(
            "Creates a new issue category in a project. "
            "Optionally assigns a default assignee for the category."
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
                    "description": "Category name"
                },
                "assigned_to_id": {
                    "type": "integer",
                    "description": "Default assignee user ID for this category"
                }
            },
            "required": ["project_id", "name"]
        }
    )


def create_update_issue_category_tool() -> types.Tool:
    """Creates tool for updating issue categories."""
    return types.Tool(
        name="update_issue_category",
        description="Updates an existing issue category.",
        inputSchema={
            "type": "object",
            "properties": {
                "category_id": {
                    "type": "integer",
                    "description": "Category ID to update"
                },
                "name": {
                    "type": "string",
                    "description": "New category name"
                },
                "assigned_to_id": {
                    "type": "integer",
                    "description": "New default assignee user ID"
                }
            },
            "required": ["category_id"]
        }
    )


def create_delete_issue_category_tool() -> types.Tool:
    """Creates tool for deleting issue categories."""
    return types.Tool(
        name="delete_issue_category",
        description=(
            "Deletes a specific issue category. "
            "Optionally reassigns issues to another category."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "category_id": {
                    "type": "integer",
                    "description": "Category ID to delete"
                },
                "reassign_to_id": {
                    "type": "integer",
                    "description": "Category ID to reassign existing issues to (optional)"
                }
            },
            "required": ["category_id"]
        }
    )


# Handler functions

async def handle_list_issue_categories(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists issue categories for a project."""
    project_id = arguments["project_id"]

    categories = client.list_issue_categories(project_id)

    return [
        types.TextContent(
            type="text",
            text=f"Found {len(categories)} category(ies) for Project '{project_id}':\n\n{format_categories(categories)}"
        )
    ]


async def handle_get_issue_category(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets issue category details."""
    category_id = arguments["category_id"]

    category = client.get_issue_category(category_id)

    return [
        types.TextContent(
            type="text",
            text=f"Category Details (ID: {category_id}):\n\n{format_category(category)}"
        )
    ]


async def handle_create_issue_category(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates a new issue category."""
    project_id = arguments.pop("project_id")
    category_data = {k: v for k, v in arguments.items() if v is not None}

    category = client.create_issue_category(project_id, category_data)

    return [
        types.TextContent(
            type="text",
            text=f"✅ Category created successfully!\n\nID: {category.get('id', 'N/A')}\n{format_category(category)}"
        )
    ]


async def handle_update_issue_category(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates an issue category."""
    category_id = arguments.pop("category_id")
    category_data = {k: v for k, v in arguments.items() if v is not None}

    success = client.update_issue_category(category_id, category_data)

    if success:
        updated_category = client.get_issue_category(category_id)
        return [
            types.TextContent(
                type="text",
                text=f"✅ Category #{category_id} updated successfully!\n\n{format_category(updated_category)}"
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to update category #{category_id}."
            )
        ]


async def handle_delete_issue_category(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes an issue category."""
    category_id = arguments["category_id"]
    reassign_to_id = arguments.get("reassign_to_id")

    success = client.delete_issue_category(category_id, reassign_to_id=reassign_to_id)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Category #{category_id} deleted successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to delete category #{category_id}."
            )
        ]


# Helper formatters

def format_category(category: Dict[str, Any]) -> str:
    """Formats a single category."""
    parts = [
        f"Name: {category.get('name', 'N/A')}",
        f"Project: {category.get('project', {}).get('name', 'N/A')}"
    ]

    assigned_to = category.get('assigned_to')
    if assigned_to:
        parts.append(f"Default Assignee: {assigned_to.get('name', 'N/A')}")

    return "\n".join(parts)


def format_categories(categories: List[Dict[str, Any]]) -> str:
    """Formats a list of categories."""
    if not categories:
        return "No categories found."

    formatted = []
    for i, cat in enumerate(categories, 1):
        formatted.append(f"{i}. ID: {cat.get('id', 'N/A')}")
        formatted.append(f"   {format_category(cat)}")
        formatted.append("")

    return "\n".join(formatted)
