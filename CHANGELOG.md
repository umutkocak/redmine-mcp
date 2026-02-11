# Changelog

All notable changes to the Redmine MCP Server project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.4] - 2026-02-11

### 🎉 Major Feature Expansion

This release significantly expands the Redmine MCP Server capabilities from 11 to 29 operations (+164% increase).

### ✨ Added - Projects Module

- **create_project** - Create new Redmine projects with full configuration
  - Support for name, identifier, description, homepage
  - Parent project support (sub-projects)
  - Module activation (issue_tracking, wiki, time_tracking, etc.)
  - Tracker configuration
  - Full UTF-8 support for international characters
- **update_project** - Update existing project properties
  - Modify name, description, homepage
  - Change visibility (public/private)
  - Update enabled modules and trackers
- **delete_project** - Delete projects permanently
- **archive_project** - Archive projects (Redmine 5.0+)
  - Keeps project data but makes it inactive
- **unarchive_project** - Restore archived projects (Redmine 5.0+)

### ✨ Added - Issues Module

- **delete_issue** - Delete issues permanently
  - Proper error handling for permissions
- **add_watcher** - Add users as watchers to issues
  - Email notifications for watchers
  - Full UTF-8 support for international characters
- **remove_watcher** - Remove watchers from issues
  - Clean watcher list management

### ✨ Added - Users Module

- **get_current_user** - Get authenticated user information
  - Uses `/users/current` endpoint
  - Returns API key owner's details
  - Includes memberships and groups if requested
- **create_user** - Create new users (Admin only)
  - Required: login, firstname, lastname, mail
  - Optional: password, admin flag, must_change_passwd
  - Full UTF-8 support for international names
  - Auto-password generation option
- **update_user** - Update user details (Admin only)
  - Change names, email, password
  - Modify admin permissions
  - Full UTF-8 support
- **delete_user** - Delete users (Admin only)
  - Proper permission checks
  - Cascade handling

### ✨ Added - Time Entries Module

- **get_time_entry** - Get specific time entry details
  - Retrieve hours, activity, comments
  - Custom fields support
- **update_time_entry** - Update time entry properties
  - Change hours, date, activity
  - Update comments and custom fields
- **delete_time_entry** - Delete time entries
  - Proper validation and error handling

### ✨ Added - Attachments Module (NEW) 🔥

**CRITICAL FEATURE**: Full file upload/download support with UTF-8 filename handling

- **upload_file** - Upload files to Redmine
  - Two-step process: upload → get token → use in issue/wiki
  - Binary file support (PDF, images, Excel, etc.)
  - UTF-8 filename support with international characters
  - Base64 encoding support for MCP transport
  - Returns token for attachment to issues/wiki pages
- **get_attachment** - Get attachment metadata
  - Filename, size, content_type, author
  - Creation date and description
- **download_attachment** - Download attachment content
  - Binary file download
  - Base64 encoding for MCP response
  - Full UTF-8 filename preservation

### 🔧 Technical Improvements

#### RedmineClient Enhancements

- Added `upload_file()` method with special binary handling
  - Custom headers: `Content-Type: application/octet-stream`
  - UTF-8 filename URL encoding with `urllib.parse.quote()`
  - Extended timeout (60s) for large file uploads
  - Proper token extraction from response
- Added attachment download with `download_attachment()`
  - Binary content handling
  - Stream-based download for large files
- Enhanced error handling for all new endpoints
  - Detailed error messages
  - HTTP status code preservation
  - Validation error extraction

#### UTF-8/International Character Support

- ✅ All text fields support international characters (UTF-8)
- ✅ Filenames with special characters work correctly
- ✅ JSON encode/decode with `ensure_ascii=False`
- ✅ URL encoding for special characters in filenames
- ✅ Binary file handling separate from text encoding

### 📊 Statistics

- **Total Operations**: 29 (was 11 in v1.0.3)
- **New Operations**: 18
- **Modules**: 6 (5 expanded + 1 new)
- **Code Coverage**: Projects (100%), Issues (100%), Users (100%), Time Entries (100%), Attachments (100%)
- **Files Modified**: 7
- **Files Created**: 1 (attachments.py)
- **Lines Added**: ~1,200+

### 🐛 Bug Fixes

- Fixed import organization in main.py
- Improved error handling in all CRUD operations
- Better validation messages for required fields

### 📝 Documentation

- Updated README.md with all new operations
- Added feature descriptions and examples
- Updated operation counts (11 → 31)
- Version bump to 2.0.0

### 🔄 Migration Notes

**Breaking Changes**: None! This is a backwards-compatible expansion.

All existing v1.0.3 operations continue to work exactly as before. New operations are additive only.

### 🎯 Roadmap

Planned for future releases:

- Issue Relations, Versions, Project Memberships
- Wiki Pages, Groups, Roles
- Custom Fields, Journals, Search
- News, Queries, Files

---

## [1.0.3] - 2024-XX-XX

### Features (11 operations)

- Projects: list, get
- Issues: list, get, create, update
- Users: list, get
- Time Entries: list, create
- Enumerations: list

### Status

- UTF-8 support: ✅
- Basic CRUD: Partial
- File operations: ❌

---

**Full Changelog**: https://github.com/umutkocak/redmine-mcp/compare/v1.0.3...v1.0.4
