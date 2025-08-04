"""
Redmine veri tipleri - Tüm Redmine veri tipleri (dataclasses/pydantic).

Bu modül Redmine API'den gelen verilerin Python type definitions'larını içerir.
Pydantic BaseModel kullanarak validation ve serialization sağlar.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field, validator


class RedmineUser(BaseModel):
    """Redmine kullanıcı modeli."""
    id: int
    login: str
    firstname: str
    lastname: str
    mail: str
    created_on: str
    last_login_on: Optional[str] = None
    status: Optional[int] = None
    
    @property
    def full_name(self) -> str:
        """Kullanıcının tam adını döndürür."""
        return f"{self.firstname} {self.lastname}"


class RedmineProject(BaseModel):
    """Redmine proje modeli."""
    id: int
    name: str
    identifier: str
    description: Optional[str] = None
    homepage: Optional[str] = None
    status: int
    is_public: bool
    inherit_members: Optional[bool] = None
    created_on: str
    updated_on: str
    parent: Optional[Dict[str, Any]] = None
    
    # İlişkili veriler (include parametresi ile gelir)
    trackers: Optional[List[Dict[str, Any]]] = None
    issue_categories: Optional[List[Dict[str, Any]]] = None
    enabled_modules: Optional[List[Dict[str, Any]]] = None
    time_entry_activities: Optional[List[Dict[str, Any]]] = None
    issue_custom_fields: Optional[List[Dict[str, Any]]] = None


class RedmineTracker(BaseModel):
    """Redmine tracker (issue türü) modeli."""
    id: int
    name: str
    default_status: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    position: Optional[int] = None


class RedmineStatus(BaseModel):
    """Redmine issue durumu modeli."""
    id: int
    name: str
    is_closed: bool
    position: Optional[int] = None


class RedminePriority(BaseModel):
    """Redmine öncelik modeli."""
    id: int
    name: str
    is_default: Optional[bool] = None
    position: Optional[int] = None


class RedmineCategory(BaseModel):
    """Redmine kategori modeli."""
    id: int
    name: str
    project: Optional[Dict[str, Any]] = None
    assigned_to: Optional[Dict[str, Any]] = None


class RedmineVersion(BaseModel):
    """Redmine versiyon modeli."""
    id: int
    name: str
    description: Optional[str] = None
    status: str
    due_date: Optional[str] = None
    sharing: Optional[str] = None
    wiki_page_title: Optional[str] = None
    created_on: str
    updated_on: str


class RedmineCustomField(BaseModel):
    """Redmine özel alan modeli."""
    id: int
    name: str
    value: Any
    multiple: Optional[bool] = None


class RedmineJournal(BaseModel):
    """Redmine issue günlük kaydı (comment/change) modeli."""
    id: int
    user: Dict[str, Any]
    notes: Optional[str] = None
    created_on: str
    private_notes: Optional[bool] = None
    details: Optional[List[Dict[str, Any]]] = None


class RedmineAttachment(BaseModel):
    """Redmine dosya eki modeli."""
    id: int
    filename: str
    filesize: int
    content_type: str
    description: Optional[str] = None
    content_url: str
    thumbnail_url: Optional[str] = None
    author: Dict[str, Any]
    created_on: str


class RedmineIssue(BaseModel):
    """Redmine issue modeli."""
    id: int
    project: Dict[str, Any]
    tracker: Dict[str, Any]
    status: Dict[str, Any]
    priority: Dict[str, Any]
    author: Dict[str, Any]
    subject: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    done_ratio: int = 0
    is_private: bool = False
    estimated_hours: Optional[float] = None
    total_estimated_hours: Optional[float] = None
    spent_hours: Optional[float] = None
    total_spent_hours: Optional[float] = None
    created_on: str
    updated_on: str
    closed_on: Optional[str] = None
    
    # İsteğe bağlı alanlar
    assigned_to: Optional[Dict[str, Any]] = None
    category: Optional[Dict[str, Any]] = None
    fixed_version: Optional[Dict[str, Any]] = None
    parent: Optional[Dict[str, Any]] = None
    custom_fields: Optional[List[RedmineCustomField]] = None
    
    # İlişkili veriler (include parametresi ile gelir)
    children: Optional[List[Dict[str, Any]]] = None
    attachments: Optional[List[RedmineAttachment]] = None
    relations: Optional[List[Dict[str, Any]]] = None
    changesets: Optional[List[Dict[str, Any]]] = None
    journals: Optional[List[RedmineJournal]] = None
    watchers: Optional[List[Dict[str, Any]]] = None


class RedmineTimeEntry(BaseModel):
    """Redmine zaman kaydı modeli."""
    id: int
    project: Dict[str, Any]
    user: Dict[str, Any]
    activity: Dict[str, Any]
    hours: float
    comments: Optional[str] = None
    spent_on: str
    created_on: str
    updated_on: str
    
    # İsteğe bağlı alanlar
    issue: Optional[Dict[str, Any]] = None
    custom_fields: Optional[List[RedmineCustomField]] = None


class RedmineActivity(BaseModel):
    """Redmine zaman kaydı aktivitesi modeli."""
    id: int
    name: str
    is_default: Optional[bool] = None
    position: Optional[int] = None


class RedmineEnumeration(BaseModel):
    """Redmine enumeration (sistem sabiti) modeli."""
    id: int
    name: str
    is_default: Optional[bool] = None
    position: Optional[int] = None
    active: Optional[bool] = None


# API Response wrappers
class RedmineListResponse(BaseModel):
    """Redmine liste API response'u için genel model."""
    total_count: int
    offset: int
    limit: int


class RedmineProjectsResponse(RedmineListResponse):
    """Redmine projeler listesi API response'u."""
    projects: List[RedmineProject]


class RedmineIssuesResponse(RedmineListResponse):
    """Redmine issue'lar listesi API response'u."""
    issues: List[RedmineIssue]


class RedmineUsersResponse(RedmineListResponse):
    """Redmine kullanıcılar listesi API response'u."""
    users: List[RedmineUser]


class RedmineTimeEntriesResponse(RedmineListResponse):
    """Redmine zaman kayıtları listesi API response'u."""
    time_entries: List[RedmineTimeEntry]


class RedmineEnumerationsResponse(BaseModel):
    """Redmine enumerations API response'u."""
    time_entry_activities: Optional[List[RedmineActivity]] = None
    issue_priorities: Optional[List[RedminePriority]] = None
    document_categories: Optional[List[RedmineEnumeration]] = None


# Single item response wrappers
class RedmineProjectResponse(BaseModel):
    """Tek proje API response'u."""
    project: RedmineProject


class RedmineIssueResponse(BaseModel):
    """Tek issue API response'u."""
    issue: RedmineIssue


class RedmineUserResponse(BaseModel):
    """Tek kullanıcı API response'u."""
    user: RedmineUser


class RedmineTimeEntryResponse(BaseModel):
    """Tek zaman kaydı API response'u."""
    time_entry: RedmineTimeEntry


# Issue creation/update payloads
class RedmineIssueCreate(BaseModel):
    """Issue oluşturma için payload modeli."""
    project_id: int
    tracker_id: int
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    subject: str
    description: Optional[str] = None
    category_id: Optional[int] = None
    fixed_version_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    parent_issue_id: Optional[int] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None
    watcher_user_ids: Optional[List[int]] = None
    is_private: Optional[bool] = None
    estimated_hours: Optional[float] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    done_ratio: Optional[int] = None
    
    @validator('subject')
    def subject_must_not_be_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Subject cannot be empty')
        return v.strip()


class RedmineIssueUpdate(BaseModel):
    """Issue güncelleme için payload modeli."""
    project_id: Optional[int] = None
    tracker_id: Optional[int] = None
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    subject: Optional[str] = None
    description: Optional[str] = None
    category_id: Optional[int] = None
    fixed_version_id: Optional[int] = None
    assigned_to_id: Optional[int] = None
    parent_issue_id: Optional[int] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None
    watcher_user_ids: Optional[List[int]] = None
    is_private: Optional[bool] = None
    estimated_hours: Optional[float] = None
    start_date: Optional[str] = None
    due_date: Optional[str] = None
    done_ratio: Optional[int] = None
    notes: Optional[str] = None  # Comment eklemek için
    private_notes: Optional[bool] = None


class RedmineTimeEntryCreate(BaseModel):
    """Zaman kaydı oluşturma için payload modeli."""
    issue_id: Optional[int] = None
    project_id: Optional[int] = None
    spent_on: str
    hours: float
    activity_id: int
    comments: Optional[str] = None
    custom_fields: Optional[List[Dict[str, Any]]] = None
    
    @validator('hours')
    def hours_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Hours must be positive')
        return v


# Helper types
IssueStatusType = Union[int, str]  # ID veya "open"/"closed" gibi string
UserIdType = Union[int, str]  # ID veya "me" gibi string
ProjectIdType = Union[int, str]  # ID veya identifier string
