"""
Redmine MCP Server - Version Management

Bu modül proje versiyonunu yönetir.
"""

__version__ = "1.0.2"
__version_info__ = (1, 0, 2)

# Changelog
CHANGELOG = {
    "1.0.2": {
        "date": "2025-08-02",
        "changes": [
            "🐛 create_issue double-wrapping bug düzeltildi",
            "✅ Issue creation validation iyileştirildi (project_id ve subject kontrolü)",
            "🔧 RedmineClient ile tool handler arasındaki format uyumsuzluğu giderildi",
            "📋 create_issue bug fix test script'i eklendi"
        ],
        "breaking_changes": [],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
    "1.0.1": {
        "date": "2025-08-02",
        "changes": [
            "🔧 MCP version check hatası düzeltildi",
            "✅ Issue validation error mesajları iyileştirildi",
            "✅ Claude Desktop uyumluluğu arttırıldı",
            "📋 Validation test script'i eklendi"
        ],
        "breaking_changes": [],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    },
    "1.0.0": {
        "date": "2025-08-02",
        "changes": [
            "✅ İlk stabil sürüm",
            "✅ Standard MCP library ile tam entegrasyon",
            "✅ 10 temel tool tamamlandı (projects, issues, users, time_entries, enumerations)",
            "✅ Issue tool'ları {'issue': {...}} wrapper formatı ile güncellendi",
            "✅ Custom field values desteği eklendi",
            "✅ Parent issue ID, start_date, due_date desteği",
            "✅ Claude Desktop entegrasyonu hazır",
            "✅ Kapsamlı error handling ve logging",
            "✅ Environment-based configuration",
            "✅ Production-ready documentation"
        ],
        "breaking_changes": [
            "⚠️ FastMCP'den Standard MCP'ye geçiş",
            "⚠️ create_issue ve update_issue tool'ları wrapper format gerektirir"
        ],
        "dependencies": {
            "mcp": ">=1.0.0",
            "requests": ">=2.31.0", 
            "pydantic": ">=2.0.0",
            "python-dotenv": ">=1.0.0"
        }
    }
}

def get_version() -> str:
    """Güncel versiyon numarasını döndürür."""
    return __version__

def get_version_info() -> tuple:
    """Version info tuple'ını döndürür (major, minor, patch)."""
    return __version_info__

def get_changelog(version: str = None) -> dict:
    """Belirtilen version veya tüm changelog'u döndürür."""
    if version:
        return CHANGELOG.get(version, {})
    return CHANGELOG

def print_version_info():
    """Version bilgilerini yazdırır."""
    print(f"Redmine MCP Server v{__version__}")
    print(f"Release Date: {CHANGELOG[__version__]['date']}")
    print(f"MCP Library: Standard MCP >= 1.0.0")
    print(f"Python: 3.9+")
