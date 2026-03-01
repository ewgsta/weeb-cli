import pytest
import time
from unittest.mock import patch, MagicMock
from weeb_cli.services.tracker import MALTracker


@pytest.fixture
def mal_tracker():
    tracker = MALTracker()
    tracker._db = MagicMock()
    return tracker


class TestMALAuthentication:
    
    def test_is_authenticated(self, mal_tracker):
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        assert mal_tracker.is_authenticated() is True
    
    def test_is_not_authenticated(self, mal_tracker):
        mal_tracker.db.get_config.return_value = None
        mal_tracker._access_token = None
        
        assert mal_tracker.is_authenticated() is False
    
    def test_logout(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker._refresh_token = "refresh_token"
        mal_tracker._expires_at = time.time() + 3600
        
        mal_tracker.logout()
        
        assert mal_tracker._access_token is None
        assert mal_tracker._refresh_token is None
        assert mal_tracker._expires_at is None
        
        mal_tracker.db.set_config.assert_any_call("mal_access_token", None)
        mal_tracker.db.set_config.assert_any_call("mal_refresh_token", None)
        mal_tracker.db.set_config.assert_any_call("mal_expires_at", None)
        mal_tracker.db.set_config.assert_any_call("mal_username", None)
        mal_tracker.db.set_config.assert_any_call("mal_user_id", None)
    
    def test_get_username(self, mal_tracker):
        mal_tracker.db.get_config.return_value = "TestUser"
        username = mal_tracker.get_username()
        assert username == "TestUser"
        mal_tracker.db.get_config.assert_called_with("mal_username")


class TestMALTokenManagement:
    
    def test_save_tokens(self, mal_tracker):
        token_data = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",
            "expires_in": 3600
        }
        
        mal_tracker._save_tokens(token_data)
        
        assert mal_tracker._access_token == "new_access_token"
        assert mal_tracker._refresh_token == "new_refresh_token"
        assert mal_tracker._expires_at is not None
        
        mal_tracker.db.set_config.assert_any_call("mal_access_token", "new_access_token")
        mal_tracker.db.set_config.assert_any_call("mal_refresh_token", "new_refresh_token")
    
    def test_exchange_code_success(self, mal_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "access_token": "test_token",
            "refresh_token": "refresh_token",
            "expires_in": 3600
        }
        
        mock_user = {"id": 123, "name": "TestUser"}
        
        with patch("requests.post", return_value=mock_resp):
            with patch.object(mal_tracker, "_get_user", return_value=mock_user):
                result = mal_tracker._exchange_code("auth_code", "code_verifier")
        
        assert result == mock_user
    
    def test_exchange_code_failure(self, mal_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        
        with patch("requests.post", return_value=mock_resp):
            result = mal_tracker._exchange_code("invalid_code", "code_verifier")
        
        assert result is None
    
    def test_refresh_access_token_success(self, mal_tracker):
        mal_tracker._refresh_token = "refresh_token"
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "access_token": "new_token",
            "refresh_token": "new_refresh",
            "expires_in": 3600
        }
        
        with patch("requests.post", return_value=mock_resp):
            result = mal_tracker._refresh_access_token()
        
        assert result is True
        assert mal_tracker._access_token == "new_token"
    
    def test_refresh_access_token_failure(self, mal_tracker):
        mal_tracker._refresh_token = "invalid_refresh"
        
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        
        with patch("requests.post", return_value=mock_resp):
            result = mal_tracker._refresh_access_token()
        
        assert result is False
    
    def test_access_token_auto_refresh(self, mal_tracker):
        expired_time = time.time() - 100
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "old_token",
            "mal_refresh_token": "refresh_token",
            "mal_expires_at": str(expired_time)
        }.get(key)
        
        with patch.object(mal_tracker, "_refresh_access_token", return_value=True):
            token = mal_tracker.access_token
            mal_tracker._refresh_access_token.assert_called_once()


class TestMALUserOperations:
    
    def test_get_user_success(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"id": 123, "name": "TestUser"}
        
        with patch("requests.get", return_value=mock_resp):
            user = mal_tracker._get_user()
        
        assert user is not None
        assert user["id"] == 123
        assert user["name"] == "TestUser"
        mal_tracker.db.set_config.assert_any_call("mal_username", "TestUser")
        mal_tracker.db.set_config.assert_any_call("mal_user_id", "123")
    
    def test_get_user_no_token(self, mal_tracker):
        mal_tracker._access_token = None
        user = mal_tracker._get_user()
        assert user is None


class TestMALSearch:
    
    def test_search_anime_success(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "data": [
                {"node": {"id": 6547, "title": "Angel Beats!"}}
            ]
        }
        
        with patch("requests.get", return_value=mock_resp):
            result = mal_tracker.search_anime("Angel Beats")
        
        assert result is not None
        assert result["id"] == 6547
    
    def test_search_anime_no_results(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": []}
        
        with patch("requests.get", return_value=mock_resp):
            result = mal_tracker.search_anime("NonexistentAnime")
        
        assert result is None
    
    def test_search_anime_not_authenticated(self, mal_tracker):
        mal_tracker.db.get_config.return_value = None
        mal_tracker._access_token = None
        
        result = mal_tracker.search_anime("Angel Beats")
        assert result is None


class TestMALProgressUpdate:
    
    def test_update_progress_not_authenticated(self, mal_tracker):
        mal_tracker.db.get_config.return_value = None
        mal_tracker._access_token = None
        
        result = mal_tracker.update_progress("Angel Beats", 5, 13)
        
        assert result is False
        pending_calls = [call for call in mal_tracker.db.set_config.call_args_list 
                        if "mal_pending" in str(call)]
        assert len(pending_calls) > 0
    
    def test_update_progress_anime_not_found(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        with patch.object(mal_tracker, "search_anime", return_value=None):
            result = mal_tracker.update_progress("NonexistentAnime", 1, 12)
        
        assert result is False
    
    def test_update_progress_success_watching(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        mock_anime = {"id": 6547, "title": "Angel Beats!"}
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        
        with patch.object(mal_tracker, "search_anime", return_value=mock_anime):
            with patch("requests.post", return_value=mock_resp):
                result = mal_tracker.update_progress("Angel Beats", 5, 13)
        
        assert result is True
    
    def test_update_progress_success_completed(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600)
        }.get(key)
        
        mock_anime = {"id": 6547, "title": "Angel Beats!"}
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        
        with patch.object(mal_tracker, "search_anime", return_value=mock_anime):
            with patch("requests.post", return_value=mock_resp):
                result = mal_tracker.update_progress("Angel Beats", 13, 13)
        
        assert result is True


class TestMALPendingSync:
    
    def test_queue_update(self, mal_tracker):
        mal_tracker.db.get_config.return_value = []
        
        mal_tracker._queue_update("Angel Beats", 5, 13)
        
        set_calls = mal_tracker.db.set_config.call_args_list
        pending_call = [call for call in set_calls if "mal_pending" in str(call)][0]
        pending_data = pending_call[0][1]
        
        assert len(pending_data) == 1
        assert pending_data[0]["title"] == "Angel Beats"
        assert pending_data[0]["episode"] == 5
        assert pending_data[0]["total"] == 13
    
    def test_sync_pending_success(self, mal_tracker):
        mal_tracker._access_token = "test_token"
        mal_tracker.db.get_config.side_effect = lambda key: {
            "mal_access_token": "test_token",
            "mal_expires_at": str(time.time() + 3600),
            "mal_pending": [
                {"title": "Anime1", "episode": 5, "total": 12, "timestamp": 123456},
                {"title": "Anime2", "episode": 3, "total": 24, "timestamp": 123457}
            ]
        }.get(key, None)
        
        with patch.object(mal_tracker, "update_progress", return_value=True):
            synced = mal_tracker.sync_pending()
        
        assert synced == 2
    
    def test_sync_pending_not_authenticated(self, mal_tracker):
        mal_tracker.db.get_config.return_value = None
        mal_tracker._access_token = None
        
        synced = mal_tracker.sync_pending()
        assert synced == 0
    
    def test_get_pending_count(self, mal_tracker):
        mal_tracker.db.get_config.return_value = [
            {"title": "Anime1", "episode": 5},
            {"title": "Anime2", "episode": 3},
            {"title": "Anime3", "episode": 1}
        ]
        
        count = mal_tracker.get_pending_count()
        assert count == 3
    
    def test_get_pending_count_empty(self, mal_tracker):
        mal_tracker.db.get_config.return_value = []
        count = mal_tracker.get_pending_count()
        assert count == 0
