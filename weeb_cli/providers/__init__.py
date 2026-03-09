from weeb_cli.providers.base import BaseProvider
from weeb_cli.providers.registry import (
    register_provider,
    get_provider,
    get_providers_for_lang,
    get_default_provider,
    list_providers
)

from weeb_cli.providers import animecix
from weeb_cli.providers import anizle
from weeb_cli.providers import turkanime
from weeb_cli.providers import hianime
from weeb_cli.providers import allanime
from weeb_cli.providers import weeb

__all__ = [
    "BaseProvider",
    "register_provider", 
    "get_provider",
    "get_providers_for_lang",
    "get_default_provider",
    "list_providers"
]
