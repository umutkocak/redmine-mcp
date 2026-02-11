"""
Redmine Enumerations MCP tools.

This module provides Redmine system enumeration tools:
- list_enumerations: Lists system constants (statuses, priorities, trackers, etc.)
- list_trackers: Lists all available trackers
- list_issue_statuses: Lists all available issue statuses
- list_roles: Lists all available roles
"""

import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from mcp.types import Tool, TextContent

# Add parent directory to path
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

logger = logging.getLogger(__name__)

def create_list_enumerations_tool() -> Tool:
    """Creates the list_enumerations tool."""
    return Tool(
        name="list_enumerations",
        description="Lists Redmine system constants (statuses, priorities, trackers, activities, etc.)",
        inputSchema={
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "Enumeration type to retrieve",
                    "enum": ["issue_statuses", "issue_priorities", "trackers", "time_entry_activities"]
                }
            },
            "required": [],
        },
    )


def create_list_trackers_tool() -> Tool:
    """Creates the list_trackers tool."""
    return Tool(
        name="list_trackers",
        description="Lists all available trackers in Redmine (e.g., Bug, Feature, Support).",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )


def create_list_issue_statuses_tool() -> Tool:
    """Creates the list_issue_statuses tool."""
    return Tool(
        name="list_issue_statuses",
        description="Lists all available issue statuses in Redmine (e.g., New, In Progress, Closed).",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )


def create_list_roles_tool() -> Tool:
    """Creates the list_roles tool."""
    return Tool(
        name="list_roles",
        description="Lists all available roles in Redmine (e.g., Manager, Developer, Reporter).",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )


async def handle_list_enumerations(client, args: Dict[str, Any]) -> List[TextContent]:
    """Handles list_enumerations tool calls."""
    try:
        resource = args.get("resource")
        
        enumerations = client.get_enumerations(resource)
        
        result = {
            "enumerations": enumerations,
            "resource_type": resource or "all",
            "total_count": len(enumerations) if isinstance(enumerations, list) else len(enumerations.values()) if isinstance(enumerations, dict) else 0
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_enumerations error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def handle_list_trackers(client, args: Dict[str, Any]) -> List[TextContent]:
    """Handles list_trackers tool calls."""
    try:
        trackers = client.list_trackers()
        
        result = {
            "trackers": trackers,
            "total_count": len(trackers)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_trackers error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def handle_list_issue_statuses(client, args: Dict[str, Any]) -> List[TextContent]:
    """Handles list_issue_statuses tool calls."""
    try:
        statuses = client.list_issue_statuses()
        
        result = {
            "issue_statuses": statuses,
            "total_count": len(statuses)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_issue_statuses error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]


async def handle_list_roles(client, args: Dict[str, Any]) -> List[TextContent]:
    """Handles list_roles tool calls."""
    try:
        roles = client.list_roles()
        
        result = {
            "roles": roles,
            "total_count": len(roles)
        }
        
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_roles error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
