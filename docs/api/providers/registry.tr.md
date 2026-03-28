# Provider Registry

::: weeb_cli.providers.registry
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Genel Bakış

Registry modülü, kayıt deseni kullanarak dinamik sağlayıcı keşfi ve yönetimi sağlar.

## Fonksiyonlar

### register_provider

Sağlayıcı sınıflarını kaydetmek için dekoratör.

### get_provider

İsme göre sağlayıcı örneği al.

### get_providers_for_lang

Bir dil için tüm sağlayıcıları al.

### list_providers

Tüm kayıtlı sağlayıcıları listele.

### get_default_provider

Bir dil için varsayılan sağlayıcıyı al.

## Kullanım Örnekleri

### Sağlayıcı Kaydetme

```python
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    pass
```

### Sağlayıcı Alma

```python
from weeb_cli.providers import get_provider

provider = get_provider("animecix")
results = provider.search("anime")
```

### Sağlayıcıları Listeleme

```python
from weeb_cli.providers import list_providers

providers = list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']}")
```

## API Referansı

::: weeb_cli.providers.registry.register_provider
::: weeb_cli.providers.registry.get_provider
::: weeb_cli.providers.registry.get_providers_for_lang
::: weeb_cli.providers.registry.list_providers
::: weeb_cli.providers.registry.get_default_provider
