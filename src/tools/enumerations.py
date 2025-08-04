"""
Redmine Enumerations Tool'ları - MCP ile

Bu modül Redmine sistem sabitleri ile ilgili MCP tool'larını içerir:
- list_enumerations: Sistem sabitlerini listeler (durum, öncelik, tracker vs.)
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

def create_list_enumerations_tool() -> Tool:
    """list_enumerations tool'unu oluşturur."""
    return Tool(
        name="list_enumerations",
        description="Redmine sistem sabitlerini listeler (durumlar, öncelikler, tracker'lar vs.)",
        inputSchema={
            "type": "object",
            "properties": {
                "resource": {
                    "type": "string",
                    "description": "Sabit türü ('issue_statuses', 'issue_priorities', 'trackers', 'time_entry_activities')",
                    "enum": ["issue_statuses", "issue_priorities", "trackers", "time_entry_activities"]
                }
            },
            "required": [],
        },
    )

async def handle_list_enumerations(client, args: Dict[str, Any]) -> List[TextContent]:
    """list_enumerations tool handler'ı."""
    try:
        resource = args.get("resource")
        
        enumerations = client.get_enumerations(resource)
        
        result = {
            "enumerations": enumerations,
            "resource_type": resource or "all",
            "total_count": len(enumerations) if isinstance(enumerations, list) else len(enumerations.values()) if isinstance(enumerations, dict) else 0
        }
        
        import json
        return [TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )]
        
    except Exception as e:
        logger.error(f"list_enumerations error: {e}")
        return [TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
