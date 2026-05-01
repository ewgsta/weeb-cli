"""Tests for Weeb CLI SDK."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from weeb_cli.sdk import WeebSDK, list_providers, get_provider_info
from weeb_cli.providers.base import AnimeResult, Episode, StreamLink, AnimeDetails
from weeb_cli.exceptions import ProviderError, WeebCLIError


class TestWeebSDK:
    """Test suite for WeebSDK class."""
    
    def test_init_default(self):
        """Test SDK initialization with defaults."""
        sdk = WeebSDK()
        assert sdk.headless is True
        assert sdk.default_provider == "animecix"
    
    def test_init_custom_provider(self):
        """Test SDK initialization with custom provider."""
        sdk = WeebSDK(default_provider="hianime")
        assert sdk.default_provider == "hianime"
    
    def test_init_non_headless(self):
        """Test SDK initialization in non-headless mode."""
        sdk = WeebSDK(headless=False)
        assert sdk.headless is False
    
    @patch('weeb_cli.sdk._list_providers')
    def test_list_providers(self, mock_list):
        """Test listing providers."""
        mock_list.return_value = [
            {"name": "animecix", "lang": "tr", "region": "TR"},
            {"name": "hianime", "lang": "en", "region": "US"}
        ]
        
        sdk = WeebSDK()
        providers = sdk.list_providers()
        
        assert len(providers) == 2
        assert providers[0]["name"] == "animecix"
        assert providers[1]["name"] == "hianime"
    
    @patch('weeb_cli.sdk._list_providers')
    def test_get_provider_info(self, mock_list):
        """Test getting provider info."""
        mock_list.return_value = [
            {"name": "animecix", "lang": "tr", "region": "TR"},
            {"name": "hianime", "lang": "en", "region": "US"}
        ]
        
        sdk = WeebSDK()
        info = sdk.get_provider_info("hianime")
        
        assert info is not None
        assert info["name"] == "hianime"
        assert info["lang"] == "en"
    
    @patch('weeb_cli.sdk._list_providers')
    def test_get_provider_info_not_found(self, mock_list):
        """Test getting info for non-existent provider."""
        mock_list.return_value = [
            {"name": "animecix", "lang": "tr", "region": "TR"}
        ]
        
        sdk = WeebSDK()
        info = sdk.get_provider_info("invalid")
        
        assert info is None
    
    @patch('weeb_cli.sdk.get_provider')
    def test_search_success(self, mock_get_provider):
        """Test successful anime search."""
        mock_provider = Mock()
        mock_provider.search.return_value = [
            AnimeResult(id="1", title="Anime 1", year=2020),
            AnimeResult(id="2", title="Anime 2", year=2021)
        ]
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        results = sdk.search("test", provider="hianime")
        
        assert len(results) == 2
        assert results[0].title == "Anime 1"
        mock_provider.search.assert_called_once_with("test")
    
    @patch('weeb_cli.sdk.get_provider')
    def test_search_provider_not_found(self, mock_get_provider):
        """Test search with invalid provider."""
        mock_get_provider.return_value = None
        
        sdk = WeebSDK()
        
        with pytest.raises(ProviderError) as exc_info:
            sdk.search("test", provider="invalid")
        
        assert "Provider not found or disabled" in str(exc_info.value)
    
    @patch('weeb_cli.sdk.get_provider')
    def test_search_uses_default_provider(self, mock_get_provider):
        """Test search uses default provider when not specified."""
        mock_provider = Mock()
        mock_provider.search.return_value = []
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK(default_provider="hianime")
        sdk.search("test")
        
        mock_get_provider.assert_called_with("hianime")
    
    @patch('weeb_cli.sdk.get_provider')
    def test_get_details_success(self, mock_get_provider):
        """Test getting anime details."""
        mock_provider = Mock()
        mock_provider.get_details.return_value = AnimeDetails(
            id="1",
            title="Test Anime",
            description="Test description",
            genres=["Action", "Adventure"]
        )
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        details = sdk.get_details("1", provider="hianime")
        
        assert details is not None
        assert details.title == "Test Anime"
        assert len(details.genres) == 2
    
    @patch('weeb_cli.sdk.get_provider')
    def test_get_episodes_success(self, mock_get_provider):
        """Test getting episode list."""
        mock_provider = Mock()
        mock_provider.get_episodes.return_value = [
            Episode(id="e1", number=1, season=1),
            Episode(id="e2", number=2, season=1),
            Episode(id="e3", number=1, season=2)
        ]
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        episodes = sdk.get_episodes("anime-id", provider="hianime")
        
        assert len(episodes) == 3
    
    @patch('weeb_cli.sdk.get_provider')
    def test_get_episodes_filter_by_season(self, mock_get_provider):
        """Test filtering episodes by season."""
        mock_provider = Mock()
        mock_provider.get_episodes.return_value = [
            Episode(id="e1", number=1, season=1),
            Episode(id="e2", number=2, season=1),
            Episode(id="e3", number=1, season=2)
        ]
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        episodes = sdk.get_episodes("anime-id", season=1, provider="hianime")
        
        assert len(episodes) == 2
        assert all(ep.season == 1 for ep in episodes)
    
    @patch('weeb_cli.sdk.get_provider')
    def test_get_streams_success(self, mock_get_provider):
        """Test getting stream URLs."""
        mock_provider = Mock()
        mock_provider.get_streams.return_value = [
            StreamLink(url="http://stream1.com", quality="1080p"),
            StreamLink(url="http://stream2.com", quality="720p")
        ]
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        streams = sdk.get_streams("anime-id", "ep-id", provider="hianime")
        
        assert len(streams) == 2
        assert streams[0].quality == "1080p"
    
    @patch('weeb_cli.sdk.download_episode')
    @patch('weeb_cli.sdk.get_provider')
    def test_download_episode_success(self, mock_get_provider, mock_download):
        """Test downloading an episode."""
        mock_provider = Mock()
        mock_provider.get_episodes.return_value = [
            Episode(id="e1", number=1, season=1)
        ]
        mock_provider.get_streams.return_value = [
            StreamLink(url="http://stream.com", quality="1080p")
        ]
        mock_provider.get_details.return_value = AnimeDetails(
            id="1", title="Test Anime"
        )
        mock_get_provider.return_value = mock_provider
        mock_download.return_value = "/path/to/file.mp4"
        
        sdk = WeebSDK()
        path = sdk.download_episode(
            anime_id="1",
            season=1,
            episode=1,
            provider="hianime"
        )
        
        assert path == "/path/to/file.mp4"
        mock_download.assert_called_once()
    
    @patch('weeb_cli.sdk.get_provider')
    def test_download_episode_not_found(self, mock_get_provider):
        """Test downloading non-existent episode."""
        mock_provider = Mock()
        mock_provider.get_episodes.return_value = [
            Episode(id="e1", number=1, season=1)
        ]
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        
        with pytest.raises(WeebCLIError) as exc_info:
            sdk.download_episode(
                anime_id="1",
                season=2,
                episode=1,
                provider="hianime"
            )
        
        assert "not found" in str(exc_info.value)
    
    @patch('weeb_cli.sdk.get_provider')
    def test_download_episode_no_streams(self, mock_get_provider):
        """Test downloading when no streams available."""
        mock_provider = Mock()
        mock_provider.get_episodes.return_value = [
            Episode(id="e1", number=1, season=1)
        ]
        mock_provider.get_streams.return_value = []
        mock_get_provider.return_value = mock_provider
        
        sdk = WeebSDK()
        
        with pytest.raises(WeebCLIError) as exc_info:
            sdk.download_episode(
                anime_id="1",
                season=1,
                episode=1,
                provider="hianime"
            )
        
        assert "No streams available" in str(exc_info.value)
    
    @patch('weeb_cli.sdk.download_episode')
    def test_download_url_success(self, mock_download):
        """Test downloading from direct URL."""
        mock_download.return_value = "/path/to/file.mp4"
        
        sdk = WeebSDK()
        path = sdk.download_url(
            stream_url="http://stream.com/video.m3u8",
            title="Test Anime",
            season=1,
            episode=1
        )
        
        assert path == "/path/to/file.mp4"
        mock_download.assert_called_once()


class TestConvenienceFunctions:
    """Test suite for convenience functions."""
    
    @patch('weeb_cli.sdk._list_providers')
    def test_list_providers_function(self, mock_list):
        """Test list_providers convenience function."""
        mock_list.return_value = [
            {"name": "animecix", "lang": "tr"}
        ]
        
        providers = list_providers()
        assert len(providers) == 1
    
    @patch('weeb_cli.sdk.list_providers')
    def test_get_provider_info_function(self, mock_list):
        """Test get_provider_info convenience function."""
        mock_list.return_value = [
            {"name": "animecix", "lang": "tr"},
            {"name": "hianime", "lang": "en"}
        ]
        
        info = get_provider_info("hianime")
        assert info["name"] == "hianime"
