# Schnellstart-Anleitung

Diese Anleitung hilft Ihnen, in wenigen Minuten mit Weeb CLI zu beginnen.

## Erster Start

Wenn Sie Weeb CLI zum ersten Mal ausführen, werden Sie durch einen Einrichtungsassistenten geführt:

```bash
weeb-cli
```

### Einrichtungsassistent

1. **Sprachauswahl**: Wählen Sie Ihre bevorzugte Sprache (Türkisch, Englisch, Deutsch oder Polnisch)
2. **Download-Verzeichnis**: Legen Sie fest, wo Anime-Dateien heruntergeladen werden
3. **Anbieterauswahl**: Wählen Sie Ihre Standard-Anime-Quelle
4. **Optionale Einstellungen**: Konfigurieren Sie Tracker, Discord RPC usw.

## Grundlegende Verwendung

### Anime suchen

1. Wählen Sie im Hauptmenü "Anime suchen"
2. Geben Sie den Anime-Namen ein
3. Durchsuchen Sie die Suchergebnisse
4. Wählen Sie einen Anime aus, um Details anzuzeigen

### Streaming

1. Wählen Sie nach der Auswahl eines Anime "Ansehen"
2. Wählen Sie eine Episode
3. Wählen Sie die Stream-Qualität
4. Das Video wird im MPV-Player geöffnet

### Herunterladen

1. Wählen Sie nach der Auswahl eines Anime "Herunterladen"
2. Wählen Sie Episoden zum Herunterladen (einzeln, Bereich oder alle)
3. Downloads werden zur Warteschlange hinzugefügt
4. Überwachen Sie den Fortschritt im Menü "Downloads"

### Downloads verwalten

Greifen Sie auf das Download-Menü zu, um:

- Aktive Downloads mit Fortschritt anzuzeigen
- Downloads pausieren/fortsetzen
- Fehlgeschlagene Downloads wiederholen
- Abgeschlossene Downloads löschen

## Häufige Aufgaben

### Wiedergabeverlauf anzeigen

```
Hauptmenü → Watchlist → Verlauf anzeigen
```

Ihr Wiedergabeverlauf zeigt:
- Kürzlich angesehene Anime
- Episodenfortschritt
- Abschlussstatus

### Tracker konfigurieren

```
Hauptmenü → Einstellungen → Tracker
```

Verbinden Sie Ihre Konten:
- AniList (OAuth)
- MyAnimeList (OAuth)
- Kitsu (E-Mail/Passwort)

Der Fortschritt wird automatisch beim Ansehen oder Herunterladen synchronisiert.

### Lokale Bibliothek verwalten

```
Hauptmenü → Bibliothek → Bibliothek scannen
```

Weeb CLI kann Ihre heruntergeladenen Anime indizieren:
- Automatische Erkennung von Anime aus Dateinamen
- Synchronisation mit Trackern
- Offline-Inhalte durchsuchen

## Tastenkombinationen

- `Strg+C`: Aktuellen Vorgang abbrechen / Zurück
- `↑/↓`: Menüs navigieren
- `Enter`: Option auswählen
- `Leertaste`: Auswahl umschalten (Mehrfachauswahl)

## API-Modus

Für Skripting und Automatisierung:

```bash
# Anime suchen
weeb-cli api search "One Piece" --provider animecix

# Episoden abrufen
weeb-cli api episodes <anime-id> --provider animecix

# Stream-Links abrufen
weeb-cli api streams <anime-id> <episode-id> --provider animecix
```

Die Ausgabe erfolgt im JSON-Format für einfaches Parsen.

## Tipps

1. **Wiedergabe fortsetzen**: Weeb CLI speichert automatisch Ihre Position. Wählen Sie einfach dieselbe Episode aus, um fortzufahren.

2. **Qualitätsauswahl**: Streams höherer Qualität können bei langsameren Verbindungen puffern. Versuchen Sie eine niedrigere Qualität, wenn Probleme auftreten.

3. **Download-Warteschlange**: Sie können mehrere Anime und Episoden in die Warteschlange stellen. Sie werden basierend auf Ihren Einstellungen gleichzeitig heruntergeladen.

4. **Externe Laufwerke**: Fügen Sie externe Laufwerke in den Einstellungen hinzu, um Anime von USB-Laufwerken oder externen Festplatten zu scannen.

5. **Offline-Modus**: Heruntergeladene Anime und lokale Bibliothek funktionieren ohne Internetverbindung.

## Fehlerbehebung

### Video wird nicht abgespielt
- Stellen Sie sicher, dass MPV installiert ist (wird beim ersten Start automatisch installiert)
- Überprüfen Sie Ihre Internetverbindung
- Versuchen Sie eine andere Stream-Qualität oder einen anderen Server

### Download schlägt fehl
- Überprüfen Sie den verfügbaren Speicherplatz
- Überprüfen Sie die Internetverbindung
- Versuchen Sie einen anderen Anbieter
- Überprüfen Sie die Download-Einstellungen (Aria2/yt-dlp)

### Tracker synchronisiert nicht
- Authentifizieren Sie sich erneut unter Einstellungen → Tracker
- Überprüfen Sie die Internetverbindung
- Überprüfen Sie, ob der Anime-Titel mit der Tracker-Datenbank übereinstimmt

## Nächste Schritte

- [Konfigurationsanleitung](configuration.md): Weeb CLI anpassen
- [Benutzerhandbuch](../user-guide/searching.md): Detaillierte Funktionsdokumentation
- [CLI-Referenz](../cli/commands.md): Befehlszeilenoptionen
