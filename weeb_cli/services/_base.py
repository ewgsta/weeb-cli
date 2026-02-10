from typing import Optional, Any


class LazyService:
    
    def __init__(self):
        self._db = None
    
    @property
    def db(self):
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db


class CachedProperty:
    
    def __init__(self, config_key: str, default: Any = None):
        self.config_key = config_key
        self.default = default
        self.attr_name = f"_cached_{config_key}"
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        
        if not hasattr(obj, self.attr_name):
            value = obj.db.get_config(self.config_key)
            setattr(obj, self.attr_name, value if value is not None else self.default)
        
        return getattr(obj, self.attr_name)
    
    def __set__(self, obj, value):
        setattr(obj, self.attr_name, value)
        obj.db.set_config(self.config_key, value)
