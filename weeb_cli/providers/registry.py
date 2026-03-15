import os
import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Type, Optional
from weeb_cli.providers.base import BaseProvider
from weeb_cli.services.logger import debug

_providers: Dict[str, Type[BaseProvider]] = {}
_provider_meta: Dict[str, dict] = {}
_initialized = False

def register_provider(name: str, lang: str = "tr", region: str = "TR"):
    def decorator(cls: Type[BaseProvider]) -> Type[BaseProvider]:
        cls.name = name
        cls.lang = lang
        cls.region = region
        
        _providers[name] = cls
        _provider_meta[name] = {
            "name": name,
            "lang": lang,
            "region": region,
            "class": cls.__name__
        }
        
        return cls
    return decorator

def _discover_providers():
    global _initialized
    if _initialized:
        return
        
    base_path = Path(__file__).parent
    # Check language directories (tr, en, de, etc.)
    for lang_dir in base_path.iterdir():
        if lang_dir.is_dir() and not lang_dir.name.startswith(("_", "extractors")):
            lang = lang_dir.name
            # Import all .py files in this lang directory
            for _, name, is_pkg in pkgutil.iter_modules([str(lang_dir)]):
                if not is_pkg:
                    try:
                        importlib.import_module(f"weeb_cli.providers.{lang}.{name}")
                        debug(f"[Registry] Discovered provider: {lang}/{name}")
                    except Exception as e:
                        debug(f"[Registry] Error loading provider {lang}/{name}: {e}")
    
    _initialized = True

def get_provider(name: str) -> Optional[BaseProvider]:
    _discover_providers()
    if name in _providers:
        return _providers[name]()
    return None

def get_providers_for_lang(lang: str) -> List[str]:
    _discover_providers()
    return [
        name for name, meta in _provider_meta.items()
        if meta["lang"] == lang
    ]

def list_providers() -> List[dict]:
    _discover_providers()
    return list(_provider_meta.values())

def get_default_provider(lang: str) -> Optional[str]:
    providers = get_providers_for_lang(lang)
    return providers[0] if providers else None
