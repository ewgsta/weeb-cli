import json
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from weeb_cli.main import app
from weeb_cli.providers.base import AnimeResult, Episode, StreamLink, AnimeDetails

runner = CliRunner()

MOCK_ANIME = AnimeResult(id="123", title="Angel Beats!", type="series")
MOCK_EPISODES = [
    Episode(id="ep1", number=1, title="Pilot", season=1),
    Episode(id="ep2", number=2, title="Second", season=1),
    Episode(id="ep3", number=1, title="S2 Pilot", season=2),
]
MOCK_STREAMS = [
    StreamLink(url="https://example.com/video.mp4", quality="1080p", server="tau"),
]
MOCK_DETAILS = AnimeDetails(
    id="123", title="Angel Beats!", description="A test", genres=["Drama"], year=2010,
)


def _mock_provider(**overrides):
    p = MagicMock()
    p.search.return_value = overrides.get("search", [MOCK_ANIME])
    p.get_episodes.return_value = overrides.get("episodes", MOCK_EPISODES)
    p.get_streams.return_value = overrides.get("streams", MOCK_STREAMS)
    p.get_details.return_value = overrides.get("details", MOCK_DETAILS)
    return p


class TestApiProviders:

    def test_providers_lists_all(self):
        result = runner.invoke(app, ["api", "providers"])
        assert result.exit_code == 0
        data = json.loads(result.output)
        assert isinstance(data, list)
        names = [p["name"] for p in data]
        assert "animecix" in names


class TestApiSearch:

    def test_search_returns_json(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "search", "Angel Beats"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert len(data) == 1
            assert data[0]["id"] == "123"
            assert data[0]["title"] == "Angel Beats!"

    def test_search_empty(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider(search=[])):
            result = runner.invoke(app, ["api", "search", "nonexistent"])
            assert result.exit_code == 0
            assert json.loads(result.output) == []


class TestApiEpisodes:

    def test_episodes_returns_all(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "episodes", "123"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert len(data) == 3

    def test_episodes_filter_season(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "episodes", "123", "--season", "1"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert len(data) == 2
            assert all(e["season"] == 1 for e in data)


class TestApiStreams:

    def test_streams_returns_json(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "streams", "123", "--episode", "1"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert len(data) == 1
            assert data[0]["quality"] == "1080p"

    def test_streams_episode_not_found(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "streams", "123", "--episode", "99"])
            assert result.exit_code == 1


class TestApiDetails:

    def test_details_returns_json(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "details", "123"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert data["title"] == "Angel Beats!"
            assert data["year"] == 2010

    def test_details_not_found(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider(details=None)):
            result = runner.invoke(app, ["api", "details", "123"])
            assert result.exit_code == 1


class TestApiDownload:

    def test_download_success(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()), \
             patch("weeb_cli.services.headless_downloader.download_episode", return_value="/tmp/test.mp4"):
            result = runner.invoke(app, ["api", "download", "123", "--episode", "1", "--output", "/tmp"])
            assert result.exit_code == 0
            data = json.loads(result.output)
            assert data["status"] == "ok"
            assert data["anime"] == "Angel Beats!"

    def test_download_episode_not_found(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider()):
            result = runner.invoke(app, ["api", "download", "123", "--episode", "99"])
            assert result.exit_code == 1

    def test_download_no_streams(self):
        with patch("weeb_cli.commands.api._get_provider", return_value=_mock_provider(streams=[])):
            result = runner.invoke(app, ["api", "download", "123", "--episode", "1"])
            assert result.exit_code == 1


class TestApiDownloadUrl:

    def test_download_url_success(self):
        with patch("weeb_cli.services.headless_downloader.download_episode", return_value="/tmp/test.mp4"):
            result = runner.invoke(app, [
                "api", "download-url", "https://example.com/video.mp4",
                "--title", "Test Anime", "--episode", "1", "--output", "/tmp",
            ])
            assert result.exit_code == 0
            assert json.loads(result.output)["status"] == "ok"

    def test_download_url_failure(self):
        with patch("weeb_cli.services.headless_downloader.download_episode", return_value=None):
            result = runner.invoke(app, [
                "api", "download-url", "https://example.com/fail.mp4",
                "--title", "Test Anime", "--episode", "1", "--output", "/tmp",
            ])
            assert result.exit_code == 1


class TestHeadlessDownloader:

    def test_sanitize_filename(self):
        from weeb_cli.services.headless_downloader import _sanitize_filename
        assert _sanitize_filename('Test: Anime / Name?') == "Test Anime Name"
        assert _sanitize_filename('') == "unnamed"
        assert _sanitize_filename('Normal Name') == "Normal Name"


class TestDatabaseLazyInit:

    def test_no_recursion_on_first_access(self, temp_dir):
        """Regression test: lazy init must not cause infinite recursion."""
        from weeb_cli.services.database import Database
        db = Database()
        db.db_path = temp_dir / "test.db"
        db._initialized = False
        assert db.get_config("language") is None
        assert db._initialized is True

    def test_set_and_get_config(self, temp_dir):
        from weeb_cli.services.database import Database
        db = Database()
        db.db_path = temp_dir / "test.db"
        db._initialized = False
        db.set_config("language", "en")
        assert db.get_config("language") == "en"
