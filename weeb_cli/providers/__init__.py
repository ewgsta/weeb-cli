"""
Provider Registry - Modüler kaynak yönetimi

Yeni kaynak eklemek için:
1. providers/ altına yeni_kaynak.py oluştur
2. BaseProvider'dan türet
3. @register_provider decorator'ı ekle

Örnek:
    @register_provider("yeni_kaynak", lang="tr", region="TR")
    class YeniKaynakProvider(BaseProvider):
        ...
"""

from weeb_cli.providers.base import BaseProvider
from weeb_cli.providers.registry import (
    register_provider,
    get_provider,
    get_providers_for_lang,
    list_providers
)

# Provider'ları otomatik yükle
from weeb_cli.providers import animecix

__all__ = [
    "BaseProvider",
    "register_provider", 
    "get_provider",
    "get_providers_for_lang",
    "list_providers"
]
