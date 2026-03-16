"""Tests for Aniworld provider"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from weeb_cli.providers.de.aniworld import AniWorldProvider
from weeb_cli.providers.base import AnimeResult, Episode, StreamLink


class TestAniWorldProvider:
    """Test suite for Aniworld provider"""

    @pytest.fixture
    def provider(self):
        """Create provider instance"""
        return AniWorldProvider()

    def test_provider_initialization(self, provider):
        """Test provider is initialized correctly"""
        assert provider.name == "aniworld"
        assert provider.lang == "de"
        assert provider.region == "DE"
        assert hasattr(provider, '_html_cache')
        assert isinstance(provider._html_cache, dict)

    def test_score_hoster_language_priority(self, provider):
        """Test hoster scoring prioritizes language correctly"""
        # GerDub should score highest
        score_gerdub = provider._score_hoster("GerDub", "720p", "Vidmoly")
        score_gersub = provider._score_hoster("GerSub", "720p", "Vidmoly")
        score_engsub = provider._score_hoster("EngSub", "720p", "Vidmoly")
        
        assert score_gerdub > score_gersub > score_engsub

    def test_score_hoster_quality_priority(self, provider):
        """Test hoster scoring prioritizes quality correctly"""
        score_1080p = provider._score_hoster("GerDub", "1080p", "Vidmoly")
        score_720p = provider._score_hoster("GerDub", "720p", "Vidmoly")
        score_480p = provider._score_hoster("GerDub", "480p", "Vidmoly")
        
        assert score_1080p > score_720p > score_480p

    def test_score_hoster_preference(self, provider):
        """Test hoster scoring prioritizes preferred hosters"""
        score_vidmoly = provider._score_hoster("GerDub", "720p", "Vidmoly")
        score_voe = provider._score_hoster("GerDub", "720p", "VOE")
        score_streamtape = provider._score_hoster("GerDub", "720p", "Streamtape")
        
        assert score_vidmoly > score_voe > score_streamtape

    def test_extract_quality_from_html(self, provider):
        """Test quality extraction from HTML"""
        assert provider._extract_quality("1080p quality") == "1080p"
        assert provider._extract_quality("720p HD") == "720p"
        assert provider._extract_quality("480p stream") == "480p"
        assert provider._extract_quality("HD quality") == "HD"
        assert provider._extract_quality("no quality info") == "N/A"

    @patch('weeb_cli.providers.de.aniworld.requests.Session.post')
    def test_search_success(self, mock_post, provider):
        """Test search returns results"""
        mock_response = Mock()
        mock_response.text = '[{"title":"One Piece","link":"/anime/stream/one-piece"}]'
        mock_post.return_value = mock_response
        
        results = provider.search("One Piece")
        
        assert len(results) == 1
        assert results[0].title == "One Piece"
        assert results[0].id == "one-piece"
        assert results[0].type == "series"

    @patch('weeb_cli.providers.de.aniworld.requests.Session.post')
    def test_search_filters_non_anime(self, mock_post, provider):
        """Test search filters out non-anime results"""
        mock_response = Mock()
        mock_response.text = '''[
            {"title":"One Piece","link":"/anime/stream/one-piece"},
            {"title":"Manga","link":"/manga/one-piece"}
        ]'''
        mock_post.return_value = mock_response
        
        results = provider.search("One Piece")
        
        assert len(results) == 1
        assert results[0].id == "one-piece"

    @patch('weeb_cli.providers.de.aniworld.requests.Session.post')
    def test_search_empty_results(self, mock_post, provider):
        """Test search with no results"""
        mock_response = Mock()
        mock_response.text = '[]'
        mock_post.return_value = mock_response
        
        results = provider.search("NonExistentAnime")
        
        assert len(results) == 0

    @patch('weeb_cli.providers.de.aniworld.requests.Session.get')
    def test_get_episodes_with_cache(self, mock_get, provider):
        """Test episode fetching uses cache"""
        mock_response = Mock()
        mock_response.text = '''
            <html>
                <a href="/anime/stream/test/staffel-1/episode-1">Episode 1</a>
                <a href="/anime/stream/test/staffel-1/episode-2">Episode 2</a>
            </html>
        '''
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # First call
        episodes1 = provider.get_episodes("test", season=1)
        # Second call should use cache
        episodes2 = provider.get_episodes("test", season=1)
        
        assert len(episodes1) == 2
        assert len(episodes2) == 2
        # Should only call get once due to caching
        assert mock_get.call_count == 1

    def test_html_cache_functionality(self, provider):
        """Test HTML caching works correctly"""
        with patch.object(provider, '_get', wraps=provider._get) as mock_get:
            with patch('weeb_cli.providers.de.aniworld.requests.Session.get') as mock_session_get:
                mock_response = Mock()
                mock_response.text = "<html>test</html>"
                mock_response.raise_for_status = Mock()
                mock_session_get.return_value = mock_response
                
                url = "https://aniworld.to/test"
                
                # First call with cache
                result1 = provider._get(url, use_cache=True)
                # Second call should use cache
                result2 = provider._get(url, use_cache=True)
                
                assert result1 == result2
                assert mock_session_get.call_count == 1

    @patch('weeb_cli.providers.de.aniworld.requests.Session.get')
    def test_extract_video_from_embed_vidmoly(self, mock_get, provider):
        """Test Vidmoly video extraction"""
        mock_response = Mock()
        mock_response.text = '''
            <script>
                sources: "https://example.com/video.m3u8"
            </script>
        '''
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        url = provider._extract_video_from_embed("https://vidmoly.to/embed/test", "Vidmoly")
        
        assert url is not None
        assert ".m3u8" in url

    def test_extract_video_from_embed_unknown_hoster(self, provider):
        """Test extraction returns None for unknown hoster"""
        url = provider._extract_video_from_embed("https://unknown.com/embed", "UnknownHoster")
        assert url is None

    @patch('weeb_cli.providers.de.aniworld.requests.Session.get')
    def test_get_streams_with_fallback(self, mock_get, provider):
        """Test stream extraction tries multiple hosters"""
        # Mock episode page with multiple hosters
        episode_html = '''
            <html>
                <li data-link-target="/redirect/123" data-lang-key="1">
                    <i class="icon Vidmoly"></i>
                    <h4>Vidmoly</h4>
                </li>
                <li data-link-target="/redirect/456" data-lang-key="1">
                    <i class="icon VOE"></i>
                    <h4>VOE</h4>
                </li>
            </html>
        '''
        
        # Mock redirect responses
        def get_side_effect(url, *args, **kwargs):
            response = Mock()
            response.raise_for_status = Mock()
            
            if "episode" in url:
                response.text = episode_html
            elif "redirect/123" in url:
                response.url = "https://vidmoly.to/embed/test"
                response.text = 'sources: "https://example.com/video1.m3u8"'
            elif "redirect/456" in url:
                response.url = "https://voe.sx/embed/test"
                response.text = 'sources: "https://example.com/video2.m3u8"'
            else:
                response.text = ""
            
            return response
        
        mock_get.side_effect = get_side_effect
        
        streams = provider.get_streams("test", "test/staffel-1/episode-1")
        
        # Should find streams from both hosters
        assert len(streams) >= 1
        assert any("GerDub" in s.quality for s in streams)

    @patch('weeb_cli.providers.de.aniworld.requests.Session.get')
    def test_get_details_extracts_title_correctly(self, mock_get, provider):
        """Test anime details extraction with proper title parsing"""
        mock_response = Mock()
        mock_response.text = '''
            <html>
                <h1 itemprop="name"><span>One Piece</span></h1>
                <a href="/anime/stream/one-piece/staffel-1/episode-1">Episode 1</a>
            </html>
        '''
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        details = provider.get_details("one-piece")
        
        assert details is not None
        assert details.title == "One Piece"
        assert details.id == "one-piece"

    def test_provider_session_has_correct_headers(self, provider):
        """Test provider session is configured with correct headers"""
        assert "User-Agent" in provider.headers
        assert "Referer" in provider.headers
        assert "aniworld.to" in provider.headers["Referer"]


class TestAniWorldProviderIntegration:
    """Integration tests for Aniworld provider (requires network)"""

    @pytest.fixture
    def provider(self):
        return AniWorldProvider()

    @pytest.mark.skip(reason="Network test - run manually")
    def test_real_search(self, provider):
        """Test real search (manual test)"""
        results = provider.search("One Piece")
        assert len(results) > 0
        assert any("One Piece" in r.title for r in results)

    @pytest.mark.skip(reason="Network test - run manually")
    def test_real_episodes(self, provider):
        """Test real episode fetching (manual test)"""
        episodes = provider.get_episodes("one-piece", season=1)
        assert len(episodes) > 0
        assert all(isinstance(e, Episode) for e in episodes)

    @pytest.mark.skip(reason="Network test - run manually")
    def test_real_streams(self, provider):
        """Test real stream extraction (manual test)"""
        streams = provider.get_streams("one-piece", "one-piece/staffel-1/episode-1")
        assert len(streams) > 0
        assert all(isinstance(s, StreamLink) for s in streams)
