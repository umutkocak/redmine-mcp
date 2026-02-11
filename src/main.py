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
from tools.projects import (
    create_list_projects_tool, create_get_project_tool,
    create_create_project_tool, create_update_project_tool,
    create_delete_project_tool, create_archive_project_tool, create_unarchive_project_tool,
    handle_list_projects, handle_get_project,
    handle_create_project, handle_update_project,
    handle_delete_project, handle_archive_project, handle_unarchive_project
)
from tools.issues import (
    create_list_issues_tool, create_get_issue_tool,
    create_create_issue_tool, create_update_issue_tool,
    create_delete_issue_tool, create_add_watcher_tool, create_remove_watcher_tool,
    handle_list_issues, handle_get_issue,
    handle_create_issue, handle_update_issue,
    handle_delete_issue, handle_add_watcher, handle_remove_watcher
)
from tools.users import (
    create_list_users_tool, create_get_user_tool,
    create_get_current_user_tool, create_create_user_tool,
    create_update_user_tool, create_delete_user_tool,
    handle_list_users, handle_get_user,
    handle_get_current_user, handle_create_user,
    handle_update_user, handle_delete_user
)
from tools.time_entries import (
    create_list_time_entries_tool, create_create_time_entry_tool,
    create_get_time_entry_tool, create_update_time_entry_tool, create_delete_time_entry_tool,
    handle_list_time_entries, handle_create_time_entry,
    handle_get_time_entry, handle_update_time_entry, handle_delete_time_entry
)
from tools.attachments import (
    create_upload_file_tool, create_get_attachment_tool, create_download_attachment_tool,
    handle_upload_file, handle_get_attachment, handle_download_attachment
)
from tools.enumerations import (
    create_list_enumerations_tool, create_list_trackers_tool,
    create_list_issue_statuses_tool, create_list_roles_tool,
    handle_list_enumerations, handle_list_trackers,
    handle_list_issue_statuses, handle_list_roles
)
from tools.issue_relations import (
    create_list_issue_relations_tool, create_create_issue_relation_tool,
    create_get_issue_relation_tool, create_delete_issue_relation_tool,
    handle_list_issue_relations, handle_create_issue_relation,
    handle_get_issue_relation, handle_delete_issue_relation
)
from tools.versions import (
    create_list_versions_tool, create_get_version_tool,
    create_create_version_tool, create_update_version_tool,
    create_delete_version_tool,
    handle_list_versions, handle_get_version,
    handle_create_version, handle_update_version,
    handle_delete_version
)
from tools.memberships import (
    create_list_memberships_tool, create_get_membership_tool,
    create_create_membership_tool, create_update_membership_tool,
    create_delete_membership_tool,
    handle_list_memberships, handle_get_membership,
    handle_create_membership, handle_update_membership,
    handle_delete_membership
)
from tools.issue_categories import (
    create_list_issue_categories_tool, create_get_issue_category_tool,
    create_create_issue_category_tool, create_update_issue_category_tool,
    create_delete_issue_category_tool,
    handle_list_issue_categories, handle_get_issue_category,
    handle_create_issue_category, handle_update_issue_category,
    handle_delete_issue_category
)

# Phase 3 imports
from tools.wiki_pages import (
    create_list_wiki_pages_tool, create_get_wiki_page_tool,
    create_create_or_update_wiki_page_tool, create_delete_wiki_page_tool,
    handle_list_wiki_pages, handle_get_wiki_page,
    handle_create_or_update_wiki_page, handle_delete_wiki_page
)
from tools.groups import (
    create_list_groups_tool, create_get_group_tool,
    create_create_group_tool, create_update_group_tool,
    create_delete_group_tool, create_add_user_to_group_tool,
    create_remove_user_from_group_tool,
    handle_list_groups, handle_get_group,
    handle_create_group, handle_update_group,
    handle_delete_group, handle_add_user_to_group,
    handle_remove_user_from_group
)
from tools.roles import (
    create_list_roles_detail_tool, create_get_role_tool,
    handle_list_roles_detail, handle_get_role
)
from tools.custom_fields import (
    create_list_custom_fields_tool,
    handle_list_custom_fields
)
from tools.journals import (
    create_list_issue_journals_tool, create_update_journal_tool,
    handle_list_issue_journals, handle_update_journal
)

# Phase 4 imports
from tools.news import (
    create_list_news_tool, create_get_news_tool,
    handle_list_news, handle_get_news
)
from tools.queries import (
    create_list_queries_tool,
    handle_list_queries
)
from tools.search import (
    create_search_tool,
    handle_search
)
from tools.files import (
    create_list_files_tool,
    handle_list_files
)
from tools.my_account import (
    create_get_my_account_tool, create_update_my_account_tool,
    handle_get_my_account, handle_update_my_account
)

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
        # Projects
        create_list_projects_tool(),
        create_get_project_tool(),
        create_create_project_tool(),
        create_update_project_tool(),
        create_delete_project_tool(),
        create_archive_project_tool(),
        create_unarchive_project_tool(),
        
        # Issues
        create_list_issues_tool(),
        create_get_issue_tool(),
        create_create_issue_tool(),
        create_update_issue_tool(),
        create_delete_issue_tool(),
        create_add_watcher_tool(),
        create_remove_watcher_tool(),
        
        # Users
        create_list_users_tool(),
        create_get_user_tool(),
        create_get_current_user_tool(),
        create_create_user_tool(),
        create_update_user_tool(),
        create_delete_user_tool(),
        
        # Time Entries
        create_list_time_entries_tool(),
        create_create_time_entry_tool(),
        create_get_time_entry_tool(),
        create_update_time_entry_tool(),
        create_delete_time_entry_tool(),
        
        # Attachments
        create_upload_file_tool(),
        create_get_attachment_tool(),
        create_download_attachment_tool(),
        
        # Enumerations
        create_list_enumerations_tool(),
        create_list_trackers_tool(),
        create_list_issue_statuses_tool(),
        create_list_roles_tool(),
        
        # Issue Relations
        create_list_issue_relations_tool(),
        create_create_issue_relation_tool(),
        create_get_issue_relation_tool(),
        create_delete_issue_relation_tool(),
        
        # Versions
        create_list_versions_tool(),
        create_get_version_tool(),
        create_create_version_tool(),
        create_update_version_tool(),
        create_delete_version_tool(),
        
        # Memberships
        create_list_memberships_tool(),
        create_get_membership_tool(),
        create_create_membership_tool(),
        create_update_membership_tool(),
        create_delete_membership_tool(),
        
        # Issue Categories
        create_list_issue_categories_tool(),
        create_get_issue_category_tool(),
        create_create_issue_category_tool(),
        create_update_issue_category_tool(),
        create_delete_issue_category_tool(),
        
        # Wiki Pages (Phase 3)
        create_list_wiki_pages_tool(),
        create_get_wiki_page_tool(),
        create_create_or_update_wiki_page_tool(),
        create_delete_wiki_page_tool(),
        
        # Groups (Phase 3)
        create_list_groups_tool(),
        create_get_group_tool(),
        create_create_group_tool(),
        create_update_group_tool(),
        create_delete_group_tool(),
        create_add_user_to_group_tool(),
        create_remove_user_from_group_tool(),
        
        # Roles Detail (Phase 3)
        create_list_roles_detail_tool(),
        create_get_role_tool(),
        
        # Custom Fields (Phase 3)
        create_list_custom_fields_tool(),
        
        # Journals (Phase 3)
        create_list_issue_journals_tool(),
        create_update_journal_tool(),
        
        # News (Phase 4)
        create_list_news_tool(),
        create_get_news_tool(),
        
        # Queries (Phase 4)
        create_list_queries_tool(),
        
        # Search (Phase 4)
        create_search_tool(),
        
        # Files (Phase 4)
        create_list_files_tool(),
        
        # My Account (Phase 4)
        create_get_my_account_tool(),
        create_update_my_account_tool(),
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Tool çağrılarını handle eder."""
    try:
        logger.info(f"Tool called: {name} with args: {arguments}")
        
        client = get_redmine_client()
        
        # Projects
        if name == "list_projects":
            return await handle_list_projects(client, arguments)
        elif name == "get_project":
            return await handle_get_project(client, arguments)
        elif name == "create_project":
            return await handle_create_project(client, arguments)
        elif name == "update_project":
            return await handle_update_project(client, arguments)
        elif name == "delete_project":
            return await handle_delete_project(client, arguments)
        elif name == "archive_project":
            return await handle_archive_project(client, arguments)
        elif name == "unarchive_project":
            return await handle_unarchive_project(client, arguments)
        
        # Issues
        elif name == "list_issues":
            return await handle_list_issues(client, arguments)
        elif name == "get_issue":
            return await handle_get_issue(client, arguments)
        elif name == "create_issue":
            return await handle_create_issue(client, arguments)
        elif name == "update_issue":
            return await handle_update_issue(client, arguments)
        elif name == "delete_issue":
            return await handle_delete_issue(client, arguments)
        elif name == "add_watcher":
            return await handle_add_watcher(client, arguments)
        elif name == "remove_watcher":
            return await handle_remove_watcher(client, arguments)
        
        # Users
        elif name == "list_users":
            return await handle_list_users(client, arguments)
        elif name == "get_user":
            return await handle_get_user(client, arguments)
        elif name == "get_current_user":
            return await handle_get_current_user(client, arguments)
        elif name == "create_user":
            return await handle_create_user(client, arguments)
        elif name == "update_user":
            return await handle_update_user(client, arguments)
        elif name == "delete_user":
            return await handle_delete_user(client, arguments)
        
        # Time Entries
        elif name == "list_time_entries":
            return await handle_list_time_entries(client, arguments)
        elif name == "create_time_entry":
            return await handle_create_time_entry(client, arguments)
        elif name == "get_time_entry":
            return await handle_get_time_entry(client, arguments)
        elif name == "update_time_entry":
            return await handle_update_time_entry(client, arguments)
        elif name == "delete_time_entry":
            return await handle_delete_time_entry(client, arguments)
        
        # Attachments
        elif name == "upload_file":
            return await handle_upload_file(client, arguments)
        elif name == "get_attachment":
            return await handle_get_attachment(client, arguments)
        elif name == "download_attachment":
            return await handle_download_attachment(client, arguments)
        
        # Enumerations
        elif name == "list_enumerations":
            return await handle_list_enumerations(client, arguments)
        elif name == "list_trackers":
            return await handle_list_trackers(client, arguments)
        elif name == "list_issue_statuses":
            return await handle_list_issue_statuses(client, arguments)
        elif name == "list_roles":
            return await handle_list_roles(client, arguments)
        
        # Issue Relations
        elif name == "list_issue_relations":
            return await handle_list_issue_relations(client, arguments)
        elif name == "create_issue_relation":
            return await handle_create_issue_relation(client, arguments)
        elif name == "get_issue_relation":
            return await handle_get_issue_relation(client, arguments)
        elif name == "delete_issue_relation":
            return await handle_delete_issue_relation(client, arguments)
        
        # Versions
        elif name == "list_versions":
            return await handle_list_versions(client, arguments)
        elif name == "get_version":
            return await handle_get_version(client, arguments)
        elif name == "create_version":
            return await handle_create_version(client, arguments)
        elif name == "update_version":
            return await handle_update_version(client, arguments)
        elif name == "delete_version":
            return await handle_delete_version(client, arguments)
        
        # Memberships
        elif name == "list_memberships":
            return await handle_list_memberships(client, arguments)
        elif name == "get_membership":
            return await handle_get_membership(client, arguments)
        elif name == "create_membership":
            return await handle_create_membership(client, arguments)
        elif name == "update_membership":
            return await handle_update_membership(client, arguments)
        elif name == "delete_membership":
            return await handle_delete_membership(client, arguments)
        
        # Issue Categories
        elif name == "list_issue_categories":
            return await handle_list_issue_categories(client, arguments)
        elif name == "get_issue_category":
            return await handle_get_issue_category(client, arguments)
        elif name == "create_issue_category":
            return await handle_create_issue_category(client, arguments)
        elif name == "update_issue_category":
            return await handle_update_issue_category(client, arguments)
        elif name == "delete_issue_category":
            return await handle_delete_issue_category(client, arguments)
        
        # Wiki Pages (Phase 3)
        elif name == "list_wiki_pages":
            return await handle_list_wiki_pages(client, arguments)
        elif name == "get_wiki_page":
            return await handle_get_wiki_page(client, arguments)
        elif name == "create_or_update_wiki_page":
            return await handle_create_or_update_wiki_page(client, arguments)
        elif name == "delete_wiki_page":
            return await handle_delete_wiki_page(client, arguments)
        
        # Groups (Phase 3)
        elif name == "list_groups":
            return await handle_list_groups(client, arguments)
        elif name == "get_group":
            return await handle_get_group(client, arguments)
        elif name == "create_group":
            return await handle_create_group(client, arguments)
        elif name == "update_group":
            return await handle_update_group(client, arguments)
        elif name == "delete_group":
            return await handle_delete_group(client, arguments)
        elif name == "add_user_to_group":
            return await handle_add_user_to_group(client, arguments)
        elif name == "remove_user_from_group":
            return await handle_remove_user_from_group(client, arguments)
        
        # Roles Detail (Phase 3)
        elif name == "list_roles_detail":
            return await handle_list_roles_detail(client, arguments)
        elif name == "get_role":
            return await handle_get_role(client, arguments)
        
        # Custom Fields (Phase 3)
        elif name == "list_custom_fields":
            return await handle_list_custom_fields(client, arguments)
        
        # Journals (Phase 3)
        elif name == "list_issue_journals":
            return await handle_list_issue_journals(client, arguments)
        elif name == "update_journal":
            return await handle_update_journal(client, arguments)
        
        # News (Phase 4)
        elif name == "list_news":
            return await handle_list_news(client, arguments)
        elif name == "get_news":
            return await handle_get_news(client, arguments)
        
        # Queries (Phase 4)
        elif name == "list_queries":
            return await handle_list_queries(client, arguments)
        
        # Search (Phase 4)
        elif name == "search":
            return await handle_search(client, arguments)
        
        # Files (Phase 4)
        elif name == "list_files":
            return await handle_list_files(client, arguments)
        
        # My Account (Phase 4)
        elif name == "get_my_account":
            return await handle_get_my_account(client, arguments)
        elif name == "update_my_account":
            return await handle_update_my_account(client, arguments)
        
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
