import pytest
from unittest.mock import patch, MagicMock
from weeb_cli.services.tracker import KitsuTracker


@pytest.fixture
def kitsu_tracker():
    tracker = KitsuTracker()
    tracker._db = MagicMock()
    return tracker


class TestKitsuAuthentication:
    
    def test_authenticate_success(self, kitsu_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"access_token": "test_token"}
        
        mock_user_resp = MagicMock()
        mock_user_resp.status_code = 200
        mock_user_resp.json.return_value = {
            "data": [{
                "id": "123",
                "attributes": {"name": "TestUser"}
            }]
        }
        
        with patch("requests.post", return_value=mock_resp):
            with patch("requests.get", return_value=mock_user_resp):
                result = kitsu_tracker.authenticate("test@example.com", "password")
        
        assert result is True
        kitsu_tracker.db.set_config.assert_any_call("kitsu_access_token", "test_token")
        kitsu_tracker.db.set_config.assert_any_call("kitsu_user_id", "123")
        kitsu_tracker.db.set_config.assert_any_call("kitsu_username", "TestUser")
    
    def test_authenticate_failure(self, kitsu_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        
        with patch("requests.post", return_value=mock_resp):
            result = kitsu_tracker.authenticate("test@example.com", "wrong_password")
        
        assert result is False
    
    def test_is_authenticated(self, kitsu_tracker):
        kitsu_tracker.db.get_config.return_value = "test_token"
        assert kitsu_tracker.is_authenticated() is True
        
        kitsu_tracker.db.get_config.return_value = None
        kitsu_tracker._access_token = None
        assert kitsu_tracker.is_authenticated() is False
    
    def test_logout(self, kitsu_tracker):
        kitsu_tracker._access_token = "test_token"
        kitsu_tracker._user_id = "123"
        
        kitsu_tracker.logout()
        
        assert kitsu_tracker._access_token is None
        assert kitsu_tracker._user_id is None
        kitsu_tracker.db.set_config.assert_any_call("kitsu_access_token", None)
        kitsu_tracker.db.set_config.assert_any_call("kitsu_user_id", None)
        kitsu_tracker.db.set_config.assert_any_call("kitsu_username", None)


class TestKitsuSearch:
    
    def test_search_anime_success(self, kitsu_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "data": [{
                "id": "1",
                "attributes": {"canonicalTitle": "Cowboy Bebop"}
            }]
        }
        
        with patch("requests.get", return_value=mock_resp):
            result = kitsu_tracker.search_anime("Cowboy Bebop")
        
        assert result is not None
        assert result["id"] == "1"
    
    def test_search_anime_no_results(self, kitsu_tracker):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"data": []}
        
        with patch("requests.get", return_value=mock_resp):
            result = kitsu_tracker.search_anime("NonexistentAnime")
        
        assert result is None


class TestKitsuProgressUpdate:
    
    def test_update_progress_not_authenticated(self, kitsu_tracker):
        kitsu_tracker.db.get_config.return_value = None
        kitsu_tracker._access_token = None
        
        result = kitsu_tracker.update_progress("Cowboy Bebop", 5, 26)
        
        assert result is False
        pending = kitsu_tracker.db.set_config.call_args_list
        assert any("kitsu_pending" in str(call) for call in pending)
    
    def test_update_progress_anime_not_found(self, kitsu_tracker):
        kitsu_tracker._access_token = "test_token"
        kitsu_tracker._user_id = "123"
        kitsu_tracker.db.get_config.side_effect = lambda key: {
            "kitsu_access_token": "test_token",
            "kitsu_user_id": "123"
        }.get(key)
        
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 200
        mock_search_resp.json.return_value = {"data": []}
        
        with patch("requests.get", return_value=mock_search_resp):
            result = kitsu_tracker.update_progress("NonexistentAnime", 1, 12)
        
        assert result is False
    
    def test_update_progress_create_entry(self, kitsu_tracker):
        kitsu_tracker._access_token = "test_token"
        kitsu_tracker._user_id = "123"
        kitsu_tracker.db.get_config.side_effect = lambda key: {
            "kitsu_access_token": "test_token",
            "kitsu_user_id": "123"
        }.get(key)
        
        mock_search_resp = MagicMock()
        mock_search_resp.status_code = 200
        mock_search_resp.json.return_value = {
            "data": [{"id": "1", "attributes": {"canonicalTitle": "Cowboy Bebop"}}]
        }
        
        mock_entry_resp = MagicMock()
        mock_entry_resp.status_code = 200
        mock_entry_resp.json.return_value = {"data": []}
        
        mock_update_resp = MagicMock()
        mock_update_resp.status_code = 201
        
        with patch("requests.get", side_effect=[mock_search_resp, mock_entry_resp]):
            with patch("requests.post", return_value=mock_update_resp):
                result = kitsu_tracker.update_progress("Cowboy Bebop", 5, 26)
        
        assert result is True


class TestKitsuPendingSync:
    
    def test_sync_pending_success(self, kitsu_tracker):
        kitsu_tracker._access_token = "test_token"
        kitsu_tracker._user_id = "123"
        kitsu_tracker.db.get_config.side_effect = lambda key: {
            "kitsu_access_token": "test_token",
            "kitsu_user_id": "123",
            "kitsu_pending": [
                {"title": "Anime1", "episode": 5, "total": 12, "timestamp": 123456}
            ]
        }.get(key, None)
        
        with patch.object(kitsu_tracker, "update_progress", return_value=True):
            synced = kitsu_tracker.sync_pending()
        
        assert synced == 1
    
    def test_get_pending_count(self, kitsu_tracker):
        kitsu_tracker.db.get_config.return_value = [
            {"title": "Anime1", "episode": 5},
            {"title": "Anime2", "episode": 3}
        ]
        
        count = kitsu_tracker.get_pending_count()
        assert count == 2
