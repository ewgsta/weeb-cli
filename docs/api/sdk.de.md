# Python SDK

Programmatische API zur direkten Integration der Weeb CLI-Funktionalität in Python-Anwendungen.

## Übersicht

Das Weeb CLI SDK bietet eine native Python-Schnittstelle für alle Anime-Streaming- und Download-Funktionen. Im Gegensatz zum CLI-API-Modus, der das Spawnen von Prozessen und JSON-Parsing erfordert, bietet das SDK:

- **Direkte Python-API** - Kein Subprocess-Overhead
- **Typsicherheit** - Vollständige Type Hints für IDE-Unterstützung
- **Thread-sicher** - Sicher für gleichzeitige Operationen
- **Headless-Modus** - Keine Datenbank- oder TUI-Abhängigkeiten
- **Gleiche Funktionen** - Alle CLI-Funktionen verfügbar

## Installation

Das SDK ist in weeb-cli enthalten:

```bash
pip install weeb-cli
```

## Schnellstart

```python
from weeb_cli import WeebSDK

# SDK initialisieren
sdk = WeebSDK(default_provider="hianime")

# Nach Anime suchen
results = sdk.search("One Piece")
print(f"{len(results)} Ergebnisse gefunden")

# Erstes Ergebnis abrufen
anime = results[0]
print(f"{anime.title} ({anime.year})")

# Episoden abrufen
episodes = sdk.get_episodes(anime.id, season=1)
print(f"Staffel 1 hat {len(episodes)} Episoden")

# Stream-URLs abrufen
streams = sdk.get_streams(
    anime_id=anime.id,
    episode_id=episodes[0].id
)
print(f"Verfügbar in {len(streams)} Qualitäten")

# Episode herunterladen
path = sdk.download_episode(
    anime_id=anime.id,
    season=1,
    episode=1,
    output_dir="./downloads"
)
print(f"Heruntergeladen nach: {path}")
```

## API-Referenz

### WeebSDK-Klasse

Haupt-SDK-Schnittstelle für alle Operationen.

#### Konstruktor

```python
WeebSDK(headless: bool = True, default_provider: Optional[str] = None)
```

**Parameter:**
- `headless` (bool): Im Headless-Modus ausführen (keine Datenbank/TUI). Standard: `True`
- `default_provider` (str, optional): Zu verwendender Standard-Anbieter. Standard: `"animecix"`

**Beispiel:**
```python
# Headless mit Standard-Anbieter
sdk = WeebSDK()

# Benutzerdefinierter Standard-Anbieter
sdk = WeebSDK(default_provider="hianime")

# Mit Datenbankzugriff (für Wiedergabeverlauf usw.)
sdk = WeebSDK(headless=False)
```

#### search()

Nach Anime anhand einer Abfragezeichenfolge suchen.

```python
def search(
    query: str, 
    provider: Optional[str] = None
) -> List[AnimeResult]
```

**Parameter:**
- `query` (str): Suchabfrage (Anime-Titel oder Schlüsselwörter)
- `provider` (str, optional): Zu verwendender Anbieter. Verwendet `default_provider`, wenn nicht angegeben

**Gibt zurück:** Liste von `AnimeResult`-Objekten

**Beispiel:**
```python
results = sdk.search("Naruto", provider="hianime")
for anime in results:
    print(f"{anime.title} - {anime.type} ({anime.year})")
```

#### get_episodes()

Liste der verfügbaren Episoden für einen Anime abrufen.

```python
def get_episodes(
    anime_id: str, 
    season: Optional[int] = None,
    provider: Optional[str] = None
) -> List[Episode]
```

**Parameter:**
- `anime_id` (str): Eindeutige Anime-ID
- `season` (int, optional): Nach Staffelnummer filtern
- `provider` (str, optional): Zu verwendender Anbieter

**Gibt zurück:** Liste von `Episode`-Objekten

**Beispiel:**
```python
# Alle Episoden abrufen
episodes = sdk.get_episodes("anime-id", provider="hianime")

# Nur Staffel 2
season2 = sdk.get_episodes("anime-id", season=2, provider="hianime")

for ep in season2:
    print(f"S{ep.season:02d}E{ep.number:02d}: {ep.title}")
```

#### download_episode()

Eine Episode in den lokalen Speicher herunterladen.

```python
def download_episode(
    anime_id: str,
    season: int,
    episode: int,
    provider: Optional[str] = None,
    output_dir: str = ".",
    anime_title: Optional[str] = None
) -> Optional[str]
```

**Parameter:**
- `anime_id` (str): Eindeutige Anime-ID
- `season` (int): Staffelnummer
- `episode` (int): Episodennummer
- `provider` (str, optional): Zu verwendender Anbieter
- `output_dir` (str): Verzeichnis zum Speichern der Datei. Standard: aktuelles Verzeichnis
- `anime_title` (str, optional): Benutzerdefinierter Titel für Dateinamen. Wird automatisch abgerufen, wenn nicht angegeben

**Gibt zurück:** Pfad zur heruntergeladenen Datei oder `None` bei Fehler

**Beispiel:**
```python
# Einfacher Download
path = sdk.download_episode(
    anime_id="anime-id",
    season=1,
    episode=1,
    provider="hianime"
)

# Benutzerdefiniertes Ausgabeverzeichnis und Titel
path = sdk.download_episode(
    anime_id="anime-id",
    season=2,
    episode=5,
    provider="hianime",
    output_dir="/media/anime",
    anime_title="Mein Lieblings-Anime"
)
print(f"Heruntergeladen nach: {path}")
```

## Erweiterte Verwendung

### Multi-Provider-Suche

Über mehrere Anbieter suchen und Ergebnisse kombinieren:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK()
query = "One Piece"

# Über mehrere Anbieter suchen
providers = ["hianime", "animecix", "aniworld"]
all_results = []

for provider in providers:
    try:
        results = sdk.search(query, provider=provider)
        all_results.extend(results)
        print(f"{provider}: {len(results)} Ergebnisse")
    except Exception as e:
        print(f"{provider} fehlgeschlagen: {e}")

print(f"Gesamt: {len(all_results)} Ergebnisse")
```

### Batch-Download

Mehrere Episoden herunterladen:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK(default_provider="hianime")

# Suchen und Anime abrufen
results = sdk.search("Naruto")
anime_id = results[0].id

# Staffel 1 herunterladen
for episode_num in range(1, 26):
    try:
        path = sdk.download_episode(
            anime_id=anime_id,
            season=1,
            episode=episode_num,
            output_dir="./naruto_s1"
        )
        print(f"✓ Episode {episode_num}: {path}")
    except Exception as e:
        print(f"✗ Episode {episode_num}: {e}")
```

## Integrationsbeispiele

### Flask Web-API

```python
from flask import Flask, jsonify, request
from weeb_cli import WeebSDK

app = Flask(__name__)
sdk = WeebSDK()

@app.route('/api/search')
def search():
    query = request.args.get('q')
    provider = request.args.get('provider', 'hianime')
    
    results = sdk.search(query, provider=provider)
    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'year': r.year,
            'cover': r.cover
        }
        for r in results
    ])

if __name__ == '__main__':
    app.run(port=5000)
```

### Discord-Bot

```python
import discord
from discord.ext import commands
from weeb_cli import WeebSDK

bot = commands.Bot(command_prefix='!')
sdk = WeebSDK(default_provider="hianime")

@bot.command()
async def anime(ctx, *, query):
    """Nach Anime suchen"""
    results = sdk.search(query)
    
    if not results:
        await ctx.send("Keine Ergebnisse gefunden")
        return
    
    anime = results[0]
    embed = discord.Embed(
        title=anime.title,
        description=f"Jahr: {anime.year}"
    )
    if anime.cover:
        embed.set_thumbnail(url=anime.cover)
    
    await ctx.send(embed=embed)

bot.run('TOKEN')
```

## Best Practices

1. **SDK-Instanz wiederverwenden**: Eine SDK-Instanz erstellen und wiederverwenden
2. **Fehler behandeln**: SDK-Aufrufe immer in try-except-Blöcke einschließen
3. **Anbieterauswahl**: Benutzern die Wahl des Anbieters ermöglichen oder sprachgerechte Standards verwenden
4. **Gleichzeitige Operationen**: Threading für Batch-Operationen verwenden
5. **Caching**: SDK verwendet denselben Cache wie CLI - Ergebnisse werden automatisch zwischengespeichert
6. **Headless-Modus**: headless=True für zustandslose Anwendungen beibehalten

## Einschränkungen

- **Kein Wiedergabeverlauf**: Headless-Modus verfolgt keinen Wiedergabefortschritt
- **Keine Tracker-Synchronisierung**: AniList/MAL-Synchronisierung erfordert Nicht-Headless-Modus
- **Keine Benachrichtigungen**: Systembenachrichtigungen im Headless-Modus nicht verfügbar
- **Kein Discord RPC**: Discord-Integration erfordert Nicht-Headless-Modus

Für diese Funktionen SDK mit `headless=False` initialisieren und sicherstellen, dass die Datenbank zugänglich ist.

## Nächste Schritte

- [API-Modus-Dokumentation](../cli/api-mode.de.md): CLI JSON-API
- [Anbieterentwicklung](../development/adding-providers.de.md): Benutzerdefinierte Anbieter erstellen
- [Architektur](../development/architecture.de.md): Systemdesign-Übersicht
