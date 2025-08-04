#!/usr/bin/env python3
"""
Redmine MCP Server - Standart MCP tabanlı server
Bu server Redmine API'yi MCP araçları olarak sunar.
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Src klasörünü path'e ekle
src_path = Path(__file__).parent
sys.path.insert(0, str(src_path))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent
import mcp

# Version import
from version import __version__, print_version_info
from dotenv import load_dotenv
from dotenv import load_dotenv

from redmine_client import RedmineClient
from tools.projects import create_list_projects_tool, create_get_project_tool, handle_list_projects, handle_get_project
from tools.issues import create_list_issues_tool, create_get_issue_tool, create_create_issue_tool, create_update_issue_tool, handle_list_issues, handle_get_issue, handle_create_issue, handle_update_issue
from tools.users import create_list_users_tool, create_get_user_tool, handle_list_users, handle_get_user
from tools.time_entries import create_list_time_entries_tool, handle_list_time_entries
from tools.enumerations import create_list_enumerations_tool, handle_list_enumerations

# Environment değişkenlerini yükle
load_dotenv()

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Global Redmine client instance
redmine_client: Optional[RedmineClient] = None

def get_redmine_client() -> RedmineClient:
    """Global Redmine client instance'ı döndürür."""
    global redmine_client
    if redmine_client is None:
        base_url = os.getenv("REDMINE_URL")
        api_key = os.getenv("REDMINE_API_KEY")
        
        if not base_url or not api_key:
            raise ValueError(
                "REDMINE_URL ve REDMINE_API_KEY environment değişkenleri gerekli. "
                ".env dosyasını kontrol edin."
            )
            
        redmine_client = RedmineClient(base_url, api_key)
        logger.info(f"Redmine client initialized for {base_url}")
    
    return redmine_client

# MCP Server instance
server = Server(f"redmine-mcp-v{__version__}")

# Version bilgisini log'la
logger.info(f"🚀 Starting Redmine MCP Server v{__version__}")
logger.info(f"📋 Server name: redmine-mcp-v{__version__}")

# MCP version check - mcp paketinde __version__ attribute'u olmayabilir
try:
    mcp_version = getattr(mcp, '__version__', 'Unknown')
    logger.info(f"🔧 MCP Standard Library: {mcp_version}")
except Exception:
    logger.info("🔧 MCP Standard Library: Available")

@server.list_tools()
async def handle_list_tools() -> List:
    """MCP server'da mevcut tool'ları listeler."""
    return [
        create_list_projects_tool(),
        create_get_project_tool(),
        create_list_issues_tool(),
        create_get_issue_tool(),
        create_create_issue_tool(),
        create_update_issue_tool(),
        create_list_users_tool(),
        create_get_user_tool(),
        create_list_time_entries_tool(),
        create_list_enumerations_tool(),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Tool çağrılarını handle eder."""
    try:
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        client = get_redmine_client()
        
        if name == "list_projects":
            return await handle_list_projects(client, arguments)
        elif name == "get_project":
            return await handle_get_project(client, arguments)
        elif name == "list_issues":
            return await handle_list_issues(client, arguments)
        elif name == "get_issue":
            return await handle_get_issue(client, arguments)
        elif name == "create_issue":
            return await handle_create_issue(client, arguments)
        elif name == "update_issue":
            return await handle_update_issue(client, arguments)
        elif name == "list_users":
            return await handle_list_users(client, arguments)
        elif name == "get_user":
            return await handle_get_user(client, arguments)
        elif name == "list_time_entries":
            return await handle_list_time_entries(client, arguments)
        elif name == "list_enumerations":
            return await handle_list_enumerations(client, arguments)
        else:
            logger.error(f"Unknown tool: {name}")
            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]
            
    except Exception as e:
        logger.error(f"Tool execution error: {e}")
        return [
            TextContent(
                type="text",
                text=f"Error executing tool '{name}': {str(e)}",
            )
        ]

async def main():
    """Ana server fonksiyonu."""
    try:
        # Version bilgisini yazdır
        print_version_info()
        print("=" * 50)
        
        # Environment değişkenlerini kontrol et
        required_vars = ["REDMINE_URL", "REDMINE_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        
        if missing_vars:
            logger.error(f"Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("Please create a .env file with the required variables.")
            return
        
        logger.info("Starting Redmine MCP Server...")
        
        async with stdio_server() as (read_stream, write_stream):
            await server.run(
                read_stream,
                write_stream,
                server.create_initialization_options(),
            )
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())
