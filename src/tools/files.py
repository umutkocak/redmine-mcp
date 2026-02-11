#!/usr/bin/env python3
"""
Redmine Files management MCP tools.

This module provides Redmine project file listing:
- List files for a project
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_files_tool() -> types.Tool:
    """Creates tool for listing project files."""
    return types.Tool(
        name="list_files",
        description="Lists all files uploaded to a specific project.",
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


# Handler functions

async def handle_list_files(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists project files."""
    project_id = arguments["project_id"]

    files = client.list_files(project_id)

    return [
        types.TextContent(
            type="text",
            text=f"Found {len(files)} file(s) for project '{project_id}':\n\n{format_files(files)}"
        )
    ]


# Helper formatters

def format_files(files: List[Dict[str, Any]]) -> str:
    """Formats a list of files."""
    if not files:
        return "No files found."

    formatted = []
    for i, f in enumerate(files, 1):
        filename = f.get('filename', 'N/A')
        filesize = f.get('filesize', 0)
        created = f.get('created_on', 'N/A')
        desc = f.get('description', '')

        size_str = format_filesize(filesize)
        line = f"{i}. {filename} ({size_str}, uploaded: {created})"
        if desc:
            line += f"\n   Description: {desc}"
        formatted.append(line)

    return "\n".join(formatted)


def format_filesize(size_bytes: int) -> str:
    """Formats file size in human-readable format."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    elif size_bytes < 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    else:
        return f"{size_bytes / (1024 * 1024 * 1024):.1f} GB"
