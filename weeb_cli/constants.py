"""Application-wide constants and enumerations.

This module defines constants used throughout the application to avoid
magic strings and improve code maintainability.
"""

from enum import Enum


class ConfigKey(str, Enum):
    """Configuration key names."""
    
    LANGUAGE = "language"
    ARIA2_ENABLED = "aria2_enabled"
    YTDLP_ENABLED = "ytdlp_enabled"
    ARIA2_MAX_CONNECTIONS = "aria2_max_connections"
    MAX_CONCURRENT_DOWNLOADS = "max_concurrent_downloads"
    DOWNLOAD_DIR = "download_dir"
    YTDLP_FORMAT = "ytdlp_format"
    SCRAPING_SOURCE = "scraping_source"
    SHOW_DESCRIPTION = "show_description"
    DEBUG_MODE = "debug_mode"
    DOWNLOAD_MAX_RETRIES = "download_max_retries"
    DOWNLOAD_RETRY_DELAY = "download_retry_delay"
    DISCORD_RPC_ENABLED = "discord_rpc_enabled"
    SHORTCUTS_ENABLED = "shortcuts_enabled"
    ANISKIP_ENABLED = "aniskip_enabled"


class DownloadStatus(str, Enum):
    """Download queue item status values."""
    
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ErrorType(str, Enum):
    """Error classification types."""
    
    TRANSIENT = "transient"
    PERMANENT = "permanent"


class Language(str, Enum):
    """Supported language codes."""
    
    ENGLISH = "en"
    TURKISH = "tr"
    GERMAN = "de"
    POLISH = "pl"
