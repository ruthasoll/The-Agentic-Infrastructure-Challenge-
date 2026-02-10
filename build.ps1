# Project Chimera Build Script (Powershell)
# 
# Spec Reference: .cursor/rules (automation and TDD workflow)
# Purpose: Automate common development tasks on Windows (Makefile equivalent)
#
# Usage:
#   .\build.ps1 setup      - Install dependencies
#   .\build.ps1 test       - Run all tests
#   .\build.ps1 lint       - Run code quality checks
#   .\build.ps1 spec-check - Verify spec references in code
#   .\build.ps1 docker-build - Build Docker image
#   .\build.ps1 help       - Show help

param (
    [string]$Target = "help"
)

$ErrorActionPreference = "Stop"

function Show-Help {
    Write-Host "Project Chimera - Windows Development Automation" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available targets:" -ForegroundColor Yellow
    Write-Host "  .\build.ps1 setup        - Install dependencies (uv or pip)"
    Write-Host "  .\build.ps1 test         - Run pytest with coverage"
    Write-Host "  .\build.ps1 lint         - Run ruff and black formatters"
    Write-Host "  .\build.ps1 spec-check   - Verify spec references in code"
    Write-Host "  .\build.ps1 docker-build - Build Docker image"
    Write-Host "  .\build.ps1 run-frontend - Launch Streamlit Dashboard"
    Write-Host "  .\build.ps1 clean        - Remove build artifacts"
    Write-Host ""
    Write-Host "Spec Reference: .cursor/rules (TDD and automation)" -ForegroundColor Gray
}

function Run-Setup {
    Write-Host "Installing dependencies..." -ForegroundColor Cyan
    if (Test-Path "pyproject.toml") {
        Write-Host "Using uv for dependency installation..." -ForegroundColor Green
        uv sync
    } else {
        Write-Host "Using pip for dependency installation..." -ForegroundColor Green
        pip install -r requirements.txt
    }
    Write-Host "Installing dev dependencies..." -ForegroundColor Cyan
    pip install pytest pytest-cov ruff black jsonschema
    Write-Host "✓ Setup complete" -ForegroundColor Green
}

function Run-Test {
    Write-Host "Running tests with pytest..." -ForegroundColor Cyan
    Write-Host "Spec Reference: specs/technical.md (Agent Task schemas)" -ForegroundColor Gray
    Write-Host "Spec Reference: skills/*/README.md (Skills contracts)" -ForegroundColor Gray
    
    # Ensure src is in PYTHONPATH
    $env:PYTHONPATH = "$PWD;src"
    
    # Run pytest directly
    python -m pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Tests complete. Coverage report: htmlcov/index.html" -ForegroundColor Green
    } else {
        Write-Host "`n❌ Tests failed!" -ForegroundColor Red
        exit 1
    }
}

function Run-Lint {
    Write-Host "Running code quality checks..." -ForegroundColor Cyan
    
    Write-Host "1. Checking with ruff..." -ForegroundColor Yellow
    try { ruff check src/ tests/ --fix } catch { Write-Host "⚠ Ruff found issues" -ForegroundColor Yellow }
    
    Write-Host "`n2. Formatting with black..." -ForegroundColor Yellow
    try { black src/ tests/ --check } catch { Write-Host "⚠ Black formatting needed" -ForegroundColor Yellow }
    
    Write-Host "`n✓ Lint checks complete" -ForegroundColor Green
}

function Run-SpecCheck {
    Write-Host "Checking for spec references in code..." -ForegroundColor Cyan
    Write-Host "Spec Reference: .cursor/rules (Prime Directive - spec-first development)" -ForegroundColor Gray
    
    $srcFiles = Get-ChildItem -Path src, tests -Recurse -Filter "*.py"
    $missingSRS = 0
    $missingSpec = 0
    
    if ($srcFiles) {
        foreach ($file in $srcFiles) {
            $content = Get-Content $file.FullName -Raw
            if ($content -notmatch "SRS Reference:") {
                Write-Host "⚠ No SRS references found in $($file.Name)" -ForegroundColor Yellow
                $missingSRS++
            }
            if ($content -notmatch "Spec:") {
                Write-Host "⚠ No Spec references found in $($file.Name)" -ForegroundColor Yellow
                $missingSpec++
            }
        }
    }
    
    if ($missingSRS -eq 0 -and $missingSpec -eq 0) {
        Write-Host "`n✓ Spec check complete - All files adhere to traceability rules" -ForegroundColor Green
    } else {
        Write-Host "`n⚠ Found files missing spec references!" -ForegroundColor Yellow
        Write-Host "REMINDER: Every implementation file should reference:"
        Write-Host "  - SRS section (e.g., SRS Reference: §4.2 Perception)"
        Write-Host "  - Spec file (e.g., Spec: specs/functional.md, FR2.1)"
    }
}

function Run-DockerBuild {
    Write-Host "Building Docker image..." -ForegroundColor Cyan
    docker build -t chimera:latest .
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Docker image built: chimera:latest" -ForegroundColor Green
    } else {
        Write-Host "❌ Docker build failed!" -ForegroundColor Red
        exit 1
    }
}

function Run-Frontend {
    Write-Host "Launching Agent Command Center..." -ForegroundColor Cyan
    Write-Host "Spec Reference: specs/frontend.md" -ForegroundColor Gray
    
    # Ensure src is in PYTHONPATH
    $env:PYTHONPATH = "$PWD;src"
    
    python -m streamlit run src/frontend/app.py
}

function Run-Clean {
    Write-Host "Cleaning build artifacts..." -ForegroundColor Cyan
    Remove-Item -Path .pytest_cache, .ruff_cache, htmlcov, .coverage, __pycache__ -Recurse -Force -ErrorAction SilentlyContinue 2>$null
    Get-ChildItem -Path . -Include "__pycache__" -Recurse | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue 2>$null
    Get-ChildItem -Path . -Include "*.pyc" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue 2>$null
    Write-Host "✓ Cleanup complete" -ForegroundColor Green
}

# Main execution logic
if ($Target -eq "setup") { Run-Setup }
elseif ($Target -eq "test") { Run-Test }
elseif ($Target -eq "lint") { Run-Lint }
elseif ($Target -eq "spec-check") { Run-SpecCheck }
elseif ($Target -eq "docker-build") { Run-DockerBuild }
elseif ($Target -eq "run-frontend") { Run-Frontend }
elseif ($Target -eq "clean") { Run-Clean }
else { Show-Help }
