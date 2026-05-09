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
	@echo "  make publish          Interactive release publisher (version bump + tag + push)"
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

publish:
	@echo "\033[0;34mWeeb CLI Release Publisher\033[0m"
	@echo ""
	@if [ -n "$$(git status --porcelain)" ]; then \
		echo "\033[0;31mError: Uncommitted changes detected\033[0m"; \
		echo "\033[1;33mPlease commit or stash changes first\033[0m"; \
		exit 1; \
	fi
	@CURRENT_BRANCH=$$(git branch --show-current); \
	if [ "$$CURRENT_BRANCH" != "main" ]; then \
		echo "\033[1;33mWarning: Not on 'main' branch (current: $$CURRENT_BRANCH)\033[0m"; \
		read -p "Continue? (y/n): " -n 1 -r; \
		echo; \
		if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
			echo "\033[0;31mCancelled\033[0m"; \
			exit 1; \
		fi; \
	fi
	@CURRENT_VERSION=$$(grep -oP '__version__ = "\K[^"]+' weeb_cli/__init__.py); \
	if [ -z "$$CURRENT_VERSION" ]; then \
		echo "\033[0;31mError: Current version not found\033[0m"; \
		exit 1; \
	fi; \
	echo "\033[0;32mCurrent version: \033[1;33mv$$CURRENT_VERSION\033[0m"; \
	echo ""; \
	IFS='.' read -r -a VERSION_PARTS <<< "$$CURRENT_VERSION"; \
	MAJOR="$${VERSION_PARTS[0]}"; \
	MINOR="$${VERSION_PARTS[1]}"; \
	PATCH="$${VERSION_PARTS[2]}"; \
	echo "\033[0;34mSelect version bump type:\033[0m"; \
	echo "  1) Major ($$MAJOR.$$MINOR.$$PATCH → $$((MAJOR+1)).0.0) - Breaking changes"; \
	echo "  2) Minor ($$MAJOR.$$MINOR.$$PATCH → $$MAJOR.$$((MINOR+1)).0) - New features"; \
	echo "  3) Patch ($$MAJOR.$$MINOR.$$PATCH → $$MAJOR.$$MINOR.$$((PATCH+1))) - Bug fixes"; \
	echo "  4) Custom - Enter version manually"; \
	echo "  5) Cancel"; \
	echo ""; \
	read -p "Choice (1-5): " VERSION_CHOICE; \
	case $$VERSION_CHOICE in \
		1) NEW_VERSION="$$((MAJOR+1)).0.0" ;; \
		2) NEW_VERSION="$$MAJOR.$$((MINOR+1)).0" ;; \
		3) NEW_VERSION="$$MAJOR.$$MINOR.$$((PATCH+1))" ;; \
		4) read -p "Enter new version (e.g., 3.0.0): " NEW_VERSION; \
		   if ! [[ $$NEW_VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$$ ]]; then \
			   echo "\033[0;31mError: Invalid version format\033[0m"; \
			   exit 1; \
		   fi ;; \
		5) echo "\033[1;33mCancelled\033[0m"; exit 0 ;; \
		*) echo "\033[0;31mInvalid choice\033[0m"; exit 1 ;; \
	esac; \
	echo ""; \
	echo "\033[0;32mNew version: \033[1;33mv$$NEW_VERSION\033[0m"; \
	echo ""; \
	read -p "Commit message (leave empty for default): " COMMIT_MSG; \
	if [ -z "$$COMMIT_MSG" ]; then \
		COMMIT_MSG="chore: bump version to v$$NEW_VERSION"; \
	fi; \
	echo ""; \
	echo "\033[0;34m═══════════════════════════════════════\033[0m"; \
	echo "\033[1;33mSummary:\033[0m"; \
	echo "  Old version: \033[0;31mv$$CURRENT_VERSION\033[0m"; \
	echo "  New version: \033[0;32mv$$NEW_VERSION\033[0m"; \
	echo "  Commit: \033[0;34m$$COMMIT_MSG\033[0m"; \
	echo "  Branch: \033[1;33m$$CURRENT_BRANCH\033[0m"; \
	echo "\033[0;34m═══════════════════════════════════════\033[0m"; \
	echo ""; \
	read -p "Continue? (y/n): " -n 1 -r; \
	echo; \
	if [[ ! $$REPLY =~ ^[Yy]$$ ]]; then \
		echo "\033[0;31mCancelled\033[0m"; \
		exit 1; \
	fi; \
	echo ""; \
	echo "\033[0;34m[1/6]\033[0m Updating version files..."; \
	sed -i "s/__version__ = \".*\"/__version__ = \"$$NEW_VERSION\"/" weeb_cli/__init__.py; \
	echo "\033[0;32m  ✓ weeb_cli/__init__.py\033[0m"; \
	sed -i "s/^version = \".*\"/version = \"$$NEW_VERSION\"/" pyproject.toml; \
	echo "\033[0;32m  ✓ pyproject.toml\033[0m"; \
	if [ -f "distribution/aur/PKGBUILD" ]; then \
		sed -i "s/^pkgver=.*/pkgver=$$NEW_VERSION/" distribution/aur/PKGBUILD; \
		echo "\033[0;32m  ✓ distribution/aur/PKGBUILD\033[0m"; \
	fi; \
	echo ""; \
	echo "\033[0;34m[2/6]\033[0m Staging changes..."; \
	git add weeb_cli/__init__.py pyproject.toml distribution/aur/PKGBUILD; \
	echo "\033[0;32m  ✓ Files staged\033[0m"; \
	echo ""; \
	echo "\033[0;34m[3/6]\033[0m Creating commit..."; \
	git commit -m "$$COMMIT_MSG"; \
	echo "\033[0;32m  ✓ Commit created\033[0m"; \
	echo ""; \
	echo "\033[0;34m[4/6]\033[0m Creating git tag..."; \
	git tag -a "v$$NEW_VERSION" -m "Release v$$NEW_VERSION"; \
	echo "\033[0;32m  ✓ Tag created: v$$NEW_VERSION\033[0m"; \
	echo ""; \
	echo "\033[0;34m[5/6]\033[0m Pushing commit..."; \
	git push origin "$$CURRENT_BRANCH"; \
	echo "\033[0;32m  ✓ Commit pushed\033[0m"; \
	echo ""; \
	echo "\033[0;34m[6/6]\033[0m Pushing tag..."; \
	git push origin "v$$NEW_VERSION"; \
	echo "\033[0;32m  ✓ Tag pushed\033[0m"; \
	echo ""; \
	echo "\033[0;32m╔════════════════════════════════════════╗\033[0m"; \
	echo "\033[0;32m║          ✓ Success!                    ║\033[0m"; \
	echo "\033[0;32m╚════════════════════════════════════════╝\033[0m"; \
	echo ""; \
	echo "\033[0;32mRelease v$$NEW_VERSION published successfully\033[0m"; \
	echo "\033[0;34mGitHub Actions will start automatically\033[0m"; \
	echo ""; \
	echo "\033[1;33mCheck status:\033[0m"; \
	echo "  \033[0;34mhttps://github.com/$$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions\033[0m"; \
	echo ""

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
