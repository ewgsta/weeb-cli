# RESTful API Mode

Weeb CLI can run as a RESTful API server, providing HTTP endpoints for all provider operations including search, episode listing, stream extraction, and anime details.

## Installation

Install with RESTful API dependencies:

```bash
pip install weeb-cli[serve-restful]
```

## Usage

### Basic Usage

Start the server with default settings:

```bash
weeb-cli serve restful
```

The server will start on `http://0.0.0.0:8080` with all available providers.

### Custom Configuration

```bash
weeb-cli serve restful \
  --port 9000 \
  --host 127.0.0.1 \
  --providers animecix,hianime \
  --no-cors \
  --debug
```

### Command Options

| Option | Environment Variable | Default | Description |
|--------|---------------------|---------|-------------|
| `--port` | `RESTFUL_PORT` | `8080` | HTTP port to bind |
| `--host` | `RESTFUL_HOST` | `0.0.0.0` | Host address to bind |
| `--providers` | `RESTFUL_PROVIDERS` | `animecix,hianime,aniworld,docchi` | Comma-separated provider names |
| `--cors/--no-cors` | `RESTFUL_CORS` | `true` | Enable/disable CORS |
| `--debug` | `RESTFUL_DEBUG` | `false` | Enable debug mode |

## API Endpoints

### Health Check

Check if the server is running:

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "service": "weeb-cli-restful",
  "providers": ["animecix", "hianime", "aniworld", "docchi"]
}
```

### List Providers

Get all available providers:

```http
GET /api/providers
```

**Response:**
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

### Search Anime

Search for anime across providers:

```http
GET /api/search?q=naruto&provider=animecix
```

**Query Parameters:**
- `q` (required): Search query
- `provider` (optional): Provider name (defaults to first loaded)

**Response:**
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

### Get Anime Details

Get detailed information about an anime:

```http
GET /api/anime/{anime_id}?provider=animecix
```

**Query Parameters:**
- `provider` (optional): Provider name (defaults to first loaded)

**Response:**
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
    "description": "Anime description...",
    "genres": ["Action", "Adventure"],
    "status": "completed",
    "episodes": [...]
  }
}
```

### Get Episodes

List all episodes for an anime:

```http
GET /api/anime/{anime_id}/episodes?provider=animecix&season=1
```

**Query Parameters:**
- `provider` (optional): Provider name (defaults to first loaded)
- `season` (optional): Filter by season number

**Response:**
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

### Get Streams

Get stream URLs for an episode:

```http
GET /api/anime/{anime_id}/episodes/{episode_id}/streams?provider=animecix&sort=desc
```

**Query Parameters:**
- `provider` (optional): Provider name (defaults to first loaded)
- `sort` (optional): Sort by quality (`asc` or `desc`, defaults to `desc`)

**Response:**
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

## Docker Deployment

### Using Docker Compose

```bash
docker-compose -f docker-compose.restful.yml up -d
```

### Using Dockerfile

Build the image:

```bash
docker build -f Dockerfile.restful -t weeb-cli-restful .
```

Run the container:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 8080:8080 \
  -e RESTFUL_PROVIDERS=animecix,hianime \
  weeb-cli-restful
```

### Environment Variables

All command options can be configured via environment variables:

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

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message description"
}
```

**Common HTTP Status Codes:**
- `200`: Success
- `400`: Bad request (missing/invalid parameters)
- `404`: Resource not found
- `500`: Internal server error

## CORS Support

CORS is enabled by default, allowing requests from any origin. To disable:

```bash
weeb-cli serve restful --no-cors
```

Or via environment variable:

```bash
export RESTFUL_CORS=false
```

## Example Usage

### cURL

```bash
# Search anime
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"

# Get episodes
curl "http://localhost:8080/api/anime/12345/episodes?season=1"

# Get streams
curl "http://localhost:8080/api/anime/12345/episodes/ep-1/streams?sort=desc"
```

### Python

```python
import requests

# Search anime
response = requests.get(
    "http://localhost:8080/api/search",
    params={"q": "naruto", "provider": "animecix"}
)
results = response.json()

# Get streams
response = requests.get(
    f"http://localhost:8080/api/anime/{anime_id}/episodes/{episode_id}/streams",
    params={"provider": "animecix", "sort": "desc"}
)
streams = response.json()
```

### JavaScript

```javascript
// Search anime
const response = await fetch(
  'http://localhost:8080/api/search?q=naruto&provider=animecix'
);
const data = await response.json();

// Get streams
const streamResponse = await fetch(
  `http://localhost:8080/api/anime/${animeId}/episodes/${episodeId}/streams?sort=desc`
);
const streams = await streamResponse.json();
```

## Production Deployment

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

### Systemd Service

Create `/etc/systemd/system/weeb-cli-restful.service`:

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

Enable and start:

```bash
sudo systemctl enable weeb-cli-restful
sudo systemctl start weeb-cli-restful
```

## Security Considerations

1. **Authentication**: The API does not include built-in authentication. Use a reverse proxy (Nginx, Traefik) with authentication if exposing publicly.

2. **Rate Limiting**: Implement rate limiting at the reverse proxy level to prevent abuse.

3. **HTTPS**: Always use HTTPS in production. Configure SSL/TLS at the reverse proxy level.

4. **Firewall**: Restrict access to trusted IPs if possible.

## Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8080

# Use a different port
weeb-cli serve restful --port 9000
```

### Provider Not Found

Ensure the provider name is correct:

```bash
# List available providers
weeb-cli api providers

# Use correct provider name
weeb-cli serve restful --providers animecix,hianime
```

### CORS Issues

If experiencing CORS issues, ensure CORS is enabled:

```bash
weeb-cli serve restful --cors
```

## See Also

- [Torznab Server Mode](serve-mode.md)
- [API Commands](api-mode.md)
- [Available Providers](../api/providers/registry.md)
