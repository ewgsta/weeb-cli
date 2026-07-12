"""
Helper utilities for Animecix provider.

This module provides dynamic header fetching, HTTP utilities, and helper functions
specifically for interacting with animecix.tv API.
"""

import json
import re
import time
from typing import Dict, Optional, Any
from pathlib import Path
from datetime import datetime, timedelta

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from weeb_cli.services.logger import debug
from weeb_cli.config import CONFIG_DIR

STATIC_HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    "priority": "u=1, i",
    "sec-ch-ua": '"Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Linux"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sec-gpc": "1",
    "user-agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    ),
}

EXCLUDED_HEADERS = {
    "accept", "accept-language", "priority", "sec-ch-ua", 
    "sec-ch-ua-mobile", "sec-ch-ua-platform", "sec-fetch-dest", 
    "sec-fetch-mode", "sec-fetch-site", "sec-gpc", "user-agent",
    "host", "connection", "content-length"
}

HEADERS_CACHE_FILE = CONFIG_DIR / "animecix_headers.json"
CACHE_DURATION = timedelta(hours=1)


def get_cached_headers() -> Optional[Dict[str, str]]:
    """
    Load cached dynamic headers if they exist and are still valid.
    
    Returns:
        Dictionary of cached headers, or None if cache is invalid/missing.
    """
    if not HEADERS_CACHE_FILE.exists():
        return None
    
    try:
        with open(HEADERS_CACHE_FILE, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        
        cached_time = datetime.fromisoformat(cache_data.get("timestamp", ""))
        if datetime.now() - cached_time > CACHE_DURATION:
            debug("[AnimeCix] Header cache expired")
            return None
        
        headers = cache_data.get("headers", {})
        if headers:
            debug("[AnimeCix] Using cached headers")
            return headers
        
        return None
    except Exception as e:
        debug(f"[AnimeCix] Failed to load header cache: {e}")
        return None


def save_headers_cache(headers: Dict[str, str]) -> None:
    """
    Save dynamic headers to cache file.
    
    Args:
        headers: Dictionary of dynamic headers to cache.
    """
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        cache_data = {
            "timestamp": datetime.now().isoformat(),
            "headers": headers
        }
        with open(HEADERS_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache_data, f, indent=2)
        debug(f"[AnimeCix] Saved headers to cache")
    except Exception as e:
        debug(f"[AnimeCix] Failed to save header cache: {e}")


def get_dynamic_headers(force_refresh: bool = False) -> Dict[str, str]:
    """
    Get dynamic headers required for animecix.tv API requests.
    
    Uses Playwright to extract headers from a real browser session.
    Falls back to cached headers if Playwright is not available or fails.
    
    Args:
        force_refresh: If True, bypass cache and fetch fresh headers.
    
    Returns:
        Dictionary of dynamic headers (e.g., x-e-h, cookies).
    """
    # Try cached headers first
    if not force_refresh:
        cached = get_cached_headers()
        if cached:
            return cached
    
    if not PLAYWRIGHT_AVAILABLE:
        debug("[AnimeCix] Playwright not available, cannot fetch dynamic headers")
        return {}
    
    debug("[AnimeCix] Fetching fresh dynamic headers with Playwright...")
    dynamic_headers = {}
    
    try:
        with sync_playwright() as p:
            browser = None
            
            browsers = [
                ("chrome", p.chromium),
                ("msedge", p.chromium),
                ("firefox", p.firefox),
            ]
            
            for channel, launcher in browsers:
                try:
                    if channel == "firefox":
                        browser = launcher.launch(headless=True)
                    else:
                        browser = launcher.launch(channel=channel, headless=True)
                    debug(f"[AnimeCix] Launched browser: {channel}")
                    break
                except Exception as e:
                    debug(f"[AnimeCix] Failed to launch {channel}: {e}")
                    continue
            
            if not browser:
                debug("[AnimeCix] Falling back to Playwright Chromium")
                browser = p.chromium.launch(headless=True)
            
            page = browser.new_page()
            
            def handle_request(request):
                nonlocal dynamic_headers
                if "secure/titles" in request.url or "secure/episode" in request.url:
                    all_headers = request.headers
                    dynamic_headers = {
                        k: v for k, v in all_headers.items() 
                        if k.lower() not in EXCLUDED_HEADERS
                    }
                    debug(f"[AnimeCix] Captured {len(dynamic_headers)} dynamic headers")
            
            page.on("request", handle_request)
            
            try:
                page.goto("https://animecix.tv/browse", 
                         wait_until="networkidle", 
                         timeout=30000)
            except PlaywrightTimeoutError:
                debug("[AnimeCix] Page load timeout, continuing anyway")
            
            if not dynamic_headers:
                debug("[AnimeCix] Waiting additional time for requests...")
                page.wait_for_timeout(3000)
            
            browser.close()
        
        if dynamic_headers:
            save_headers_cache(dynamic_headers)
        
        return dynamic_headers
        
    except Exception as e:
        debug(f"[AnimeCix] Error fetching dynamic headers: {e}")
        return {}


def build_headers(dynamic_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Build complete headers by merging static and dynamic headers.
    
    Args:
        dynamic_headers: Optional dynamic headers to merge. If None, fetches them.
    
    Returns:
        Complete headers dictionary ready for HTTP requests.
    """
    headers = dict(STATIC_HEADERS)
    
    if dynamic_headers is None:
        dynamic_headers = get_dynamic_headers()
    
    headers.update(dynamic_headers)
    
    return headers


def clean_title_name(title: str) -> str:
    """
    Convert anime title to URL-safe slug format.
    
    Removes/replaces special characters to match animecix.tv URL format.
    
    Args:
        title: Original anime title.
    
    Returns:
        URL-safe slug string.
    
    Example:
        >>> clean_title_name("One Piece: Episode 1000!")
        "one-piece-episode-1000"
    """
    if not title:
        return ""
    
    # Convert to lowercase
    title = title.lower()
    
    # Replace/remove special characters
    title = title.replace("&", "and")
    title = title.replace("'", "")
    title = title.replace("!", "")
    title = title.replace("?", "")
    title = title.replace(":", "")
    title = title.replace(".", "")
    
    title = re.sub(r'[^a-z0-9\s-]', '', title)
    
    title = title.replace(" ", "-")
    
    title = re.sub(r'-+', '-', title)
    
    title = title.strip('-')
    
    return title


def parse_episode_number(name: str, fallback: int = 1) -> int:
    """
    Extract episode number from episode name.
    
    Supports various naming patterns:
    - "Bölüm 5"
    - "Episode 12"
    - "5. Bölüm"
    - "12"
    
    Args:
        name: Episode name string.
        fallback: Default number if parsing fails.
    
    Returns:
        Extracted episode number or fallback.
    
    Example:
        >>> parse_episode_number("Bölüm 42")
        42
        >>> parse_episode_number("Unknown Name", 10)
        10
    """
    if not name:
        return fallback
    
    patterns = [
        r'(?:bölüm|episode|ep)\s*[:\-]?\s*(\d+)', 
        r'(\d+)\.\s*(?:bölüm|episode)',            
        r'^(\d+)$',                                 
        r'[sS](\d+)[eE](\d+)',                    
    ]
    
    name_lower = name.lower()
    for pattern in patterns:
        match = re.search(pattern, name_lower)
        if match:
            if len(match.groups()) > 1:
                return int(match.group(2))
            return int(match.group(1))
    
    debug(f"[AnimeCix] Could not parse episode number from '{name}', using fallback {fallback}")
    return fallback


def parse_season_number(data: Any, fallback: int = 1) -> int:
    """
    Extract season number from various data formats.
    
    Args:
        data: Season data (dict with 'number' key, int, or URL string).
        fallback: Default season number if parsing fails.
    
    Returns:
        Extracted season number or fallback.
    """
    if isinstance(data, dict):
        return data.get("number", fallback)
    
    if isinstance(data, int):
        return data
    
    if isinstance(data, str):
        try:
            from urllib.parse import parse_qs
            if "?" in data:
                qs = parse_qs(data.split("?", 1)[1])
                if "season" in qs:
                    return int(qs["season"][0])
        except (ValueError, KeyError, IndexError):
            pass
    
    return fallback


def retry_with_backoff(func, max_retries: int = 3, initial_delay: float = 1.0):
    """
    Retry a function with exponential backoff.
    
    Args:
        func: Function to retry (should raise exception on failure).
        max_retries: Maximum number of retry attempts.
        initial_delay: Initial delay in seconds between retries.
    
    Returns:
        Function result if successful.
    
    Raises:
        Last exception if all retries fail.
    """
    last_exception = None
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            last_exception = e
            debug(f"[AnimeCix] Attempt {attempt + 1}/{max_retries} failed: {e}")
            
            if attempt < max_retries - 1:
                debug(f"[AnimeCix] Retrying in {delay:.1f}s...")
                time.sleep(delay)
                delay *= 2  
    
    # All retries failed
    raise last_exception
