# Deutsche Provider

Deutsche Anime-Quellen-Provider.

## Verfügbare Provider

### AniWorld

Provider für AniWorld.to

- Große deutsche Anime-Bibliothek
- Deutsche Synchronisationen und Untertitel
- Mehrere Qualitätsoptionen
- Schnelle Server

## Verwendung

```python
from weeb_cli.providers import get_provider

# Provider abrufen
provider = get_provider("aniworld")

# Suchen
results = provider.search("One Piece")

# Details abrufen
details = provider.get_details(results[0].id)

# Streams abrufen
streams = provider.get_streams(details.id, episode_id)
```

## Provider-Details

| Provider | Bibliotheksgröße | Qualität | Geschwindigkeit | Untertitel |
|----------|-------------|---------|-------|-----------|
| AniWorld | Groß | HD | Schnell | Deutsch |

## Nächste Schritte

- [Base Provider](base.md): Provider-Schnittstelle
- [Provider hinzufügen](../../development/adding-providers.md): Provider erstellen
