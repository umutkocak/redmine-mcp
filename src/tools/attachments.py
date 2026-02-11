"""
Redmine Attachment Tool'ları - MCP ile

Bu modül Redmine dosya ekleri ile ilgili MCP tool'larını içerir:
- upload_file: Dosya yükler ve token döner
- get_attachment: Ek bilgisini getirir
- download_attachment: Ek dosyasını indirir

NOT: Redmine'da dosya yükleme iki aşamalıdır:
1. POST /uploads.json (binary, Content-Type: application/octet-stream) -> token
2. Issue/Wiki create/update'de token kullan
"""

import logging
import sys
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional
from mcp.types import Tool, TextContent

# Parent klasörü path'e ekle
parent_path = Path(__file__).parent.parent
sys.path.insert(0, str(parent_path))

logger = logging.getLogger(__name__)

def create_upload_file_tool() -> Tool:
    """upload_file tool'unu oluşturur."""
    return Tool(
        name="upload_file",
        description="Redmine'a dosya yükler ve upload token döner. Token'ı issue/wiki'ye eklemek için kullanın.",
        inputSchema={
            "type": "object",
            "properties": {
                "file_content": {
                    "type": "string",
                    "description": "Dosya içeriği (base64 encoded veya text)"
                },
                "filename": {
                    "type": "string",
                    "description": "Dosya adı (UTF-8 karakterler desteklenir: örn. 'döküman.pdf')"
                },
                "content_type": {
                    "type": "string",
                    "description": "MIME type (örn: 'application/pdf', 'image/png')",
                    "default": "application/octet-stream"
                },
                "description": {
                    "type": "string",
                    "description": "Dosya açıklaması (opsiyonel)"
                }
            },
            "required": ["file_content", "filename"],
        },
    )

def create_get_attachment_tool() -> Tool:
    """get_attachment tool'unu oluşturur."""
    return Tool(
        name="get_attachment",
        description="Ek dosyanın bilgilerini getirir (metadata)",
        inputSchema={
            "type": "object",
            "properties": {
                "attachment_id": {
                    "type": "number",
                    "description": "Ek ID'si"
                }
            },
            "required": ["attachment_id"],
        },
    )

def create_download_attachment_tool() -> Tool:
    """download_attachment tool'unu oluşturur."""
    return Tool(
        name="download_attachment",
        description="Ek dosyasını indirir (content'i base64 encoded olarak döner)",
        inputSchema={
            "type": "object",
            "properties": {
                "attachment_id": {
                    "type": "number",
                    "description": "İndirilecek ek ID'si"
                }
            },
            "required": ["attachment_id"],
        },
    )

async def handle_upload_file(client, args: Dict[str, Any]) -> List[TextContent]:
    """upload_file tool handler'ı."""
    try:
        file_content = args.get("file_content")
        filename = args.get("filename")
        content_type = args.get("content_type", "application/octet-stream")
        description = args.get("description", "")
        
        if not file_content:
            raise ValueError("file_content is required")
        if not filename:
            raise ValueError("filename is required")
        
        # Base64 decode if needed
        try:
            # Try to decode as base64
            file_data = base64.b64decode(file_content)
        except Exception:
            # If not base64, treat as text
            file_data = file_content.encode('utf-8')
        
        # Upload file
        token = client.upload_file(file_data, filename)
        
        result = {
            "status": "uploaded",
            "token": token,
            "filename": filename,
            "content_type": content_type,
            "description": description,
            "usage": {
                "message": "Use this token when creating/updating issue or wiki",
                "example_issue": {
                    "issue": {
                        "project_id": 1,
                        "subject": "Issue with attachment",
                        "uploads": [
                            {
                                "token": token,
                                "filename": filename,
                                "content_type": content_type,
                                "description": description
                            }
                        ]
                    }
                }
            }
        }
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"upload_file error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_get_attachment(client, args: Dict[str, Any]) -> List[TextContent]:
    """get_attachment tool handler'ı."""
    try:
        attachment_id = args.get("attachment_id")
        if not attachment_id:
            raise ValueError("attachment_id is required")
        
        result = client.get_attachment(attachment_id)
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"get_attachment error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]

async def handle_download_attachment(client, args: Dict[str, Any]) -> List[TextContent]:
    """download_attachment tool handler'ı."""
    try:
        attachment_id = args.get("attachment_id")
        if not attachment_id:
            raise ValueError("attachment_id is required")
        
        # Get attachment metadata first
        attachment_info = client.get_attachment(attachment_id)
        
        # Download content
        content = client.download_attachment(attachment_id)
        
        # Encode as base64 for transport
        content_base64 = base64.b64encode(content).decode('utf-8')
        
        result = {
            "attachment_info": attachment_info,
            "content_base64": content_base64,
            "note": "Decode content_base64 to get original file content"
        }
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"download_attachment error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
