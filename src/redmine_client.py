"""
Redmine API Client - requests ile API çağrıları.

Bu modül Redmine REST API ile etkileşim için kullanılır.
Tüm HTTP isteklerini ve authentication'ı handle eder.
"""

import json
import logging
import os
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
    
    # Enumerations API
    def get_enumerations(self, resource: Optional[str] = None) -> Dict[str, Any]:
        """Sistem sabitlerini (enumerations) listeler."""
        endpoint = "enumerations"
        if resource:
            endpoint = f"enumerations/{resource}"
        return self._request("GET", endpoint)
    
    # Utility methods
    def test_connection(self) -> bool:
        """API bağlantısını test eder."""
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
