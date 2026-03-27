# Weeb CLI Dokumentation

**Kein Browser, keine Werbung, keine Ablenkungen. Nur Sie und ein unvergleichliches Anime-Seherlebnis.**

## Willkommen

Weeb CLI ist eine leistungsstarke terminalbasierte Anime-Streaming- und Download-Anwendung, die ein browserfreies, werbefreies Anime-Seherlebnis bietet. Mit Unterstützung für mehrere Anime-Quellen in verschiedenen Sprachen, integrierten Tracking-Diensten und erweitertem Download-Management ist Weeb CLI Ihr All-in-One-Anime-Begleiter.

## Hauptmerkmale

### Multi-Quellen-Unterstützung
- Türkisch: Animecix, Turkanime, Anizle, Weeb
- Englisch: HiAnime, AllAnime
- Deutsch: AniWorld
- Polnisch: Docchi

### Intelligentes Streaming
- Hochwertige HLS/MP4-Wiedergabe mit MPV
- Fortsetzen, wo Sie aufgehört haben
- Wiedergabeverlauf und Statistiken
- Episoden-Fortschrittsverfolgung

### Erweiterte Downloads
- Schnelle Multi-Verbindungs-Downloads mit Aria2
- Komplexe Stream-Unterstützung mit yt-dlp
- Warteschlangensystem mit gleichzeitigen Downloads
- Unterbrochene Downloads fortsetzen
- Intelligente Dateibenennung

### Tracker-Integration
- AniList, MyAnimeList und Kitsu Unterstützung
- OAuth-Authentifizierung
- Automatische Fortschrittssynchronisation
- Offline-Warteschlange für ausstehende Updates

### Lokale Bibliothek
- Automatisches Scannen heruntergeladener Anime
- Externe Laufwerksunterstützung (USB, HDD)
- Offline-Anime-Indizierung
- Intelligente Titelzuordnung

### Zusätzliche Funktionen
- Mehrsprachige Unterstützung (TR, EN, DE, PL)
- Discord Rich Presence
- Systembenachrichtigungen
- Nicht-interaktive JSON-API
- Torznab-Server für *arr-Integration

## Schnellstart

```bash
# Installation über pip
pip install weeb-cli

# Interaktiver Modus
weeb-cli

# API-Modus
weeb-cli api search "anime name"
```

## Dokumentationsstruktur

- **Erste Schritte**: Installation und Ersteinrichtung
- **Benutzerhandbuch**: Detaillierte Nutzungsanweisungen
- **API-Referenz**: Vollständige API-Dokumentation
- **Entwicklung**: Beitrags- und Entwicklungsleitfaden
- **CLI-Referenz**: Befehlszeilenschnittstellen-Dokumentation

## Unterstützung

- GitHub: [ewgsta/weeb-cli](https://github.com/ewgsta/weeb-cli)
- Probleme: [Fehler melden](https://github.com/ewgsta/weeb-cli/issues)
- PyPI: [weeb-cli](https://pypi.org/project/weeb-cli/)

## Lizenz

Weeb CLI ist unter der GPL-3.0-Lizenz lizenziert. Siehe [LICENSE](https://github.com/ewgsta/weeb-cli/blob/main/LICENSE) für Details.
