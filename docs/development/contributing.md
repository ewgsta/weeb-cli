# Contributing to Weeb CLI

Thank you for your interest in contributing to Weeb CLI! This guide will help you get started.

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git
- pip or pipenv

### Clone and Install

```bash
# Clone the repository
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=weeb_cli --cov-report=html

# Run specific test file
pytest tests/test_providers.py
```

## Code Style

### Python Style Guide

We follow PEP 8 with some modifications:

- Line length: 100 characters (not 79)
- Use type hints for all function signatures
- Use docstrings (Google style) for all public functions and classes

### Type Hints

All functions should have type hints:

```python
def search(self, query: str) -> List[AnimeResult]:
    """Search for anime by query.
    
    Args:
        query: Search query string.
    
    Returns:
        List of anime search results.
    """
    pass
```

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1.
        param2: Description of param2.
    
    Returns:
        Description of return value.
    
    Raises:
        ValueError: When param1 is invalid.
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

## Adding a New Provider

### 1. Create Provider File

Create a new file in the appropriate language directory:

```
weeb_cli/providers/<lang>/<provider_name>.py
```

### 2. Implement Provider Class

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.providers.registry import register_provider
from typing import List, Optional

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    """Provider for MyAnimeSource.com.
    
    Provides anime content from MyAnimeSource with search,
    details, and stream extraction.
    """
    
    BASE_URL = "https://myanime source.com"
    
    def search(self, query: str) -> List[AnimeResult]:
        """Search for anime."""
        # Implementation
        pass
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Get anime details."""
        # Implementation
        pass
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Get episode list."""
        # Implementation
        pass
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Extract stream URLs."""
        # Implementation
        pass
```

### 3. Add Tests

Create test file in `tests/`:

```python
import pytest
from weeb_cli.providers import get_provider

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
    assert results[0].title is not None
```

### 4. Update Documentation

Add provider documentation in `docs/api/providers/`.

## Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Make Changes

- Write code following style guidelines
- Add type hints and docstrings
- Write tests for new functionality
- Update documentation

### 3. Test Your Changes

```bash
# Run tests
pytest

# Check code style
flake8 weeb_cli/

# Type checking (optional)
mypy weeb_cli/
```

### 4. Commit Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new provider for XYZ"
git commit -m "fix: resolve stream extraction issue"
git commit -m "docs: update installation guide"
```

Commit types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### 5. Push and Create PR

```bash
git push origin feature/my-new-feature
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Reference to related issues
- Screenshots (if UI changes)

## Code Review

All submissions require review. We'll review your PR and may request changes. Please be patient and responsive to feedback.

## Community Guidelines

- Be respectful and constructive
- Help others in discussions
- Report bugs with detailed information
- Suggest features with clear use cases

## Questions?

- Open an issue for bugs or feature requests
- Start a discussion for questions
- Check existing issues before creating new ones

Thank you for contributing to Weeb CLI!
