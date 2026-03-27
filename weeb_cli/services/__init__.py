"""Core services for Weeb CLI business logic.

This package contains the service layer that handles all business logic
including downloads, streaming, tracking, caching, and database operations.

Services are designed with lazy loading and dependency injection patterns
for optimal performance and testability.

Core Services:
    database: SQLite database manager with migrations
    downloader: Queue-based download manager with Aria2/yt-dlp
    tracker: AniList, MAL, and Kitsu integration
    player: MPV integration with IPC monitoring
    cache: File and memory-based caching system
    scraper: Provider facade with error handling
    
Supporting Services:
    local_library: Local anime indexing and management
    progress: Watch progress tracking and statistics
    dependency_manager: Auto-installation of external tools
    discord_rpc: Discord Rich Presence integration
    notifier: System notifications
    logger: Debug logging system
    error_handler: Global error handling

Example:
    Using services::

        from weeb_cli.services.database import db
        from weeb_cli.services.downloader import queue_manager
        
        # Get watch progress
        progress = db.get_progress("anime-slug")
        
        # Start download queue
        queue_manager.start_queue()

Thread Safety:
    All services are designed to be thread-safe with proper locking
    mechanisms for concurrent access.
"""

__all__ = [
    "database",
    "downloader",
    "tracker",
    "player",
    "cache",
    "scraper",
    "local_library",
    "progress",
    "dependency_manager",
    "discord_rpc",
    "notifier",
    "logger",
    "error_handler",
]
