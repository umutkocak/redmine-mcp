<p align="center">
  <h1 align="center">Redmine MCP Server</h1>
  <p align="center">
    A comprehensive <a href="https://modelcontextprotocol.io/">Model Context Protocol</a> server for seamless Redmine integration.
  </p>
</p>

<p align="center">
  <a href="https://github.com/umutkocak/redmine-mcp/releases"><img src="https://img.shields.io/badge/version-2.0.0-blue.svg" alt="Version"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License"></a>
  <a href="https://modelcontextprotocol.io/"><img src="https://img.shields.io/badge/MCP-1.0%2B-purple.svg" alt="MCP"></a>
  <a href="https://www.redmine.org/"><img src="https://img.shields.io/badge/Redmine-REST%20API-red.svg" alt="Redmine"></a>
</p>

<p align="center">
  <b>74 tools</b> · <b>20 modules</b> · <b>Full CRUD</b> · <b>Docker Ready</b> · <b>UTF-8 Safe</b>
</p>

---

## Overview

Redmine MCP Server exposes the Redmine REST API as MCP tools, enabling AI assistants like Claude to manage projects, issues, users, wiki pages, and more — directly through natural language.

Built with the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for guaranteed protocol compliance.

## Quick Start

### Option 1: Docker (Recommended)

```bash
git clone https://github.com/umutkocak/redmine-mcp.git
cd redmine-mcp
cp .env.example .env   # Edit with your credentials
docker build -t redmine-mcp .
docker run -it --env-file .env redmine-mcp
```

### Option 2: Local Installation

```bash
git clone https://github.com/umutkocak/redmine-mcp.git
cd redmine-mcp
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # Edit with your credentials
python src/main.py
```

### Environment Variables

```env
REDMINE_URL=https://redmine.example.com
REDMINE_API_KEY=your_api_key_here
LOG_LEVEL=INFO
```

> **Tip:** Enable REST API in Redmine under _Administration → Settings → API_, then generate your key from your user profile.

---

## Supported Operations

### Projects — 7 tools

| Tool                | Description                                  |
| ------------------- | -------------------------------------------- |
| `list_projects`     | List all projects with pagination            |
| `get_project`       | Get project details                          |
| `create_project`    | Create a new project                         |
| `update_project`    | Update project properties                    |
| `delete_project`    | Delete a project                             |
| `archive_project`   | Archive a project _(Redmine 5.0+)_           |
| `unarchive_project` | Restore an archived project _(Redmine 5.0+)_ |

### Issues — 7 tools

| Tool             | Description                                      |
| ---------------- | ------------------------------------------------ |
| `list_issues`    | List and filter issues                           |
| `get_issue`      | Get issue details with relations, journals, etc. |
| `create_issue`   | Create a new issue with full metadata            |
| `update_issue`   | Update issue fields, add notes                   |
| `delete_issue`   | Delete an issue                                  |
| `add_watcher`    | Add a watcher to an issue                        |
| `remove_watcher` | Remove a watcher from an issue                   |

### Users — 6 tools

| Tool               | Description                      |
| ------------------ | -------------------------------- |
| `list_users`       | List users with status filtering |
| `get_user`         | Get user details                 |
| `get_current_user` | Get authenticated user info      |
| `create_user`      | Create a new user _(admin)_      |
| `update_user`      | Update user details _(admin)_    |
| `delete_user`      | Delete a user _(admin)_          |

### Time Entries — 5 tools

| Tool                | Description                     |
| ------------------- | ------------------------------- |
| `list_time_entries` | List time entries with filters  |
| `create_time_entry` | Log time with activity tracking |
| `get_time_entry`    | Get time entry details          |
| `update_time_entry` | Update a time entry             |
| `delete_time_entry` | Delete a time entry             |

### Attachments — 3 tools

| Tool                  | Description                                   |
| --------------------- | --------------------------------------------- |
| `upload_file`         | Upload a file and receive an attachment token |
| `get_attachment`      | Get attachment metadata                       |
| `download_attachment` | Download attachment content                   |

### Issue Relations — 4 tools

| Tool                    | Description                                  |
| ----------------------- | -------------------------------------------- |
| `list_issue_relations`  | List relations for an issue                  |
| `create_issue_relation` | Create a relation (blocks, duplicates, etc.) |
| `get_issue_relation`    | Get relation details                         |
| `delete_issue_relation` | Delete a relation                            |

### Versions / Milestones — 5 tools

| Tool             | Description            |
| ---------------- | ---------------------- |
| `list_versions`  | List project versions  |
| `get_version`    | Get version details    |
| `create_version` | Create a new milestone |
| `update_version` | Update a version       |
| `delete_version` | Delete a version       |

### Memberships — 5 tools

| Tool                | Description                      |
| ------------------- | -------------------------------- |
| `list_memberships`  | List project members             |
| `get_membership`    | Get membership details           |
| `create_membership` | Add a user or group to a project |
| `update_membership` | Update member roles              |
| `delete_membership` | Remove a member                  |

### Issue Categories — 5 tools

| Tool                    | Description                   |
| ----------------------- | ----------------------------- |
| `list_issue_categories` | List categories for a project |
| `get_issue_category`    | Get category details          |
| `create_issue_category` | Create a category             |
| `update_issue_category` | Update a category             |
| `delete_issue_category` | Delete a category             |

### Wiki Pages — 4 tools

| Tool                         | Description                             |
| ---------------------------- | --------------------------------------- |
| `list_wiki_pages`            | List all wiki pages for a project       |
| `get_wiki_page`              | Get page content (with version history) |
| `create_or_update_wiki_page` | Create or update a wiki page            |
| `delete_wiki_page`           | Delete a wiki page                      |

### Groups — 7 tools

| Tool                     | Description                          |
| ------------------------ | ------------------------------------ |
| `list_groups`            | List all groups _(admin)_            |
| `get_group`              | Get group details with members       |
| `create_group`           | Create a new group _(admin)_         |
| `update_group`           | Update a group _(admin)_             |
| `delete_group`           | Delete a group _(admin)_             |
| `add_user_to_group`      | Add a user to a group _(admin)_      |
| `remove_user_from_group` | Remove a user from a group _(admin)_ |

### Roles — 2 tools

| Tool                | Description                       |
| ------------------- | --------------------------------- |
| `list_roles_detail` | List all roles                    |
| `get_role`          | Get role details with permissions |

### Journals — 2 tools

| Tool                  | Description              |
| --------------------- | ------------------------ |
| `list_issue_journals` | Get issue change history |
| `update_journal`      | Update journal notes     |

### News — 2 tools

| Tool        | Description                               |
| ----------- | ----------------------------------------- |
| `list_news` | List news entries (global or per project) |
| `get_news`  | Get news details                          |

### System & Metadata — 8 tools

| Tool                  | Description                                    |
| --------------------- | ---------------------------------------------- |
| `list_enumerations`   | List system constants (priorities, activities) |
| `list_trackers`       | List all trackers                              |
| `list_issue_statuses` | List all issue statuses                        |
| `list_roles`          | List all roles                                 |
| `list_custom_fields`  | List all custom field definitions _(admin)_    |
| `list_queries`        | List saved/custom queries                      |
| `search`              | Global search across all resources             |
| `list_files`          | List project files                             |

### My Account — 2 tools

| Tool                | Description                 |
| ------------------- | --------------------------- |
| `get_my_account`    | Get current account details |
| `update_my_account` | Update account settings     |

---

## Claude Desktop Integration

Add the following to your Claude Desktop configuration file:

**Local installation:**

```json
{
  "mcpServers": {
    "redmine": {
      "command": "/path/to/project/.venv/bin/python",
      "args": ["/path/to/project/src/main.py"],
      "env": {
        "REDMINE_URL": "https://redmine.example.com",
        "REDMINE_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

**Docker:**

```json
{
  "mcpServers": {
    "redmine": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "-e",
        "REDMINE_URL=https://redmine.example.com",
        "-e",
        "REDMINE_API_KEY=your_api_key_here",
        "redmine-mcp:latest"
      ]
    }
  }
}
```

<details>
<summary><b>Config file locations</b></summary>

| OS      | Path                                                              |
| ------- | ----------------------------------------------------------------- |
| macOS   | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json`                     |
| Linux   | `~/.config/claude/claude_desktop_config.json`                     |

</details>

---

## Usage Examples

### Create an Issue

```json
{
  "issue": {
    "project_id": 1,
    "subject": "Fix login page validation",
    "description": "Email field accepts invalid format",
    "tracker_id": 1,
    "priority_id": 3,
    "assigned_to_id": 5,
    "due_date": "2026-03-01"
  }
}
```

### Log Time

```json
{
  "issue_id": 123,
  "hours": 2.5,
  "activity_id": 9,
  "comments": "Backend API implementation"
}
```

### Search Across Redmine

```json
{
  "query": "authentication",
  "titles_only": false,
  "limit": 10
}
```

---

## Project Structure

```
src/
├── main.py              # MCP server entry point
├── redmine_client.py    # Redmine REST API client
├── version.py           # Version management
└── tools/
    ├── projects.py          # Project CRUD + archive
    ├── issues.py            # Issue CRUD + watchers
    ├── users.py             # User CRUD + current user
    ├── time_entries.py      # Time entry CRUD
    ├── attachments.py       # File upload/download
    ├── enumerations.py      # Trackers, statuses, roles
    ├── issue_relations.py   # Issue relations
    ├── versions.py          # Milestones
    ├── memberships.py       # Project memberships
    ├── issue_categories.py  # Issue categories
    ├── wiki_pages.py        # Wiki management
    ├── groups.py            # Group management
    ├── roles.py             # Role details + permissions
    ├── custom_fields.py     # Custom field definitions
    ├── journals.py          # Issue change history
    ├── news.py              # News entries
    ├── queries.py           # Saved queries
    ├── search.py            # Global search
    ├── files.py             # Project files
    └── my_account.py        # Account management
```

## Requirements

- **Python** 3.10+
- **Redmine** 4.0+ (5.0+ for archive/unarchive)
- REST API enabled on your Redmine instance

### Dependencies

| Package         | Version  | Purpose                    |
| --------------- | -------- | -------------------------- |
| `mcp`           | ≥ 1.0.0  | Model Context Protocol SDK |
| `requests`      | ≥ 2.31.0 | HTTP client                |
| `pydantic`      | ≥ 2.0.0  | Data validation            |
| `python-dotenv` | ≥ 1.0.0  | Environment configuration  |

---

## Troubleshooting

| Issue                 | Solution                                                                    |
| --------------------- | --------------------------------------------------------------------------- |
| `ModuleNotFoundError` | Activate your virtual environment and run `pip install -r requirements.txt` |
| API key rejected      | Verify REST API is enabled in Redmine settings                              |
| Connection refused    | Check `REDMINE_URL` — include protocol (`https://`)                         |
| Admin tools fail      | Ensure your API key belongs to an admin user                                |

Set `LOG_LEVEL=DEBUG` in your `.env` file for verbose output.

---

## License

This project is licensed under the [MIT License](LICENSE).

## Links

- [Model Context Protocol](https://modelcontextprotocol.io/) — MCP specification
- [Redmine REST API](https://www.redmine.org/projects/redmine/wiki/Rest_api) — API reference
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) — Official SDK

---

<p align="center">
  <sub>Built with ❤️ for the MCP ecosystem</sub>
</p>
