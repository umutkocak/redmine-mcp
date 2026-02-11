"""
Redmine API Client - requests ile API çağrıları.

Bu modül Redmine REST API ile etkileşim için kullanılır.
Tüm HTTP isteklerini ve authentication'ı handle eder.
"""

import json
import logging
import os
import urllib.parse
from typing import Any, Dict, List, Optional, Union
from urllib.parse import urljoin

import requests
from requests.adapters import HTTPAdapter
from requests.auth import HTTPBasicAuth
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class RedmineAPIError(Exception):
    """Redmine API ile ilgili hatalar için özel exception."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class RedmineClient:
    """Redmine REST API client sınıfı.
    
    Bu sınıf Redmine API ile etkileşim için gerekli tüm metodları içerir.
    Authentication, request handling ve error management sağlar.
    """
    
    def __init__(self, url: Optional[str] = None, api_key: Optional[str] = None, 
                 username: Optional[str] = None, password: Optional[str] = None):
        """RedmineClient'ı başlatır.
        
        Args:
            url: Redmine instance URL'i (örn: https://redmine.example.com)
            api_key: Redmine API key (tercih edilen yöntem)
            username: Kullanıcı adı (basic auth için)
            password: Şifre (basic auth için)
        """
        # Environment variables'dan yapılandırma al
        self.url = url or os.getenv("REDMINE_URL")
        self.api_key = api_key or os.getenv("REDMINE_API_KEY")
        self.username = username or os.getenv("REDMINE_USERNAME")
        self.password = password or os.getenv("REDMINE_PASSWORD")
        
        if not self.url:
            raise ValueError("Redmine URL gerekli (REDMINE_URL environment variable veya url parametresi)")
        
        # URL'in sonunda slash olmamasını sağla
        self.url = self.url.rstrip("/")
        
        # Authentication kontrolü
        if not (self.api_key or (self.username and self.password)):
            raise ValueError("API key veya username/password gerekli")
        
        # HTTP session oluştur
        self.session = requests.Session()
        
        # Retry stratejisi
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Headers ayarla
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "Redmine-MCP/1.0.0"
        })
        
        # Authentication ayarla
        if self.api_key:
            self.session.headers["X-Redmine-API-Key"] = self.api_key
        elif self.username and self.password:
            self.session.auth = HTTPBasicAuth(self.username, self.password)
    
    def _build_url(self, endpoint: str) -> str:
        """API endpoint URL'ini oluşturur."""
        return urljoin(f"{self.url}/", f"{endpoint.lstrip('/')}.json")
    
    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None, 
                 data: Optional[Dict] = None) -> Dict[str, Any]:
        """HTTP request gönderir ve response'u handle eder.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (örn: "projects", "issues")
            params: Query parametreleri
            data: Request body datası
            
        Returns:
            API response'u JSON olarak
            
        Raises:
            RedmineAPIError: API isteği başarısız olursa
        """
        url = self._build_url(endpoint)
        
        try:
            logger.debug(f"Making {method} request to {url}")
            logger.debug(f"Params: {params}")
            logger.debug(f"Data: {data}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=30
            )
            
            logger.debug(f"Response status: {response.status_code}")
            
            # Success status codes
            if response.status_code in [200, 201, 204]:
                if response.status_code == 204:  # No content
                    return {}
                return response.json()
            
            # Error handling
            try:
                error_data = response.json()
                error_message = error_data.get("errors", [f"HTTP {response.status_code}"])
                if isinstance(error_message, list):
                    error_message = ", ".join(error_message)
            except json.JSONDecodeError:
                error_message = f"HTTP {response.status_code}: {response.text}"
            
            raise RedmineAPIError(
                message=error_message,
                status_code=response.status_code,
                response_data=error_data if 'error_data' in locals() else None
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise RedmineAPIError(f"Request failed: {str(e)}")
    
    # Projects API
    def get_projects(self, limit: int = 25, offset: int = 0, 
                     include_archived: bool = False) -> List[Dict[str, Any]]:
        """Projeleri listeler."""
        params = {"limit": limit, "offset": offset}
        if include_archived:
            params["status"] = "*"  # Tüm projeler (aktif + arşivli)
        
        response = self._request("GET", "projects", params=params)
        return response.get("projects", [])
    
    def get_project(self, project_id: Union[int, str]) -> Optional[Dict[str, Any]]:
        """Belirli bir projeyi getirir."""
        try:
            response = self._request("GET", f"projects/{project_id}")
            return response.get("project")
        except RedmineAPIError as e:
            if e.status_code == 404:
                return None
            raise
    
    def create_project(self, project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni proje oluşturur.
        
        Args:
            project_data: Proje verisi (name, identifier zorunlu)
            
        Returns:
            Oluşturulan proje bilgisi
        """
        return self._request("POST", "projects", data={"project": project_data})
    
    def update_project(self, project_id: Union[int, str], 
                      project_data: Dict[str, Any]) -> Dict[str, Any]:
        """Proje günceller.
        
        Args:
            project_id: Proje ID veya identifier
            project_data: Güncellenecek proje verisi
            
        Returns:
            API response
        """
        return self._request("PUT", f"projects/{project_id}", 
                           data={"project": project_data})
    
    def delete_project(self, project_id: Union[int, str]) -> Dict[str, Any]:
        """Projeyi siler.
        
        Args:
            project_id: Proje ID veya identifier
            
        Returns:
            API response
        """
        return self._request("DELETE", f"projects/{project_id}")
    
    def archive_project(self, project_id: Union[int, str]) -> Dict[str, Any]:
        """Projeyi arşivler (Redmine 5.0+).
        
        Args:
            project_id: Proje ID veya identifier
            
        Returns:
            API response
        """
        return self._request("PUT", f"projects/{project_id}/archive")
    
    def unarchive_project(self, project_id: Union[int, str]) -> Dict[str, Any]:
        """Projeyi arşivden çıkarır (Redmine 5.0+).
        
        Args:
            project_id: Proje ID veya identifier
            
        Returns:
            API response
        """
        return self._request("PUT", f"projects/{project_id}/unarchive")
    
    # Issues API
    def get_issues(self, project_id: Optional[int] = None, 
                   assigned_to_id: Optional[Union[int, str]] = None,
                   status_id: Optional[Union[int, str]] = None,
                   tracker_id: Optional[int] = None,
                   priority_id: Optional[int] = None,
                   limit: int = 25, offset: int = 0,
                   sort: Optional[str] = None,
                   include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Issue'ları listeler."""
        params = {"limit": limit, "offset": offset}
        
        if project_id:
            params["project_id"] = project_id
        if assigned_to_id:
            params["assigned_to_id"] = assigned_to_id
        if status_id:
            params["status_id"] = status_id
        if tracker_id:
            params["tracker_id"] = tracker_id
        if priority_id:
            params["priority_id"] = priority_id
        if sort:
            params["sort"] = sort
        if include:
            params["include"] = ",".join(include)
            
        return self._request("GET", "issues", params=params)
    
    def get_issue(self, issue_id: int, 
                  include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Belirli bir issue'yu getirir."""
        params = {}
        if include:
            params["include"] = ",".join(include)
        return self._request("GET", f"issues/{issue_id}", params=params)
    
    def create_issue(self, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni issue oluşturur."""
        return self._request("POST", "issues", data={"issue": issue_data})
    
    def update_issue(self, issue_id: int, issue_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mevcut issue'yu günceller."""
        return self._request("PUT", f"issues/{issue_id}", data={"issue": issue_data})
    
    def delete_issue(self, issue_id: int) -> Dict[str, Any]:
        """Issue'yu siler."""
        return self._request("DELETE", f"issues/{issue_id}")
    
    def add_watcher(self, issue_id: int, user_id: int) -> Dict[str, Any]:
        """Issue'ya watcher (takipçi) ekler.
        
        Args:
            issue_id: Issue ID
            user_id: Eklenecek kullanıcı ID
            
        Returns:
            API response
        """
        return self._request("POST", f"issues/{issue_id}/watchers", 
                           data={"user_id": user_id})
    
    def remove_watcher(self, issue_id: int, user_id: int) -> Dict[str, Any]:
        """Issue'dan watcher (takipçi) çıkarır.
        
        Args:
            issue_id: Issue ID
            user_id: Çıkarılacak kullanıcı ID
            
        Returns:
            API response
        """
        return self._request("DELETE", f"issues/{issue_id}/watchers/{user_id}")
    
    # Users API
    def get_users(self, limit: int = 25, offset: int = 0,
                  status: Optional[int] = None) -> Dict[str, Any]:
        """Kullanıcıları listeler."""
        params = {"limit": limit, "offset": offset}
        if status:
            params["status"] = status
        return self._request("GET", "users", params=params)
    
    def get_user(self, user_id: Union[int, str], 
                 include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Belirli bir kullanıcıyı getirir."""
        params = {}
        if include:
            params["include"] = ",".join(include)
        return self._request("GET", f"users/{user_id}", params=params)
    
    def get_current_user(self, include: Optional[List[str]] = None) -> Dict[str, Any]:
        """Mevcut kullanıcıyı getirir (/users/current).
        
        Args:
            include: İçerilecek ilişkiler (memberships, groups)
            
        Returns:
            Kullanıcı bilgisi
        """
        return self.get_user("current", include=include)
    
    def create_user(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Yeni kullanıcı oluşturur (Admin yetkisi gerekli).
        
        Args:
            user_data: Kullanıcı verisi (login, firstname, lastname, mail zorunlu)
            
        Returns:
            Oluşturulan kullanıcı bilgisi
        """
        return self._request("POST", "users", data={"user": user_data})
    
    def update_user(self, user_id: int, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Kullanıcı günceller (Admin yetkisi gerekli).
        
        Args:
            user_id: Kullanıcı ID
            user_data: Güncellenecek kullanıcı verisi
            
        Returns:
            API response
        """
        return self._request("PUT", f"users/{user_id}", data={"user": user_data})
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Kullanıcıyı siler (Admin yetkisi gerekli).
        
        Args:
            user_id: Kullanıcı ID
            
        Returns:
            API response
        """
        return self._request("DELETE", f"users/{user_id}")
    
    # Time Entries API
    def get_time_entries(self, user_id: Optional[int] = None,
                        project_id: Optional[int] = None,
                        issue_id: Optional[int] = None,
                        activity_id: Optional[int] = None,
                        spent_on: Optional[str] = None,
                        from_date: Optional[str] = None,
                        to_date: Optional[str] = None,
                        limit: int = 25, offset: int = 0) -> Dict[str, Any]:
        """Zaman kayıtlarını listeler."""
        params = {"limit": limit, "offset": offset}
        
        if user_id:
            params["user_id"] = user_id
        if project_id:
            params["project_id"] = project_id
        if issue_id:
            params["issue_id"] = issue_id
        if activity_id:
            params["activity_id"] = activity_id
        if spent_on:
            params["spent_on"] = spent_on
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
            
        return self._request("GET", "time_entries", params=params)
    
    def create_time_entry(self, time_entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new time entry."""
        return self._request("POST", "time_entries", data={"time_entry": time_entry_data})
    
    def get_time_entry(self, time_entry_id: int) -> Dict[str, Any]:
        """Belirli bir zaman kaydını getirir.
        
        Args:
            time_entry_id: Zaman kaydı ID
            
        Returns:
            Zaman kaydı bilgisi
        """
        response = self._request("GET", f"time_entries/{time_entry_id}")
        return response.get("time_entry", {})
    
    def update_time_entry(self, time_entry_id: int, 
                         time_entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Zaman kaydını günceller.
        
        Args:
            time_entry_id: Zaman kaydı ID
            time_entry_data: Güncellenecek veri
            
        Returns:
            API response
        """
        return self._request("PUT", f"time_entries/{time_entry_id}", 
                           data={"time_entry": time_entry_data})
    
    def delete_time_entry(self, time_entry_id: int) -> Dict[str, Any]:
        """Zaman kaydını siler.
        
        Args:
            time_entry_id: Zaman kaydı ID
            
        Returns:
            API response
        """
        return self._request("DELETE", f"time_entries/{time_entry_id}")
    
    # Enumerations API
    def get_enumerations(self, resource: Optional[str] = None) -> Dict[str, Any]:
        """Lists system enumerations."""
        endpoint = "enumerations"
        if resource:
            endpoint = f"enumerations/{resource}"
        return self._request("GET", endpoint)
    
    def list_trackers(self) -> List[Dict[str, Any]]:
        """Lists all available trackers.
        
        Returns:
            List of trackers (id, name, default_status, description)
        """
        response = self._request("GET", "trackers")
        return response.get("trackers", [])
    
    def list_issue_statuses(self) -> List[Dict[str, Any]]:
        """Lists all available issue statuses.
        
        Returns:
            List of issue statuses (id, name, is_closed)
        """
        response = self._request("GET", "issue_statuses")
        return response.get("issue_statuses", [])
    
    def list_roles(self) -> List[Dict[str, Any]]:
        """Lists all available roles.
        
        Returns:
            List of roles (id, name)
        """
        response = self._request("GET", "roles")
        return response.get("roles", [])
    
    # Attachments API
    def upload_file(self, file_data: bytes, filename: str) -> str:
        """Uploads a file and returns an upload token.
        
        NOTE: File upload in Redmine is two-stage:
        1. This method: POST /uploads.json -> gets token
        2. Use token in Issue/Wiki create/update
        
        Args:
            file_data: Binary file data
            filename: Filename (supports UTF-8)
            
        Returns:
            Upload token (string)
            
        Example:
            token = client.upload_file(file_content, "document.pdf")
            client.create_issue({
                "project_id": 1,
                "subject": "Issue with attachment",
                "uploads": [{"token": token, "filename": "document.pdf"}]
            })
        """
        # UTF-8 filename encode for URL
        filename_encoded = urllib.parse.quote(filename.encode('utf-8'))
        
        url = f"{self.url}/uploads.json?filename={filename_encoded}"
        
        try:
            # Special headers: Content-Type changes!
            headers = {
                'Content-Type': 'application/octet-stream',
                'Accept': 'application/json'
            }
            
            # API key authentication
            if self.api_key:
                headers['X-Redmine-API-Key'] = self.api_key
            
            logger.debug(f"Uploading file: {filename} ({len(file_data)} bytes)")
            
            response = self.session.post(
                url,
                data=file_data,  # NOT json=, direct data=
                headers=headers,
                timeout=60  # Longer timeout for file upload
            )
            
            logger.debug(f"Upload response status: {response.status_code}")
            
            if response.status_code == 201:
                result = response.json()
                token = result.get('upload', {}).get('token')
                if not token:
                    raise RedmineAPIError("Upload successful but no token in response")
                return token
            
            # Error handling
            try:
                error_data = response.json()
                error_message = error_data.get("errors", [f"HTTP {response.status_code}"])
                if isinstance(error_message, list):
                    error_message = ", ".join(error_message)
            except json.JSONDecodeError:
                error_message = f"HTTP {response.status_code}: {response.text}"
            
            raise RedmineAPIError(
                message=error_message,
                status_code=response.status_code,
                response_data=error_data if 'error_data' in locals() else None
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"File upload failed: {e}")
            raise RedmineAPIError(f"File upload failed: {str(e)}")
    
    def get_attachment(self, attachment_id: int) -> Dict[str, Any]:
        """Gets attachment metadata.
        
        Args:
            attachment_id: Attachment ID
            
        Returns:
            Attachment info (filename, filesize, content_type, etc.)
        """
        response = self._request("GET", f"attachments/{attachment_id}")
        return response.get("attachment", {})
    
    def download_attachment(self, attachment_id: int) -> bytes:
        """Downloads an attachment file.
        
        Args:
            attachment_id: Attachment ID
            
        Returns:
            Binary file data
        """
        # Get attachment info first
        attachment_info = self.get_attachment(attachment_id)
        content_url = attachment_info.get('content_url')
        
        if not content_url:
            raise RedmineAPIError("Attachment has no content_url")
        
        try:
            # Download the file
            headers = {}
            if self.api_key:
                headers['X-Redmine-API-Key'] = self.api_key
            
            response = self.session.get(
                content_url,
                headers=headers,
                timeout=60
            )
            
            if response.status_code == 200:
                return response.content
            
            raise RedmineAPIError(
                f"Failed to download attachment: HTTP {response.status_code}",
                status_code=response.status_code
            )
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Attachment download failed: {e}")
            raise RedmineAPIError(f"Attachment download failed: {str(e)}")

    # Issue Relations API
    def list_issue_relations(self, issue_id: int) -> List[Dict[str, Any]]:
        """Lists all relations for a specific issue.
        
        Args:
            issue_id: Issue ID to list relations for
            
        Returns:
            List of relations
        """
        # Relations are included in issue details with 'relations' include
        response = self._request("GET", f"issues/{issue_id}", 
                                params={"include": "relations"})
        relations = response.get("issue", {}).get("relations", [])
        return relations
    
    def create_issue_relation(self, issue_id: int, issue_to_id: int, 
                             relation_type: str, delay: Optional[int] = None) -> Dict[str, Any]:
        """Creates a relation between two issues.
        
        Args:
            issue_id: Source issue ID
            issue_to_id: Target issue ID
            relation_type: Type of relation (relates, duplicates, blocks, etc.)
            delay: Delay in days (only for precedes/follows relations)
            
        Returns:
            Created relation details
        """
        relation_data = {
            "issue_to_id": issue_to_id,
            "relation_type": relation_type
        }
        
        if delay is not None:
            relation_data["delay"] = delay
            
        return self._request("POST", f"issues/{issue_id}/relations", 
                           data={"relation": relation_data})
    
    def get_issue_relation(self, relation_id: int) -> Dict[str, Any]:
        """Gets details of a specific relation.
        
        Args:
            relation_id: Relation ID
            
        Returns:
            Relation details
        """
        response = self._request("GET", f"relations/{relation_id}")
        return response.get("relation", {})
    
    def delete_issue_relation(self, relation_id: int) -> bool:
        """Deletes a specific issue relation.
        
        Args:
            relation_id: Relation ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"relations/{relation_id}")
            return True
        except RedmineAPIError:
            return False

    # Versions API
    def list_versions(self, project_id: Union[str, int]) -> List[Dict[str, Any]]:
        """Lists all versions for a specific project.
        
        Args:
            project_id: Project ID or identifier
            
        Returns:
            List of versions
        """
        response = self._request("GET", f"projects/{project_id}/versions")
        return response.get("versions", [])
    
    def get_version(self, version_id: int) -> Dict[str, Any]:
        """Gets details of a specific version.
        
        Args:
            version_id: Version ID
            
        Returns:
            Version details
        """
        response = self._request("GET", f"versions/{version_id}")
        return response.get("version", {})
    
    def create_version(self, project_id: Union[str, int], 
                      version_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new version in a project.
        
        Args:
            project_id: Project ID or identifier
            version_data: Version properties (name, description, status, etc.)
            
        Returns:
            Created version details
        """
        version_data["project_id"] = project_id
        return self._request("POST", "versions", data={"version": version_data})
    
    def update_version(self, version_id: int, 
                      version_data: Dict[str, Any]) -> bool:
        """Updates an existing version.
        
        Args:
            version_id: Version ID to update
            version_data: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", f"versions/{version_id}", 
                         data={"version": version_data})
            return True
        except RedmineAPIError:
            return False
    
    def delete_version(self, version_id: int) -> bool:
        """Deletes a specific version.
        
        Args:
            version_id: Version ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"versions/{version_id}")
            return True
        except RedmineAPIError:
            return False

    # Memberships API
    def list_memberships(self, project_id: Union[str, int]) -> List[Dict[str, Any]]:
        """Lists all memberships for a specific project.
        
        Args:
            project_id: Project ID or identifier
            
        Returns:
            List of memberships
        """
        response = self._request("GET", f"projects/{project_id}/memberships")
        return response.get("memberships", [])
    
    def get_membership(self, membership_id: int) -> Dict[str, Any]:
        """Gets details of a specific membership.
        
        Args:
            membership_id: Membership ID
            
        Returns:
            Membership details
        """
        response = self._request("GET", f"memberships/{membership_id}")
        return response.get("membership", {})
    
    def create_membership(self, project_id: Union[str, int], 
                        membership_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new membership in a project.
        
        Args:
            project_id: Project ID or identifier
            membership_data: Membership properties (user_id/group_id and role_ids)
            
        Returns:
            Created membership details
        """
        membership_data["project_id"] = project_id
        return self._request("POST", "memberships", data={"membership": membership_data})
    
    def update_membership(self, membership_id: int, 
                        role_ids: List[int]) -> bool:
        """Updates roles for an existing membership.
        
        Args:
            membership_id: Membership ID to update
            role_ids: New list of role IDs
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", f"memberships/{membership_id}", 
                         data={"membership": {"role_ids": role_ids}})
            return True
        except RedmineAPIError:
            return False
    
    def delete_membership(self, membership_id: int) -> bool:
        """Deletes a specific membership.
        
        Args:
            membership_id: Membership ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"memberships/{membership_id}")
            return True
        except RedmineAPIError:
            return False

    # Issue Categories API
    def list_issue_categories(self, project_id: Union[str, int]) -> List[Dict[str, Any]]:
        """Lists all issue categories for a specific project.
        
        Args:
            project_id: Project ID or identifier
            
        Returns:
            List of issue categories
        """
        response = self._request("GET", f"projects/{project_id}/issue_categories")
        return response.get("issue_categories", [])
    
    def get_issue_category(self, category_id: int) -> Dict[str, Any]:
        """Gets details of a specific issue category.
        
        Args:
            category_id: Category ID
            
        Returns:
            Category details
        """
        response = self._request("GET", f"issue_categories/{category_id}")
        return response.get("issue_category", {})
    
    def create_issue_category(self, project_id: Union[str, int],
                             category_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new issue category in a project.
        
        Args:
            project_id: Project ID or identifier
            category_data: Category properties (name required, assigned_to_id optional)
            
        Returns:
            Created category details
        """
        response = self._request("POST", f"projects/{project_id}/issue_categories",
                                data={"issue_category": category_data})
        return response.get("issue_category", response)
    
    def update_issue_category(self, category_id: int,
                             category_data: Dict[str, Any]) -> bool:
        """Updates an existing issue category.
        
        Args:
            category_id: Category ID to update
            category_data: Properties to update (name, assigned_to_id)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", f"issue_categories/{category_id}",
                         data={"issue_category": category_data})
            return True
        except RedmineAPIError:
            return False
    
    def delete_issue_category(self, category_id: int,
                             reassign_to_id: Optional[int] = None) -> bool:
        """Deletes a specific issue category.
        
        Args:
            category_id: Category ID to delete
            reassign_to_id: Category ID to reassign existing issues to (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            params = {}
            if reassign_to_id is not None:
                params["reassign_to_id"] = reassign_to_id
            self._request("DELETE", f"issue_categories/{category_id}", params=params)
            return True
        except RedmineAPIError:
            return False

    # Wiki Pages API
    def list_wiki_pages(self, project_id: Union[str, int]) -> List[Dict[str, Any]]:
        """Lists all wiki pages for a specific project.
        
        Args:
            project_id: Project ID or identifier
            
        Returns:
            List of wiki pages
        """
        response = self._request("GET", f"projects/{project_id}/wiki/index")
        return response.get("wiki_pages", [])
    
    def get_wiki_page(self, project_id: Union[str, int], page_name: str,
                      version: Optional[int] = None) -> Dict[str, Any]:
        """Gets a specific wiki page content.
        
        Args:
            project_id: Project ID or identifier
            page_name: Wiki page name (URL title)
            version: Specific version number (optional)
            
        Returns:
            Wiki page details including content
        """
        endpoint = f"projects/{project_id}/wiki/{page_name}"
        if version is not None:
            endpoint = f"{endpoint}/{version}"
        response = self._request("GET", endpoint)
        return response.get("wiki_page", {})
    
    def create_or_update_wiki_page(self, project_id: Union[str, int],
                                    page_name: str,
                                    wiki_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates or updates a wiki page.
        
        Args:
            project_id: Project ID or identifier
            page_name: Wiki page name
            wiki_data: Page data (text, comments, parent_title)
            
        Returns:
            Wiki page details
        """
        response = self._request("PUT", f"projects/{project_id}/wiki/{page_name}",
                                data={"wiki_page": wiki_data})
        return response.get("wiki_page", response)
    
    def delete_wiki_page(self, project_id: Union[str, int], page_name: str) -> bool:
        """Deletes a wiki page.
        
        Args:
            project_id: Project ID or identifier
            page_name: Wiki page name to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"projects/{project_id}/wiki/{page_name}")
            return True
        except RedmineAPIError:
            return False

    # Groups API
    def list_groups(self) -> List[Dict[str, Any]]:
        """Lists all groups. Requires admin privileges.
        
        Returns:
            List of groups
        """
        response = self._request("GET", "groups")
        return response.get("groups", [])
    
    def get_group(self, group_id: int, include_users: bool = False) -> Dict[str, Any]:
        """Gets details of a specific group.
        
        Args:
            group_id: Group ID
            include_users: Whether to include group members
            
        Returns:
            Group details
        """
        params = {}
        if include_users:
            params["include"] = "users,memberships"
        response = self._request("GET", f"groups/{group_id}", params=params)
        return response.get("group", {})
    
    def create_group(self, group_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new group. Requires admin privileges.
        
        Args:
            group_data: Group data (name required, user_ids optional)
            
        Returns:
            Created group details
        """
        response = self._request("POST", "groups", data={"group": group_data})
        return response.get("group", response)
    
    def update_group(self, group_id: int, group_data: Dict[str, Any]) -> bool:
        """Updates an existing group. Requires admin privileges.
        
        Args:
            group_id: Group ID to update
            group_data: Properties to update
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", f"groups/{group_id}", data={"group": group_data})
            return True
        except RedmineAPIError:
            return False
    
    def delete_group(self, group_id: int) -> bool:
        """Deletes a group. Requires admin privileges.
        
        Args:
            group_id: Group ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"groups/{group_id}")
            return True
        except RedmineAPIError:
            return False
    
    def add_user_to_group(self, group_id: int, user_id: int) -> bool:
        """Adds a user to a group. Requires admin privileges.
        
        Args:
            group_id: Group ID
            user_id: User ID to add
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("POST", f"groups/{group_id}/users",
                         data={"user_id": user_id})
            return True
        except RedmineAPIError:
            return False
    
    def remove_user_from_group(self, group_id: int, user_id: int) -> bool:
        """Removes a user from a group. Requires admin privileges.
        
        Args:
            group_id: Group ID
            user_id: User ID to remove
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("DELETE", f"groups/{group_id}/users/{user_id}")
            return True
        except RedmineAPIError:
            return False

    # Roles API (extended)
    def get_role(self, role_id: int) -> Dict[str, Any]:
        """Gets details of a specific role, including permissions.
        
        Args:
            role_id: Role ID
            
        Returns:
            Role details with permissions
        """
        response = self._request("GET", f"roles/{role_id}")
        return response.get("role", {})

    # Custom Fields API
    def list_custom_fields(self) -> List[Dict[str, Any]]:
        """Lists all custom fields. Requires admin privileges.
        
        Returns:
            List of custom field definitions
        """
        response = self._request("GET", "custom_fields")
        return response.get("custom_fields", [])

    # Journals API
    def list_issue_journals(self, issue_id: int) -> List[Dict[str, Any]]:
        """Lists the change history (journals) of an issue.
        
        Args:
            issue_id: Issue ID
            
        Returns:
            List of journal entries
        """
        response = self._request("GET", f"issues/{issue_id}",
                                params={"include": "journals"})
        return response.get("issue", {}).get("journals", [])
    
    def update_journal(self, journal_id: int, journal_data: Dict[str, Any]) -> bool:
        """Updates journal notes.
        
        Args:
            journal_id: Journal ID to update
            journal_data: Data to update (notes, private_notes)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", f"journals/{journal_id}",
                         data={"journal": journal_data})
            return True
        except RedmineAPIError:
            return False

    # News API
    def list_news(self, project_id: Optional[Union[str, int]] = None,
                  limit: int = 25, offset: int = 0) -> List[Dict[str, Any]]:
        """Lists news entries.
        
        Args:
            project_id: Project ID or identifier (optional, omit for all news)
            limit: Maximum number of entries
            offset: Pagination offset
            
        Returns:
            List of news entries
        """
        params = {"limit": limit, "offset": offset}
        if project_id:
            endpoint = f"projects/{project_id}/news"
        else:
            endpoint = "news"
        response = self._request("GET", endpoint, params=params)
        return response.get("news", [])
    
    def get_news(self, news_id: int) -> Dict[str, Any]:
        """Gets details of a specific news entry.
        
        Args:
            news_id: News ID
            
        Returns:
            News details
        """
        response = self._request("GET", f"news/{news_id}")
        return response.get("news", {})

    # Queries API
    def list_queries(self, project_id: Optional[Union[str, int]] = None) -> List[Dict[str, Any]]:
        """Lists saved/custom queries.
        
        Args:
            project_id: Project ID or identifier (optional)
            
        Returns:
            List of saved queries
        """
        params = {}
        if project_id:
            params["project_id"] = project_id
        response = self._request("GET", "queries", params=params)
        return response.get("queries", [])

    # Search API
    def search(self, query: str, project_id: Optional[Union[str, int]] = None,
               titles_only: bool = False, open_issues: bool = False,
               scope: Optional[str] = None,
               limit: int = 25, offset: int = 0) -> Dict[str, Any]:
        """Performs a global search across Redmine.
        
        Args:
            query: Search query string
            project_id: Project scope (optional)
            titles_only: Search only in titles
            open_issues: Search only open issues
            scope: Search scope ('subprojects' or 'all')
            limit: Maximum results
            offset: Pagination offset
            
        Returns:
            Search results with total_count
        """
        params = {
            "q": query,
            "limit": limit,
            "offset": offset
        }
        if titles_only:
            params["titles_only"] = 1
        if open_issues:
            params["open_issues"] = 1
        if scope:
            params["scope"] = scope
        
        if project_id:
            endpoint = f"projects/{project_id}/search"
        else:
            endpoint = "search"
        
        return self._request("GET", endpoint, params=params)

    # Files API
    def list_files(self, project_id: Union[str, int]) -> List[Dict[str, Any]]:
        """Lists all files for a specific project.
        
        Args:
            project_id: Project ID or identifier
            
        Returns:
            List of files
        """
        response = self._request("GET", f"projects/{project_id}/files")
        return response.get("files", [])

    # My Account API
    def get_my_account(self) -> Dict[str, Any]:
        """Gets the current user's account information.
        
        Returns:
            Account details
        """
        response = self._request("GET", "my/account")
        return response.get("user", {})
    
    def update_my_account(self, account_data: Dict[str, Any]) -> bool:
        """Updates the current user's account settings.
        
        Args:
            account_data: Data to update (firstname, lastname, mail, custom_fields)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self._request("PUT", "my/account", data={"user": account_data})
            return True
        except RedmineAPIError:
            return False

    # Utility methods
    def test_connection(self) -> bool:
        """Tests the API connection."""
        try:
            self._request("GET", "projects", params={"limit": 1})
            return True
        except RedmineAPIError:
            return False


# Global client instance (lazy initialization)
_client_instance: Optional[RedmineClient] = None


def get_client() -> RedmineClient:
    """Global RedmineClient instance'ını döndürür."""
    global _client_instance
    if _client_instance is None:
        _client_instance = RedmineClient()
    return _client_instance


def set_client(client: RedmineClient) -> None:
    """Global RedmineClient instance'ını ayarlar (test için)."""
    global _client_instance
    _client_instance = client
