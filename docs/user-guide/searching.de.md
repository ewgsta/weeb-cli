# Anime suchen

Erfahren Sie, wie Sie über mehrere Anbieter nach Anime suchen und finden, was Sie sehen möchten.

## Grundlegende Suche

### Vom Hauptmenü

1. Starten Sie Weeb CLI: `weeb-cli`
2. Wählen Sie "Anime suchen" aus dem Hauptmenü
3. Geben Sie Ihre Suchanfrage ein
4. Durchsuchen Sie die Ergebnisse

### Suchtipps

- Verwenden Sie englische oder muttersprachliche Titel
- Probieren Sie alternative Schreibweisen, wenn nicht gefunden
- Verwenden Sie Teiltitel für breitere Ergebnisse
- Die Suche unterscheidet nicht zwischen Groß- und Kleinschreibung

## Suchergebnisse

Ergebnisse zeigen:
- Anime-Titel
- Typ (Serie, Film, OVA usw.)
- Erscheinungsjahr
- Coverbild (wenn Terminal unterstützt)
- Anbieterquelle

### Navigation in Ergebnissen

- Verwenden Sie Pfeiltasten zur Navigation
- Drücken Sie Enter zum Auswählen
- Drücken Sie Ctrl+C zum Zurückgehen

## Anbieterauswahl

### Standard-Anbieter

Der Standard-Anbieter basiert auf Ihrer Spracheinstellung:
- Türkisch: Animecix
- Englisch: HiAnime
- Deutsch: AniWorld
- Polnisch: Docchi

### Anbieter wechseln

1. Gehen Sie zu Einstellungen → Konfiguration
2. Wählen Sie "Standard-Anbieter"
3. Wählen Sie aus verfügbaren Anbietern

### Anbieterspezifische Suche

Verschiedene Anbieter können unterschiedliche Inhalte haben:
- Probieren Sie mehrere Anbieter, wenn nicht gefunden
- Einige Anbieter haben exklusive Inhalte
- Qualität und Verfügbarkeit variieren

## Suchverlauf

### Verlauf anzeigen

1. Wählen Sie im Hauptmenü "Anime suchen"
2. Drücken Sie die Nach-oben-Taste, um letzte Suchen zu sehen
3. Wählen Sie aus dem Verlauf, um die Suche zu wiederholen

### Verlauf löschen

Einstellungen → Cache → Suchverlauf löschen

## Erweiterte Suche

### API-Modus

Für Skripting und Automatisierung:

```bash
# Suche mit spezifischem Anbieter
weeb-cli api search "One Piece" --provider animecix

# Ausgabe ist JSON
weeb-cli api search "Naruto" --provider hianime | jq
```

### Ergebnisse filtern

Derzeit erfolgt die Filterung nach Anbieter. Zukünftige Versionen können enthalten:
- Genre-Filterung
- Jahres-Filterung
- Typ-Filterung (Serie/Film/OVA)

## Fehlerbehebung

### Keine Ergebnisse gefunden

1. Überprüfen Sie die Rechtschreibung
2. Probieren Sie alternativen Titel (Englisch/Japanisch/Muttersprache)
3. Probieren Sie anderen Anbieter
4. Überprüfen Sie die Internetverbindung

### Langsame Suche

1. Überprüfen Sie die Netzwerkgeschwindigkeit
2. Probieren Sie anderen Anbieter
3. Cache leeren: Einstellungen → Cache → Anbieter-Cache leeren

### Anbieterfehler

Wenn ein Anbieter fehlschlägt:
1. Probieren Sie einen anderen Anbieter
2. Überprüfen Sie, ob die Anbieter-Website erreichbar ist
3. Melden Sie das Problem auf GitHub, wenn es anhält

## Nächste Schritte

- [Streaming-Anleitung](streaming.md): Erfahren Sie, wie Sie Anime ansehen
- [Download-Anleitung](downloading.md): Erfahren Sie, wie Sie Anime herunterladen
- [Tracker-Integration](trackers.md): Synchronisieren Sie Ihren Fortschritt
