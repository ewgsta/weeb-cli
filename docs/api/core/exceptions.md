# Exceptions Module

::: weeb_cli.exceptions
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

Custom exception hierarchy for structured error handling throughout Weeb CLI. All exceptions inherit from `WeebCLIError` base class.

## Exception Hierarchy

```
WeebCLIError (base)
├── ProviderError
├── DownloadError
├── NetworkError
├── AuthenticationError
├── DatabaseError
├── ValidationError
└── DependencyError
```

## Usage Examples

### Raising Exceptions

```python
from weeb_cli.exceptions import ProviderError, DownloadError

# With message only
raise ProviderError("Failed to fetch anime details")

# With error code
raise ProviderError("Search failed", code="PROVIDER_001")

# Download errors
raise DownloadError("Insufficient disk space", code="DISK_FULL")
```

### Catching Exceptions

```python
from weeb_cli.exceptions import (
    ProviderError, 
    NetworkError, 
    WeebCLIError
)

try:
    provider.search("anime")
except ProviderError as e:
    print(f"Provider error: {e.message} ({e.code})")
except NetworkError as e:
    print(f"Network error: {e.message}")
except WeebCLIError as e:
    print(f"General error: {e}")
```

### Specific Exception Handling

```python
from weeb_cli.exceptions import (
    AuthenticationError,
    DatabaseError,
    ValidationError
)

# Authentication
try:
    tracker.authenticate()
except AuthenticationError as e:
    print(f"Auth failed: {e.message}")
    # Re-authenticate

# Database
try:
    db.save_progress()
except DatabaseError as e:
    print(f"Database error: {e.code}")
    # Retry or backup

# Validation
try:
    validate_input(user_input)
except ValidationError as e:
    print(f"Invalid input: {e.message}")
    # Prompt again
```

## Exception Types

### WeebCLIError

Base exception for all Weeb CLI errors. Provides structured error handling with optional error codes.

**Attributes:**
- `message` (str): Human-readable error message
- `code` (str): Optional error code for categorization

### ProviderError

Raised for anime provider-related errors:
- Search failures
- Failed to fetch anime details
- Episode list unavailable
- Stream extraction errors

### DownloadError

Raised for download operation failures:
- Network issues during download
- Insufficient disk space
- Invalid stream URLs
- Aria2/yt-dlp errors

### NetworkError

Raised for network connectivity issues:
- HTTP request failures
- Connection timeouts
- DNS resolution errors
- Network unavailable

### AuthenticationError

Raised for tracker authentication failures:
- OAuth flow errors
- Invalid credentials
- Token expiration
- API authentication failures

### DatabaseError

Raised for database operation errors:
- SQLite errors
- Database corruption
- Migration failures
- Query errors

### ValidationError

Raised for input validation failures:
- Invalid configuration values
- Malformed user input
- Invalid file paths
- URL validation errors

### DependencyError

Raised for external dependency issues:
- Missing required tools (FFmpeg, MPV, Aria2)
- Tool execution failures
- Version incompatibilities
- Installation errors

## Error Codes

Common error codes used throughout the application:

| Code | Exception | Description |
|------|-----------|-------------|
| `PROVIDER_001` | ProviderError | Search failed |
| `PROVIDER_002` | ProviderError | Details fetch failed |
| `PROVIDER_003` | ProviderError | Stream extraction failed |
| `DOWNLOAD_001` | DownloadError | Disk space insufficient |
| `DOWNLOAD_002` | DownloadError | Download failed |
| `NETWORK_001` | NetworkError | Connection timeout |
| `AUTH_001` | AuthenticationError | OAuth failed |
| `DB_001` | DatabaseError | Query failed |
| `VALIDATION_001` | ValidationError | Invalid input |
| `DEP_001` | DependencyError | Tool missing |

## Best Practices

1. **Use Specific Exceptions**: Catch specific exceptions before general ones
2. **Include Error Codes**: Use error codes for logging and debugging
3. **Provide Context**: Include relevant information in error messages
4. **Handle Gracefully**: Provide fallback behavior when possible
5. **Log Errors**: Log exceptions with full context for debugging

## API Reference

::: weeb_cli.exceptions.WeebCLIError
::: weeb_cli.exceptions.ProviderError
::: weeb_cli.exceptions.DownloadError
::: weeb_cli.exceptions.NetworkError
::: weeb_cli.exceptions.AuthenticationError
::: weeb_cli.exceptions.DatabaseError
::: weeb_cli.exceptions.ValidationError
::: weeb_cli.exceptions.DependencyError
