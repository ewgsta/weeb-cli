"""Weeb CLI screens package."""

from .main import MainScreen
from .search import SearchScreen
from .anime_detail import AnimeDetailScreen, StreamSelectModal, ConfirmModal
from .watchlist import WatchlistScreen
from .downloads import DownloadsScreen
from .library import LibraryScreen
from .settings import SettingsScreen
from .setup import SetupScreen

__all__ = [
    "MainScreen",
    "SearchScreen",
    "AnimeDetailScreen",
    "StreamSelectModal",
    "ConfirmModal",
    "WatchlistScreen",
    "DownloadsScreen",
    "LibraryScreen",
    "SettingsScreen",
    "SetupScreen",
]
