---
description: Available tools and MCP server information
---

# Available Tools Reference

This document provides an overview of all available tools for working on The Agentic Infrastructure Challenge.

## MCP Servers

### tenxfeedbackanalytics
- **Type**: HTTP Proxy Server
- **URL**: https://mcppulse.10academy.org/proxy
- **Purpose**: 10 Academy feedback analytics and challenge submission tools
- **Configuration**: `.antigravity/mcp.json`

To use MCP server tools, ensure the server is connected and use the `list_resources` or similar commands to discover available tools.

## Built-in AI Assistant Tools

### File Operations
- **view_file** - View file contents with line numbers
- **view_file_outline** - See file structure (classes, functions)
- **view_code_item** - View specific code items (functions, classes)
- **write_to_file** - Create new files
- **replace_file_content** - Edit existing files (single edit)
- **multi_replace_file_content** - Edit existing files (multiple edits)
- **find_by_name** - Search for files by name/pattern
- **grep_search** - Search file contents using patterns
- **list_dir** - List directory contents

### Command Execution
- **run_command** - Execute PowerShell commands
- **send_command_input** - Send input to running processes
- **command_status** - Check background command status
- **read_terminal** - Read terminal output

### Web & Browser
- **browser_subagent** - Automate browser interactions
- **read_url_content** - Fetch content from URLs
- **search_web** - Search the internet

### Development Tools
- **generate_image** - Create images from text descriptions
- **task_boundary** - Track complex tasks with progress updates
- **notify_user** - Request reviews and ask questions during tasks

## Common Workflows

### Activate Virtual Environment
```powershell
& .venv/Scripts/Activate.ps1
```

### Install Dependencies
```powershell
pip install -r requirements.txt
```

### Update pip
```powershell
python.exe -m pip install --upgrade pip
```

## Tips
- Use `/tools` command to view this reference
- MCP servers can provide additional specialized tools
- Check `.antigravity/mcp.json` for MCP server configuration
