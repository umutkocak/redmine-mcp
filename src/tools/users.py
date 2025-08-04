"""
Redmine User Tool'ları - MCP ile

Bu modül Redmine kullanıcılar ile ilgili MCP tool'larını içerir:
- list_users: Kullanıcıları listeler
- get_user: Belirli bir kullanıcının detaylarını getirir
- get_current_user: Mevcut kullanıcının bilgilerini getirir
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

def create_list_users_tool() -> Tool:
    """list_users tool'unu oluşturur."""
    return Tool(
        name="list_users",
        description="Redmine kullanıcılarını listeler",
        inputSchema={
            "type": "object",
            "properties": {
                "status": {
                    "type": "number",
                    "description": "Kullanıcı durumu (1=aktif, 2=kayıtlı, 3=kilitli)"
                },
                "limit": {
                    "type": "number",
                    "description": "Döndürülecek maksimum kullanıcı sayısı (varsayılan: 25)",
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

def create_get_user_tool() -> Tool:
    """get_user tool'unu oluşturur.""" 
    return Tool(
        name="get_user",
        description="Belirli bir Redmine kullanıcısının detaylarını getirir",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": ["number", "string"],
                    "description": "Kullanıcı ID'si veya 'current' (mevcut kullanıcı)"
                }
            },
            "required": ["user_id"],
        },
    )

async def handle_list_users(client, args: Dict[str, Any]) -> List[TextContent]:
    """list_users tool handler'ı."""
    try:
        status = args.get("status")
        limit = args.get("limit", 25)
        offset = args.get("offset", 0)
        
        users = client.get_users(
            status=status,
            limit=limit,
            offset=offset
        )
        
        result = {
            "users": users,
            "total_count": len(users),
            "filters": {
                "status": status
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
        logger.error(f"list_users error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_get_user(client, args: Dict[str, Any]) -> List[TextContent]:
    """get_user tool handler'ı."""
    try:
        user_id = args.get("user_id")
        if not user_id:
            raise ValueError("user_id is required")
        
        user = client.get_user(user_id)
        
        if not user:
            return [TextContent(
                type="text",
                text=f"User with ID {user_id} not found"
            )]
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(user, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"get_user error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
