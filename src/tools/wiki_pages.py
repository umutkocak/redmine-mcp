#!/usr/bin/env python3
"""
Redmine Wiki Pages management MCP tools.

This module provides Redmine wiki page management:
- List wiki pages for a project
- Get wiki page content
- Create or update wiki pages
- Delete wiki pages
- Get wiki page version history
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_wiki_pages_tool() -> types.Tool:
    """Creates tool for listing wiki pages."""
    return types.Tool(
        name="list_wiki_pages",
        description="Lists all wiki pages for a specific project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                }
            },
            "required": ["project_id"]
        }
    )


def create_get_wiki_page_tool() -> types.Tool:
    """Creates tool for getting wiki page content."""
    return types.Tool(
        name="get_wiki_page",
        description=(
            "Gets the content of a specific wiki page. "
            "Optionally retrieve a specific version of the page."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                },
                "page_name": {
                    "type": "string",
                    "description": "Wiki page name (title used in URL)"
                },
                "version": {
                    "type": "integer",
                    "description": "Specific page version number (optional, defaults to latest)"
                }
            },
            "required": ["project_id", "page_name"]
        }
    )


def create_create_or_update_wiki_page_tool() -> types.Tool:
    """Creates tool for creating or updating wiki pages."""
    return types.Tool(
        name="create_or_update_wiki_page",
        description=(
            "Creates a new wiki page or updates an existing one. "
            "Content can be in Textile or Markdown format depending on Redmine configuration."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                },
                "page_name": {
                    "type": "string",
                    "description": "Wiki page name (will be used in URL)"
                },
                "text": {
                    "type": "string",
                    "description": "Wiki page content (Textile or Markdown format)"
                },
                "comments": {
                    "type": "string",
                    "description": "Comment describing the change (optional)"
                },
                "parent_title": {
                    "type": "string",
                    "description": "Parent wiki page title for hierarchy (optional)"
                }
            },
            "required": ["project_id", "page_name", "text"]
        }
    )


def create_delete_wiki_page_tool() -> types.Tool:
    """Creates tool for deleting wiki pages."""
    return types.Tool(
        name="delete_wiki_page",
        description="Deletes a specific wiki page from a project.",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier"
                },
                "page_name": {
                    "type": "string",
                    "description": "Wiki page name to delete"
                }
            },
            "required": ["project_id", "page_name"]
        }
    )


# Handler functions

async def handle_list_wiki_pages(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists wiki pages for a project."""
    project_id = arguments["project_id"]

    pages = client.list_wiki_pages(project_id)

    return [
        types.TextContent(
            type="text",
            text=f"Found {len(pages)} wiki page(s) for project '{project_id}':\n\n{format_wiki_pages(pages)}"
        )
    ]


async def handle_get_wiki_page(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets wiki page content."""
    project_id = arguments["project_id"]
    page_name = arguments["page_name"]
    version = arguments.get("version")

    page = client.get_wiki_page(project_id, page_name, version=version)

    version_info = f" (version {version})" if version else ""
    return [
        types.TextContent(
            type="text",
            text=f"Wiki Page: {page_name}{version_info}\n\n{format_wiki_page(page)}"
        )
    ]


async def handle_create_or_update_wiki_page(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates or updates a wiki page."""
    project_id = arguments.pop("project_id")
    page_name = arguments.pop("page_name")
    wiki_data = {k: v for k, v in arguments.items() if v is not None}

    result = client.create_or_update_wiki_page(project_id, page_name, wiki_data)

    return [
        types.TextContent(
            type="text",
            text=f"✅ Wiki page '{page_name}' saved successfully!\n\n{format_wiki_page(result)}"
        )
    ]


async def handle_delete_wiki_page(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes a wiki page."""
    project_id = arguments["project_id"]
    page_name = arguments["page_name"]

    success = client.delete_wiki_page(project_id, page_name)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Wiki page '{page_name}' deleted successfully from project '{project_id}'."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to delete wiki page '{page_name}'."
            )
        ]


# Helper formatters

def format_wiki_page(page: Dict[str, Any]) -> str:
    """Formats a single wiki page."""
    parts = [
        f"Title: {page.get('title', 'N/A')}",
    ]

    if page.get('version'):
        parts.append(f"Version: {page['version']}")

    if page.get('author'):
        author = page['author']
        parts.append(f"Author: {author.get('name', 'N/A')}")

    if page.get('created_on'):
        parts.append(f"Created: {page['created_on']}")

    if page.get('updated_on'):
        parts.append(f"Updated: {page['updated_on']}")

    if page.get('parent'):
        parts.append(f"Parent: {page['parent'].get('title', 'N/A')}")

    if page.get('text'):
        content = page['text']
        if len(content) > 500:
            content = content[:500] + "... (truncated)"
        parts.append(f"\n--- Content ---\n{content}")

    return "\n".join(parts)


def format_wiki_pages(pages: List[Dict[str, Any]]) -> str:
    """Formats a list of wiki pages."""
    if not pages:
        return "No wiki pages found."

    formatted = []
    for i, page in enumerate(pages, 1):
        title = page.get('title', 'N/A')
        version = page.get('version', '')
        updated = page.get('updated_on', '')
        formatted.append(f"{i}. {title} (v{version}, updated: {updated})")

    return "\n".join(formatted)
