#!/usr/bin/env python3
"""
Redmine Search MCP tools.

This module provides Redmine global search:
- Search across issues, projects, wiki pages, news, etc.
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_search_tool() -> types.Tool:
    """Creates tool for global search."""
    return types.Tool(
        name="search",
        description=(
            "Performs a global search across Redmine. "
            "Searches issues, projects, wiki pages, news, changesets, messages, and documents."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query string"
                },
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to limit search scope (optional)"
                },
                "titles_only": {
                    "type": "boolean",
                    "description": "Search only in titles (default: false)"
                },
                "open_issues": {
                    "type": "boolean",
                    "description": "Search only open issues (default: false)"
                },
                "scope": {
                    "type": "string",
                    "description": "Search scope when project_id is given",
                    "enum": ["subprojects", "all"]
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of results to return (default: 25)",
                    "default": 25
                },
                "offset": {
                    "type": "integer",
                    "description": "Pagination offset (default: 0)",
                    "default": 0
                }
            },
            "required": ["query"]
        }
    )


# Handler functions

async def handle_search(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Performs global search."""
    query = arguments["query"]
    project_id = arguments.get("project_id")
    titles_only = arguments.get("titles_only", False)
    open_issues = arguments.get("open_issues", False)
    scope = arguments.get("scope")
    limit = arguments.get("limit", 25)
    offset = arguments.get("offset", 0)

    results = client.search(
        query=query,
        project_id=project_id,
        titles_only=titles_only,
        open_issues=open_issues,
        scope=scope,
        limit=limit,
        offset=offset
    )

    total = results.get("total_count", 0)
    items = results.get("results", [])

    return [
        types.TextContent(
            type="text",
            text=f"Search results for '{query}' ({total} total):\n\n{format_search_results(items)}"
        )
    ]


# Helper formatters

def format_search_results(results: List[Dict[str, Any]]) -> str:
    """Formats search results."""
    if not results:
        return "No results found."

    formatted = []
    for i, result in enumerate(results, 1):
        rtype = result.get('type', 'unknown')
        title = result.get('title', 'N/A')
        rid = result.get('id', 'N/A')
        url = result.get('url', '')
        desc = result.get('description', '')

        parts = [f"{i}. [{rtype}] {title} (ID: {rid})"]
        if url:
            parts.append(f"   URL: {url}")
        if desc:
            if len(desc) > 150:
                desc = desc[:150] + "..."
            parts.append(f"   {desc}")

        formatted.append("\n".join(parts))

    return "\n\n".join(formatted)
