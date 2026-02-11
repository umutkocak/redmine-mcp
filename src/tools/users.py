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

def create_get_current_user_tool() -> Tool:
    """get_current_user tool'unu oluşturur."""
    return Tool(
        name="get_current_user",
        description="Mevcut kullanıcının (API key sahibi) bilgilerini getirir",
        inputSchema={
            "type": "object",
            "properties": {},
            "required": [],
        },
    )

def create_create_user_tool() -> Tool:
    """create_user tool'unu oluşturur."""
    return Tool(
        name="create_user",
        description="Yeni Redmine kullanıcısı oluşturur (Admin yetkisi gerekli)",
        inputSchema={
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "description": "Kullanıcı verisi",
                    "properties": {
                        "login": {
                            "type": "string",
                            "description": "Kullanıcı adı (ZORUNLU)"
                        },
                        "firstname": {
                            "type": "string",
                            "description": "Ad (ZORUNLU)"
                        },
                        "lastname": {
                            "type": "string",
                            "description": "Soyad (ZORUNLU)"
                        },
                        "mail": {
                            "type": "string",
                            "description": "E-posta (ZORUNLU)"
                        },
                        "password": {
                            "type": "string",
                            "description": "Şifre"
                        },
                        "generate_password": {
                            "type": "boolean",
                            "description": "Otomatik şifre oluştur"
                        },
                        "must_change_passwd": {
                            "type": "boolean",
                            "description": "İlk girişte şifre değiştirme zorunlu mu?"
                        },
                        "admin": {
                            "type": "boolean",
                            "description": "Admin yetkisi ver"
                        }
                    },
                    "required": ["login", "firstname", "lastname", "mail"]
                }
            },
            "required": ["user"],
        },
    )

def create_update_user_tool() -> Tool:
    """update_user tool'unu oluşturur."""
    return Tool(
        name="update_user",
        description="Mevcut Redmine kullanıcısını günceller (Admin yetkisi gerekli)",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "number",
                    "description": "Kullanıcı ID'si"
                },
                "user": {
                    "type": "object",
                    "description": "Güncellenecek kullanıcı verisi",
                    "properties": {
                        "firstname": {
                            "type": "string",
                            "description": "Yeni ad"
                        },
                        "lastname": {
                            "type": "string",
                            "description": "Yeni soyad"
                        },
                        "mail": {
                            "type": "string",
                            "description": "Yeni e-posta"
                        },
                        "password": {
                            "type": "string",
                            "description": "Yeni şifre"
                        },
                        "admin": {
                            "type": "boolean",
                            "description": "Admin yetkisi"
                        }
                    }
                }
            },
            "required": ["user_id", "user"],
        },
    )

def create_delete_user_tool() -> Tool:
    """delete_user tool'unu oluşturur."""
    return Tool(
        name="delete_user",
        description="Redmine kullanıcısını siler (Admin yetkisi gerekli)",
        inputSchema={
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "number",
                    "description": "Silinecek kullanıcı ID'si"
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

async def handle_get_current_user(client, args: Dict[str, Any]) -> List[TextContent]:
    """get_current_user tool handler'ı."""
    try:
        user = client.get_current_user()
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(user, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"get_current_user error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_create_user(client, args: Dict[str, Any]) -> List[TextContent]:
    """create_user tool handler'ı."""
    try:
        user_data = args.get("user")
        if not user_data:
            raise ValueError("Missing 'user' wrapper in request")
        
        required_fields = ["login", "firstname", "lastname", "mail"]
        for field in required_fields:
            if not user_data.get(field):
                raise ValueError(f"'{field}' is required")
        
        result = client.create_user(user_data)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"create_user error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_update_user(client, args: Dict[str, Any]) -> List[TextContent]:
    """update_user tool handler'ı."""
    try:
        user_id = args.get("user_id")
        if not user_id:
            raise ValueError("user_id is required")
        
        user_data = args.get("user")
        if not user_data:
            raise ValueError("Missing 'user' wrapper in request")
        
        result = client.update_user(user_id, user_data)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result or {"status": "updated"}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"update_user error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_delete_user(client, args: Dict[str, Any]) -> List[TextContent]:
    """delete_user tool handler'ı."""
    try:
        user_id = args.get("user_id")
        if not user_id:
            raise ValueError("user_id is required")
        
        result = client.delete_user(user_id)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps({"status": "deleted", "user_id": user_id}, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"delete_user error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
