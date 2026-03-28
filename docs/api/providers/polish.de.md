# Polnische Provider

Polnische Anime-Quellen-Provider.

## Verfügbare Provider

### Docchi

Provider für Docchi.pl

- Polnische Anime-Bibliothek
- Polnische Untertitel
- Mehrere Server
- Gute Qualität

## Verwendung

```python
from weeb_cli.providers import get_provider

# Provider abrufen
provider = get_provider("docchi")

# Suchen
results = provider.search("Naruto")

# Details abrufen
details = provider.get_details(results[0].id)

# Streams abrufen
streams = provider.get_streams(details.id, episode_id)
```

## Provider-Details

| Provider | Bibliotheksgröße | Qualität | Geschwindigkeit | Untertitel |
|----------|-------------|---------|-------|-----------|
| Docchi | Mittel | HD | Mittel | Polnisch |

## Nächste Schritte

- [Base Provider](base.md): Provider-Schnittstelle
- [Provider hinzufügen](../../development/adding-providers.md): Provider erstellen
