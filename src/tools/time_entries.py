"""
Redmine Time Entry Tool'ları - MCP ile

Bu modül Redmine zaman kayıtları ile ilgili MCP tool'larını içerir:
- list_time_entries: Zaman kayıtlarını listeler
- create_time_entry: Yeni zaman kaydı oluşturur
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

def create_list_time_entries_tool() -> Tool:
    """list_time_entries tool'unu oluşturur."""
    return Tool(
        name="list_time_entries",
        description="Redmine zaman kayıtlarını listeler ve filtreler",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "number",
                    "description": "Kullanıcı ID'si (filtreleme için)"
                },
                "project_id": {
                    "type": "number",
                    "description": "Proje ID'si (filtreleme için)"
                },
                "issue_id": {
                    "type": "number", 
                    "description": "Issue ID'si (filtreleme için)"
                },
                "activity_id": {
                    "type": "number",
                    "description": "Aktivite ID'si (filtreleme için)"
                },
                "spent_on": {
                    "type": "string",
                    "description": "Belirli tarih (YYYY-MM-DD formatında)"
                },
                "from_date": {
                    "type": "string",
                    "description": "Başlangıç tarihi (YYYY-MM-DD formatında)"
                },
                "to_date": {
                    "type": "string",
                    "description": "Bitiş tarihi (YYYY-MM-DD formatında)"
                },
                "limit": {
                    "type": "number",
                    "description": "Döndürülecek maksimum kayıt sayısı (varsayılan: 25)",
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

def create_create_time_entry_tool() -> Tool:
    """create_time_entry tool'unu oluşturur."""
    return Tool(
        name="create_time_entry",
        description="Creates a new time entry in Redmine",
        inputSchema={
            "type": "object",
            "properties": {
                "issue_id": {
                    "type": "number",
                    "description": "Issue ID (either issue_id or project_id is required)"
                },
                "project_id": {
                    "type": "number",
                    "description": "Project ID (either issue_id or project_id is required)"
                },
                "spent_on": {
                    "type": "string",
                    "description": "Date spent (YYYY-MM-DD format) - required"
                },
                "hours": {
                    "type": "number",
                    "description": "Hours spent - required",
                    "minimum": 0.01
                },
                "activity_id": {
                    "type": "number",
                    "description": "Activity ID - required"
                },
                "comments": {
                    "type": "string",
                    "description": "Comments/description (optional)"
                },
                "custom_fields": {
                    "type": "array",
                    "description": "Custom fields",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "number"},
                            "value": {"type": "string"}
                        },
                        "required": ["id", "value"]
                    }
                }
            },
            "required": ["spent_on", "hours", "activity_id"],
        },
    )

async def handle_list_time_entries(client, args: Dict[str, Any]) -> List[TextContent]:
    """list_time_entries tool handler'ı."""
    try:
        user_id = args.get("user_id")
        project_id = args.get("project_id")
        issue_id = args.get("issue_id")
        activity_id = args.get("activity_id")
        spent_on = args.get("spent_on")
        from_date = args.get("from_date")
        to_date = args.get("to_date")
        limit = args.get("limit", 25)
        offset = args.get("offset", 0)
        
        time_entries = client.get_time_entries(
            user_id=user_id,
            project_id=project_id,
            issue_id=issue_id,
            activity_id=activity_id,
            spent_on=spent_on,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset
        )
        
        result = {
            "time_entries": time_entries,
            "total_count": len(time_entries),
            "filters": {
                "user_id": user_id,
                "project_id": project_id,
                "issue_id": issue_id,
                "activity_id": activity_id,
                "spent_on": spent_on,
                "from_date": from_date,
                "to_date": to_date
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
        logger.error(f"list_time_entries error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_create_time_entry(client, args: Dict[str, Any]) -> List[TextContent]:
    """create_time_entry tool handler'ı."""
    try:
        # Required fields
        spent_on = args.get("spent_on")
        hours = args.get("hours")
        activity_id = args.get("activity_id")
        
        if not spent_on:
            raise ValueError("spent_on is required (YYYY-MM-DD format)")
        if not hours:
            raise ValueError("hours is required")
        if not activity_id:
            raise ValueError("activity_id is required")
        
        # Either issue_id or project_id is required
        issue_id = args.get("issue_id")
        project_id = args.get("project_id")
        
        if not issue_id and not project_id:
            raise ValueError("Either issue_id or project_id is required")
        
        # Prepare time entry data
        time_entry_data = {
            "spent_on": spent_on,
            "hours": hours,
            "activity_id": activity_id
        }
        
        if issue_id:
            time_entry_data["issue_id"] = issue_id
        if project_id:
            time_entry_data["project_id"] = project_id
        
        # Optional fields
        comments = args.get("comments")
        if comments:
            time_entry_data["comments"] = comments
            
        custom_fields = args.get("custom_fields")
        if custom_fields:
            time_entry_data["custom_fields"] = custom_fields
        
        # Create time entry
        result = client.create_time_entry(time_entry_data)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"create_time_entry error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
