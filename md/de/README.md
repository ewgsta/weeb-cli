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
  <a href="#funktionen">Funktionen</a> •
  <a href="#nutzung">Nutzung</a> •
  <a href="#quellen">Quellen</a> •
  <a href="https://ewgsta.github.io/weeb-cli/">Dokumentation</a>
</p>

---

## Funktionen

### Plugin-System
- **Benutzerdefiniertes .weeb-Format**: Paketieren und Teilen eigener Anbieter
- **Sichere Sandbox**: Plugins sicher mit eingeschränkten Berechtigungen ausführen
- **Plugin Builder**: Einfach zu bedienendes Skript zum Paketieren von Plugins
- **Plugin-Galerie**: Durchsuchen und Installieren von Community-Plugins aus der [Galerie](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html)
- **Automatische Erkennung**: Plugins werden beim Start automatisch geladen

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

### Tracking & Synchronisation
- **AniList** Integration mit OAuth
- **MyAnimeList** Integration mit OAuth
- **Kitsu** Integration mit E-Mail/Passwort
- Automatische Fortschrittssynchronisation für Online- und Offline-Wiedergabe
- Offline-Warteschlange für ausstehende Updates
- Intelligente Anime-Titel-Erkennung aus Dateinamen

### Lokale Bibliothek
- Automatischer Scan heruntergeladener Animes
- Unterstützung für externe Laufwerke (USB, HDD)
- Offline-Anime-Indizierung mit automatischer Tracker-Synchronisation
- Suche über alle Quellen hinweg

### Zusätzliche Funktionen
- SQLite-Datenbank (schnell und zuverlässig)
- Systembenachrichtigungen bei Abschluss des Downloads
- Discord RPC-Integration (zeige auf Discord, was du gerade schaust)
- Suchverlauf
- Debug-Modus und Protokollierung
- Automatische Update-Prüfung
- Nicht-interaktive JSON-API für Skripte und KI-Agenten
- Torznab-Servermodus für Sonarr/*arr-Integration
- RESTful-API-Server für Web/Mobile-Anwendungen

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
Laden Sie die entsprechende Datei für Ihre Plattform unter [Releases](https://github.com/ewgsta/weeb-cli/releases) herunter.

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
```

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
- [x] MAL/AniList Integration
- [x] Datenbank-Sicherung/Wiederherstellung
- [x] Tastenkombinationen
- [x] Nicht-interaktiver API-Modus (JSON-Ausgabe)
- [x] Torznab-Server für Sonarr/*arr-Integration
- [x] RESTful-API-Server für Web/Mobile-Apps
- [x] Plugin-System mit Sandbox-Unterstützung
- [x] Plugin Builder & Galerie-Seite

---

## Lizenz

Dieses Projekt ist unter der **GNU General Public License v3.0** lizenziert.  
Die vollständige Lizenzvereinbarung findest du in der Datei [LICENSE](../../LICENSE).

Weeb-CLI (C) 2026
