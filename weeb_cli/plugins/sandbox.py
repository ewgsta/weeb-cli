import importlib
import importlib.util
import sys
import types
from pathlib import Path
from typing import Optional, Type

from weeb_cli.providers.base import BaseProvider
from weeb_cli.services.logger import debug


ALLOWED_MODULES = {
    "json", "re", "time", "math", "string", "collections",
    "urllib", "urllib.request", "urllib.parse",
    "hashlib", "base64", "html", "html.parser",
    "typing", "dataclasses",
    "xml", "xml.etree", "xml.etree.ElementTree",
    
    "requests", "bs4", "BeautifulSoup", "lxml",
    
    "weeb_cli.providers.base",
    "weeb_cli.providers.registry",
    "weeb_cli.services.logger",
    "weeb_cli.exceptions",
}

BLOCKED_BUILTINS = {
    "exec", "eval", "compile",
    "__import__",
    "breakpoint",
}


def _create_safe_builtins():
    import builtins
    
    safe = {}
    for name in dir(builtins):
        if name not in BLOCKED_BUILTINS:
            safe[name] = getattr(builtins, name)
    
    original_import = builtins.__import__
    
    def safe_import(name, *args, **kwargs):
        if _is_module_allowed(name):
            return original_import(name, *args, **kwargs)
        raise ImportError(
            f"Plugin security: access to '{name}' module is not allowed."
        )
    
    safe["__import__"] = safe_import
    safe["open"] = _blocked_open
    
    return safe


def _blocked_open(*args, **kwargs):
    raise PermissionError(
        "Plugin security: filesystem access is not allowed."
    )


def _is_module_allowed(module_name: str) -> bool:
    if module_name in ALLOWED_MODULES:
        return True
    
    for allowed in ALLOWED_MODULES:
        if module_name.startswith(allowed + "."):
            return True
    
    return False


def load_plugin_module(
    plugin_name: str,
    plugin_dir: Path,
    entry_point: str,
    entry_class: str,
) -> Optional[Type[BaseProvider]]:
    module_path = plugin_dir / entry_point
    
    if not module_path.exists():
        debug(f"[Sandbox] Entry point not found: {module_path}")
        return None
    
    module_name = f"weeb_plugin_{plugin_name}"
    
    try:
        spec = importlib.util.spec_from_file_location(
            module_name, 
            str(module_path)
        )
        
        if spec is None or spec.loader is None:
            debug(f"[Sandbox] Could not create module spec: {module_path}")
            return None
        
        module = importlib.util.module_from_spec(spec)
        
        safe_builtins = _create_safe_builtins()
        module.__builtins__ = safe_builtins
        
        if plugin_dir not in sys.path:
            sys.path.insert(0, str(plugin_dir))
        
        try:
            spec.loader.exec_module(module)
        finally:
            if str(plugin_dir) in sys.path:
                sys.path.remove(str(plugin_dir))
        
        sys.modules[module_name] = module
        
        provider_class = getattr(module, entry_class, None)
        
        if provider_class is None:
            debug(f"[Sandbox] '{entry_class}' class not found in module.")
            return None
        
        if not (isinstance(provider_class, type) and issubclass(provider_class, BaseProvider)):
            debug(f"[Sandbox] '{entry_class}' is not a BaseProvider subclass.")
            return None
        
        debug(f"[Sandbox] Plugin '{plugin_name}' loaded successfully.")
        return provider_class
        
    except ImportError as e:
        debug(f"[Sandbox] Import error: {e}")
        return None
    except PermissionError as e:
        debug(f"[Sandbox] Security error: {e}")
        return None
    except Exception as e:
        debug(f"[Sandbox] Plugin load error: {e}")
        return None


def unload_plugin_module(plugin_name: str):
    module_name = f"weeb_plugin_{plugin_name}"
    
    if module_name in sys.modules:
        del sys.modules[module_name]
        debug(f"[Sandbox] Plugin '{plugin_name}' unloaded from memory.")
