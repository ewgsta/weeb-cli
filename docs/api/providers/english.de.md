# Englische Provider

Englische Anime-Quellen-Provider.

## Verfügbare Provider

### HiAnime

Provider für HiAnime.to

- Riesige Anime-Bibliothek
- Mehrere Qualitätsoptionen
- Schnelle Server
- Englische Untertitel und Synchronisationen

### AllAnime

Provider für AllAnime.to

- Große Sammlung
- Mehrere Server
- HD-Qualität
- Untertitel- und Synchronisationsoptionen

## Verwendung

```python
from weeb_cli.providers import get_provider

# Provider abrufen
provider = get_provider("hianime")

# Suchen
results = provider.search("Naruto")

# Details abrufen
details = provider.get_details(results[0].id)

# Streams abrufen
streams = provider.get_streams(details.id, episode_id)
```

## Provider-Vergleich

| Provider | Bibliotheksgröße | Qualität | Geschwindigkeit | Untertitel |
|----------|-------------|---------|-------|-----------|
| HiAnime | Sehr groß | 1080p | Schnell | Englisch |
| AllAnime | Groß | 1080p | Schnell | Englisch |

## Nächste Schritte

- [Base Provider](base.md): Provider-Schnittstelle
- [Provider hinzufügen](../../development/adding-providers.md): Provider erstellen
