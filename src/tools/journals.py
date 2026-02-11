#!/usr/bin/env python3
"""
Redmine Journals (Issue History) management MCP tools.

This module provides Redmine issue journal/history management:
- List issue journals (change history and notes)
- Update journal notes
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_issue_journals_tool() -> types.Tool:
    """Creates tool for listing issue journals."""
    return types.Tool(
        name="list_issue_journals",
        description=(
            "Lists the change history (journals) of an issue. "
            "Each journal entry contains notes and/or property changes."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "integer",
                    "description": "Issue ID to get journals for"
                }
            },
            "required": ["issue_id"]
        }
    )


def create_update_journal_tool() -> types.Tool:
    """Creates tool for updating journal notes."""
    return types.Tool(
        name="update_journal",
        description=(
            "Updates the notes of an existing journal entry. "
            "Only the author of the journal or an admin can update it."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "journal_id": {
                    "type": "integer",
                    "description": "Journal ID to update"
                },
                "notes": {
                    "type": "string",
                    "description": "New notes content"
                },
                "private_notes": {
                    "type": "boolean",
                    "description": "Whether the notes should be private (optional)"
                }
            },
            "required": ["journal_id", "notes"]
        }
    )


# Handler functions

async def handle_list_issue_journals(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists issue journals."""
    issue_id = arguments["issue_id"]

    journals = client.list_issue_journals(issue_id)

    return [
        types.TextContent(
            type="text",
            text=f"Found {len(journals)} journal(s) for issue #{issue_id}:\n\n{format_journals(journals)}"
        )
    ]


async def handle_update_journal(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates journal notes."""
    journal_id = arguments["journal_id"]
    notes = arguments["notes"]
    private_notes = arguments.get("private_notes")

    journal_data = {"notes": notes}
    if private_notes is not None:
        journal_data["private_notes"] = private_notes

    success = client.update_journal(journal_id, journal_data)

    if success:
        return [
            types.TextContent(
                type="text",
                text=f"✅ Journal #{journal_id} updated successfully."
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text=f"❌ Failed to update journal #{journal_id}."
            )
        ]


# Helper formatters

def format_journal(journal: Dict[str, Any]) -> str:
    """Formats a single journal entry."""
    parts = [
        f"ID: {journal.get('id', 'N/A')}",
    ]

    if journal.get('user'):
        parts.append(f"Author: {journal['user'].get('name', 'N/A')}")

    if journal.get('created_on'):
        parts.append(f"Date: {journal['created_on']}")

    if journal.get('private_notes'):
        parts.append("Private: Yes")

    if journal.get('notes'):
        notes = journal['notes']
        if len(notes) > 200:
            notes = notes[:200] + "... (truncated)"
        parts.append(f"Notes: {notes}")

    if journal.get('details'):
        details = journal['details']
        parts.append(f"Changes ({len(details)}):")
        for detail in details:
            prop = detail.get('property', '')
            name = detail.get('name', '')
            old = detail.get('old_value', '')
            new = detail.get('new_value', '')
            parts.append(f"  - {prop}.{name}: '{old}' -> '{new}'")

    return "\n".join(parts)


def format_journals(journals: List[Dict[str, Any]]) -> str:
    """Formats a list of journal entries."""
    if not journals:
        return "No journals found."

    formatted = []
    for i, journal in enumerate(journals, 1):
        formatted.append(f"--- Entry {i} ---")
        formatted.append(format_journal(journal))
        formatted.append("")

    return "\n".join(formatted)
