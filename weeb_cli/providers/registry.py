from typing import Dict, List, Type, Optional
from weeb_cli.providers.base import BaseProvider

_providers: Dict[str, Type[BaseProvider]] = {}
_provider_meta: Dict[str, dict] = {}


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


def get_provider(name: str) -> Optional[BaseProvider]:
    if name in _providers:
        return _providers[name]()
    return None


def get_providers_for_lang(lang: str) -> List[str]:
    return [
        name for name, meta in _provider_meta.items()
        if meta["lang"] == lang
    ]


def list_providers() -> List[dict]:
    return list(_provider_meta.values())


def get_default_provider(lang: str) -> Optional[str]:
    providers = get_providers_for_lang(lang)
    return providers[0] if providers else None
