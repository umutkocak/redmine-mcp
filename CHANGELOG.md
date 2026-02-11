# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-02-11

### Overview

Major release achieving comprehensive Redmine REST API coverage. Total tools expanded from **11** to **74** across **20 modules**.

### Added

#### Phase 1 & 2 — Core Module Expansion

- **Projects**: `create_project`, `update_project`, `delete_project`, `archive_project`, `unarchive_project`
- **Issues**: `delete_issue`, `add_watcher`, `remove_watcher`
- **Users**: `get_current_user`, `create_user`, `update_user`, `delete_user`
- **Time Entries**: `get_time_entry`, `update_time_entry`, `delete_time_entry`
- **Attachments** _(new module)_: `upload_file`, `get_attachment`, `download_attachment`
- **Versions** _(new module)_: `list_versions`, `get_version`, `create_version`, `update_version`, `delete_version`
- **Memberships** _(new module)_: `list_memberships`, `get_membership`, `create_membership`, `update_membership`, `delete_membership`
- **Enumerations**: `list_issue_priorities`, `list_time_entry_activities`, `list_document_categories`
- **Issue Categories** _(new module)_: `list_issue_categories`, `get_issue_category`, `create_issue_category`, `update_issue_category`, `delete_issue_category`
- **Issue Relations** _(new module)_: `list_issue_relations`, `get_issue_relation`, `create_issue_relation`, `delete_issue_relation`

#### Phase 3 — Administration & Collaboration

- **Wiki Pages** _(new module)_: `list_wiki_pages`, `get_wiki_page`, `create_or_update_wiki_page`, `delete_wiki_page`
- **Groups** _(new module)_: `list_groups`, `get_group`, `create_group`, `update_group`, `delete_group`, `add_user_to_group`, `remove_user_from_group`
- **Roles** _(new module)_: `list_roles_detail`, `get_role`
- **Custom Fields** _(new module)_: `list_custom_fields`
- **Journals** _(new module)_: `list_issue_journals`, `update_journal`

#### Phase 4 — Information & Search

- **News** _(new module)_: `list_news`, `get_news`
- **Queries** _(new module)_: `list_queries`
- **Search** _(new module)_: `search`
- **Files** _(new module)_: `list_files`
- **My Account** _(new module)_: `get_my_account`, `update_my_account`

### Changed

- Rewrote `README.md` — professional English, GitHub-optimized with badges and tables
- Extended `RedmineClient` with 40+ API methods covering all Redmine REST endpoints
- Unified error handling and response formatting across all tool modules
- Updated dependencies to latest compatible versions

### Fixed

- Import organization in `main.py`
- Consistent error messages and HTTP status code propagation
- Validation messages for required fields in all CRUD operations

### Migration Notes

No breaking changes. All v1.0.x tools remain fully compatible. New tools are purely additive.

---

## [1.0.4] - 2026-02-01

### Added

- Projects: `create_project`, `update_project`, `delete_project`, `archive_project`, `unarchive_project`
- Issues: `delete_issue`, `add_watcher`, `remove_watcher`
- Users: `get_current_user`, `create_user`, `update_user`, `delete_user`
- Time Entries: `get_time_entry`, `update_time_entry`, `delete_time_entry`
- Attachments module: `upload_file`, `get_attachment`, `download_attachment`
- Full UTF-8/international character support across all operations

### Changed

- Total operations expanded from 11 to 29

---

## [1.0.3] - 2024-12-01

### Added

- Initial release with 11 core operations
- Projects: `list_projects`, `get_project`
- Issues: `list_issues`, `get_issue`, `create_issue`, `update_issue`
- Users: `list_users`, `get_user`
- Time Entries: `list_time_entries`, `create_time_entry`
- Enumerations: `list_enumerations`

---

**Full Changelog**: https://github.com/umutkocak/redmine-mcp/compare/v1.0.3...v2.0.0
