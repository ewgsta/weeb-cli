"""Utility decorators for common patterns.

This module provides reusable decorators to reduce code duplication
and improve maintainability.
"""

from functools import wraps
from typing import Callable, TypeVar

T = TypeVar('T')


def lazy_property(import_path: str):
    """Decorator for lazy-loading properties.
    
    Defers importing and initializing a dependency until first access.
    Useful for avoiding circular imports and reducing startup time.
    
    Args:
        import_path: Full import path to the object (e.g., 'weeb_cli.services.database.db').
    
    Returns:
        Property decorator that lazy-loads the dependency.
    
    Example:
        >>> class MyService:
        ...     @lazy_property('weeb_cli.services.database.db')
        ...     def db(self):
        ...         pass
        ...
        ...     def query(self):
        ...         return self.db.execute("SELECT * FROM table")
    """
    def decorator(func: Callable[[], T]) -> property:
        attr_name = f'_lazy_{func.__name__}'
        
        @wraps(func)
        def wrapper(self):
            if not hasattr(self, attr_name):
                module_path, obj_name = import_path.rsplit('.', 1)
                module = __import__(module_path, fromlist=[obj_name])
                setattr(self, attr_name, getattr(module, obj_name))
            return getattr(self, attr_name)
        
        return property(wrapper)
    return decorator
