import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

DB_PATH = Path.home() / ".weeb-cli" / "weeb.db"

class Database:
    def __init__(self):
        self.db_path = DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        self._migrate_from_json()
    
    @contextmanager
    def _conn(self):
        conn = sqlite3.connect(self.db_path, timeout=10)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()
    
    def _init_db(self):
        with self._conn() as conn:
            conn.executescript('''
                CREATE TABLE IF NOT EXISTS config (
                    key TEXT PRIMARY KEY,
                    value TEXT
                );
                
                CREATE TABLE IF NOT EXISTS progress (
                    slug TEXT PRIMARY KEY,
                    title TEXT,
                    last_watched INTEGER DEFAULT 0,
                    total_episodes INTEGER DEFAULT 0,
                    completed TEXT DEFAULT '[]',
                    last_watched_at TEXT
                );
                
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT UNIQUE,
                    searched_at TEXT
                );
                
                CREATE TABLE IF NOT EXISTS download_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    anime_title TEXT,
                    episode_number INTEGER,
                    episode_id TEXT,
                    slug TEXT,
                    season INTEGER DEFAULT 1,
                    status TEXT DEFAULT 'pending',
                    progress INTEGER DEFAULT 0,
                    eta TEXT DEFAULT '?',
                    error TEXT,
                    added_at REAL
                );
                
                CREATE TABLE IF NOT EXISTS external_drives (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT UNIQUE,
                    name TEXT,
                    added_at TEXT
                );
                
                CREATE TABLE IF NOT EXISTS anime_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    source_path TEXT,
                    source_name TEXT,
                    folder_path TEXT,
                    episode_count INTEGER DEFAULT 0,
                    indexed_at TEXT
                );
                
                CREATE INDEX IF NOT EXISTS idx_queue_status ON download_queue(status);
                CREATE INDEX IF NOT EXISTS idx_progress_slug ON progress(slug);
                CREATE INDEX IF NOT EXISTS idx_anime_title ON anime_index(title);
                CREATE INDEX IF NOT EXISTS idx_anime_source ON anime_index(source_path);
            ''')
    
    def _migrate_from_json(self):
        config_dir = Path.home() / ".weeb-cli"
        
        config_file = config_dir / "config.json"
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for key, value in data.items():
                    self.set_config(key, value)
                config_file.rename(config_file.with_suffix('.json.bak'))
            except:
                pass
        
        progress_file = config_dir / "progress.json"
        if progress_file.exists():
            try:
                with open(progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for slug, info in data.items():
                    self.save_progress(
                        slug,
                        info.get("title", slug),
                        info.get("last_watched", 0),
                        info.get("total_episodes", 0),
                        info.get("completed", []),
                        info.get("last_watched_at")
                    )
                progress_file.rename(progress_file.with_suffix('.json.bak'))
            except:
                pass
        
        history_file = config_dir / "search_history.json"
        if history_file.exists():
            try:
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for query in reversed(data):
                    self.add_search_history(query)
                history_file.rename(history_file.with_suffix('.json.bak'))
            except:
                pass
        
        queue_file = config_dir / "download_queue.json"
        if queue_file.exists():
            try:
                with open(queue_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                for item in data:
                    self.add_to_queue(item)
                queue_file.rename(queue_file.with_suffix('.json.bak'))
            except:
                pass
    
    def get_config(self, key, default=None):
        with self._conn() as conn:
            row = conn.execute('SELECT value FROM config WHERE key = ?', (key,)).fetchone()
            if row:
                try:
                    return json.loads(row['value'])
                except:
                    return row['value']
            return default
    
    def set_config(self, key, value):
        with self._conn() as conn:
            conn.execute(
                'INSERT OR REPLACE INTO config (key, value) VALUES (?, ?)',
                (key, json.dumps(value))
            )
    
    def get_all_config(self):
        with self._conn() as conn:
            rows = conn.execute('SELECT key, value FROM config').fetchall()
            result = {}
            for row in rows:
                try:
                    result[row['key']] = json.loads(row['value'])
                except:
                    result[row['key']] = row['value']
            return result
    
    def save_progress(self, slug, title, last_watched, total_episodes, completed, last_watched_at=None):
        with self._conn() as conn:
            conn.execute('''
                INSERT OR REPLACE INTO progress 
                (slug, title, last_watched, total_episodes, completed, last_watched_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (slug, title, last_watched, total_episodes, json.dumps(completed), last_watched_at))
    
    def get_progress(self, slug):
        with self._conn() as conn:
            row = conn.execute('SELECT * FROM progress WHERE slug = ?', (slug,)).fetchone()
            if row:
                return {
                    "slug": row['slug'],
                    "title": row['title'],
                    "last_watched": row['last_watched'],
                    "total_episodes": row['total_episodes'],
                    "completed": json.loads(row['completed'] or '[]'),
                    "last_watched_at": row['last_watched_at']
                }
            return {"last_watched": 0, "completed": [], "title": "", "total_episodes": 0, "last_watched_at": None}
    
    def get_all_progress(self):
        with self._conn() as conn:
            rows = conn.execute('SELECT * FROM progress').fetchall()
            result = {}
            for row in rows:
                result[row['slug']] = {
                    "title": row['title'],
                    "last_watched": row['last_watched'],
                    "total_episodes": row['total_episodes'],
                    "completed": json.loads(row['completed'] or '[]'),
                    "last_watched_at": row['last_watched_at']
                }
            return result
    
    def add_search_history(self, query):
        with self._conn() as conn:
            conn.execute('DELETE FROM search_history WHERE query = ?', (query,))
            conn.execute(
                'INSERT INTO search_history (query, searched_at) VALUES (?, ?)',
                (query, datetime.now().isoformat())
            )
            conn.execute('''
                DELETE FROM search_history WHERE id NOT IN (
                    SELECT id FROM search_history ORDER BY searched_at DESC LIMIT 10
                )
            ''')
    
    def get_search_history(self):
        with self._conn() as conn:
            rows = conn.execute(
                'SELECT query FROM search_history ORDER BY searched_at DESC LIMIT 10'
            ).fetchall()
            return [row['query'] for row in rows]
    
    def add_to_queue(self, item):
        with self._conn() as conn:
            existing = conn.execute(
                'SELECT id FROM download_queue WHERE episode_id = ? AND status IN (?, ?)',
                (item.get('episode_id'), 'pending', 'processing')
            ).fetchone()
            if existing:
                return False
            
            conn.execute('''
                INSERT INTO download_queue 
                (anime_title, episode_number, episode_id, slug, status, progress, eta, added_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                item.get('anime_title'),
                item.get('episode_number'),
                item.get('episode_id'),
                item.get('slug'),
                item.get('status', 'pending'),
                item.get('progress', 0),
                item.get('eta', '?'),
                item.get('added_at', datetime.now().timestamp())
            ))
            return True
    
    def get_queue(self):
        with self._conn() as conn:
            rows = conn.execute('SELECT * FROM download_queue ORDER BY added_at').fetchall()
            return [dict(row) for row in rows]
    
    def update_queue_item(self, episode_id, **kwargs):
        with self._conn() as conn:
            sets = ', '.join(f'{k} = ?' for k in kwargs.keys())
            values = list(kwargs.values()) + [episode_id]
            conn.execute(f'UPDATE download_queue SET {sets} WHERE episode_id = ?', values)
    
    def clear_completed_queue(self):
        with self._conn() as conn:
            conn.execute('DELETE FROM download_queue WHERE status NOT IN (?, ?)', ('pending', 'processing'))
    
    def get_external_drives(self):
        with self._conn() as conn:
            rows = conn.execute('SELECT * FROM external_drives ORDER BY name').fetchall()
            return [dict(row) for row in rows]
    
    def add_external_drive(self, path, name=None):
        with self._conn() as conn:
            conn.execute(
                'INSERT OR REPLACE INTO external_drives (path, name, added_at) VALUES (?, ?, ?)',
                (path, name or os.path.basename(path), datetime.now().isoformat())
            )
    
    def remove_external_drive(self, path):
        with self._conn() as conn:
            conn.execute('DELETE FROM external_drives WHERE path = ?', (path,))
    
    def update_drive_name(self, path, name):
        with self._conn() as conn:
            conn.execute('UPDATE external_drives SET name = ? WHERE path = ?', (name, path))
    
    def index_anime(self, title, source_path, source_name, folder_path, episode_count):
        with self._conn() as conn:
            conn.execute('DELETE FROM anime_index WHERE folder_path = ?', (folder_path,))
            conn.execute('''
                INSERT INTO anime_index (title, source_path, source_name, folder_path, episode_count, indexed_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (title, source_path, source_name, folder_path, episode_count, datetime.now().isoformat()))
    
    def clear_source_index(self, source_path):
        with self._conn() as conn:
            conn.execute('DELETE FROM anime_index WHERE source_path = ?', (source_path,))
    
    def get_all_indexed_anime(self):
        with self._conn() as conn:
            rows = conn.execute('SELECT * FROM anime_index ORDER BY title').fetchall()
            return [dict(row) for row in rows]
    
    def search_indexed_anime(self, query):
        with self._conn() as conn:
            rows = conn.execute(
                'SELECT * FROM anime_index WHERE title LIKE ? ORDER BY title',
                (f'%{query}%',)
            ).fetchall()
            return [dict(row) for row in rows]
    
    def remove_indexed_anime(self, folder_path):
        with self._conn() as conn:
            conn.execute('DELETE FROM anime_index WHERE folder_path = ?', (folder_path,))
    
    def backup_database(self, backup_path):
        import shutil
        try:
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            return False
    
    def restore_database(self, backup_path):
        import shutil
        try:
            if not Path(backup_path).exists():
                return False
            
            backup_temp = self.db_path.with_suffix('.db.restore_backup')
            shutil.copy2(self.db_path, backup_temp)
            
            try:
                shutil.copy2(backup_path, self.db_path)
                backup_temp.unlink()
                return True
            except Exception:
                shutil.copy2(backup_temp, self.db_path)
                backup_temp.unlink()
                return False
        except Exception:
            return False

db = Database()
