"""
Provider Registry - Kaynak kayıt ve keşif sistemi

Decorator tabanlı otomatik kayıt:
    @register_provider("animecix", lang="tr")
    class AnimeCixProvider(BaseProvider):
        ...
"""

from typing import Dict, List, Type, Optional
from weeb_cli.providers.base import BaseProvider

# Global provider registry
_providers: Dict[str, Type[BaseProvider]] = {}
_provider_meta: Dict[str, dict] = {}


def register_provider(name: str, lang: str = "tr", region: str = "TR"):
    """
    Provider kayıt decorator'ı
    
    Args:
        name: Provider adı (unique)
        lang: Dil kodu (tr, en, jp)
        region: Bölge kodu (TR, US, JP)
    
    Usage:
        @register_provider("animecix", lang="tr", region="TR")
        class AnimeCixProvider(BaseProvider):
            ...
    """
    def decorator(cls: Type[BaseProvider]):
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


def get_provider(name: str) -> Optional[BaseProvider]:
    """
    Provider instance'ı getir
    
    Args:
        name: Provider adı
        
    Returns:
        Provider instance veya None
    """
    if name in _providers:
        return _providers[name]()
    return None


def get_providers_for_lang(lang: str) -> List[str]:
    """
    Belirli dil için provider listesi
    
    Args:
        lang: Dil kodu (tr, en)
        
    Returns:
        Provider adları listesi
    """
    return [
        name for name, meta in _provider_meta.items()
        if meta["lang"] == lang
    ]


def list_providers() -> List[dict]:
    """
    Tüm provider'ları listele
    
    Returns:
        Provider metadata listesi
    """
    return list(_provider_meta.values())


def get_default_provider(lang: str) -> Optional[str]:
    """
    Dil için varsayılan provider
    
    Args:
        lang: Dil kodu
        
    Returns:
        Provider adı veya None
    """
    providers = get_providers_for_lang(lang)
    return providers[0] if providers else None
