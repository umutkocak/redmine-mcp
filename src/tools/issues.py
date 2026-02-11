"""
Redmine Issue Tool'ları - MCP ile

Bu modül Redmine issue'lar ile ilgili MCP tool'larını içerir:
- list_issues: Issue'ları listeler ve filtreler
- get_issue: Belirli bir issue detayını getirir  
- create_issue: Yeni issue oluşturur
- update_issue: Mevcut issue'yu günceller
"""

import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from mcp.types import Tool, TextContent

# Parent klasörü path'e ekle
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

logger = logging.getLogger(__name__)

def create_list_issues_tool() -> Tool:
    """list_issues tool'unu oluşturur."""
    return Tool(
        name="list_issues",
        description="Redmine issue'larını listeler ve filtreler",
        inputSchema={
            "type": "object",
            "properties": {
                "project_id": {
                    "type": "number",
                    "description": "Proje ID'si (filtreleme için)"
                },
                "assigned_to_id": {
                    "type": "number", 
                    "description": "Atanan kişi ID'si"
                },
                "status_id": {
                    "type": "string",
                    "description": "Durum ID'si veya 'open'/'closed'"
                },
                "priority_id": {
                    "type": "number",
                    "description": "Öncelik ID'si"
                },
                "tracker_id": {
                    "type": "number",
                    "description": "Tracker ID'si"
                },
                "limit": {
                    "type": "number",
                    "description": "Döndürülecek maksimum issue sayısı (varsayılan: 25)",
                    "default": 25
                },
                "offset": {
                    "type": "number",
                    "description": "Pagination offset (varsayılan: 0)",
                    "default": 0
                }
            },
            "required": [],
        },
    )

def create_get_issue_tool() -> Tool:
    """get_issue tool'unu oluşturur."""
    return Tool(
        name="get_issue",
        description="Belirli bir Redmine issue'sinin detaylarını getirir",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Issue ID'si"
                }
            },
            "required": ["issue_id"],
        },
    )

def create_create_issue_tool() -> Tool:
    """create_issue tool'unu oluşturur."""
    return Tool(
        name="create_issue",
        description="Yeni Redmine issue'sı oluşturur. ZORUNLU FORMAT: {'issue': {project_id, subject, ...}}",
        inputSchema={
            "type": "object",
            "properties": {
                "issue": {
                    "type": "object",
                    "description": "Issue verisi - project_id ve subject zorunlu",
                    "properties": {
                        "project_id": {
                            "type": "number",
                            "description": "Proje ID'si (ZORUNLU)"
                        },
                        "subject": {
                            "type": "string",
                            "description": "Issue başlığı (ZORUNLU)"
                        },
                        "description": {
                            "type": "string",
                            "description": "Issue açıklaması"
                        },
                        "tracker_id": {
                            "type": "number",
                            "description": "Tracker ID'si"
                        },
                        "status_id": {
                            "type": "number",
                            "description": "Başlangıç durumu ID'si"
                        },
                        "priority_id": {
                            "type": "number",
                            "description": "Öncelik ID'si"
                        },
                        "assigned_to_id": {
                            "type": "number",
                            "description": "Atanacak kişi ID'si"
                        },
                        "parent_issue_id": {
                            "type": "number",
                            "description": "Parent issue ID'si"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Başlangıç tarihi (YYYY-MM-DD)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Bitiş tarihi (YYYY-MM-DD)"
                        },
                        "custom_fields": {
                            "type": "array",
                            "description": "Custom field'lar [{'id': 76, 'value': 'değer'}] formatında",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "number"},
                                    "value": {"type": "string"}
                                }
                            }
                        }
                    },
                    "required": ["project_id", "subject"]
                }
            },
            "required": ["issue"],
        },
    )

def create_delete_issue_tool() -> Tool:
    """delete_issue tool'unu oluşturur."""
    return Tool(
        name="delete_issue",
        description="Redmine issue'sını siler",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Silinecek issue ID'si"
                }
            },
            "required": ["issue_id"],
        },
    )

def create_add_watcher_tool() -> Tool:
    """add_watcher tool'unu oluşturur."""
    return Tool(
        name="add_watcher",
        description="Issue'ya takipçi (watcher) ekler",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Issue ID'si"
                },
                "user_id": {
                    "type": "number",
                    "description": "Takipçi olarak eklenecek kullanıcı ID'si"
                }
            },
            "required": ["issue_id", "user_id"],
        },
    )

def create_remove_watcher_tool() -> Tool:
    """remove_watcher tool'unu oluşturur."""
    return Tool(
        name="remove_watcher",
        description="Issue'dan takipçi (watcher) çıkarır",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Issue ID'si"
                },
                "user_id": {
                    "type": "number",
                    "description": "Çıkarılacak kullanıcı ID'si"
                }
            },
            "required": ["issue_id", "user_id"],
        },
    )

def create_update_issue_tool() -> Tool:
    """update_issue tool'unu oluşturur."""
    return Tool(
        name="update_issue", 
        description="Mevcut Redmine issue'sını günceller. Format: {'issue_id': int, 'issue': {...}}",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Issue ID'si (zorunlu)"
                },
                "issue": {
                    "type": "object",
                    "description": "Güncellenecek issue verisi",
                    "properties": {
                        "subject": {
                            "type": "string",
                            "description": "Yeni başlık"
                        },
                        "description": {
                            "type": "string",
                            "description": "Yeni açıklama"
                        },
                        "status_id": {
                            "type": "number",
                            "description": "Yeni durum ID'si"
                        },
                        "priority_id": {
                            "type": "number",
                            "description": "Yeni öncelik ID'si"
                        },
                        "assigned_to_id": {
                            "type": "number",
                            "description": "Yeni atanan kişi ID'si"
                        },
                        "parent_issue_id": {
                            "type": "number",
                            "description": "Parent issue ID'si"
                        },
                        "start_date": {
                            "type": "string",
                            "description": "Başlangıç tarihi (YYYY-MM-DD)"
                        },
                        "due_date": {
                            "type": "string",
                            "description": "Bitiş tarihi (YYYY-MM-DD)"
                        },
                        "notes": {
                            "type": "string",
                            "description": "Güncelleme notu"
                        },
                        "custom_fields": {
                            "type": "array",
                            "description": "Custom field'lar [{'id': 76, 'value': 'değer'}] formatında",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "id": {"type": "number"},
                                    "value": {"type": "string"}
                                }
                            }
                        }
                    }
                }
            },
            "required": ["issue_id", "issue"],
        },
    )

async def handle_list_issues(client, args: Dict[str, Any]) -> List[TextContent]:
    """list_issues tool handler'ı."""
    try:
        project_id = args.get("project_id")
        assigned_to_id = args.get("assigned_to_id")  
        status_id = args.get("status_id")
        priority_id = args.get("priority_id")
        tracker_id = args.get("tracker_id")
        limit = args.get("limit", 25)
        offset = args.get("offset", 0)
        
        issues = client.get_issues(
            project_id=project_id,
            assigned_to_id=assigned_to_id,
            status_id=status_id,
            priority_id=priority_id,
            tracker_id=tracker_id,
            limit=limit,
            offset=offset
        )
        
        result = {
            "issues": issues,
            "total_count": len(issues),
            "filters": {
                "project_id": project_id,
                "assigned_to_id": assigned_to_id,
                "status_id": status_id,
                "priority_id": priority_id,
                "tracker_id": tracker_id
            },
            "pagination": {
                "limit": limit,
                "offset": offset
            }
        }
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_issues error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_get_issue(client, args: Dict[str, Any]) -> List[TextContent]:
    """get_issue tool handler'ı."""
    try:
        issue_id = args.get("issue_id")
        if not issue_id:
            raise ValueError("issue_id is required")
        
        issue = client.get_issue(issue_id)
        
        if not issue:
            return [TextContent(
                type="text",
                text=f"Issue with ID {issue_id} not found"
            )]
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(issue, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"get_issue error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_create_issue(client, args: Dict[str, Any]) -> List[TextContent]:
    """create_issue tool handler'ı."""

    # ✅ BAŞARILI JSON MODEL - Tool'a giren format:
    # {
    #     "issue": {
    #         "project_id": 18,
    #         "subject": "SCM Analiz Merkezi - Merge Request Code Review & Approval Metrikleri",
    #         "description": "## 🤖 MCP ile Otomatik Oluşturulan Task...",
    #         "tracker_id": 22,
    #         "priority_id": 4,
    #         "assigned_to_id": 348,
    #         "parent_issue_id": 44227,
    #         "start_date": "2025-08-04",
    #         "due_date": "2025-08-05",
    #         "custom_fields": [
    #             { "id": 76, "value": "Yeni Özellik" },
    #             { "id": 97, "value": "features" }
    #         ]
    #     }
    # }
    #
    # NOT: custom_fields kullanın!

    try:
        # Issue wrapper'ından issue data'sını al
        issue_data = args.get("issue")
        if not issue_data:
            raise ValueError("❌ Missing 'issue' wrapper in request. Format should be: {'issue': {...}}")
        
        # Zorunlu field kontrolü
        if not issue_data.get("project_id"):
            raise ValueError("❌ 'project_id' is required inside 'issue' object")
        if not issue_data.get("subject"):
            raise ValueError("❌ 'subject' is required inside 'issue' object")
        
        # RedmineClient, issue_data'yı alır ve {"issue": issue_data} ile sarar
        result = client.create_issue(issue_data)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"create_issue error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_update_issue(client, args: Dict[str, Any]) -> List[TextContent]:
    """update_issue tool handler'ı."""
    try:
        issue_id = args.get("issue_id")
        if not issue_id:
            raise ValueError("❌ 'issue_id' is required at top level")
            
        # Issue wrapper'ından issue data'sını al
        issue_data = args.get("issue")
        if not issue_data:
            raise ValueError("❌ Missing 'issue' wrapper in request. Format should be: {'issue_id': 123, 'issue': {...}}")
        
        # RedmineClient, issue_data'yı doğrudan alır (zaten {"issue": {...}} ile sarar)
        result = client.update_issue(issue_id, issue_data)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result or {"status": "updated"}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"update_issue error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_delete_issue(client, args: Dict[str, Any]) -> List[TextContent]:
    """delete_issue tool handler'ı."""
    try:
        issue_id = args.get("issue_id")
        if not issue_id:
            raise ValueError("issue_id is required")
        
        result = client.delete_issue(issue_id)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps({"status": "deleted", "issue_id": issue_id}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"delete_issue error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_add_watcher(client, args: Dict[str, Any]) -> List[TextContent]:
    """add_watcher tool handler'ı."""
    try:
        issue_id = args.get("issue_id")
        user_id = args.get("user_id")
        
        if not issue_id:
            raise ValueError("issue_id is required")
        if not user_id:
            raise ValueError("user_id is required")
        
        result = client.add_watcher(issue_id, user_id)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps({"status": "watcher_added", "issue_id": issue_id, "user_id": user_id}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"add_watcher error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_remove_watcher(client, args: Dict[str, Any]) -> List[TextContent]:
    """remove_watcher tool handler'ı."""
    try:
        issue_id = args.get("issue_id")
        user_id = args.get("user_id")
        
        if not issue_id:
            raise ValueError("issue_id is required")
        if not user_id:
            raise ValueError("user_id is required")
        
        result = client.remove_watcher(issue_id, user_id)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps({"status": "watcher_removed", "issue_id": issue_id, "user_id": user_id}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"remove_watcher error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
