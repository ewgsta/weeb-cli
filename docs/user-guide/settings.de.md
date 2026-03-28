# Einstellungen-Leitfaden

Vollständiger Leitfaden zur Konfiguration von Weeb CLI nach Ihren Vorlieben.

## Zugriff auf Einstellungen

Hauptmenü → Einstellungen

## Allgemeine Einstellungen

### Sprache

UI-Sprache ändern:
- Türkçe (Türkisch)
- English (Englisch)
- Deutsch
- Polski (Polnisch)

Pfad: Einstellungen → Konfiguration → Sprache

### Standard-Anbieter

Bevorzugte Anime-Quelle festlegen:
- Basierend auf Ihrer Sprache
- Kann manuell überschrieben werden

Pfad: Einstellungen → Konfiguration → Standard-Anbieter

### Beschreibungen anzeigen

Anime-Beschreibungen in der Suche umschalten:
- Ein: Zeigt vollständige Synopsis
- Aus: Kompakte Ansicht

Pfad: Einstellungen → Konfiguration → Beschreibungen anzeigen

### Debug-Modus

Detaillierte Protokollierung aktivieren:
- Protokolle werden in ~/.weeb-cli/logs/ gespeichert
- Nützlich zur Fehlerbehebung
- Kann die Leistung beeinträchtigen

Pfad: Einstellungen → Konfiguration → Debug-Modus

## Download-Einstellungen

### Download-Verzeichnis

Festlegen, wo Anime-Dateien gespeichert werden:
- Standard: ./weeb-downloads
- Kann jeder beschreibbare Pfad sein
- Unterstützt relative und absolute Pfade

Pfad: Einstellungen → Downloads → Download-Verzeichnis

### Aria2-Einstellungen

Aria2-Downloader konfigurieren:
- Aria2 aktivieren/deaktivieren
- Max. Verbindungen (1-32)
- Standard: 16 Verbindungen

Pfad: Einstellungen → Downloads → Aria2

### yt-dlp-Einstellungen

yt-dlp konfigurieren:
- yt-dlp aktivieren/deaktivieren
- Format-String
- Standard: bestvideo+bestaudio/best

Pfad: Einstellungen → Downloads → yt-dlp

### Gleichzeitige Downloads

Max. gleichzeitige Downloads:
- Bereich: 1-10
- Standard: 3
- Höher nutzt mehr Bandbreite

Pfad: Einstellungen → Downloads → Gleichzeitig

### Wiederholungseinstellungen

Download-Wiederholungen konfigurieren:
- Max. Wiederholungen: 0-10
- Wiederholungsverzögerung: 1-60 Sekunden
- Exponentieller Backoff

Pfad: Einstellungen → Downloads → Wiederholung

## Tracker-Einstellungen

### AniList

AniList-Integration konfigurieren:
- Mit OAuth authentifizieren
- Verbindungsstatus anzeigen
- Konto trennen

Pfad: Einstellungen → Tracker → AniList

### MyAnimeList

MAL-Integration konfigurieren:
- Mit OAuth authentifizieren
- Sync-Status anzeigen
- Konto trennen

Pfad: Einstellungen → Tracker → MyAnimeList

### Kitsu

Kitsu-Integration konfigurieren:
- Mit E-Mail/Passwort anmelden
- Verbindungsstatus anzeigen
- Abmelden

Pfad: Einstellungen → Tracker → Kitsu

## Integrationseinstellungen

### Discord Rich Presence

Zeigen Sie auf Discord, was Sie ansehen:
- Aktivieren/Deaktivieren
- Zeigt Anime-Titel
- Zeigt Episodennummer
- Zeigt verstrichene Zeit

Pfad: Einstellungen → Integrationen → Discord RPC

### Tastaturkürzel

Globale Tastaturkürzel (experimentell):
- Aktivieren/Deaktivieren
- Hotkeys konfigurieren
- Systemweite Steuerung

Pfad: Einstellungen → Integrationen → Tastenkürzel

## Cache-Einstellungen

### Cache-Statistiken anzeigen

Cache-Informationen anzeigen:
- Speichereinträge
- Dateieinträge
- Gesamtgröße

Pfad: Einstellungen → Cache → Statistiken

### Cache leeren

Zwischengespeicherte Daten entfernen:
- Gesamten Cache leeren
- Anbieter-Cache leeren
- Suchverlauf leeren

Pfad: Einstellungen → Cache → Leeren

### Cache-Bereinigung

Alte Cache-Einträge entfernen:
- Max. Alter festlegen
- Automatische Bereinigung
- Manuelle Bereinigung

Pfad: Einstellungen → Cache → Bereinigung

## Externe Laufwerke

### Laufwerk hinzufügen

Externe Laufwerke registrieren:
1. Einstellungen → Externe Laufwerke
2. "Laufwerk hinzufügen" auswählen
3. Pfad eingeben
4. Namen vergeben

### Laufwerke verwalten

- Alle Laufwerke anzeigen
- Laufwerke entfernen
- Laufwerke umbenennen
- Laufwerke scannen

Pfad: Einstellungen → Externe Laufwerke

## Sicherung & Wiederherstellung

### Sicherung erstellen

Ihre Daten sichern:
- Konfiguration
- Wiedergabefortschritt
- Download-Warteschlange
- Bibliotheksindex

Pfad: Einstellungen → Sicherung → Sicherung erstellen

### Sicherung wiederherstellen

Aus Sicherung wiederherstellen:
1. Einstellungen → Sicherung → Wiederherstellen
2. Sicherungsdatei auswählen
3. Wiederherstellung bestätigen

Warnung: Überschreibt aktuelle Daten

## Erweiterte Einstellungen

### Einstellungen zurücksetzen

Auf Standardwerte zurücksetzen:
1. Einstellungen → Erweitert
2. "Alle Einstellungen zurücksetzen" auswählen
3. Zurücksetzen bestätigen

Warnung: Kann nicht rückgängig gemacht werden

### Einstellungen exportieren

Konfiguration exportieren:
- JSON-Format
- Enthält alle Einstellungen
- Schließt Anmeldedaten aus

Pfad: Einstellungen → Erweitert → Exportieren

### Einstellungen importieren

Konfiguration importieren:
1. Einstellungen → Erweitert → Importieren
2. JSON-Datei auswählen
3. Import bestätigen

## Konfigurationsdatei

Einstellungen gespeichert in:
```
~/.weeb-cli/weeb.db
```

SQLite-Datenbank mit Tabellen:
- config
- progress
- download_queue
- external_drives
- anime_index

## Tipps

1. Vor größeren Änderungen sichern
2. Einstellungen mit einzelnem Download testen
3. Debug für Fehlerbehebung aktivieren
4. Externe Laufwerke für große Sammlungen verwenden
5. Tracker regelmäßig synchronisieren

## Nächste Schritte

- [Konfigurationsleitfaden](../getting-started/configuration.md): Detaillierte Konfigurationsoptionen
- [Download-Leitfaden](downloading.md): Downloads optimieren
- [Tracker-Leitfaden](trackers.md): Tracker einrichten
