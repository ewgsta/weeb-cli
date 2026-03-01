import pytest
from unittest.mock import patch, MagicMock
from weeb_cli.services.tracker import AniListTracker


@pytest.fixture
def anilist_tracker():
    tracker = AniListTracker()
    tracker._db = MagicMock()
    return tracker


class TestAniListAuthentication:
    
    def test_authenticate_success(self, anilist_tracker):
        mock_viewer = {"id": 123, "name": "TestUser"}
        
        with patch.object(anilist_tracker, "_get_viewer", return_value=mock_viewer):
            result = anilist_tracker.authenticate("test_token_123")
        
        assert result is True
        anilist_tracker.db.set_config.assert_any_call("anilist_token", "test_token_123")
        anilist_tracker.db.set_config.assert_any_call("anilist_user_id", "123")
        anilist_tracker.db.set_config.assert_any_call("anilist_username", "TestUser")
    
    def test_authenticate_failure(self, anilist_tracker):
        with patch.object(anilist_tracker, "_get_viewer", return_value=None):
            result = anilist_tracker.authenticate("invalid_token")
        
        assert result is False
    
    def test_is_authenticated(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = "test_token"
        assert anilist_tracker.is_authenticated() is True
        
        anilist_tracker.db.get_config.return_value = None
        anilist_tracker._token = None
        assert anilist_tracker.is_authenticated() is False
    
    def test_logout(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker._user_id = "123"
        
        anilist_tracker.logout()
        
        assert anilist_tracker._token is None
        assert anilist_tracker._user_id is None
        anilist_tracker.db.set_config.assert_any_call("anilist_token", None)
        anilist_tracker.db.set_config.assert_any_call("anilist_user_id", None)
        anilist_tracker.db.set_config.assert_any_call("anilist_username", None)
    
    def test_get_username(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = "TestUser"
        username = anilist_tracker.get_username()
        assert username == "TestUser"
        anilist_tracker.db.get_config.assert_called_with("anilist_username")


class TestAniListGraphQL:
    
    def test_graphql_success(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": {"Media": {"id": 1}}}
        
        with patch("requests.post", return_value=mock_resp):
            result = anilist_tracker._graphql("query { Media { id } }")
        
        assert result == {"Media": {"id": 1}}
    
    def test_graphql_no_token(self, anilist_tracker):
        anilist_tracker._token = None
        result = anilist_tracker._graphql("query { Media { id } }")
        assert result is None
    
    def test_graphql_error(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        
        with patch("requests.post", return_value=mock_resp):
            result = anilist_tracker._graphql("invalid query")
        
        assert result is None


class TestAniListSearch:
    
    def test_search_anime_success(self, anilist_tracker):
        mock_data = {
            "Media": {
                "id": 6547,
                "title": {"romaji": "Angel Beats!", "english": "Angel Beats!"},
                "episodes": 13
            }
        }
        
        with patch.object(anilist_tracker, "_graphql", return_value=mock_data):
            result = anilist_tracker.search_anime("Angel Beats")
        
        assert result is not None
        assert result["id"] == 6547
        assert result["episodes"] == 13
    
    def test_search_anime_not_found(self, anilist_tracker):
        with patch.object(anilist_tracker, "_graphql", return_value=None):
            result = anilist_tracker.search_anime("NonexistentAnime")
        
        assert result is None


class TestAniListProgressUpdate:
    
    def test_update_progress_not_authenticated(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = None
        anilist_tracker._token = None
        
        result = anilist_tracker.update_progress("Angel Beats", 5, 13)
        
        assert result is False
        pending_calls = [call for call in anilist_tracker.db.set_config.call_args_list 
                        if "anilist_pending" in str(call)]
        assert len(pending_calls) > 0
    
    def test_update_progress_anime_not_found(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker.db.get_config.return_value = "test_token"
        
        with patch.object(anilist_tracker, "search_anime", return_value=None):
            result = anilist_tracker.update_progress("NonexistentAnime", 1, 12)
        
        assert result is False
    
    def test_update_progress_success_current(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker.db.get_config.return_value = "test_token"
        
        mock_anime = {"id": 6547, "episodes": 13}
        mock_result = {"SaveMediaListEntry": {"id": 1, "progress": 5, "status": "CURRENT"}}
        
        with patch.object(anilist_tracker, "search_anime", return_value=mock_anime):
            with patch.object(anilist_tracker, "_graphql", return_value=mock_result):
                result = anilist_tracker.update_progress("Angel Beats", 5, 13)
        
        assert result is True
    
    def test_update_progress_success_completed(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker.db.get_config.return_value = "test_token"
        
        mock_anime = {"id": 6547, "episodes": 13}
        mock_result = {"SaveMediaListEntry": {"id": 1, "progress": 13, "status": "COMPLETED"}}
        
        with patch.object(anilist_tracker, "search_anime", return_value=mock_anime):
            with patch.object(anilist_tracker, "_graphql", return_value=mock_result):
                result = anilist_tracker.update_progress("Angel Beats", 13, 13)
        
        assert result is True


class TestAniListPendingSync:
    
    def test_queue_update(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = []
        
        anilist_tracker._queue_update("Angel Beats", 5, 13)
        
        set_calls = anilist_tracker.db.set_config.call_args_list
        pending_call = [call for call in set_calls if "anilist_pending" in str(call)][0]
        pending_data = pending_call[0][1]
        
        assert len(pending_data) == 1
        assert pending_data[0]["title"] == "Angel Beats"
        assert pending_data[0]["episode"] == 5
        assert pending_data[0]["total"] == 13
    
    def test_sync_pending_success(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker.db.get_config.side_effect = lambda key: {
            "anilist_token": "test_token",
            "anilist_pending": [
                {"title": "Anime1", "episode": 5, "total": 12, "timestamp": 123456},
                {"title": "Anime2", "episode": 3, "total": 24, "timestamp": 123457}
            ]
        }.get(key, None)
        
        with patch.object(anilist_tracker, "update_progress", return_value=True):
            synced = anilist_tracker.sync_pending()
        
        assert synced == 2
    
    def test_sync_pending_partial_failure(self, anilist_tracker):
        anilist_tracker._token = "test_token"
        anilist_tracker.db.get_config.side_effect = lambda key: {
            "anilist_token": "test_token",
            "anilist_pending": [
                {"title": "Anime1", "episode": 5, "total": 12, "timestamp": 123456},
                {"title": "Anime2", "episode": 3, "total": 24, "timestamp": 123457}
            ]
        }.get(key, None)
        
        with patch.object(anilist_tracker, "update_progress", side_effect=[True, False]):
            synced = anilist_tracker.sync_pending()
        
        assert synced == 1
    
    def test_get_pending_count(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = [
            {"title": "Anime1", "episode": 5},
            {"title": "Anime2", "episode": 3}
        ]
        
        count = anilist_tracker.get_pending_count()
        assert count == 2
    
    def test_get_pending_count_empty(self, anilist_tracker):
        anilist_tracker.db.get_config.return_value = []
        count = anilist_tracker.get_pending_count()
        assert count == 0
