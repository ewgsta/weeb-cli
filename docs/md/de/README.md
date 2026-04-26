<p align="center">
  <img src="https://8upload.com/image/a6cdd79fc5a25c99/wl-512x512.jpg" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>Kein Browser, keine Werbung, keine Ablenkungen. Nur du und ein unvergleichliches Anime-Streaming-Erlebnis.</strong>
</p>

<div align="center">
  <a href="../../README.md">English</a> | <a href="../tr/README.md">Türkçe</a> | <a href="README.md">Deutsch</a> | <a href="../pl/README.md">Polski</a>
</div>
<br>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/ewgsta/weeb-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/ewgsta/weeb-cli/tests.yml?style=flat-square" alt="Tests"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Funktionen</a> •
  <a href="#nutzung">Nutzung</a> •
  <a href="#quellen">Quellen</a>
</p>

---

## Funktionen

### Mehrere Quellen
- **Türkisch**: Animecix, Turkanime, Anizle, Weeb
- **Englisch**: HiAnime, AllAnime
- **Deutsch**: AniWorld
- **Polnisch**: Docchi

### Intelligentes Streaming
- Hochwertige HLS/MP4-Wiedergabe mit MPV
- Fortsetzen, wo du aufgehört hast (zeitstempelbasiert)
- Wiedergabeverlauf und Statistiken
- Markierungen für abgeschlossene (✓) und angefangene (●) Episoden

### Leistungsstarkes Download-System
- **Aria2** für schnelle Downloads mit mehreren Verbindungen
- **yt-dlp** für komplexe Stream-Unterstützung
- Warteschlangensystem mit gleichzeitigen Downloads
- Unterbrochene Downloads fortsetzen
- Intelligente Dateibenennung (`Anime Name - S1E1.mp4`)

### Nachverfolgung & Synchronisation
- **AniList** Integration mit OAuth
- **MyAnimeList** Integration mit OAuth
- **Kitsu** Integration mit E-Mail/Passwort
- Automatische Fortschrittssynchronisierung für Online- und Offline-Wiedergabe
- Offline-Warteschlange für ausstehende Updates
- Intelligenter Abgleich von Anime-Titeln anhand von Dateinamen

### Lokale Bibliothek
- Heruntergeladene Animes automatisch scannen
- Unterstützung externer Laufwerke (USB, HDD)
- Offline-Anime-Indexierung mit automatischer Tracker-Synchronisation
- Suche über alle Quellen hinweg
- **Empfohlenes Format**: `Anime Name - S1E1.mp4` für beste Tracker-Kompatibilität

### Zusätzliche Funktionen
- SQLite-Datenbank (schnell und zuverlässig)
- Systembenachrichtigungen bei Abschluss des Downloads
- Discord RPC-Integration (Zeige auf Discord, was du dir gerade anschaust)
- Suchverlauf
- Debug-Modus und Protokollierung
- Automatische Update-Prüfungen
- Nicht interaktive JSON-API für Skripte und KI-Agenten
- Torznab-Servermodus für Sonarr/*arr-Integration

---

## Installation

### PyPI (Universell)
```bash
pip install weeb-cli
```

### Arch Linux (AUR)
```bash
yay -S weeb-cli
```

### Portable
Lade die entsprechende Datei für deine Plattform unter [Releases](https://github.com/ewgsta/weeb-cli/releases) herunter.

### Für Entwickler
```bash
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli
pip install -e .
```

---

## Nutzung

```bash
weeb-cli
```

### API-Modus (Nicht interaktiv)

Für Skripte, Automatisierung und KI-Agenten bietet weeb-cli JSON-API-Befehle, die ohne Datenbank oder TUI ausgeführt werden:

```bash
# Verfügbare Anbieter auflisten
weeb-cli api providers

# Nach Animes suchen (gibt IDs zurück)
weeb-cli api search "Angel Beats"
# Rückgabe: [{"id": "12345", "title": "Angel Beats!", ...}]

# Episoden auflisten (ID aus der Suche verwenden)
weeb-cli api episodes 12345 --season 1

# Stream-URLs für eine Episode abrufen
weeb-cli api streams 12345 --season 1 --episode 1

# Anime-Details abrufen
weeb-cli api details 12345

# Eine Episode herunterladen
weeb-cli api download 12345 --season 1 --episode 1 --output ./downloads
```

Alle API-Befehle geben JSON über stdout aus.

### Sonarr/*arr-Integration (Serve-Modus)

weeb-cli kann als Torznab-kompatibler Server für Sonarr und andere *arr-Anwendungen betrieben werden:

```bash
pip install weeb-cli[serve]

weeb-cli serve --port 9876 \
  --watch-dir /downloads/watch \
  --completed-dir /downloads/completed \
  --sonarr-url http://sonarr:8989 \
  --sonarr-api-key DEIN_KEY
```

Dann `http://weeb-cli-host:9876` als Torznab-Indexer in Sonarr mit der Kategorie 5070 (TV/Anime) hinzufügen. Der Server enthält einen Blackhole-Download-Worker, der heruntergeladene Episoden automatisch verarbeitet.

**Docker-Unterstützung:**
```bash
docker-compose -f docs/docker-compose.torznab.yml up -d
```

Siehe [Torznab Server Dokumentation](https://ewgsta.github.io/weeb-cli/cli/serve-mode.de/) für vollständige Details.

### RESTful API Server

### RESTful API Server

Für Web-/Mobilanwendungen und benutzerdefinierte Integrationen bietet weeb-cli einen RESTful API-Server:

```bash
pip install weeb-cli[serve-restful]

weeb-cli serve restful --port 8080 --cors
```

**API-Endpunkte:**
- `GET /health` - Gesundheitsprüfung
- `GET /api/providers` - Verfügbare Provider auflisten
- `GET /api/search?q=naruto&provider=animecix` - Anime suchen
- `GET /api/anime/{id}?provider=animecix` - Anime-Details abrufen
- `GET /api/anime/{id}/episodes?season=1` - Episoden auflisten
- `GET /api/anime/{id}/episodes/{ep_id}/streams` - Stream-URLs abrufen

Alle verfügbaren Provider werden automatisch geladen. Wählen Sie über den `provider` Query-Parameter, welchen Provider Sie verwenden möchten.

**Docker-Unterstützung:**
```bash
docker-compose -f docs/docker-compose.restful.yml up -d
```

Siehe [RESTful API Dokumentation](https://ewgsta.github.io/weeb-cli/cli/restful-api.de/) für vollständige Details.

### Tastatursteuerung
| Taste | Aktion |
|-------|--------|
| `↑` `↓` | Im Menü navigieren |
| `Enter` | Auswählen |
| `s` | Anime suchen (Hauptmenü) |
| `d` | Downloads (Hauptmenü) |
| `w` | Watchlist (Hauptmenü) |
| `c` | Einstellungen (Hauptmenü) |
| `q` | Beenden (Hauptmenü) |
| `Ctrl+C` | Zurück / Beenden |

**Hinweis:** Alle Tastenkombinationen können in "Einstellungen > Tastaturkurzbefehle" angepasst werden.

---

## Quellen

| Quelle | Sprache |
|--------|---------|
| Animecix | Türkisch |
| Turkanime | Türkisch |
| Anizle | Türkisch |
| Weeb | Türkisch |
| HiAnime | Englisch |
| AllAnime | Englisch |
| AniWorld | Deutsch |
| Docchi | Polnisch |

---

## Konfiguration

Speicherort der Konfiguration: `~/.weeb-cli/weeb.db` (SQLite)

### Verfügbare Einstellungen

| Einstellung | Beschreibung | Standard | Typ |
|-------------|--------------|----------|-----|
| `language` | Interface-Sprache (tr/en/de/pl) | `null` (fragt beim ersten Start) | string |
| `scraping_source` | Aktive Anime-Quelle | `animecix` | string |
| `aria2_enabled` | Aria2 für Downloads verwenden | `true` | boolean |
| `aria2_max_connections` | Max. Verbindungen pro Download | `16` | integer |
| `ytdlp_enabled` | yt-dlp für HLS-Streams verwenden | `true` | boolean |
| `ytdlp_format` | yt-dlp Format string | `bestvideo+bestaudio/best` | string |
| `max_concurrent_downloads` | Gleichzeitige Downloads | `3` | integer |
| `download_dir` | Download-Ordnerpfad | `./weeb-downloads` | string |
| `download_max_retries` | Fehlgeschlagene Downloads wiederholen | `3` | integer |
| `download_retry_delay` | Verzögerung zwischen Wiederholungen (Sek.) | `10` | integer |
| `show_description` | Anime-Beschreibungen anzeigen | `true` | boolean |
| `discord_rpc_enabled` | Discord Rich Presence | `false` | boolean |
| `shortcuts_enabled` | Tastaturkurzbefehle | `true` | boolean |
| `debug_mode` | Debug-Protokollierung | `false` | boolean |

### Tracker-Einstellungen (separat gespeichert)
- `anilist_token` - AniList OAuth-Token
- `anilist_user_id` - AniList-Benutzer-ID
- `mal_token` - MyAnimeList OAuth-Token
- `mal_refresh_token` - MAL Refresh-Token
- `mal_username` - MAL Benutzername

### Externe Laufwerke
Verwaltet über "Einstellungen > Externe Laufwerke". Jedes Laufwerk speichert:
- Pfad (z.B., `D:\Anime`)
- Benutzerdefinierter Name/Spitzname
- Hinzugefügt-Zeitstempel

Alle Einstellungen können über das interaktive Einstellungsmenü geändert werden.

---

## Roadmap

### Abgeschlossen
- [x] Unterstützung mehrerer Quellen (TR/EN/DE/PL)
- [x] MPV-Streaming
- [x] Wiedergabeverlauf und Fortschrittsverfolgung
- [x] Aria2/yt-dlp Download-Integration
- [x] Externe Laufwerke und lokale Bibliothek
- [x] SQLite-Datenbank
- [x] Benachrichtigungssystem
- [x] Debug-Modus
- [x] MAL/AniList-Integration
- [x] Datenbanksicherung/-wiederherstellung
- [x] Tastaturkurzbefehle
- [x] Nicht interaktiver API-Modus (JSON-Ausgabe)
- [x] Torznab-Server für Sonarr/*arr-Integration

### Geplant
- [ ] Anime-Empfehlungen
- [ ] Stapelverarbeitung
- [ ] Wiedergabestatistiken (Grafiken)
- [ ] Theme-Unterstützung
- [ ] Untertitel-Downloads
- [ ] Torrent-Unterstützung (nyaa.si)
- [ ] Watch Party

---

## Projektstruktur
*Siehe englische oder türkische README für Details zur Projektstruktur.*

---

## Lizenz

Dieses Projekt ist unter der **GNU General Public License v3.0** lizenziert.  
Die vollständige Lizenzvereinbarung findest du in der Datei [LICENSE](LICENSE).

Weeb-CLI (C) 2026
