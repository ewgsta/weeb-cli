"""Download strategies for different methods."""

from weeb_cli.services.download.strategies.base import DownloadStrategy
from weeb_cli.services.download.strategies.aria2 import Aria2Strategy
from weeb_cli.services.download.strategies.ytdlp import YtdlpStrategy
from weeb_cli.services.download.strategies.ffmpeg import FFmpegStrategy
from weeb_cli.services.download.strategies.generic import GenericStrategy

__all__ = [
    'DownloadStrategy',
    'Aria2Strategy',
    'YtdlpStrategy',
    'FFmpegStrategy',
    'GenericStrategy'
]
