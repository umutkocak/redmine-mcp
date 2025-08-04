Collecting workspace information# Redmine MCP Server

> **Version**: 1.0.2 | **Status: Production Ready** 🚀

A comprehensive Model Context Protocol (MCP) server that provides seamless integration with Redmine project management systems. Built using the standard MCP library for reliable and type-safe API interactions.

## 🌟 Features

- **Complete Redmine API Coverage** - Full CRUD operations for projects, issues, users, time entries, and system enumerations
- **MCP Standard Compliant** - Built with official MCP library for guaranteed compatibility
- **Docker Ready** - Optimized for containerization with security and performance best practices
- **Type-Safe Architecture** - Comprehensive type hints and Pydantic validation
- **Production Ready** - Robust error handling, logging, and monitoring capabilities
- **Flexible Configuration** - Environment-based setup with multiple deployment options

## 🚀 Quick Start

### Option 1: Docker (Recommended)
```bash
git clone https://github.com/umutkocak/redmine-mcp.git
cd redmine-mcp
cp .env.example .env
# Edit .env with your Redmine credentials
docker build -t redmine-mcp .
docker run -it --env-file .env redmine-mcp
```

### Option 2: Local Installation
```bash
git clone https://github.com/umutkocak/redmine-mcp.git
cd redmine-mcp
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your settings
python src/main.py
```

## 📦 Supported Operations

### Projects
- `list_projects` - List all projects with filtering and pagination
- `get_project` - Get detailed information about a specific project

### Issues
- `list_issues` - List and filter issues (by project, assignee, status, priority, etc.)
- `get_issue` - Get issue details including comments, attachments, and history
- `create_issue` - Create new issues with full metadata support
- `update_issue` - Update issues (change status, add comments, reassign, etc.)

### Users
- `list_users` - List users with status filtering
- `get_user` - Get user details and information

### Time Entries
- `list_time_entries` - List time entries with user, project, and date filters

### System Enumerations
- `list_enumerations` - Get system constants (statuses, priorities, trackers, activities)

## 🔧 Configuration

### Environment Variables

Create a .env file in the project root:

```env
REDMINE_URL=https://your-redmine-server.example.com
REDMINE_API_KEY=your_api_key_here_example_12345
LOG_LEVEL=INFO
```

### Getting Redmine API Key

1. Go to **Administration > Settings > Authentication** in Redmine
2. Enable **REST web service** option
3. Create an **API access key** in your user profile
4. Add this key to your .env file

## 🐳 Docker Deployment

### Basic Docker Run
```bash
docker build -t redmine-mcp .
docker run -it --env-file .env redmine-mcp
```

### Docker Compose (Recommended for Production)
```bash
cp .env.example .env
# Edit .env with your settings
docker-compose up -d

# Check logs
docker-compose logs -f redmine-mcp
```

## 🛠️ Local Development Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
.venv\Scripts\activate     # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development tools
```

### 3. Environment Configuration

```bash
cp .env.example .env
# Edit the .env file with your settings
```

### 4. Running in Development Mode

```bash
python src/debug_main.py  # For detailed logging and debugging
# OR
python src/main.py        # Standard execution
```

## 🎯 Claude Desktop Integration

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "redmine-mcp": {
      "command": "/path/to/your/project/.venv/Scripts/python.exe",
      "args": ["/path/to/your/project/src/main.py"],
      "env": {
        "REDMINE_URL": "https://your-redmine-server.example.com",
        "REDMINE_API_KEY": "your_api_key_here_example_12345",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

## 🎯 Claude Desktop Integration with Docker

Add to your Claude Desktop with Docker configuration:

```json
{
  "mcpServers": {
    "redmine-mcp": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "--name", "redmine-mcp",
        "-e", "REDMINE_URL=https://your-redmine-server.example.com",
        "-e", "REDMINE_API_KEY=your_api_key_here_example_12345",
        "-e", "LOG_LEVEL=INFO",
        "redmine-mcp:latest"
      ]
    }
  }
}
```



**Config file locations:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

## 📝 API Examples

### List Projects
```json
{
  "limit": 10,
  "include_archived": true
}
```

### Get Project Details
```json
{
  "project_id": 1
}
```

### Create Issue
```json
{
  "issue": {
    "project_id": 1,
    "subject": "Issue title",
    "description": "Issue description with **Markdown** support",
    "tracker_id": 2,
    "priority_id": 3,
    "assigned_to_id": 5,
    "start_date": "2025-08-10",
    "due_date": "2025-08-15",
    "custom_fields": [
      {"id": 1, "value": "example_value"}
    ]
  }
}
```

### Update Issue
```json
{
  "issue_id": 123,
  "issue": {
    "subject": "Updated title",
    "status_id": 3,
    "notes": "Progress update - work is 50% complete"
  }
}
```

### List Time Entries
```json
{
  "user_id": 5,
  "from_date": "2025-08-01",
  "to_date": "2025-08-31",
  "limit": 50
}
```

## 🐛 Troubleshooting

### Common Issues

- **ModuleNotFoundError**: Activate virtual environment and run `pip install -r requirements.txt`
- **API Key Error**: Check .env file and ensure REST API is enabled in Redmine
- **Connection Error**: Verify Redmine URL is accessible and protocol (HTTP/HTTPS) is correct
- **Import Errors**: Ensure you're running the scripts from the project root directory

### Debug Mode

Set `LOG_LEVEL=DEBUG` in your .env file for detailed logging.

For advanced debugging:
```bash
python src/debug_main.py
```

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- [Model Context Protocol](https://modelcontextprotocol.io/) - Claude AI integration framework
- [Redmine](https://www.redmine.org/) - Open source project management tool

---

**Current Version:** 1.0.2 | **Last Updated:** August 2025