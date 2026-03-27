"""Search command submodules.

This package contains the implementation of the search command,
split into logical components for better maintainability.

Modules:
    anime_details: Anime details display and selection
    download_flow: Download workflow and queue management
    episode_utils: Episode selection and filtering utilities
    search_handlers: Search query handling and results display
    stream_utils: Stream quality selection and validation
    watch_flow: Watch workflow with player integration

The search command is the primary entry point for discovering and
accessing anime content across all providers.
"""

__all__ = [
    "anime_details",
    "download_flow",
    "episode_utils",
    "search_handlers",
    "stream_utils",
    "watch_flow",
]
