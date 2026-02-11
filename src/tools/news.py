#!/usr/bin/env python3
"""
Redmine News management MCP tools.

This module provides Redmine news management:
- List news (global or per project)
- Get news details
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_list_news_tool() -> types.Tool:
    """Creates tool for listing news."""
    return types.Tool(
        name="list_news",
        description=(
            "Lists news entries. Can be filtered by project. "
            "Returns news with title, summary, author, and creation date."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "string",
                    "description": "Project ID or identifier to filter news (optional, omit for all news)"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of news entries to return (default: 25)",
                    "default": 25
                },
                "offset": {
                    "type": "integer",
                    "description": "Pagination offset (default: 0)",
                    "default": 0
                }
            },
            "required": []
        }
    )


def create_get_news_tool() -> types.Tool:
    """Creates tool for getting news details."""
    return types.Tool(
        name="get_news",
        description="Gets details of a specific news entry.",
        inputSchema={
            "type": "object",
            "properties": {
                "news_id": {
                    "type": "integer",
                    "description": "News ID"
                }
            },
            "required": ["news_id"]
        }
    )


# Handler functions

async def handle_list_news(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Lists news entries."""
    project_id = arguments.get("project_id")
    limit = arguments.get("limit", 25)
    offset = arguments.get("offset", 0)

    news = client.list_news(project_id=project_id, limit=limit, offset=offset)

    scope = f"project '{project_id}'" if project_id else "all projects"
    return [
        types.TextContent(
            type="text",
            text=f"Found {len(news)} news entry/entries for {scope}:\n\n{format_news_list(news)}"
        )
    ]


async def handle_get_news(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets news details."""
    news_id = arguments["news_id"]

    news = client.get_news(news_id)

    return [
        types.TextContent(
            type="text",
            text=f"News Details (ID: {news_id}):\n\n{format_news(news)}"
        )
    ]


# Helper formatters

def format_news(news: Dict[str, Any]) -> str:
    """Formats a single news entry."""
    parts = [
        f"ID: {news.get('id', 'N/A')}",
        f"Title: {news.get('title', 'N/A')}",
    ]

    if news.get('project'):
        parts.append(f"Project: {news['project'].get('name', 'N/A')}")

    if news.get('author'):
        parts.append(f"Author: {news['author'].get('name', 'N/A')}")

    if news.get('created_on'):
        parts.append(f"Created: {news['created_on']}")

    if news.get('summary'):
        parts.append(f"Summary: {news['summary']}")

    if news.get('description'):
        desc = news['description']
        if len(desc) > 500:
            desc = desc[:500] + "... (truncated)"
        parts.append(f"\n--- Description ---\n{desc}")

    return "\n".join(parts)


def format_news_list(news_list: List[Dict[str, Any]]) -> str:
    """Formats a list of news entries."""
    if not news_list:
        return "No news found."

    formatted = []
    for i, news in enumerate(news_list, 1):
        title = news.get('title', 'N/A')
        author = news.get('author', {}).get('name', 'N/A')
        created = news.get('created_on', 'N/A')
        formatted.append(f"{i}. [{news.get('id', 'N/A')}] {title} (by {author}, {created})")

    return "\n".join(formatted)
