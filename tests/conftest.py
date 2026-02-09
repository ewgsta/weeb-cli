"""Pytest configuration and fixtures."""
import pytest
from pathlib import Path
import tempfile
import shutil


@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests."""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


@pytest.fixture
def mock_config(temp_dir):
    """Mock configuration for tests."""
    return {
        "language": "en",
        "download_dir": str(temp_dir / "downloads"),
        "aria2_enabled": True,
        "ytdlp_enabled": True,
        "max_concurrent_downloads": 2,
        "debug_mode": False
    }
