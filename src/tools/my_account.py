#!/usr/bin/env python3
"""
Redmine My Account management MCP tools.

This module provides Redmine account management for the authenticated user:
- Get current account information
- Update current account settings
"""

import json
from typing import Dict, Any, List, Optional
import mcp.types as types


def create_get_my_account_tool() -> types.Tool:
    """Creates tool for getting current account info."""
    return types.Tool(
        name="get_my_account",
        description=(
            "Gets the account details of the currently authenticated user. "
            "Returns personal information, mail, API key status, and custom fields."
        ),
        inputSchema={
            "type": "object",
            "properties": {},
            "required": []
        }
    )


def create_update_my_account_tool() -> types.Tool:
    """Creates tool for updating current account."""
    return types.Tool(
        name="update_my_account",
        description=(
            "Updates the account settings of the currently authenticated user. "
            "Can update first name, last name, mail, and custom fields."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "firstname": {
                    "type": "string",
                    "description": "First name"
                },
                "lastname": {
                    "type": "string",
                    "description": "Last name"
                },
                "mail": {
                    "type": "string",
                    "description": "Email address"
                },
                "custom_fields": {
                    "type": "array",
                    "description": "Custom fields in [{'id': N, 'value': '...'}] format",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "integer"},
                            "value": {"type": "string"}
                        }
                    }
                }
            },
            "required": []
        }
    )


# Handler functions

async def handle_get_my_account(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Gets current account information."""
    account = client.get_my_account()

    return [
        types.TextContent(
            type="text",
            text=f"My Account Details:\n\n{format_account(account)}"
        )
    ]


async def handle_update_my_account(client, arguments: Dict[str, Any]) -> List[types.TextContent]:
    """Updates current account."""
    account_data = {k: v for k, v in arguments.items() if v is not None}

    if not account_data:
        return [
            types.TextContent(
                type="text",
                text="❌ No fields provided to update."
            )
        ]

    success = client.update_my_account(account_data)

    if success:
        updated = client.get_my_account()
        return [
            types.TextContent(
                type="text",
                text=f"✅ Account updated successfully!\n\n{format_account(updated)}"
            )
        ]
    else:
        return [
            types.TextContent(
                type="text",
                text="❌ Failed to update account."
            )
        ]


# Helper formatters

def format_account(account: Dict[str, Any]) -> str:
    """Formats account details."""
    parts = [
        f"ID: {account.get('id', 'N/A')}",
        f"Login: {account.get('login', 'N/A')}",
        f"Name: {account.get('firstname', '')} {account.get('lastname', '')}",
        f"Email: {account.get('mail', 'N/A')}",
    ]

    if account.get('admin') is not None:
        parts.append(f"Admin: {account['admin']}")

    if account.get('created_on'):
        parts.append(f"Created: {account['created_on']}")

    if account.get('last_login_on'):
        parts.append(f"Last Login: {account['last_login_on']}")

    if account.get('api_key'):
        parts.append(f"API Key: {account['api_key'][:8]}...")

    if account.get('custom_fields'):
        parts.append("\nCustom Fields:")
        for cf in account['custom_fields']:
            parts.append(f"  - {cf.get('name', 'N/A')}: {cf.get('value', 'N/A')}")

    return "\n".join(parts)
