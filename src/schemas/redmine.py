"""
JSON Schema tanımları - MCP tool schema'ları.

Bu modül MCP tool'ları için JSON Schema tanımlarını içerir.
Her tool'un input parametreleri için schema sağlar.
"""

from typing import Any, Dict, List

# Ortak parametreler
LIMIT_PARAM = {
    "type": "integer",
    "description": "Döndürülecek maksimum kayıt sayısı (varsayılan: 25, maksimum: 100)",
    "minimum": 1,
    "maximum": 100,
    "default": 25
}

OFFSET_PARAM = {
    "type": "integer", 
    "description": "Kaç kaydın atlanacağı (pagination için)",
    "minimum": 0,
    "default": 0
}

PROJECT_ID_PARAM = {
    "type": ["integer", "string"],
    "description": "Proje ID'si (sayı) veya proje identifier (string)"
}

USER_ID_PARAM = {
    "type": ["integer", "string"],
    "description": "Kullanıcı ID'si (sayı) veya 'me' (mevcut kullanıcı)"
}

ISSUE_ID_PARAM = {
    "type": "integer",
    "description": "Issue ID'si",
    "minimum": 1
}

INCLUDE_PARAM = {
    "type": "array",
    "description": "İlişkili verileri dahil etmek için liste",
    "items": {"type": "string"}
}

# Project Schemas
LIST_PROJECTS_SCHEMA = {
    "type": "object",
    "properties": {
        "limit": LIMIT_PARAM,
        "offset": OFFSET_PARAM,
        "include": {
            **INCLUDE_PARAM,
            "description": "İlişkili verileri dahil et (trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)"
        }
    },
    "additionalProperties": False
}

GET_PROJECT_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": {
            **PROJECT_ID_PARAM,
            "description": "Getirilecek proje ID'si veya identifier"
        },
        "include": {
            **INCLUDE_PARAM,
            "description": "İlişkili verileri dahil et (trackers, issue_categories, enabled_modules, time_entry_activities, issue_custom_fields)"
        }
    },
    "required": ["project_id"],
    "additionalProperties": False
}

# Issue Schemas
LIST_ISSUES_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": PROJECT_ID_PARAM,
        "assigned_to_id": {
            **USER_ID_PARAM,
            "description": "Atanan kullanıcı ID'si ('me' mevcut kullanıcı için)"
        },
        "status_id": {
            "type": ["integer", "string"],
            "description": "Durum ID'si (sayı) veya 'open'/'closed' (string)"
        },
        "tracker_id": {
            "type": "integer",
            "description": "Tracker (issue türü) ID'si",
            "minimum": 1
        },
        "priority_id": {
            "type": "integer",
            "description": "Öncelik ID'si",
            "minimum": 1
        },
        "category_id": {
            "type": "integer",
            "description": "Kategori ID'si",
            "minimum": 1
        },
        "fixed_version_id": {
            "type": "integer",
            "description": "Hedef versiyon ID'si",
            "minimum": 1
        },
        "subject": {
            "type": "string",
            "description": "Başlık içinde arama (kısmi eşleşme)"
        },
        "description": {
            "type": "string",
            "description": "Açıklama içinde arama (kısmi eşleşme)"
        },
        "created_on": {
            "type": "string",
            "description": "Oluşturma tarihi filtresi (YYYY-MM-DD veya ><YYYY-MM-DD)",
            "pattern": r"^(>=?|<=?)?\\d{4}-\\d{2}-\\d{2}$"
        },
        "updated_on": {
            "type": "string",
            "description": "Güncelleme tarihi filtresi (YYYY-MM-DD veya ><YYYY-MM-DD)",
            "pattern": r"^(>=?|<=?)?\\d{4}-\\d{2}-\\d{2}$"
        },
        "sort": {
            "type": "string",
            "description": "Sıralama (id, project, tracker, status, priority, subject, author, assigned_to, updated_on, category, fixed_version, created_on)",
            "enum": ["id", "project", "tracker", "status", "priority", "subject", "author", "assigned_to", "updated_on", "category", "fixed_version", "created_on"]
        },
        "limit": LIMIT_PARAM,
        "offset": OFFSET_PARAM,
        "include": {
            **INCLUDE_PARAM,
            "description": "İlişkili verileri dahil et (children, attachments, relations, changesets, journals, watchers)"
        }
    },
    "additionalProperties": False
}

GET_ISSUE_SCHEMA = {
    "type": "object",
    "properties": {
        "issue_id": {
            **ISSUE_ID_PARAM,
            "description": "Getirilecek issue ID'si"
        },
        "include": {
            **INCLUDE_PARAM,
            "description": "İlişkili verileri dahil et (children, attachments, relations, changesets, journals, watchers)"
        }
    },
    "required": ["issue_id"],
    "additionalProperties": False
}

CREATE_ISSUE_SCHEMA = {
    "type": "object",
    "properties": {
        "project_id": {
            **PROJECT_ID_PARAM,
            "description": "Issue'nin ait olacağı proje ID'si (gerekli)"
        },
        "tracker_id": {
            "type": "integer",
            "description": "Tracker (issue türü) ID'si (gerekli)",
            "minimum": 1
        },
        "status_id": {
            "type": "integer",
            "description": "Durum ID'si (opsiyonel, varsayılan: yeni)",
            "minimum": 1
        },
        "priority_id": {
            "type": "integer",
            "description": "Öncelik ID'si (opsiyonel, varsayılan: normal)",
            "minimum": 1
        },
        "subject": {
            "type": "string",
            "description": "Issue başlığı (gerekli)",
            "minLength": 1,
            "maxLength": 255
        },
        "description": {
            "type": "string",
            "description": "Issue açıklaması (opsiyonel)"
        },
        "category_id": {
            "type": "integer",
            "description": "Kategori ID'si (opsiyonel)",
            "minimum": 1
        },
        "fixed_version_id": {
            "type": "integer",
            "description": "Hedef versiyon ID'si (opsiyonel)",
            "minimum": 1
        },
        "assigned_to_id": {
            "type": "integer",
            "description": "Atanacak kullanıcı ID'si (opsiyonel)",
            "minimum": 1
        },
        "parent_issue_id": {
            "type": "integer",
            "description": "Üst issue ID'si (alt görev için)",
            "minimum": 1
        },
        "is_private": {
            "type": "boolean",
            "description": "Issue'yu özel yap (varsayılan: false)"
        },
        "estimated_hours": {
            "type": "number",
            "description": "Tahmini süre (saat)",
            "minimum": 0
        },
        "start_date": {
            "type": "string",
            "description": "Başlangıç tarihi (YYYY-MM-DD)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "due_date": {
            "type": "string",
            "description": "Bitiş tarihi (YYYY-MM-DD)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "done_ratio": {
            "type": "integer",
            "description": "Tamamlanma yüzdesi (0-100)",
            "minimum": 0,
            "maximum": 100
        },
        "custom_fields": {
            "type": "array",
            "description": "Özel alanlar",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "value": {}
                },
                "required": ["id", "value"]
            }
        },
        "watcher_user_ids": {
            "type": "array",
            "description": "Takip edecek kullanıcı ID'leri",
            "items": {"type": "integer", "minimum": 1}
        }
    },
    "required": ["project_id", "tracker_id", "subject"],
    "additionalProperties": False
}

UPDATE_ISSUE_SCHEMA = {
    "type": "object",
    "properties": {
        "issue_id": {
            **ISSUE_ID_PARAM,
            "description": "Güncellenecek issue ID'si (gerekli)"
        },
        **{k: v for k, v in CREATE_ISSUE_SCHEMA["properties"].items() 
           if k not in ["project_id", "tracker_id", "subject"]},  # Gerekli alanları opsiyonel yap
        "project_id": {
            **PROJECT_ID_PARAM,
            "description": "Issue'nin ait olacağı proje ID'si (opsiyonel)"
        },
        "tracker_id": {
            "type": "integer",
            "description": "Tracker (issue türü) ID'si (opsiyonel)",
            "minimum": 1
        },
        "subject": {
            "type": "string",
            "description": "Issue başlığı (opsiyonel)",
            "minLength": 1,
            "maxLength": 255
        },
        "notes": {
            "type": "string",
            "description": "Güncelleme notu/yorumu (opsiyonel)"
        },
        "private_notes": {
            "type": "boolean",
            "description": "Notları özel yap (varsayılan: false)"
        }
    },
    "required": ["issue_id"],
    "additionalProperties": False
}

# User Schemas
LIST_USERS_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {
            "type": "integer",
            "description": "Kullanıcı durumu (1: aktif, 2: kayıtlı, 3: kilitli)",
            "enum": [1, 2, 3]
        },
        "name": {
            "type": "string",
            "description": "İsim veya email adresi arama"
        },
        "group_id": {
            "type": "integer",
            "description": "Grup ID'si",
            "minimum": 1
        },
        "limit": LIMIT_PARAM,
        "offset": OFFSET_PARAM
    },
    "additionalProperties": False
}

GET_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            **USER_ID_PARAM,
            "description": "Getirilecek kullanıcı ID'si veya 'me'"
        },
        "include": {
            **INCLUDE_PARAM,
            "description": "İlişkili verileri dahil et (memberships, groups)"
        }
    },
    "required": ["user_id"],
    "additionalProperties": False
}

# Time Entry Schemas
LIST_TIME_ENTRIES_SCHEMA = {
    "type": "object",
    "properties": {
        "user_id": {
            **USER_ID_PARAM,
            "description": "Kullanıcı ID'si ('me' mevcut kullanıcı için)"
        },
        "project_id": PROJECT_ID_PARAM,
        "issue_id": ISSUE_ID_PARAM,
        "activity_id": {
            "type": "integer",
            "description": "Aktivite ID'si",
            "minimum": 1
        },
        "spent_on": {
            "type": "string",
            "description": "Harcanan tarih (YYYY-MM-DD)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "from": {
            "type": "string",
            "description": "Başlangıç tarihi (YYYY-MM-DD)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "to": {
            "type": "string",
            "description": "Bitiş tarihi (YYYY-MM-DD)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "limit": LIMIT_PARAM,
        "offset": OFFSET_PARAM
    },
    "additionalProperties": False
}

CREATE_TIME_ENTRY_SCHEMA = {
    "type": "object",
    "properties": {
        "issue_id": {
            **ISSUE_ID_PARAM,
            "description": "Issue ID'si (issue_id veya project_id gerekli)"
        },
        "project_id": {
            **PROJECT_ID_PARAM,
            "description": "Proje ID'si (issue_id veya project_id gerekli)"
        },
        "spent_on": {
            "type": "string",
            "description": "Harcanan tarih (YYYY-MM-DD) (gerekli)",
            "pattern": r"^\\d{4}-\\d{2}-\\d{2}$"
        },
        "hours": {
            "type": "number",
            "description": "Harcanan saat (gerekli)",
            "minimum": 0.01
        },
        "activity_id": {
            "type": "integer",
            "description": "Aktivite ID'si (gerekli)",
            "minimum": 1
        },
        "comments": {
            "type": "string",
            "description": "Açıklama/yorum (opsiyonel)"
        },
        "custom_fields": {
            "type": "array",
            "description": "Özel alanlar",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "value": {}
                },
                "required": ["id", "value"]
            }
        }
    },
    "required": ["spent_on", "hours", "activity_id"],
    "additionalProperties": False,
    "anyOf": [
        {"required": ["issue_id"]},
        {"required": ["project_id"]}
    ]
}

# Enumeration Schemas
LIST_ENUMERATIONS_SCHEMA = {
    "type": "object",
    "properties": {
        "resource": {
            "type": "string",
            "description": "Enumeration türü (opsiyonel, boş ise tümü)",
            "enum": [
                "time_entry_activities",
                "issue_priorities", 
                "document_categories"
            ]
        }
    },
    "additionalProperties": False
}

# Ortak şemalar
REDMINE_DATE_PATTERN = r"^\\d{4}-\\d{2}-\\d{2}$"
REDMINE_DATETIME_PATTERN = r"^\\d{4}-\\d{2}-\\d{2}T\\d{2}:\\d{2}:\\d{2}Z$"

# Tool tanımları için yardımcı fonksiyonlar
def create_tool_schema(name: str, description: str, schema: Dict[str, Any]) -> Dict[str, Any]:
    """MCP tool için standart schema oluşturur."""
    return {
        "name": name,
        "description": description,
        "inputSchema": schema
    }
