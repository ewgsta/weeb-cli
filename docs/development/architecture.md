# Architecture Overview

This document provides a high-level overview of Weeb CLI's architecture and design decisions.

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     CLI Layer (Typer)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Search  │  │Downloads │  │ Watchlist│  │Settings │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Service Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Downloader│  │ Tracker  │  │  Player  │  │  Cache  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Database │  │  Scraper │  │  Logger  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                   Provider Layer                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Turkish   │  │ English  │  │  German  │  │ Polish  │ │
│  │Providers │  │Providers │  │Providers │  │Providers│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Data Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  SQLite  │  │   Cache  │  │   Logs   │              │
│  │ Database │  │  Files   │  │  Files   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## Design Patterns

### 1. Registry Pattern (Providers)

Providers are automatically discovered and registered using decorators:

```python
@register_provider("animecix", lang="tr", region="TR")
class AnimecixProvider(BaseProvider):
    pass
```

**Benefits:**
- Easy to add new providers
- No manual registration needed
- Automatic discovery from filesystem

### 2. Lazy Loading (Services)

Services use lazy loading to defer initialization:

```python
@property
def db(self):
    if self._db is None:
        from weeb_cli.services.database import db
        self._db = db
    return self._db
```

**Benefits:**
- Faster startup time
- Reduced memory usage
- Avoid circular imports

### 3. Singleton Pattern (Global Instances)

Global instances for shared resources:

```python
config = Config()
i18n = I18n()
cache = CacheManager()
```

**Benefits:**
- Single source of truth
- Easy access throughout application
- Consistent state

### 4. Strategy Pattern (Download Methods)

Multiple download strategies with fallback:

```python
def _try_download(self, url, path, item):
    strategies = [
        self._download_aria2,
        self._download_ytdlp,
        self._download_ffmpeg,
        self._download_generic
    ]
    for strategy in strategies:
        if strategy(url, path, item):
            return True
    return False
```

**Benefits:**
- Graceful degradation
- Flexible download methods
- Easy to add new strategies

## Key Components

### CLI Layer

**Technology:** Typer + Rich + Questionary

**Responsibilities:**
- Parse command-line arguments
- Display interactive menus
- Handle user input
- Show progress indicators

### Service Layer

**Core Services:**

1. **Database**: SQLite with WAL mode
   - Configuration storage
   - Progress tracking
   - Download queue
   - Local library index

2. **Downloader**: Queue-based download manager
   - Concurrent downloads
   - Multiple download methods
   - Retry logic
   - Progress tracking

3. **Tracker**: Anime tracking integration
   - OAuth authentication
   - Progress synchronization
   - Offline queue

4. **Player**: MPV integration
   - IPC communication
   - Progress monitoring
   - Resume functionality

5. **Cache**: Two-tier caching
   - Memory cache
   - File cache
   - TTL support

### Provider Layer

**Structure:**
- Language-organized directories
- Base provider interface
- Registry system
- Stream extractors

**Provider Lifecycle:**
1. Discovery (filesystem scan)
2. Registration (decorator)
3. Instantiation (on demand)
4. Caching (results)

### Data Layer

**Storage:**
- SQLite database (~/.weeb-cli/weeb.db)
- Cache files (~/.weeb-cli/cache/)
- Log files (~/.weeb-cli/logs/)
- Downloaded binaries (~/.weeb-cli/bin/)

## Data Flow

### Search Flow

```
User Input → CLI → Scraper → Provider → Cache → API
                                ↓
                            Results
                                ↓
                         CLI Display
```

### Download Flow

```
User Selection → Queue Manager → Download Worker
                                      ↓
                              Try Strategies
                                      ↓
                         ┌─────────────────────┐
                         │  Aria2 → yt-dlp →   │
                         │  FFmpeg → Generic   │
                         └─────────────────────┘
                                      ↓
                              Progress Update
                                      ↓
                              Database Save
```

### Watch Flow

```
User Selection → Stream Extraction → Player (MPV)
                                          ↓
                                   IPC Monitor
                                          ↓
                                  Progress Save
                                          ↓
                                  Tracker Sync
```

## Thread Safety

### Locking Strategy

1. **Database**: RLock for connection management
2. **Download Queue**: Lock for queue operations
3. **Cache**: No locking (single-threaded access)

### Concurrent Operations

- Download workers run in separate threads
- MPV monitor runs in daemon thread
- Tracker sync runs in background

## Error Handling

### Exception Hierarchy

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

### Error Recovery

1. **Retry Logic**: Exponential backoff for transient errors
2. **Fallback**: Alternative methods when primary fails
3. **Graceful Degradation**: Continue with reduced functionality
4. **User Notification**: Clear error messages with i18n

## Performance Optimizations

### 1. Caching

- Search results cached for 1 hour
- Details cached for 6 hours
- Two-tier (memory + file) for speed

### 2. Lazy Loading

- Services loaded on first use
- Providers discovered on demand
- Database connection pooling

### 3. Concurrent Downloads

- Multiple downloads in parallel
- Configurable concurrency limit
- Resource-aware scheduling

### 4. Database Optimization

- WAL mode for concurrent access
- Prepared statements
- Indexed queries
- Batch operations

## Security Considerations

### 1. Input Sanitization

- Filename sanitization
- URL validation
- SQL injection prevention (parameterized queries)

### 2. Credential Storage

- OAuth tokens in database
- No plaintext passwords
- Secure token refresh

### 3. Network Security

- HTTPS for API calls
- Certificate verification
- Timeout limits

## Extensibility

### Adding New Features

1. **New Provider**: Implement BaseProvider interface
2. **New Tracker**: Implement TrackerBase interface
3. **New Command**: Add Typer command
4. **New Service**: Follow service pattern

### Plugin System

Currently not implemented, but architecture supports:
- Provider plugins
- Extractor plugins
- Command plugins

## Future Improvements

1. **Plugin System**: Dynamic plugin loading
2. **API Server**: REST API for remote control
3. **Web UI**: Browser-based interface
4. **Mobile App**: Companion mobile application
5. **Cloud Sync**: Cross-device synchronization
