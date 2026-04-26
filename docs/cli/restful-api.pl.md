# Tryb RESTful API

Weeb CLI może działać jako serwer RESTful API, zapewniając punkty końcowe HTTP dla wszystkich operacji dostawców, w tym wyszukiwania, listy odcinków, ekstrakcji strumieni i szczegółów anime.

## Instalacja

Zainstaluj z zależnościami RESTful API:

```bash
pip install weeb-cli[serve-restful]
```

## Użycie

### Podstawowe użycie

Uruchom serwer z domyślnymi ustawieniami:

```bash
weeb-cli serve restful
```

Serwer uruchomi się na `http://0.0.0.0:8080` ze wszystkimi dostępnymi dostawcami.

### Niestandardowa konfiguracja

```bash
weeb-cli serve restful \
  --port 9000 \
  --host 127.0.0.1 \
  --no-cors \
  --debug
```

Wszyscy dostępni dostawcy są ładowani automatycznie. Wybierz, którego dostawcy użyć, za pomocą parametru zapytania `provider` w żądaniach API.

### Opcje polecenia

| Opcja | Zmienna środowiskowa | Domyślna | Opis |
|-------|---------------------|----------|------|
| `--port` | `RESTFUL_PORT` | `8080` | Port HTTP do powiązania |
| `--host` | `RESTFUL_HOST` | `0.0.0.0` | Adres hosta do powiązania |
| `--cors/--no-cors` | `RESTFUL_CORS` | `true` | Włącz/wyłącz CORS |
| `--debug` | `RESTFUL_DEBUG` | `false` | Włącz tryb debugowania |

**Uwaga:** Wszyscy dostępni dostawcy są ładowani automatycznie. Użyj parametru zapytania `provider` w żądaniach API, aby wybrać, którego dostawcy użyć.

## Punkty końcowe API

### Sprawdzenie stanu

Sprawdź, czy serwer działa:

```http
GET /health
```

**Odpowiedź:**
```json
{
  "status": "ok",
  "service": "weeb-cli-restful",
  "providers": ["animecix", "hianime", "aniworld", "docchi"]
}
```

### Lista dostawców

Pobierz wszystkich dostępnych dostawców:

```http
GET /api/providers
```

**Odpowiedź:**
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

### Wyszukaj anime

Wyszukaj anime u dostawców:

```http
GET /api/search?q=naruto&provider=animecix
```

**Parametry zapytania:**
- `q` (wymagane): Zapytanie wyszukiwania
- `provider` (opcjonalne): Nazwa dostawcy (domyślnie pierwszy załadowany)

**Odpowiedź:**
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

### Pobierz szczegóły anime

Pobierz szczegółowe informacje o anime:

```http
GET /api/anime/{anime_id}?provider=animecix
```

**Parametry zapytania:**
- `provider` (opcjonalne): Nazwa dostawcy (domyślnie pierwszy załadowany)

**Odpowiedź:**
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
    "description": "Opis anime...",
    "genres": ["Akcja", "Przygoda"],
    "status": "completed",
    "episodes": [...]
  }
}
```

### Pobierz odcinki

Wyświetl wszystkie odcinki anime:

```http
GET /api/anime/{anime_id}/episodes?provider=animecix&season=1
```

**Parametry zapytania:**
- `provider` (opcjonalne): Nazwa dostawcy (domyślnie pierwszy załadowany)
- `season` (opcjonalne): Filtruj według numeru sezonu

**Odpowiedź:**
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

### Pobierz strumienie

Pobierz adresy URL strumieni dla odcinka:

```http
GET /api/anime/{anime_id}/episodes/{episode_id}/streams?provider=animecix&sort=desc
```

**Parametry zapytania:**
- `provider` (opcjonalne): Nazwa dostawcy (domyślnie pierwszy załadowany)
- `sort` (opcjonalne): Sortuj według jakości (`asc` lub `desc`, domyślnie `desc`)

**Odpowiedź:**
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

## Wdrożenie Docker

### Używając Docker Compose

```bash
docker-compose -f docs/docker-compose.restful.yml up -d
```

### Używając Inline Dockerfile

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir weeb-cli[serve-restful]
EXPOSE 8080
CMD ["weeb-cli", "serve", "restful"]
```

Uruchom kontener:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 8080:8080 \
  -e RESTFUL_PORT=8080 \
  -e RESTFUL_HOST=0.0.0.0 \
  -e RESTFUL_CORS=true \
  weeb-cli-restful
```

### Zmienne środowiskowe

Skonfiguruj serwer za pomocą zmiennych środowiskowych:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 9000:9000 \
  -e RESTFUL_PORT=9000 \
  -e RESTFUL_HOST=0.0.0.0 \
  -e RESTFUL_CORS=true \
  -e RESTFUL_DEBUG=false \
  weeb-cli-restful
```

## Obsługa błędów

Wszystkie punkty końcowe zwracają spójne odpowiedzi błędów:

```json
{
  "success": false,
  "error": "Opis komunikatu o błędzie"
}
```

**Typowe kody stanu HTTP:**
- `200`: Sukces
- `400`: Złe żądanie (brakujące/nieprawidłowe parametry)
- `404`: Zasób nie znaleziony
- `500`: Wewnętrzny błąd serwera

## Obsługa CORS

CORS jest domyślnie włączony, zezwalając na żądania z dowolnego źródła. Aby wyłączyć:

```bash
weeb-cli serve restful --no-cors
```

Lub za pomocą zmiennej środowiskowej:

```bash
export RESTFUL_CORS=false
```

## Przykładowe użycie

### cURL

```bash
# Wyszukaj anime
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"

# Pobierz odcinki
curl "http://localhost:8080/api/anime/12345/episodes?season=1"

# Pobierz strumienie
curl "http://localhost:8080/api/anime/12345/episodes/ep-1/streams?sort=desc"
```

### Python

```python
import requests

# Wyszukaj anime
response = requests.get(
    "http://localhost:8080/api/search",
    params={"q": "naruto", "provider": "animecix"}
)
results = response.json()

# Pobierz strumienie
response = requests.get(
    f"http://localhost:8080/api/anime/{anime_id}/episodes/{episode_id}/streams",
    params={"provider": "animecix", "sort": "desc"}
)
streams = response.json()
```

### JavaScript

```javascript
// Wyszukaj anime
const response = await fetch(
  'http://localhost:8080/api/search?q=naruto&provider=animecix'
);
const data = await response.json();

// Pobierz strumienie
const streamResponse = await fetch(
  `http://localhost:8080/api/anime/${animeId}/episodes/${episodeId}/streams?sort=desc`
);
const streams = await streamResponse.json();
```

## Wdrożenie produkcyjne

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

### Usługa Systemd

Utwórz `/etc/systemd/system/weeb-cli-restful.service`:

```ini
[Unit]
Description=Weeb CLI RESTful API
After=network.target

[Service]
Type=simple
User=weeb
WorkingDirectory=/opt/weeb-cli
Environment="RESTFUL_PORT=8080"
ExecStart=/usr/local/bin/weeb-cli serve restful
Restart=always

[Install]
WantedBy=multi-user.target
```

Włącz i uruchom:

```bash
sudo systemctl enable weeb-cli-restful
sudo systemctl start weeb-cli-restful
```

## Kwestie bezpieczeństwa

1. **Uwierzytelnianie**: API nie zawiera wbudowanego uwierzytelniania. Użyj reverse proxy (Nginx, Traefik) z uwierzytelnianiem, jeśli udostępniasz publicznie.

2. **Ograniczanie szybkości**: Zaimplementuj ograniczanie szybkości na poziomie reverse proxy, aby zapobiec nadużyciom.

3. **HTTPS**: Zawsze używaj HTTPS w produkcji. Skonfiguruj SSL/TLS na poziomie reverse proxy.

4. **Firewall**: Ogranicz dostęp do zaufanych adresów IP, jeśli to możliwe.

## Rozwiązywanie problemów

### Port już w użyciu

```bash
# Sprawdź, co używa portu
lsof -i :8080

# Użyj innego portu
weeb-cli serve restful --port 9000
```

### Dostawca nie znaleziony

Upewnij się, że nazwa dostawcy jest poprawna i dostępna:

```bash
# Wyświetl dostępnych dostawców
weeb-cli api providers

# Użyj poprawnej nazwy dostawcy w żądaniu API
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"
```

### Problemy z CORS

Jeśli występują problemy z CORS, upewnij się, że CORS jest włączony:

```bash
weeb-cli serve restful --cors
```

## Zobacz także

- [Tryb serwera Torznab](serve-mode.pl.md)
- [Polecenia API](api-mode.pl.md)
- [Dostępni dostawcy](../api/providers/registry.pl.md)
