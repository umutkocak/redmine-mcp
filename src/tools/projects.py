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

def create_create_project_tool() -> Tool:
    """create_project tool'unu oluşturur."""
    return Tool(
        name="create_project",
        description="Yeni Redmine projesi oluşturur",
        inputSchema={
            "type": "object",
            "properties": {
                "project": {
                    "type": "object",
                    "description": "Proje verisi",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Proje adı (ZORUNLU)"
                        },
                        "identifier": {
                            "type": "string",
                            "description": "Proje identifier (ZORUNLU, küçük harf, tire içerebilir)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Proje açıklaması"
                        },
                        "homepage": {
                            "type": "string",
                            "description": "Proje web sitesi"
                        },
                        "is_public": {
                            "type": "boolean",
                            "description": "Proje herkese açık mı?"
                        },
                        "parent_id": {
                            "type": "number",
                            "description": "Üst proje ID'si"
                        },
                        "inherit_members": {
                            "type": "boolean",
                            "description": "Üst proje üyelerini miras alsın mı?"
                        },
                        "tracker_ids": {
                            "type": "array",
                            "description": "Aktif tracker ID'leri",
                            "items": {"type": "number"}
                        },
                        "enabled_module_names": {
                            "type": "array",
                            "description": "Aktif modül isimleri (örn: issue_tracking, time_tracking, wiki)",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["name", "identifier"]
                }
            },
            "required": ["project"],
        },
    )

def create_update_project_tool() -> Tool:
    """update_project tool'unu oluşturur."""
    return Tool(
        name="update_project",
        description="Mevcut Redmine projesini günceller",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Proje ID'si"
                },
                "project": {
                    "type": "object",
                    "description": "Güncellenecek proje verisi",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Yeni proje adı"
                        },
                        "description": {
                            "type": "string",
                            "description": "Yeni açıklama"
                        },
                        "homepage": {
                            "type": "string",
                            "description": "Yeni web sitesi"
                        },
                        "is_public": {
                            "type": "boolean",
                            "description": "Proje herkese açık mı?"
                        },
                        "tracker_ids": {
                            "type": "array",
                            "description": "Aktif tracker ID'leri",
                            "items": {"type": "number"}
                        },
                        "enabled_module_names": {
                            "type": "array",
                            "description": "Aktif modül isimleri",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "required": ["project_id", "project"],
        },
    )

def create_delete_project_tool() -> Tool:
    """delete_project tool'unu oluşturur."""
    return Tool(
        name="delete_project",
        description="Redmine projesini siler",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Silinecek proje ID'si"
                }
            },
            "required": ["project_id"],
        },
    )

def create_archive_project_tool() -> Tool:
    """archive_project tool'unu oluşturur."""
    return Tool(
        name="archive_project",
        description="Redmine projesini arşivler (Redmine 5.0+)",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Arşivlenecek proje ID'si"
                }
            },
            "required": ["project_id"],
        },
    )

def create_unarchive_project_tool() -> Tool:
    """unarchive_project tool'unu oluşturur."""
    return Tool(
        name="unarchive_project",
        description="Redmine projesini arşivden çıkarır (Redmine 5.0+)",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Arşivden çıkarılacak proje ID'si"
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

async def handle_create_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """create_project tool'unu handle eder."""
    try:
        project_data = args.get("project")
        if not project_data:
            raise ValueError("Missing 'project' wrapper in request")
        
        if not project_data.get("name"):
            raise ValueError("'name' is required")
        if not project_data.get("identifier"):
            raise ValueError("'identifier' is required")
        
        result = client.create_project(project_data)
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"create_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]

async def handle_update_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """update_project tool'unu handle eder."""
    try:
        project_id = args.get("project_id")
        if not project_id:
            raise ValueError("project_id is required")
        
        project_data = args.get("project")
        if not project_data:
            raise ValueError("Missing 'project' wrapper in request")
        
        result = client.update_project(project_id, project_data)
        
        return [
            TextContent(
                type="text",
                text=json.dumps(result or {"status": "updated"}, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"update_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]

async def handle_delete_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """delete_project tool'unu handle eder."""
    try:
        project_id = args.get("project_id")
        if not project_id:
            raise ValueError("project_id is required")
        
        result = client.delete_project(project_id)
        
        return [
            TextContent(
                type="text",
                text=json.dumps({"status": "deleted", "project_id": project_id}, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"delete_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]

async def handle_archive_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """archive_project tool'unu handle eder."""
    try:
        project_id = args.get("project_id")
        if not project_id:
            raise ValueError("project_id is required")
        
        result = client.archive_project(project_id)
        
        return [
            TextContent(
                type="text",
                text=json.dumps({"status": "archived", "project_id": project_id}, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"archive_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]

async def handle_unarchive_project(client, args: Dict[str, Any]) -> List[TextContent]:
    """unarchive_project tool'unu handle eder."""
    try:
        project_id = args.get("project_id")
        if not project_id:
            raise ValueError("project_id is required")
        
        result = client.unarchive_project(project_id)
        
        return [
            TextContent(
                type="text",
                text=json.dumps({"status": "unarchived", "project_id": project_id}, indent=2, ensure_ascii=False),
            )
        ]
        
    except Exception as e:
        logger.error(f"unarchive_project error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error: {str(e)}",
            )
        ]
