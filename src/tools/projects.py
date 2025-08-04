"""
Redmine Proje Tool'ları - MCP ile

Bu modül Redmine projeler ile ilgili MCP tool'larını içerir:
- list_projects: Tüm projeleri listeler
- get_project: Belirli bir proje detayını getirir
"""

import logging
import json
from typing import Dict, Any, List, Optional

from mcp.types import Tool, TextContent

logger = logging.getLogger(__name__)

def create_list_projects_tool() -> Tool:
    """list_projects tool'unu oluşturur."""
    return Tool(
        name="list_projects",
        description="Redmine projelerini listeler",
        inputSchema={
            "type": "object",
            "properties": {
                "limit": {
                    "type": "number",
                    "description": "Döndürülecek maksimum proje sayısı (varsayılan: 25)",
                    "default": 25
                },
                "offset": {
                    "type": "number", 
                    "description": "Kaç proje atlanacağı (pagination için)",
                    "default": 0
                },
                "include_archived": {
                    "type": "boolean",
                    "description": "Arşivlenen projeleri de dahil et",
                    "default": False
                }
            },
            "required": [],
        },
    )

def create_get_project_tool() -> Tool:
    """get_project tool'unu oluşturur."""
    return Tool(
        name="get_project",
        description="Belirli bir Redmine projesinin detaylarını getirir",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Proje ID'si"
                }
            },
            "required": ["project_id"],
        },
    )

async def handle_list_projects(client, args: Dict[str, Any]) -> List[TextContent]:
    """list_projects tool'unu handle eder."""
    try:
        limit = args.get("limit", 25)
        offset = args.get("offset", 0)
        include_archived = args.get("include_archived", False)
        
        projects = client.get_projects(
            limit=limit,
            offset=offset,
            include_archived=include_archived
        )
        
        result = {
            "projects": projects,
            "total_count": len(projects),
            "limit": limit,
            "offset": offset
        }
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"list_projects error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]

async def handle_get_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """get_project tool'unu handle eder."""
    try:
        project_id = args.get("project_id")
        if not project_id:
            raise ValueError("project_id is required")
        
        project = client.get_project(project_id)
        
        if not project:
            return [
                TextContent(
                    type="text",
                    text=f"Project with ID {project_id} not found",
                )
            ]
        
        return [
            TextContent(
                type="text",
                text=json.dumps(project, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"get_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]
