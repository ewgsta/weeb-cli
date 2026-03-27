# Serve Mode - Torznab Server

Run Weeb CLI as a Torznab server for integration with Sonarr and other *arr applications.

## Overview

Serve mode provides a Torznab-compatible API server that allows *arr applications to search and download anime through Weeb CLI providers.

## Starting Server

```bash
weeb-cli serve [OPTIONS]
```

Options:
- `--host`: Host to bind (default: 127.0.0.1)
- `--port`: Port to listen (default: 8080)
- `--api-key`: API key for authentication

Example:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080 --api-key myapikey123
```

## Sonarr Integration

### Adding Indexer

1. Sonarr → Settings → Indexers
2. Add → Torznab → Custom
3. Configure:
   - Name: Weeb CLI
   - URL: http://localhost:8080
   - API Key: (your key)
   - Categories: 5070 (Anime)

### Testing Connection

1. Click "Test" in Sonarr
2. Should show success
3. Save indexer

## API Endpoints

### Capabilities

```
GET /api?t=caps
```

Returns Torznab capabilities XML.

### Search

```
GET /api?t=search&q=QUERY&apikey=KEY
```

Search for anime by title.

### TV Search

```
GET /api?t=tvsearch&q=QUERY&season=1&ep=1&apikey=KEY
```

Search for specific episode.

## Configuration

### API Key

Generate secure API key:
```bash
openssl rand -hex 16
```

Use in serve command and Sonarr config.

### Network Access

For remote access:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080
```

Warning: Ensure firewall is configured properly.

## Limitations

- Read-only (no download management)
- Search only (no RSS feeds)
- Single provider per instance
- No authentication beyond API key

## Next Steps

- [API Mode](api-mode.md): JSON API
- [Commands](commands.md): CLI reference
