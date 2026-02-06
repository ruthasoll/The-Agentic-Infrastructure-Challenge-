# The Agentic Infrastructure Challenge

A 10 Academy challenge focused on building agentic infrastructure with AI-powered development tools and MCP integration.

## Quick Start

### 1. Activate Virtual Environment
```powershell
& .venv/Scripts/Activate.ps1
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 3. Update pip (optional)
```powershell
python.exe -m pip install --upgrade pip
```

## Project Structure

```
.
├── .agent/workflows/     # Workflow documentation
├── .antigravity/         # Antigravity AI configuration
├── .vscode/              # VS Code configuration
├── communication/        # Client communications
├── data/                 # Data files
├── notebook/             # Jupyter notebooks
├── research/             # Research notes
├── specs/                # Specifications
├── task1/                # Task implementations
└── tests/                # Test files
```

## MCP Integration

This project uses the **tenxfeedbackanalytics** MCP server to track development activity and provide feedback analytics.

- **Status**: Connected (session: mcpsess_0a1b2c3d)
- **Logs**: See `tenx_mcp_sense_log.txt`
- **Config**: `.antigravity/mcp.json` and `.vscode/mcp.json`

For more details, see `.agent/workflows/mcp-setup.md`

## Available Workflows

Use the `/` command prefix to access workflows:
- `/tools` - View available tools and commands
- See `.agent/workflows/` for all available workflows

## Development

This project leverages AI-powered development with:
- **Antigravity AI Assistant** - Advanced code generation and analysis
- **MCP Protocol** - External tool and resource integration
- **Automated Tracking** - Development activity monitoring

## Resources

- [10 Academy Challenge Portal](https://10academy.org)
- [MCP Documentation](https://mcppulse.10academy.org)