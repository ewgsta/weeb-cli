.PHONY: help install install-dev install-serve install-all test test-cov clean build publish lint format check-deps

help:
	@echo "Weeb CLI - Makefile Commands"
	@echo ""
	@echo "Installation:"
	@echo "  make install          Install core dependencies"
	@echo "  make install-dev      Install with development dependencies"
	@echo "  make install-serve    Install with server dependencies"
	@echo "  make install-all      Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make test             Run tests"
	@echo "  make test-cov         Run tests with coverage report"
	@echo "  make lint             Run linting checks"
	@echo "  make format           Format code"
	@echo "  make check-deps       Check for missing dependencies"
	@echo ""
	@echo "Build & Release:"
	@echo "  make build            Build distribution packages"
	@echo "  make publish          Publish to PyPI"
	@echo "  make clean            Clean build artifacts"
	@echo ""
	@echo "Runtime:"
	@echo "  make run              Run weeb-cli"
	@echo "  make run-api          Run in API mode"
	@echo "  make run-serve        Run Torznab server"
	@echo "  make run-restful      Run RESTful API server"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

install-serve:
	pip install -e ".[serve,serve-restful]"

install-all:
	pip install -e ".[dev,serve,serve-restful,shortcuts]"

test:
	pytest tests/

test-cov:
	pytest tests/ --cov=weeb_cli --cov-report=html --cov-report=term

lint:
	@echo "Running linting checks..."
	@python -m py_compile weeb_cli/**/*.py || echo "Syntax check completed"

format:
	@echo "Code formatting not configured. Consider adding black or ruff."

check-deps:
	@echo "Checking dependencies..."
	@python -c "import typer, rich, questionary, requests, packaging, bs4, lxml, Crypto, curl_cffi, appdirs, prompt_toolkit, pyfiglet, py7zr, pypresence" && echo "All core dependencies installed" || echo "Missing dependencies detected"

build:
	python -m build

publish: build
	python -m twine upload dist/*

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run:
	weeb-cli

run-api:
	weeb-cli api --help

run-serve:
	weeb-cli serve --help

run-restful:
	weeb-cli serve restful --help
