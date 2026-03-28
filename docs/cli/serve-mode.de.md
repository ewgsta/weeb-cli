# Serve-Modus - Torznab-Server

Weeb CLI als Torznab-Server für Integration mit Sonarr und anderen *arr-Anwendungen ausführen.

## Übersicht

Der Serve-Modus bietet einen Torznab-kompatiblen API-Server, der *arr-Anwendungen ermöglicht, über Weeb CLI-Anbieter nach Anime zu suchen und herunterzuladen.

## Server starten

```bash
weeb-cli serve [OPTIONEN]
```

Optionen:
- `--host`: Host zum Binden (Standard: 127.0.0.1)
- `--port`: Port zum Lauschen (Standard: 8080)
- `--api-key`: API-Schlüssel für Authentifizierung

Beispiel:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080 --api-key meinapikey123
```

## Sonarr-Integration

### Indexer hinzufügen

1. Sonarr → Einstellungen → Indexer
2. Hinzufügen → Torznab → Benutzerdefiniert
3. Konfigurieren:
   - Name: Weeb CLI
   - URL: http://localhost:8080
   - API-Schlüssel: (Ihr Schlüssel)
   - Kategorien: 5070 (Anime)

### Verbindung testen

1. In Sonarr auf "Test" klicken
2. Sollte Erfolg anzeigen
3. Indexer speichern

## API-Endpunkte

### Fähigkeiten

```
GET /api?t=caps
```

Gibt Torznab-Fähigkeiten-XML zurück.

### Suche

```
GET /api?t=search&q=ABFRAGE&apikey=SCHLÜSSEL
```

Nach Anime nach Titel suchen.

### TV-Suche

```
GET /api?t=tvsearch&q=ABFRAGE&season=1&ep=1&apikey=SCHLÜSSEL
```

Nach bestimmter Episode suchen.

## Konfiguration

### API-Schlüssel

Sicheren API-Schlüssel generieren:
```bash
openssl rand -hex 16
```

Im Serve-Befehl und Sonarr-Konfiguration verwenden.

### Netzwerkzugriff

Für Fernzugriff:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080
```

Warnung: Stellen Sie sicher, dass die Firewall ordnungsgemäß konfiguriert ist.

## Einschränkungen

- Nur-Lesen (keine Download-Verwaltung)
- Nur Suche (keine RSS-Feeds)
- Ein Anbieter pro Instanz
- Keine Authentifizierung über API-Schlüssel hinaus

## Nächste Schritte

- [API-Modus](api-mode.md): JSON-API
- [Befehle](commands.md): CLI-Referenz
