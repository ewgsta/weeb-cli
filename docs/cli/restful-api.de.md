# RESTful API Modus

Weeb CLI kann als RESTful API-Server ausgeführt werden und bietet HTTP-Endpunkte für alle Provider-Operationen, einschließlich Suche, Episodenliste, Stream-Extraktion und Anime-Details.

## Installation

Mit RESTful API-Abhängigkeiten installieren:

```bash
pip install weeb-cli[serve-restful]
```

## Verwendung

### Grundlegende Verwendung

Server mit Standardeinstellungen starten:

```bash
weeb-cli serve restful
```

Der Server startet auf `http://0.0.0.0:8080` mit allen verfügbaren Providern.

### Benutzerdefinierte Konfiguration

```bash
weeb-cli serve restful \
  --port 9000 \
  --host 127.0.0.1 \
  --providers animecix,hianime \
  --no-cors \
  --debug
```

### Befehlsoptionen

| Option | Umgebungsvariable | Standard | Beschreibung |
|--------|------------------|----------|--------------|
| `--port` | `RESTFUL_PORT` | `8080` | HTTP-Port zum Binden |
| `--host` | `RESTFUL_HOST` | `0.0.0.0` | Host-Adresse zum Binden |
| `--providers` | `RESTFUL_PROVIDERS` | `animecix,hianime,aniworld,docchi` | Kommagetrennte Provider-Namen |
| `--cors/--no-cors` | `RESTFUL_CORS` | `true` | CORS aktivieren/deaktivieren |
| `--debug` | `RESTFUL_DEBUG` | `false` | Debug-Modus aktivieren |

## API-Endpunkte

### Gesundheitsprüfung

Überprüfen, ob der Server läuft:

```http
GET /health
```

**Antwort:**
```json
{
  "status": "ok",
  "service": "weeb-cli-restful",
  "providers": ["animecix", "hianime", "aniworld", "docchi"]
}
```

### Provider auflisten

Alle verfügbaren Provider abrufen:

```http
GET /api/providers
```

**Antwort:**
```json
{
  "success": true,
  "providers": [
    {
      "name": "animecix",
      "lang": "tr",
      "region": "TR",
      "class": "AnimecixProvider"
    }
  ],
  "loaded": ["animecix", "hianime"]
}
```

### Anime suchen

Anime über Provider suchen:

```http
GET /api/search?q=naruto&provider=animecix
```

**Abfrageparameter:**
- `q` (erforderlich): Suchanfrage
- `provider` (optional): Provider-Name (Standard: erster geladener)

**Antwort:**
```json
{
  "success": true,
  "provider": "animecix",
  "query": "naruto",
  "count": 10,
  "results": [
    {
      "id": "12345",
      "title": "Naruto",
      "type": "series",
      "cover": "https://example.com/cover.jpg",
      "year": 2002
    }
  ]
}
```

### Anime-Details abrufen

Detaillierte Informationen über einen Anime abrufen:

```http
GET /api/anime/{anime_id}?provider=animecix
```

**Abfrageparameter:**
- `provider` (optional): Provider-Name (Standard: erster geladener)

**Antwort:**
```json
{
  "success": true,
  "provider": "animecix",
  "anime": {
    "id": "12345",
    "title": "Naruto",
    "type": "series",
    "cover": "https://example.com/cover.jpg",
    "year": 2002,
    "description": "Anime-Beschreibung...",
    "genres": ["Action", "Abenteuer"],
    "status": "completed",
    "episodes": [...]
  }
}
```

### Episoden abrufen

Alle Episoden für einen Anime auflisten:

```http
GET /api/anime/{anime_id}/episodes?provider=animecix&season=1
```

**Abfrageparameter:**
- `provider` (optional): Provider-Name (Standard: erster geladener)
- `season` (optional): Nach Staffelnummer filtern

**Antwort:**
```json
{
  "success": true,
  "provider": "animecix",
  "anime_id": "12345",
  "count": 220,
  "episodes": [
    {
      "id": "ep-1",
      "number": 1,
      "title": "Enter: Naruto Uzumaki!",
      "season": 1,
      "url": "https://example.com/episode/1"
    }
  ]
}
```

### Streams abrufen

Stream-URLs für eine Episode abrufen:

```http
GET /api/anime/{anime_id}/episodes/{episode_id}/streams?provider=animecix&sort=desc
```

**Abfrageparameter:**
- `provider` (optional): Provider-Name (Standard: erster geladener)
- `sort` (optional): Nach Qualität sortieren (`asc` oder `desc`, Standard: `desc`)

**Antwort:**
```json
{
  "success": true,
  "provider": "animecix",
  "anime_id": "12345",
  "episode_id": "ep-1",
  "count": 3,
  "streams": [
    {
      "url": "https://example.com/stream.m3u8",
      "quality": "1080p",
      "server": "default",
      "headers": {
        "Referer": "https://example.com"
      },
      "subtitles": null
    }
  ]
}
```

## Docker-Bereitstellung

### Mit Docker Compose

```bash
docker-compose -f docs/docker-compose.restful.yml up -d
```

### Mit Inline Dockerfile

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir weeb-cli[serve-restful]
EXPOSE 8080
CMD ["weeb-cli", "serve", "restful"]
```

Container ausführen:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 8080:8080 \
  -e RESTFUL_PORT=8080 \
  -e RESTFUL_HOST=0.0.0.0 \
  -e RESTFUL_CORS=true \
  -e RESTFUL_PROVIDERS=animecix,hianime \
  weeb-cli-restful
```

### Umgebungsvariablen

Alle Befehlsoptionen können über Umgebungsvariablen konfiguriert werden:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 9000:9000 \
  -e RESTFUL_PORT=9000 \
  -e RESTFUL_HOST=0.0.0.0 \
  -e RESTFUL_PROVIDERS=animecix,hianime,aniworld \
  -e RESTFUL_CORS=true \
  -e RESTFUL_DEBUG=false \
  weeb-cli-restful
```

## Fehlerbehandlung

Alle Endpunkte geben konsistente Fehlerantworten zurück:

```json
{
  "success": false,
  "error": "Fehlermeldungsbeschreibung"
}
```

**Häufige HTTP-Statuscodes:**
- `200`: Erfolg
- `400`: Ungültige Anfrage (fehlende/ungültige Parameter)
- `404`: Ressource nicht gefunden
- `500`: Interner Serverfehler

## CORS-Unterstützung

CORS ist standardmäßig aktiviert und erlaubt Anfragen von jedem Origin. Zum Deaktivieren:

```bash
weeb-cli serve restful --no-cors
```

Oder über Umgebungsvariable:

```bash
export RESTFUL_CORS=false
```

## Beispielverwendung

### cURL

```bash
# Anime suchen
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"

# Episoden abrufen
curl "http://localhost:8080/api/anime/12345/episodes?season=1"

# Streams abrufen
curl "http://localhost:8080/api/anime/12345/episodes/ep-1/streams?sort=desc"
```

### Python

```python
import requests

# Anime suchen
response = requests.get(
    "http://localhost:8080/api/search",
    params={"q": "naruto", "provider": "animecix"}
)
results = response.json()

# Streams abrufen
response = requests.get(
    f"http://localhost:8080/api/anime/{anime_id}/episodes/{episode_id}/streams",
    params={"provider": "animecix", "sort": "desc"}
)
streams = response.json()
```

### JavaScript

```javascript
// Anime suchen
const response = await fetch(
  'http://localhost:8080/api/search?q=naruto&provider=animecix'
);
const data = await response.json();

// Streams abrufen
const streamResponse = await fetch(
  `http://localhost:8080/api/anime/${animeId}/episodes/${episodeId}/streams?sort=desc`
);
const streams = await streamResponse.json();
```

## Produktionsbereitstellung

### Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name api.example.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Systemd-Dienst

`/etc/systemd/system/weeb-cli-restful.service` erstellen:

```ini
[Unit]
Description=Weeb CLI RESTful API
After=network.target

[Service]
Type=simple
User=weeb
WorkingDirectory=/opt/weeb-cli
Environment="RESTFUL_PORT=8080"
Environment="RESTFUL_PROVIDERS=animecix,hianime"
ExecStart=/usr/local/bin/weeb-cli serve restful
Restart=always

[Install]
WantedBy=multi-user.target
```

Aktivieren und starten:

```bash
sudo systemctl enable weeb-cli-restful
sudo systemctl start weeb-cli-restful
```

## Sicherheitsüberlegungen

1. **Authentifizierung**: Die API enthält keine integrierte Authentifizierung. Verwenden Sie einen Reverse Proxy (Nginx, Traefik) mit Authentifizierung, wenn Sie öffentlich verfügbar machen.

2. **Rate Limiting**: Implementieren Sie Rate Limiting auf Reverse-Proxy-Ebene, um Missbrauch zu verhindern.

3. **HTTPS**: Verwenden Sie in der Produktion immer HTTPS. Konfigurieren Sie SSL/TLS auf Reverse-Proxy-Ebene.

4. **Firewall**: Beschränken Sie den Zugriff auf vertrauenswürdige IPs, wenn möglich.

## Fehlerbehebung

### Port bereits in Verwendung

```bash
# Prüfen, was den Port verwendet
lsof -i :8080

# Anderen Port verwenden
weeb-cli serve restful --port 9000
```

### Provider nicht gefunden

Stellen Sie sicher, dass der Provider-Name korrekt ist:

```bash
# Verfügbare Provider auflisten
weeb-cli api providers

# Korrekten Provider-Namen verwenden
weeb-cli serve restful --providers animecix,hianime
```

### CORS-Probleme

Wenn CORS-Probleme auftreten, stellen Sie sicher, dass CORS aktiviert ist:

```bash
weeb-cli serve restful --cors
```

## Siehe auch

- [Torznab-Servermodus](serve-mode.de.md)
- [API-Befehle](api-mode.de.md)
- [Verfügbare Provider](../api/providers/registry.de.md)
