"""Provider registry system for dynamic provider discovery and management.

This module implements a registry pattern for anime providers, allowing
automatic discovery and registration of providers from the filesystem.

The registry scans language directories (tr/, en/, de/, pl/) and imports
all provider modules, registering them with metadata for easy lookup.

Functions:
    register_provider: Decorator for registering provider classes
    get_provider: Get provider instance by name
    get_providers_for_lang: Get all providers for a language
    list_providers: List all registered providers
    get_default_provider: Get default provider for a language

Example:
    Registering a provider::

        from weeb_cli.providers.registry import register_provider
        from weeb_cli.providers.base import BaseProvider
        
        @register_provider("myprovider", lang="en", region="US")
        class MyProvider(BaseProvider):
            # Implementation
            pass
    
    Using providers::

        from weeb_cli.providers import get_provider, list_providers
        
        # Get specific provider
        provider = get_provider("animecix")
        results = provider.search("One Piece")
        
        # List all providers
        all_providers = list_providers()
        for p in all_providers:
            print(f"{p['name']} ({p['lang']})")
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Type, Optional

from weeb_cli.providers.base import BaseProvider
from weeb_cli.services.logger import debug

# Global registry storage
_providers: Dict[str, Type[BaseProvider]] = {}
_provider_meta: Dict[str, dict] = {}
_initialized: bool = False


def register_provider(name: str, lang: str = "tr", region: str = "TR", disabled: bool = False):
    """Decorator for registering provider classes.
    
    Registers a provider class with metadata in the global registry.
    Sets class attributes (name, lang, region, disabled) for easy access.
    
    Args:
        name: Unique provider identifier (e.g., 'animecix', 'hianime').
        lang: Language code (e.g., 'en', 'tr', 'de', 'pl').
        region: Region code (e.g., 'US', 'TR', 'DE', 'PL').
        disabled: If True, provider is registered but not available for use.
    
    Returns:
        Decorator function that registers the class.
    
    Example:
        >>> @register_provider("myprovider", lang="en", region="US")
        ... class MyProvider(BaseProvider):
        ...     pass
        
        >>> @register_provider("oldprovider", lang="en", region="US", disabled=True)
        ... class OldProvider(BaseProvider):
        ...     pass  # Registered but not usable
    """
    def decorator(cls: Type[BaseProvider]) -> Type[BaseProvider]:
        cls.name = name
        cls.lang = lang
        cls.region = region
        cls.disabled = disabled
        
        _providers[name] = cls
        _provider_meta[name] = {
            "name": name,
            "lang": lang,
            "region": region,
            "class": cls.__name__,
            "disabled": disabled
        }
        
        return cls
    return decorator


def _discover_providers() -> None:
    """Discover and import all provider modules.
    
    Scans language directories (tr/, en/, de/, pl/) and imports all
    Python modules, triggering their @register_provider decorators.
    
    This function is called automatically on first registry access.
    Uses a global flag to ensure it only runs once.
    """
    global _initialized
    if _initialized:
        return
        
    base_path = Path(__file__).parent
    
    # Scan language directories
    for lang_dir in base_path.iterdir():
        if lang_dir.is_dir() and not lang_dir.name.startswith(("_", "extractors")):
            lang = lang_dir.name
            
            # Import all .py files in this language directory
            for _, name, is_pkg in pkgutil.iter_modules([str(lang_dir)]):
                if not is_pkg:
                    try:
                        importlib.import_module(f"weeb_cli.providers.{lang}.{name}")
                        debug(f"[Registry] Discovered provider: {lang}/{name}")
                    except Exception as e:
                        debug(f"[Registry] Error loading provider {lang}/{name}: {e}")
    
    # Discover plugins as well
    try:
        from weeb_cli.services.plugin_manager import plugin_manager
        enabled_plugins = plugin_manager.get_enabled_plugins()
        for plugin in enabled_plugins:
            try:
                plugin_manager.enable_plugin(plugin.manifest.id)
                debug(f"[Registry] Discovered plugin provider: {plugin.manifest.id}")
            except Exception as e:
                debug(f"[Registry] Error loading plugin provider {plugin.manifest.id}: {e}")
    except (ImportError, Exception) as e:
        debug(f"[Registry] Error during plugin discovery: {e}")

    _initialized = True


def get_provider(name: str) -> Optional[BaseProvider]:
    """Get provider instance by name.
    
    Triggers provider discovery if not already done, then returns
    a new instance of the requested provider. Returns None if provider
    is disabled or not found.
    
    Args:
        name: Provider identifier (e.g., 'animecix', 'hianime').
    
    Returns:
        Provider instance, or None if not found or disabled.
    
    Example:
        >>> provider = get_provider("animecix")
        >>> if provider:
        ...     results = provider.search("anime")
    """
    _discover_providers()
    if name in _providers:
        # Check if provider is disabled
        if _provider_meta.get(name, {}).get("disabled", False):
            debug(f"[Registry] Provider '{name}' is disabled")
            return None
        return _providers[name]()
    return None


def get_providers_for_lang(lang: str) -> List[str]:
    """Get all provider names for a specific language.
    
    Args:
        lang: Language code (e.g., 'en', 'tr', 'de', 'pl').
    
    Returns:
        List of provider names for the language.
    
    Example:
        >>> turkish_providers = get_providers_for_lang("tr")
        >>> print(turkish_providers)
        ['animecix', 'turkanime', 'anizle', 'weeb']
    """
    _discover_providers()
    return [
        name for name, meta in _provider_meta.items()
        if meta["lang"] == lang
    ]


def list_providers() -> List[dict]:
    """List all registered providers with metadata.
    
    Returns:
        List of provider metadata dictionaries containing:
            - name: Provider identifier
            - lang: Language code
            - region: Region code
            - class: Provider class name
    
    Example:
        >>> providers = list_providers()
        >>> for p in providers:
        ...     print(f"{p['name']}: {p['lang']} ({p['region']})")
        animecix: tr (TR)
        hianime: en (US)
        aniworld: de (DE)
    """
    _discover_providers()
    return list(_provider_meta.values())


def get_default_provider(lang: str) -> Optional[str]:
    """Get default provider name for a language.
    
    Returns the first registered provider for the given language.
    Useful for setting initial defaults.
    
    Args:
        lang: Language code (e.g., 'en', 'tr', 'de', 'pl').
    
    Returns:
        Provider name, or None if no providers for language.
    
    Example:
        >>> default = get_default_provider("tr")
        >>> print(default)
        'animecix'
    """
    providers = get_providers_for_lang(lang)
    return providers[0] if providers else None
