---
description: Project setup and common commands
---

# Project Setup Guide

## Initial Setup

### 1. Clone Repository (if not already done)
```powershell
git clone <repository-url>
cd The-Agentic-Infrastructure-Challenge-
```

### 2. Create Virtual Environment
```powershell
python -m venv .venv
```

### 3. Activate Virtual Environment
// turbo
```powershell
& .venv/Scripts/Activate.ps1
```

### 4. Install Dependencies
// turbo
```powershell
pip install -r requirements.txt
```

### 5. Upgrade pip (optional)
// turbo
```powershell
python.exe -m pip install --upgrade pip
```

## Common Commands

### Python Environment
```powershell
# Activate environment
& .venv/Scripts/Activate.ps1

# Deactivate environment
deactivate

# Install package
pip install <package-name>

# Save dependencies
pip freeze > requirements.txt
```

### Jupyter Notebooks
```powershell
# Start Jupyter
jupyter notebook

# Start JupyterLab
jupyter lab
```

### Git Commands
```powershell
# Check status
git status

# Stage changes
git add .

# Commit changes
git commit -m "Your message"

# Push changes
git push
```

### Testing
```powershell
# Run tests
pytest

# Run with coverage
pytest --cov
```

## Project-Specific Commands

### Data Analysis
```powershell
# Run EDA notebook
jupyter notebook notebook/analysis_eda.ipynb
```

### View Logs
```powershell
# View MCP tracking logs
Get-Content tenx_mcp_sense_log.txt

# View git log
git log --oneline
```

## Troubleshooting

### Virtual Environment Issues
If activation fails, ensure execution policy allows scripts:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Package Installation Issues
If pip install fails:
```powershell
# Update pip
python -m pip install --upgrade pip

# Use trusted hosts
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org <package>
```

### MCP Connection Issues
Check the MCP log for errors:
```powershell
Get-Content tenx_mcp_sense_log.txt -Tail 20
```
