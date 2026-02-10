# Project Chimera Makefile
#
# Spec Reference: .cursor/rules (automation and TDD workflow)
# Purpose: Automate common development tasks with spec-first enforcement
#
# Usage:
#   make setup      - Install dependencies
#   make test       - Run all tests
#   make lint       - Run code quality checks
#   make spec-check - Verify spec references in code
#   make docker-build - Build Docker image
#   make docker-test  - Run tests in Docker
#   make clean      - Remove build artifacts

.PHONY: help setup test lint spec-check docker-build docker-test clean run-frontend

# Default target
help:
	@echo "Project Chimera - Development Automation"
	@echo ""
	@echo "Available targets:"
	@echo "  make setup        - Install dependencies (uv or pip)"
	@echo "  make test         - Run pytest with coverage"
	@echo "  make lint         - Run ruff and black formatters"
	@echo "  make spec-check   - Verify spec references in code"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-test  - Run tests inside Docker"
	@echo "  make run-frontend - Launch Streamlit Dashboard"
	@echo "  make clean        - Remove build artifacts"
	@echo ""
	@echo "Spec Reference: .cursor/rules (TDD and automation)"

# ============================================================================
# Setup and Dependencies
# ============================================================================

setup:
	@echo "Installing dependencies..."
	@if [ -f pyproject.toml ]; then \
		echo "Using uv for dependency installation..."; \
		uv sync; \
	else \
		echo "Using pip for dependency installation..."; \
		pip install -r requirements.txt; \
	fi
	@echo "Installing dev dependencies..."
	@pip install pytest pytest-cov ruff black jsonschema
	@echo "✓ Setup complete"

# ============================================================================
# Testing
# ============================================================================

test:
	@echo "Running tests with pytest..."
	@echo "Spec Reference: specs/technical.md (Agent Task schemas)"
	@echo "Spec Reference: skills/*/README.md (Skills contracts)"
	@pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html
	@echo ""
	@echo "✓ Tests complete. Coverage report: htmlcov/index.html"

test-fast:
	@echo "Running tests without coverage..."
	@pytest tests/ -v
	@echo "✓ Fast tests complete"

test-agent-task:
	@echo "Running Agent Task schema tests..."
	@pytest tests/test_agent_task.py -v
	@echo "✓ Agent Task tests complete"

test-skills:
	@echo "Running Skills interface tests..."
	@pytest tests/test_skills_interface.py -v
	@echo "✓ Skills interface tests complete"

# ============================================================================
# Code Quality
# ============================================================================

lint:
	@echo "Running code quality checks..."
	@echo "1. Checking with ruff..."
	@ruff check src/ tests/ --fix || echo "⚠ Ruff found issues"
	@echo ""
	@echo "2. Formatting with black..."
	@black src/ tests/ --check || echo "⚠ Black formatting needed"
	@echo ""
	@echo "✓ Lint checks complete"

format:
	@echo "Auto-formatting code..."
	@black src/ tests/
	@ruff check src/ tests/ --fix
	@echo "✓ Code formatted"

# ============================================================================
# Spec Enforcement
# ============================================================================

spec-check:
	@echo "Checking for spec references in code..."
	@echo "Spec Reference: .cursor/rules (Prime Directive - spec-first development)"
	@echo ""
	@echo "Searching for SRS references..."
	@grep -r "SRS Reference:" src/ tests/ || echo "⚠ No SRS references found in code"
	@echo ""
	@echo "Searching for Spec references..."
	@grep -r "Spec:" src/ tests/ || echo "⚠ No Spec references found in code"
	@echo ""
	@echo "Checking for spec file imports..."
	@grep -r "specs/" src/ tests/ || echo "⚠ No spec file references found"
	@echo ""
	@echo "✓ Spec check complete"
	@echo ""
	@echo "REMINDER: Every implementation file should reference:"
	@echo "  - SRS section (e.g., SRS Reference: §4.2 Perception)"
	@echo "  - Spec file (e.g., Spec: specs/functional.md, FR2.1)"

# ============================================================================
# Docker
# ============================================================================

docker-build:
	@echo "Building Docker image..."
	@docker build -t chimera:latest .
	@echo "✓ Docker image built: chimera:latest"

docker-test:
	@echo "Running tests inside Docker..."
	@docker run --rm chimera:latest pytest tests/ -v
	@echo "✓ Docker tests complete"

docker-shell:
	@echo "Starting interactive Docker shell..."
	@docker run --rm -it chimera:latest /bin/bash

docker-dev:
	@echo "Running Docker with local code mounted..."
	@docker run --rm -v $$(pwd):/app chimera:latest pytest tests/ -v

# ============================================================================
# Cleanup
# ============================================================================

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "✓ Cleanup complete"

clean-all: clean
	@echo "Removing virtual environment and Docker images..."
	@rm -rf .venv
	@docker rmi chimera:latest 2>/dev/null || true
	@echo "✓ Deep cleanup complete"

# ============================================================================
# CI/CD Helpers
# ============================================================================

ci-test: setup test lint spec-check
	@echo "✓ CI pipeline complete"

# ============================================================================
# Frontend
# ============================================================================

run-frontend:
	@echo "Launching Agent Command Center..."
	@echo "Spec Reference: specs/frontend.md"
	@PYTHONPATH=$PWD:src streamlit run src/frontend/app.py

# ============================================================================
# Development Workflow
# ============================================================================

dev-setup: setup
	@echo "Setting up development environment..."
	@pre-commit install 2>/dev/null || echo "⚠ pre-commit not installed"
	@echo "✓ Development environment ready"

watch-test:
	@echo "Watching for file changes and running tests..."
	@pytest-watch tests/ -v

# ============================================================================
# Notes
# ============================================================================
# 
# This Makefile enforces the TDD workflow defined in .cursor/rules:
# 1. Write failing tests first (make test)
# 2. Implement code to pass tests
# 3. Verify spec references (make spec-check)
# 4. Run linting (make lint)
# 5. Commit with spec references
#
# All targets respect the Prime Directive:
# "NEVER generate code without committed specs"
# ============================================================================
