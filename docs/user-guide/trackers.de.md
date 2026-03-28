# Tracker-Integration

Synchronisieren Sie Ihren Anime-Wiedergabefortschritt mit AniList, MyAnimeList und Kitsu.

## Unterstützte Tracker

### AniList

- OAuth-Authentifizierung
- Automatische Fortschrittssynchronisation
- Manga- und Anime-Tracking
- Soziale Funktionen

### MyAnimeList

- OAuth-Authentifizierung
- Umfassende Datenbank
- Community-Funktionen
- Empfehlungen

### Kitsu

- E-Mail/Passwort-Authentifizierung
- Moderne Oberfläche
- Soziale Funktionen
- Fortschrittsverfolgung

## Tracker einrichten

### AniList-Einrichtung

1. Einstellungen → Tracker → AniList
2. Wählen Sie "Authentifizieren"
3. Browser öffnet sich für OAuth
4. Anwendung autorisieren
5. Zurück zur CLI (automatische Erkennung)

### MyAnimeList-Einrichtung

1. Einstellungen → Tracker → MyAnimeList
2. Wählen Sie "Authentifizieren"
3. Browser öffnet sich für OAuth
4. Anwendung autorisieren
5. Zurück zur CLI

### Kitsu-Einrichtung

1. Einstellungen → Tracker → Kitsu
2. E-Mail eingeben
3. Passwort eingeben
4. Anmeldedaten werden sicher gespeichert

## Fortschrittssynchronisation

### Automatische Synchronisation

Fortschritt wird automatisch synchronisiert:
- Beim Ansehen von Anime (bei 80% Abschluss)
- Beim Herunterladen von Episoden
- Beim Scannen der lokalen Bibliothek
- Beim Starten der Anwendung

### Manuelle Synchronisation

Synchronisation erzwingen:
1. Einstellungen → Tracker
2. Tracker auswählen
3. "Jetzt synchronisieren" wählen

### Offline-Warteschlange

Wenn offline:
- Updates werden lokal in die Warteschlange gestellt
- Synchronisiert, wenn Verbindung wiederhergestellt
- Kein Fortschritt geht verloren

## Anime abgleichen

### Automatischer Abgleich

Weeb CLI gleicht automatisch ab:
- Nach Anime-Titel
- Nach alternativen Titeln
- Nach Jahr und Typ

### Abgleichgenauigkeit

Abgleich verbessern:
- Exakte Titel verwenden
- Jahr in Suche einbeziehen
- Englische Titel verwenden, wenn möglich

### Manueller Abgleich

Wenn automatischer Abgleich fehlschlägt:
1. Watchlist → Anime auswählen
2. "Mit Tracker verknüpfen" wählen
3. Tracker-Datenbank durchsuchen
4. Korrekte Übereinstimmung auswählen

## Tracker verwalten

### Status anzeigen

Tracker-Status überprüfen:
- Authentifizierungsstatus
- Letzte Synchronisationszeit
- Ausstehende Updates
- Synchronisationsfehler

Zugriff: Einstellungen → Tracker → Status

### Trennen

Tracker entfernen:
1. Einstellungen → Tracker
2. Tracker auswählen
3. "Trennen" wählen
4. Entfernung bestätigen

### Erneut authentifizieren

Wenn Token abläuft:
1. Einstellungen → Tracker
2. Tracker auswählen
3. "Erneut authentifizieren" wählen

## Tracker-Funktionen

### Fortschrittsaktualisierungen

Aktualisiert automatisch:
- Aktuelle Episode
- Wiedergabestatus (ansehen/abgeschlossen/abgebrochen)
- Bewertung (falls festgelegt)
- Wiedergabezähler

### Statusverwaltung

Anime-Status festlegen:
- Ansehen
- Abgeschlossen
- Pausiert
- Abgebrochen
- Geplant anzusehen

### Bewertung

Anime bewerten:
- 1-10 Skala (AniList/Kitsu)
- 1-10 Skala (MyAnimeList)
- Aktualisiert auf Tracker

## Datenschutz

### Geteilte Daten

Teilt nur:
- Wiedergabefortschritt
- Episodennummern
- Abschlussstatus
- Bewertungen (falls festgelegt)

### Nicht geteilte Daten

Teilt niemals:
- Heruntergeladene Dateien
- Stream-Quellen
- Suchverlauf
- Lokale Pfade

## Fehlerbehebung

### Authentifizierung fehlgeschlagen

1. Internetverbindung überprüfen
2. Anmeldedaten überprüfen
3. Erneute Authentifizierung versuchen
4. Tracker-Website-Status überprüfen

### Fortschritt wird nicht synchronisiert

1. Tracker-Verbindung überprüfen
2. Überprüfen, ob Anime abgeglichen ist
3. Offline-Warteschlange überprüfen
4. Manuelle Synchronisation

### Falscher Anime abgeglichen

1. Aktuelle Übereinstimmung aufheben
2. Tracker manuell durchsuchen
3. Korrekten Anime auswählen
4. Übereinstimmung bestätigen

### Synchronisationsfehler

Protokolle überprüfen:
```bash
~/.weeb-cli/logs/debug.log
```

Debug-Modus aktivieren:
Einstellungen → Konfiguration → Debug-Modus

## Mehrere Tracker

### Mehrere verwenden

Sie können alle drei Tracker gleichzeitig verwenden:
- Fortschritt wird mit allen synchronisiert
- Unabhängige Authentifizierung
- Separate Offline-Warteschlangen

### Synchronisationspriorität

Bei Konflikten:
1. Neueste Aktualisierung gewinnt
2. Manuelle Updates überschreiben automatische
3. Jeden Tracker separat überprüfen

## Best Practices

1. Bei allen verwendeten Trackern authentifizieren
2. Konsistente Anime-Titel verwenden
3. Synchronisationsstatus regelmäßig überprüfen
4. Offline-Warteschlange regelmäßig leeren
5. Bei anhaltenden Problemen erneut authentifizieren

## Nächste Schritte

- [Watchlist-Anleitung](../cli/commands.md): Wiedergabeverlauf verwalten
- [Bibliotheksanleitung](library.md): Lokale Bibliothekssynchronisation
- [Konfiguration](../getting-started/configuration.md): Tracker-Einstellungen
