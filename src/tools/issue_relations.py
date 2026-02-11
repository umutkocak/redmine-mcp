#!/usr/bin/env python3
"""
Redmine Issue Relations management MCP tools.

This module provides Redmine issue relationship management:
- List issue relations
- Create new relations (blocks, relates, duplicates, etc.)
- Get relation details
- Delete relations
"""

from typing import Dict, Any, List, Optional
import mcp.types as types

# Relation types supported by Redmine
RELATION_TYPES = [
    "relates",      # Related to
    "duplicates",   # Duplicates
    "duplicated",   # Duplicated by
    "blocks",       # Blocks
    "blocked",      # Blocked by
    "precedes",     # Precedes
    "follows",      # Follows
    "copied_to",    # Copied to
    "copied_from"   # Copied from
]


def create_list_issue_relations_tool() -> types.Tool:
    """Creates tool for listing issue relations."""
    return types.Tool(
        name="list_issue_relations",
        description=(
            "Lists all relations for a specific issue. "
            "Returned relations: relates, duplicates, blocks, precedes, etc."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "integer",
                    "description": "Issue ID to list relations for"
                }
            },
            "required": ["issue_id"]
        }
    )


def create_create_issue_relation_tool() -> types.Tool:
    """Creates tool for creating issue relations."""
    return types.Tool(
        name="create_issue_relation",
        description=(
            "Creates a relation between two issues. "
            "Relation types: relates, duplicates, blocks, precedes, follows, etc. "
            "Delay parameter (in days) can be used for precedes/follows relations."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "integer",
                    "description": "Source issue ID"
                },
                "issue_to_id": {
                    "type": "integer",
                    "description": "Target issue ID"
                },
                "relation_type": {
                    "type": "string",
                    "description": "Relation type",
                    "enum": RELATION_TYPES
                },
                "delay": {
                    "type": "integer",
                    "description": "Delay in days (only for precedes/follows relations)"
                }
            },
            "required": ["issue_id", "issue_to_id", "relation_type"]
        }
    )


def create_get_issue_relation_tool() -> types.Tool:
    """Creates tool for getting issue relation details."""
    return types.Tool(
        name="get_issue_relation",
        description="Gets details of a specific relation.",
        inputSchema={
            "type": "object",
            "properties": {
                "relation_id": {
                    "type": "integer",
                    "description": "Relation ID"
                }
            },
            "required": ["relation_id"]
        }
    )


def create_delete_issue_relation_tool() -> types.Tool:
    """Creates tool for deleting issue relations."""
    return types.Tool(
        name="delete_issue_relation",
        description="Deletes a specific issue relation.",
        inputSchema={
            "type": "object",
            "properties": {
                "relation_id": {
                    "type": "integer",
                    "description": "Relation ID to delete"
                }
            },
            "required": ["relation_id"]
        }
    )


# Handler functions

async def handle_list_issue_relations(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists issue relations."""
    issue_id = arguments["issue_id"]
    
    relations = client.list_issue_relations(issue_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Found {len(relations)} relation(s) for Issue #{issue_id}:\n\n{format_relations(relations)}"
        )
    ]


async def handle_create_issue_relation(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Creates a new issue relation."""
    issue_id = arguments["issue_id"]
    issue_to_id = arguments["issue_to_id"]
    relation_type = arguments["relation_type"]
    delay = arguments.get("delay")
    
    relation = client.create_issue_relation(
        issue_id=issue_id,
        issue_to_id=issue_to_id,
        relation_type=relation_type,
        delay=delay
    )
    
    return [
        types.TextContent(
            type="text",
            text=f"✅ Relation created successfully!\n\nID: {relation['id']}\n{format_relation(relation)}"
        )
    ]


async def handle_get_issue_relation(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets issue relation details."""
    relation_id = arguments["relation_id"]
    
    relation = client.get_issue_relation(relation_id)
    
    return [
        types.TextContent(
            type="text",
            text=f"Relation Details (ID: {relation_id}):\n\n{format_relation(relation)}"
        )
    ]


async def handle_delete_issue_relation(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Deletes an issue relation."""
    relation_id = arguments["relation_id"]
    
    success = client.delete_issue_relation(relation_id)
    
    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Relation #{relation_id} deleted successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to delete relation #{relation_id}."
            )
        ]


# Helper formatters

def format_relation(relation: Dict[str, Any]) -> str:
    """Formats a single relation."""
    parts = [
        f"Type: {relation.get('relation_type', 'N/A')}",
        f"Issue ID: {relation.get('issue_id', 'N/A')}",
        f"Issue To ID: {relation.get('issue_to_id', 'N/A')}"
    ]
    
    if relation.get('delay'):
        parts.append(f"Delay: {relation['delay']} day(s)")
    
    return "\n".join(parts)


def format_relations(relations: List[Dict[str, Any]]) -> str:
    """Formats a list of relations."""
    if not relations:
        return "No relations found."
    
    formatted = []
    for i, rel in enumerate(relations, 1):
        formatted.append(f"{i}. ID: {rel.get('id', 'N/A')}")
        formatted.append(f"   {format_relation(rel)}")
        formatted.append("")
    
    return "\n".join(formatted)
