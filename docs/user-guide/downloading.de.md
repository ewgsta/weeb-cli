# Download-Verwaltung

Erfahren Sie, wie Sie Anime für die Offline-Ansicht mit dem leistungsstarken Download-System von Weeb CLI herunterladen.

## Downloads starten

### Aus der Suche

1. Suchen Sie nach Anime
2. Wählen Sie Anime
3. Wählen Sie die Option "Herunterladen"
4. Wählen Sie Episoden:
   - Einzelne Episode
   - Episodenbereich (z.B. 1-12)
   - Alle Episoden
5. Downloads zur Warteschlange hinzugefügt

### Aus der Watchlist

1. Hauptmenü → Watchlist
2. Wählen Sie Anime
3. Wählen Sie "Episoden herunterladen"
4. Wählen Sie Episoden

## Download-Warteschlange

### Warteschlange anzeigen

Hauptmenü → Downloads

Zeigt:
- Aktive Downloads mit Fortschritt
- Ausstehende Downloads
- Abgeschlossene Downloads
- Fehlgeschlagene Downloads

### Warteschlangeninformationen

Für jeden Download:
- Anime-Titel und Episode
- Fortschritt in Prozent
- Download-Geschwindigkeit
- Geschätzte Zeit
- Status (ausstehend/verarbeitung/abgeschlossen/fehlgeschlagen)

## Downloads verwalten

### Pause/Fortsetzen

Die Warteschlange kann:
- Pausiert: Stoppt alle aktiven Downloads
- Fortgesetzt: Setzt dort fort, wo gestoppt wurde

### Fehlgeschlagene wiederholen

Wenn Downloads fehlschlagen:
1. Gehen Sie zum Downloads-Menü
2. Wählen Sie "Fehlgeschlagene wiederholen"
3. Fehlgeschlagene Downloads werden neu gestartet

### Abgeschlossene löschen

Abgeschlossene Downloads aus der Warteschlange entfernen:
1. Downloads-Menü
2. Wählen Sie "Abgeschlossene löschen"

## Download-Methoden

Weeb CLI verwendet mehrere Download-Methoden mit automatischem Fallback:

### 1. Aria2 (Am schnellsten)

- Multi-Verbindungs-Downloads
- Fortsetzungsunterstützung
- Fortschrittsverfolgung
- Standard: 16 Verbindungen

Konfigurieren: Einstellungen → Downloads → Aria2-Einstellungen

### 2. yt-dlp

- Komplexe Stream-Unterstützung
- Formatauswahl
- Untertitel-Download
- Fallback für HLS-Streams

Konfigurieren: Einstellungen → Downloads → yt-dlp-Einstellungen

### 3. FFmpeg

- HLS-Stream-Konvertierung
- Formatkonvertierung
- Fallback-Methode

### 4. Generisches HTTP

- Einfache HTTP-Downloads
- Letzter Ausweg Fallback

## Download-Einstellungen

### Gleichzeitige Downloads

Maximale gleichzeitige Downloads:
- Standard: 3
- Bereich: 1-10
- Höher = schneller, aber mehr Ressourcen

Einstellungen → Downloads → Gleichzeitige Downloads

### Download-Verzeichnis

Legen Sie fest, wo Dateien gespeichert werden:
- Standard: `./weeb-downloads`
- Kann jedes beschreibbare Verzeichnis sein

Einstellungen → Downloads → Download-Verzeichnis

### Wiederholungseinstellungen

Wiederholungsverhalten konfigurieren:
- Max. Wiederholungen: 0-10 (Standard: 3)
- Wiederholungsverzögerung: 1-60 Sekunden (Standard: 10)

Einstellungen → Downloads → Wiederholungseinstellungen

## Dateibenennung

### Standardformat

```
Anime Name - S1E1.mp4
Anime Name - S1E2.mp4
```

### Benutzerdefinierte Benennung

Dateien werden automatisch benannt:
- Für Dateisystem bereinigt
- Staffel- und Episodennummern
- .mp4-Erweiterung

## Download-Probleme

### Unzureichender Speicherplatz

Weeb CLI prüft verfügbaren Speicherplatz vor dem Download:
- Erfordert mindestens 1GB frei
- Zeigt Fehler bei Unzureichend
- Speicherplatz freigeben oder Verzeichnis ändern

### Download schlägt fehl

Häufige Ursachen:
1. Netzwerkunterbrechung
2. Ungültige Stream-URL
3. Anbieterprobleme
4. Speicherplatz

Lösungen:
1. Download wiederholen
2. Andere Qualität versuchen
3. Anderen Anbieter versuchen
4. Protokolle für Details prüfen

### Langsame Downloads

Geschwindigkeit verbessern:
1. Aria2 aktivieren
2. Max. Verbindungen erhöhen
3. Netzwerkgeschwindigkeit prüfen
4. Anderen Server versuchen

### Unterbrochene fortsetzen

Downloads werden automatisch fortgesetzt:
- Aria2 unterstützt Fortsetzung
- Teilweise Dateien bleiben erhalten
- Setzt vom letzten Byte fort

## Erweiterte Funktionen

### Batch-Downloads

Mehrere Anime herunterladen:
1. Suchen und zur Warteschlange hinzufügen
2. Für andere Anime wiederholen
3. Alle werden gleichzeitig heruntergeladen

### Qualitätspräferenz

Weeb CLI wählt automatisch:
- Höchste verfügbare Qualität
- Bester verfügbarer Server
- Fallback auf niedrigere Qualität bei Bedarf

### Fortschrittsbenachrichtigungen

Systembenachrichtigungen wenn:
- Download abgeschlossen
- Download fehlgeschlagen
- Warteschlange beendet

Aktivieren: Einstellungen → Benachrichtigungen

## Downloads überwachen

### Echtzeit-Fortschritt

Downloads-Menü zeigt:
- Aktuelle Geschwindigkeit (MB/s)
- Heruntergeladene Größe / Gesamtgröße
- Fortschrittsbalken
- Geschätzte Zeit

### Download-Statistiken

Nach Abschluss:
- Gesamt heruntergeladen
- Durchschnittsgeschwindigkeit
- Benötigte Zeit
- Erfolgsrate

## Tipps

1. Aktivieren Sie Aria2 für schnellste Downloads
2. Laden Sie außerhalb der Stoßzeiten herunter
3. Verwenden Sie Episodenbereiche für Batch-Downloads
4. Überwachen Sie regelmäßig den Speicherplatz
5. Wiederholen Sie fehlgeschlagene Downloads, bevor Sie aufgeben

## Nächste Schritte

- [Lokale Bibliothek](library.md): Heruntergeladene Anime verwalten
- [Tracker-Integration](trackers.md): Download-Fortschritt synchronisieren
- [Konfiguration](../getting-started/configuration.md): Einstellungen optimieren
