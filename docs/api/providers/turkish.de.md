# Türkische Provider

Türkische Anime-Quellen-Provider.

## Verfügbare Provider

### Animecix

Provider für Animecix.net

- Große Anime-Bibliothek
- Türkische Untertitel
- Mehrere Server
- HD-Qualität

### Turkanime

Provider für TurkAnime.co

- Umfangreiche Sammlung
- Türkische Synchronisationen und Untertitel
- Mehrere Qualitätsoptionen

### Anizle

Provider für Anizle.com

- Moderne Oberfläche
- Schnelle Server
- HD-Streams

### Weeb

Provider für Weeb.com.tr

- Türkische Inhalte
- Mehrere Server
- Gute Qualität

## Verwendung

```python
from weeb_cli.providers import get_provider

# Provider abrufen
provider = get_provider("animecix")

# Suchen
results = provider.search("One Piece")

# Details abrufen
details = provider.get_details(results[0].id)

# Streams abrufen
streams = provider.get_streams(details.id, episode_id)
```

## Provider-Vergleich

| Provider | Bibliotheksgröße | Qualität | Geschwindigkeit | Untertitel |
|----------|-------------|---------|-------|-----------|
| Animecix | Groß | HD | Schnell | Türkisch |
| Turkanime | Groß | HD | Mittel | Türkisch |
| Anizle | Mittel | HD | Schnell | Türkisch |
| Weeb | Mittel | HD | Mittel | Türkisch |

## Nächste Schritte

- [Base Provider](base.md): Provider-Schnittstelle
- [Provider hinzufügen](../../development/adding-providers.md): Provider erstellen
