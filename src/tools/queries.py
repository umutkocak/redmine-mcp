#!/usr/bin/env python3
"""
Redmine Queries management MCP tools.

This module provides Redmine saved query listing:
- List saved queries (public and user-specific)
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_queries_tool() -> types.Tool:
    """Creates tool for listing saved queries."""
    return types.Tool(
        name="list_queries",
        description=(
            "Lists all saved/custom queries available to the current user. "
            "Includes both public queries and user-specific queries. "
            "Query IDs can be used to filter issues via list_issues."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to filter queries (optional)"
                }
            },
            "required": []
        }
    )


# Handler functions

async def handle_list_queries(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists saved queries."""
    project_id = arguments.get("project_id")

    queries = client.list_queries(project_id=project_id)

    result = {
        "queries": queries,
        "total_count": len(queries)
    }

    return [
        types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )
    ]
