#!/usr/bin/env python3
"""
Redmine Custom Fields management MCP tools.

This module provides Redmine custom field listing:
- List all custom fields defined in the system
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_custom_fields_tool() -> types.Tool:
    """Creates tool for listing custom fields."""
    return types.Tool(
        name="list_custom_fields",
        description=(
            "Lists all custom fields defined in Redmine. "
            "Returns field definitions including type, format, possible values, and associated trackers/projects. "
            "Requires admin privileges."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )


# Handler functions

async def handle_list_custom_fields(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists all custom fields."""
    custom_fields = client.list_custom_fields()

    result = {
        "custom_fields": custom_fields,
        "total_count": len(custom_fields)
    }

    return [
        types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )
    ]
