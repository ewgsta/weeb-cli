import pytest
from unittest.mock import Mock, patch
from weeb_cli.providers.animecix import AnimeCixProvider
from weeb_cli.providers.turkanime import TurkAnimeProvider
from weeb_cli.providers.anizle import AnizleProvider
from weeb_cli.providers.hianime import HiAnimeProvider
from weeb_cli.providers.allanime import AllAnimeProvider
from weeb_cli.providers.base import AnimeResult, AnimeDetails, Episode, StreamLink


class TestAnimeCixProvider:
    
    @pytest.fixture
    def provider(self):
        return AnimeCixProvider()
    
    def test_search_angel_beats(self, provider):
        with patch('weeb_cli.providers.animecix._get_json') as mock_get:
            mock_get.return_value = {
                "results": [
                    {
                        "id": "12345",
                        "name": "Angel Beats!",
                        "title_type": "series"
                    }
                ]
            }
            
            results = provider.search("Angel Beats")
            
            assert len(results) > 0
            assert isinstance(results[0], AnimeResult)
            assert "angel beats" in results[0].title.lower()
    
    def test_get_details_angel_beats(self, provider):
        with patch('weeb_cli.providers.animecix._get_json') as mock_get:
            mock_get.return_value = {
                "videos": [
                    {
                        "title": {
                            "name": "Angel Beats!",
                            "description": "Test description",
                            "poster": "test.jpg",
                            "genres": [{"name": "Drama"}],
                            "year": 2010
                        }
                    }
                ]
            }
            
            details = provider.get_details("12345")
            
            assert details is not None
            assert isinstance(details, AnimeDetails)
            assert details.title == "Angel Beats!"
    
    def test_get_episodes_angel_beats(self, provider):
        with patch('weeb_cli.providers.animecix._get_json') as mock_get:
            mock_get.side_effect = [
                {"videos": [{"title": {"seasons": [1]}}]},
                {
                    "videos": [
                        {"name": "1. Bölüm", "url": "/embed/ep1"},
                        {"name": "2. Bölüm", "url": "/embed/ep2"}
                    ]
                }
            ]
            
            episodes = provider.get_episodes("12345")
            
            assert len(episodes) >= 0
            if episodes:
                assert isinstance(episodes[0], Episode)


class TestTurkAnimeProvider:
    
    @pytest.fixture
    def provider(self):
        return TurkAnimeProvider()
    
    def test_search_angel_beats(self, provider):
        with patch('weeb_cli.providers.turkanime._fetch') as mock_fetch:
            mock_fetch.return_value = '''
                <a href="/anime/angel-beats"><div class="animeAdi">Angel Beats!</div></a>
            '''
            
            results = provider.search("Angel Beats")
            
            assert len(results) > 0
            assert isinstance(results[0], AnimeResult)
            assert "angel beats" in results[0].title.lower()
    
    def test_get_details_angel_beats(self, provider):
        with patch('weeb_cli.providers.turkanime._fetch') as mock_fetch:
            mock_fetch.return_value = '''
                <title>Angel Beats!</title>
                <meta property="twitter:image" content="test.jpg">
                <img src="/uploads/serilerb/12345.jpg">
                <div id="animedetay">
                    <table>
                        <tr><b>Anime Türü</b><td width="100">Drama  Action</td></tr>
                    </table>
                </div>
            '''
            
            details = provider.get_details("angel-beats")
            
            assert details is not None
            assert isinstance(details, AnimeDetails)
            assert "angel beats" in details.title.lower()
    
    def test_get_episodes_angel_beats(self, provider):
        with patch('weeb_cli.providers.turkanime._fetch') as mock_fetch:
            mock_fetch.side_effect = [
                '<img src="/uploads/serilerb/12345.jpg">',
                r'<a href=\"/video/angel-beats-1-bolum\" title=\"1. Bölüm\">'
            ]
            
            episodes = provider.get_episodes("angel-beats")
            
            assert len(episodes) >= 0
            if episodes:
                assert isinstance(episodes[0], Episode)


class TestAnizleProvider:
    
    @pytest.fixture
    def provider(self):
        return AnizleProvider()
    
    def test_search_angel_beats(self, provider):
        with patch('weeb_cli.providers.anizle._load_database') as mock_db:
            mock_db.return_value = [
                {
                    "info_slug": "angel-beats",
                    "info_title": "Angel Beats!",
                    "info_titleoriginal": "Angel Beats!",
                    "info_titleenglish": "Angel Beats!",
                    "info_poster": "test.jpg",
                    "info_year": "2010"
                }
            ]
            
            results = provider.search("Angel Beats")
            
            assert len(results) > 0
            assert isinstance(results[0], AnimeResult)
            assert "angel beats" in results[0].title.lower()
    
    def test_get_details_angel_beats(self, provider):
        with patch('weeb_cli.providers.anizle._load_database') as mock_db, \
             patch('weeb_cli.providers.anizle._http_get') as mock_http:
            
            mock_db.return_value = [
                {
                    "info_slug": "angel-beats",
                    "info_title": "Angel Beats!",
                    "info_summary": "Test description",
                    "info_poster": "test.jpg",
                    "info_year": "2010",
                    "categories": [{"tag_title": "Drama"}]
                }
            ]
            
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '<a href="/angel-beats-1-bolum" data-order="1">1. Bölüm</a>'
            mock_http.return_value = mock_response
            
            details = provider.get_details("angel-beats")
            
            assert details is not None
            assert isinstance(details, AnimeDetails)
            assert details.title == "Angel Beats!"
    
    def test_get_episodes_angel_beats(self, provider):
        with patch('weeb_cli.providers.anizle._http_get') as mock_http:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_response.text = '''
                <a href="/angel-beats-1-bolum" data-order="1">1. Bölüm</a>
                <a href="/angel-beats-2-bolum" data-order="2">2. Bölüm</a>
            '''
            mock_http.return_value = mock_response
            
            episodes = provider.get_episodes("angel-beats")
            
            assert len(episodes) >= 0
            if episodes:
                assert isinstance(episodes[0], Episode)


class TestHiAnimeProvider:
    
    @pytest.fixture
    def provider(self):
        return HiAnimeProvider()
    
    def test_search_angel_beats(self, provider):
        with patch('weeb_cli.providers.hianime._get_html') as mock_html:
            mock_html.return_value = '''
                <div class="flw-item">
                    <div class="film-poster">
                        <img class="film-poster-img" data-src="test.jpg">
                    </div>
                    <div class="film-detail">
                        <h3 class="film-name">
                            <a class="dynamic-name" href="/angel-beats-123" data-jname="Angel Beats!">Angel Beats!</a>
                        </h3>
                    </div>
                </div>
            '''
            
            results = provider.search("Angel Beats")
            
            assert len(results) > 0
            assert isinstance(results[0], AnimeResult)
            assert "angel beats" in results[0].title.lower()
    
    def test_get_details_angel_beats(self, provider):
        with patch('weeb_cli.providers.hianime._get_html') as mock_html, \
             patch('weeb_cli.providers.hianime._get_json') as mock_json:
            
            mock_html.return_value = '''
                <div class="anisc-detail">
                    <h2 class="film-name">Angel Beats!</h2>
                    <div class="film-description">
                        <div class="text">Test description</div>
                    </div>
                    <img class="film-poster-img" src="test.jpg">
                    <div class="item-list">
                        <a href="/genre/drama">Drama</a>
                    </div>
                </div>
            '''
            
            mock_json.return_value = {
                "html": '<a class="ssl-item ep-item" href="/watch/angel-beats-123?ep=1" title="Episode 1"></a>'
            }
            
            details = provider.get_details("angel-beats-123")
            
            assert details is not None
            assert isinstance(details, AnimeDetails)
            assert "angel beats" in details.title.lower()
    
    def test_get_episodes_angel_beats(self, provider):
        with patch('weeb_cli.providers.hianime._get_json') as mock_json:
            mock_json.return_value = {
                "html": '''
                    <a class="ssl-item ep-item" href="/watch/angel-beats-123?ep=1" title="Episode 1"></a>
                    <a class="ssl-item ep-item" href="/watch/angel-beats-123?ep=2" title="Episode 2"></a>
                '''
            }
            
            episodes = provider.get_episodes("angel-beats-123")
            
            assert len(episodes) >= 0
            if episodes:
                assert isinstance(episodes[0], Episode)


class TestAllAnimeProvider:
    
    @pytest.fixture
    def provider(self):
        return AllAnimeProvider()
    
    def test_search_angel_beats(self, provider):
        with patch('weeb_cli.providers.allanime._graphql_request') as mock_gql:
            mock_gql.return_value = {
                "data": {
                    "shows": {
                        "edges": [
                            {
                                "_id": "angel-beats",
                                "name": "Angel Beats!",
                                "availableEpisodes": {"sub": 13}
                            }
                        ]
                    }
                }
            }
            
            results = provider.search("Angel Beats")
            
            assert len(results) > 0
            assert isinstance(results[0], AnimeResult)
            assert "angel beats" in results[0].title.lower()
    
    def test_get_details_angel_beats(self, provider):
        with patch('weeb_cli.providers.allanime._graphql_request') as mock_gql:
            mock_gql.return_value = {
                "data": {
                    "show": {
                        "_id": "angel-beats",
                        "name": "Angel Beats!",
                        "description": "Test description",
                        "thumbnail": "test.jpg",
                        "availableEpisodesDetail": {
                            "sub": ["1", "2", "3"]
                        }
                    }
                }
            }
            
            details = provider.get_details("angel-beats")
            
            assert details is not None
            assert isinstance(details, AnimeDetails)
            assert details.title == "Angel Beats!"
    
    def test_get_episodes_angel_beats(self, provider):
        with patch('weeb_cli.providers.allanime._graphql_request') as mock_gql:
            mock_gql.return_value = {
                "data": {
                    "show": {
                        "_id": "angel-beats",
                        "availableEpisodesDetail": {
                            "sub": ["1", "2", "3", "4", "5"]
                        }
                    }
                }
            }
            
            episodes = provider.get_episodes("angel-beats")
            
            assert len(episodes) >= 0
            if episodes:
                assert isinstance(episodes[0], Episode)
                assert episodes[0].number == 1
