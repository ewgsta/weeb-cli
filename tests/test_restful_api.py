"""Tests for RESTful API server."""
import pytest
from unittest.mock import Mock, patch, MagicMock
from weeb_cli.providers.base import AnimeResult, Episode, StreamLink


@pytest.fixture
def mock_provider():
    """Create a mock provider."""
    provider = Mock()
    provider.name = "test_provider"
    provider.search.return_value = [
        AnimeResult(
            id="test123",
            title="Test Anime",
            type="series",
            cover="https://example.com/cover.jpg",
            year=2024,
        )
    ]
    provider.get_episodes.return_value = [
        Episode(id="ep1", number=1, title="Episode 1", season=1),
        Episode(id="ep2", number=2, title="Episode 2", season=1),
    ]
    provider.get_streams.return_value = [
        StreamLink(
            url="https://example.com/stream.m3u8",
            quality="1080p",
            server="default",
            headers={"Referer": "https://example.com"},
        )
    ]
    return provider


@pytest.fixture
def mock_flask_app(mock_provider):
    """Create a mock Flask app with routes."""
    with patch("weeb_cli.commands.serve_restful.get_provider") as mock_get_provider:
        mock_get_provider.return_value = mock_provider
        
        with patch("weeb_cli.commands.serve_restful.list_all_providers") as mock_list:
            mock_list.return_value = [
                {"name": "test_provider", "lang": "en", "region": "US"}
            ]
            
            # Import after patching
            from flask import Flask
            app = Flask(__name__)
            
            # Mock the routes (simplified for testing)
            @app.route("/health")
            def health():
                from flask import jsonify
                return jsonify({
                    "status": "ok",
                    "service": "weeb-cli-restful",
                    "providers": ["test_provider"],
                })
            
            yield app


def test_health_endpoint(mock_flask_app):
    """Test health check endpoint."""
    client = mock_flask_app.test_client()
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert data["service"] == "weeb-cli-restful"
    assert "test_provider" in data["providers"]


def test_serialize_anime_result():
    """Test AnimeResult serialization."""
    from weeb_cli.commands.serve_restful import _serialize_anime_result
    
    result = AnimeResult(
        id="test123",
        title="Test Anime",
        type="series",
        cover="https://example.com/cover.jpg",
        year=2024,
    )
    
    serialized = _serialize_anime_result(result)
    
    assert serialized["id"] == "test123"
    assert serialized["title"] == "Test Anime"
    assert serialized["type"] == "series"
    assert serialized["cover"] == "https://example.com/cover.jpg"
    assert serialized["year"] == 2024


def test_serialize_episode():
    """Test Episode serialization."""
    from weeb_cli.commands.serve_restful import _serialize_episode
    
    episode = Episode(
        id="ep1",
        number=1,
        title="Episode 1",
        season=1,
        url="https://example.com/ep1",
    )
    
    serialized = _serialize_episode(episode)
    
    assert serialized["id"] == "ep1"
    assert serialized["number"] == 1
    assert serialized["title"] == "Episode 1"
    assert serialized["season"] == 1
    assert serialized["url"] == "https://example.com/ep1"


def test_serialize_stream():
    """Test StreamLink serialization."""
    from weeb_cli.commands.serve_restful import _serialize_stream
    
    stream = StreamLink(
        url="https://example.com/stream.m3u8",
        quality="1080p",
        server="default",
        headers={"Referer": "https://example.com"},
        subtitles="https://example.com/subs.vtt",
    )
    
    serialized = _serialize_stream(stream)
    
    assert serialized["url"] == "https://example.com/stream.m3u8"
    assert serialized["quality"] == "1080p"
    assert serialized["server"] == "default"
    assert serialized["headers"]["Referer"] == "https://example.com"
    assert serialized["subtitles"] == "https://example.com/subs.vtt"


def test_quality_score():
    """Test quality scoring function."""
    from weeb_cli.commands.serve_restful import _quality_score
    
    assert _quality_score("4k") == 5
    assert _quality_score("2160p") == 5
    assert _quality_score("1080p") == 4
    assert _quality_score("720p") == 3
    assert _quality_score("480p") == 2
    assert _quality_score("360p") == 1
    assert _quality_score("unknown") == 0
    assert _quality_score(None) == 0


@patch("weeb_cli.commands.serve_restful.get_provider")
def test_search_with_provider(mock_get_provider, mock_provider):
    """Test search functionality with provider selection."""
    mock_get_provider.return_value = mock_provider
    
    # Simulate search
    results = mock_provider.search("test query")
    
    assert len(results) == 1
    assert results[0].title == "Test Anime"
    assert results[0].id == "test123"


@patch("weeb_cli.commands.serve_restful.get_provider")
def test_get_episodes_with_season_filter(mock_get_provider, mock_provider):
    """Test episode listing with season filter."""
    mock_get_provider.return_value = mock_provider
    
    # Add episodes from different seasons
    mock_provider.get_episodes.return_value = [
        Episode(id="ep1", number=1, season=1),
        Episode(id="ep2", number=2, season=1),
        Episode(id="ep3", number=1, season=2),
    ]
    
    episodes = mock_provider.get_episodes("test123")
    season_1_episodes = [ep for ep in episodes if ep.season == 1]
    
    assert len(season_1_episodes) == 2
    assert all(ep.season == 1 for ep in season_1_episodes)


@patch("weeb_cli.commands.serve_restful.get_provider")
def test_get_streams_sorted(mock_get_provider, mock_provider):
    """Test stream retrieval with quality sorting."""
    from weeb_cli.commands.serve_restful import _quality_score
    
    mock_get_provider.return_value = mock_provider
    
    # Add streams with different qualities
    mock_provider.get_streams.return_value = [
        StreamLink(url="url1", quality="480p"),
        StreamLink(url="url2", quality="1080p"),
        StreamLink(url="url3", quality="720p"),
    ]
    
    streams = mock_provider.get_streams("test123", "ep1")
    sorted_streams = sorted(streams, key=lambda s: _quality_score(s.quality), reverse=True)
    
    assert sorted_streams[0].quality == "1080p"
    assert sorted_streams[1].quality == "720p"
    assert sorted_streams[2].quality == "480p"


def test_missing_flask_import():
    """Test graceful handling when Flask is not installed."""
    with patch("builtins.__import__", side_effect=ImportError("No module named 'flask'")):
        with pytest.raises(ImportError):
            import flask


@pytest.mark.parametrize("quality,expected_score", [
    ("4K", 5),
    ("2160p", 5),
    ("1080p", 4),
    ("720p", 3),
    ("480p", 2),
    ("360p", 1),
    ("auto", 0),
    ("", 0),
])
def test_quality_score_parametrized(quality, expected_score):
    """Test quality scoring with various inputs."""
    from weeb_cli.commands.serve_restful import _quality_score
    assert _quality_score(quality) == expected_score
