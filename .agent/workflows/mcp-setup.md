---
description: MCP server configuration and usage
---

# MCP Server Setup and Usage

## What is MCP?

Model Context Protocol (MCP) allows AI assistants to connect to external servers that provide specialized tools and resources. For this challenge, the `tenxfeedbackanalytics` server tracks your work and provides feedback analytics.

## Current Configuration

### tenxfeedbackanalytics Server
- **URL**: https://mcppulse.10academy.org/proxy
- **Type**: HTTP Proxy
- **Purpose**: Tracks your development activity, git commits, file changes, and provides analytics
- **Status**: ✅ Connected (session: mcpsess_0a1b2c3d)

### Configuration Files
- **Antigravity**: `.antigravity/mcp.json` (X-Coding-Tool: antigravity)
- **VS Code**: `.vscode/mcp.json` (X-Coding-Tool: vscode)

## What the MCP Server Tracks

Based on `tenx_mcp_sense_log.txt`, the server monitors:
- ✅ File creation and modifications
- ✅ Git commits and patches
- ✅ Todo list updates
- ✅ Notebook inspections
- ✅ Data loading events
- ✅ Analysis completions

## How to Use MCP Tools

### In Antigravity (this AI assistant)
The MCP server connection is automatic when configured. The server passively tracks your work.

### Checking MCP Status
Review the log file:
```powershell
Get-Content tenx_mcp_sense_log.txt
```

## Adding More MCP Servers

To add additional MCP servers, edit `.antigravity/mcp.json` or `.vscode/mcp.json`:

```json
{
    "servers": {
        "tenxfeedbackanalytics": { ... },
        "new-server-name": {
            "url": "https://example.com/mcp",
            "type": "http",
            "headers": {
                "Authorization": "Bearer YOUR_TOKEN"
            }
        }
    },
    "inputs": []
}
```

## Troubleshooting

- **Server not connecting**: Check network connectivity and URL
- **Missing events**: Ensure git commits are being made
- **Session expired**: Restart your coding tool to re-establish connection
