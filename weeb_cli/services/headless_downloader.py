"""Headless download module that works without database, TUI, or i18n dependencies.

Used by the API commands and the Torznab serve mode.
"""
import logging
import re
import shutil
import subprocess
from pathlib import Path

log = logging.getLogger("weeb-cli")


def _find_tool(name: str) -> str | None:
    return shutil.which(name)


def _sanitize_filename(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"\s+", " ", name).strip()
    name = name.rstrip(".")
    return name or "unnamed"


def download_episode(
    stream_url: str,
    series_title: str,
    season: int,
    episode: int,
    download_dir: str,
) -> str | None:
    safe_title = _sanitize_filename(series_title)
    anime_dir = Path(download_dir)
    anime_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{safe_title} - S{season:02d}E{episode:02d}.mp4"
    output_path = anime_dir / filename

    if output_path.exists():
        log.info(f"Already exists: {output_path}")
        return str(output_path)

    temp_path = output_path.with_suffix(".mp4.part")

    is_hls = ".m3u8" in stream_url

    try:
        if is_hls:
            _download_hls(stream_url, temp_path)
        else:
            aria2 = _find_tool("aria2c")
            if aria2:
                _download_aria2(aria2, stream_url, temp_path)
            else:
                _download_ffmpeg(stream_url, temp_path)

        if temp_path.exists() and temp_path.stat().st_size > 0:
            temp_path.rename(output_path)
            log.info(f"Downloaded: {output_path}")
            return str(output_path)
        else:
            log.error(f"Download produced empty file: {temp_path}")
            temp_path.unlink(missing_ok=True)
            return None

    except Exception as e:
        log.error(f"Download failed for {filename}: {e}")
        temp_path.unlink(missing_ok=True)
        return None


def _download_aria2(aria2_path: str, url: str, output_path: Path):
    cmd = [
        aria2_path, url,
        "-d", str(output_path.parent),
        "-o", output_path.name,
        "-x", "16", "-s", "16", "-j", "1", "-c",
        "--console-log-level=warn",
        "--summary-interval=5",
        "--file-allocation=none",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(f"aria2 failed (rc={result.returncode}): {result.stderr[:500]}")


def _download_hls(url: str, output_path: Path):
    ytdlp = _find_tool("yt-dlp")
    if ytdlp:
        cmd = [ytdlp, "-f", "best", "-o", str(output_path), "--no-part", url]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        if result.returncode != 0:
            raise RuntimeError(f"yt-dlp failed (rc={result.returncode}): {result.stderr[:500]}")
    else:
        _download_ffmpeg(url, output_path)


def _download_ffmpeg(url: str, output_path: Path):
    ffmpeg = _find_tool("ffmpeg")
    if not ffmpeg:
        raise RuntimeError("No download tool available (need aria2c, yt-dlp, or ffmpeg)")
    cmd = [
        ffmpeg, "-i", url,
        "-c", "copy", "-bsf:a", "aac_adtstoasc",
        "-y", str(output_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed (rc={result.returncode}): {result.stderr[:500]}")
