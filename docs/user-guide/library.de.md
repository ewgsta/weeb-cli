# Lokale Bibliotheksverwaltung

Verwalten Sie Ihre heruntergeladene Anime-Sammlung mit den lokalen Bibliotheksfunktionen von Weeb CLI.

## Überblick

Die lokale Bibliothek ermöglicht Ihnen:
- Heruntergeladene Anime indizieren
- Offline-Inhalte durchsuchen
- Mit Trackern synchronisieren
- Externe Laufwerke verwalten

## Bibliothek scannen

### Auto-Scan

Weeb CLI scannt automatisch Ihr Download-Verzeichnis:

1. Hauptmenü → Bibliothek
2. Wählen Sie "Bibliothek scannen"
3. Warten Sie, bis der Scan abgeschlossen ist

### Scan-Ergebnisse

Zeigt:
- Erkannte Anime-Titel
- Episodenzahlen
- Quellspeicherort
- Tracker-Übereinstimmungsstatus

### Dateiformat

Für beste Ergebnisse verwenden Sie dieses Format:

```
Anime Name - S1E1.mp4
Anime Name - S1E2.mp4
Anime Name - S2E1.mp4
```

Unterstützte Muster:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Gruppe] Anime Name - 01.mp4`

## Externe Laufwerke

### Laufwerke hinzufügen

USB-Laufwerke oder externe Festplatten hinzufügen:

1. Einstellungen → Externe Laufwerke
2. Wählen Sie "Laufwerk hinzufügen"
3. Geben Sie den Laufwerkspfad ein
4. Geben Sie einen Namen

### Laufwerke scannen

1. Bibliothek → Externe Laufwerke
2. Wählen Sie Laufwerk
3. Wählen Sie "Laufwerk scannen"

### Laufwerksverwaltung

- Alle registrierten Laufwerke anzeigen
- Laufwerke entfernen
- Laufwerke umbenennen
- Einzelne Laufwerke scannen

## Virtuelle Bibliothek

### Was ist die virtuelle Bibliothek?

Online-Anime für schnellen Zugriff mit Lesezeichen versehen:
- Kein Download erforderlich
- Schneller Zugriff auf Favoriten
- Organisierte Sammlung

### Zur virtuellen Bibliothek hinzufügen

1. Suchen Sie nach Anime
2. Details anzeigen
3. Wählen Sie "Zur Bibliothek hinzufügen"

### Auf virtuelle Bibliothek zugreifen

1. Hauptmenü → Bibliothek
2. Wählen Sie "Virtuelle Bibliothek"
3. Durchsuchen Sie mit Lesezeichen versehene Anime

## Bibliothek durchsuchen

### Lokale Anime

Heruntergeladene Anime anzeigen:
- Nach Titel sortiert
- Zeigt Episodenzahl
- Gibt Abschlussstatus an

### Aus Bibliothek abspielen

1. Wählen Sie Anime
2. Wählen Sie Episode
3. Wird in MPV abgespielt

### Bibliotheksstatistiken

Statistiken anzeigen:
- Gesamtzahl der Anime
- Gesamtepisoden
- Verwendeter Gesamtspeicher
- Am meisten angesehen

## Tracker-Synchronisation

### Auto-Sync

Beim Scannen der Bibliothek:
- Gleicht Anime mit Tracker-Datenbank ab
- Synchronisiert Wiedergabefortschritt
- Aktualisiert Abschlussstatus

### Manuelle Synchronisation

Synchronisation erzwingen:
1. Bibliothek → Einstellungen
2. Wählen Sie "Mit Trackern synchronisieren"

### Übereinstimmungsgenauigkeit

Übereinstimmung verbessern:
- Verwenden Sie Standard-Dateibenennung
- Fügen Sie Staffelnummern hinzu
- Verwenden Sie vollständige Anime-Titel

## Bibliotheksorganisation

### Ordnerstruktur

Empfohlene Struktur:

```
downloads/
├── Anime 1/
│   ├── S1E1.mp4
│   ├── S1E2.mp4
│   └── ...
├── Anime 2/
│   ├── S1E1.mp4
│   └── ...
```

### Aufräumen

Anime aus Index entfernen:
1. Bibliothek → Verwalten
2. Wählen Sie Anime
3. Wählen Sie "Aus Index entfernen"

Hinweis: Dies entfernt nur aus dem Index, nicht die Dateien.

## Erweiterte Funktionen

### Multi-Quellen-Bibliothek

Anime kombinieren von:
- Download-Verzeichnis
- Externe Laufwerke
- Netzwerkfreigaben (falls gemountet)

### Bibliothek durchsuchen

Schnellsuche in Bibliothek:
1. Bibliotheksmenü
2. Zum Suchen tippen
3. Filtert Ergebnisse in Echtzeit

### Bibliothek exportieren

Bibliotheksliste exportieren:
1. Bibliothek → Exportieren
2. Format wählen (JSON/CSV)
3. In Datei speichern

## Fehlerbehebung

### Anime nicht erkannt

1. Überprüfen Sie Dateibenennungsformat
2. Stellen Sie sicher, dass Dateien im Download-Verzeichnis sind
3. Bibliothek erneut scannen
4. Überprüfen Sie Dateierweiterungen (.mp4, .mkv)

### Falsche Episodenzahl

1. Überprüfen Sie Dateibenennung
2. Überprüfen Sie auf doppelte Dateien
3. Bibliothek erneut scannen

### Tracker stimmt nicht überein

1. Verwenden Sie exakten Anime-Titel
2. Fügen Sie Jahr im Ordnernamen hinzu
3. Manuelle Übereinstimmung in Tracker-Einstellungen

### Externes Laufwerk nicht gefunden

1. Überprüfen Sie, ob Laufwerk gemountet ist
2. Überprüfen Sie, ob Pfad korrekt ist
3. Laufwerk in Einstellungen erneut hinzufügen

## Best Practices

1. Verwenden Sie konsistente Dateibenennung
2. Organisieren Sie nach Anime-Ordnern
3. Fügen Sie Staffelnummern hinzu
4. Scannen Sie nach Abschluss der Downloads
5. Sichern Sie Bibliotheksdatenbank regelmäßig

## Nächste Schritte

- [Tracker-Integration](trackers.md): Mit Online-Trackern synchronisieren
- [Download-Anleitung](downloading.md): Mehr Anime herunterladen
- [Konfiguration](../getting-started/configuration.md): Bibliothekseinstellungen
