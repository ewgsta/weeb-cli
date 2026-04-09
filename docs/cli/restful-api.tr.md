# RESTful API Modu

Weeb CLI, arama, bölüm listeleme, stream çıkarma ve anime detayları dahil tüm provider işlemleri için HTTP endpoint'leri sağlayan bir RESTful API sunucusu olarak çalıştırılabilir.

## Kurulum

RESTful API bağımlılıklarıyla birlikte kurun:

```bash
pip install weeb-cli[serve-restful]
```

## Kullanım

### Temel Kullanım

Sunucuyu varsayılan ayarlarla başlatın:

```bash
weeb-cli serve restful
```

Sunucu `http://0.0.0.0:8080` adresinde başlayacak ve tüm mevcut provider'ları otomatik olarak yükleyecektir.

### Özel Yapılandırma

```bash
weeb-cli serve restful \
  --port 9000 \
  --host 127.0.0.1 \
  --no-cors \
  --debug
```

Tüm mevcut provider'lar otomatik olarak yüklenir. API isteklerinde `provider` sorgu parametresi ile hangi provider'ı kullanacağınızı seçin.

### Komut Seçenekleri

| Seçenek | Ortam Değişkeni | Varsayılan | Açıklama |
|---------|----------------|-----------|----------|
| `--port` | `RESTFUL_PORT` | `8080` | Bağlanılacak HTTP portu |
| `--host` | `RESTFUL_HOST` | `0.0.0.0` | Bağlanılacak host adresi |
| `--cors/--no-cors` | `RESTFUL_CORS` | `true` | CORS'u etkinleştir/devre dışı bırak |
| `--debug` | `RESTFUL_DEBUG` | `false` | Debug modunu etkinleştir |

**Not:** Tüm mevcut provider'lar otomatik olarak yüklenir. API isteklerinde `provider` sorgu parametresi ile hangi provider'ı kullanacağınızı seçin.

## API Endpoint'leri

### Sağlık Kontrolü

Sunucunun çalışıp çalışmadığını kontrol edin:

```http
GET /health
```

**Yanıt:**
```json
{
  "status": "ok",
  "service": "weeb-cli-restful",
  "providers": ["animecix", "hianime", "aniworld", "docchi"]
}
```

### Provider'ları Listele

Tüm mevcut provider'ları alın:

```http
GET /api/providers
```

**Yanıt:**
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

### Anime Ara

Provider'lar arasında anime arayın:

```http
GET /api/search?q=naruto&provider=animecix
```

**Sorgu Parametreleri:**
- `q` (zorunlu): Arama sorgusu
- `provider` (opsiyonel): Provider adı (varsayılan olarak ilk yüklenen)

**Yanıt:**
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

### Anime Detaylarını Al

Bir anime hakkında detaylı bilgi alın:

```http
GET /api/anime/{anime_id}?provider=animecix
```

**Sorgu Parametreleri:**
- `provider` (opsiyonel): Provider adı (varsayılan olarak ilk yüklenen)

**Yanıt:**
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
    "description": "Anime açıklaması...",
    "genres": ["Aksiyon", "Macera"],
    "status": "completed",
    "episodes": [...]
  }
}
```

### Bölümleri Al

Bir anime için tüm bölümleri listeleyin:

```http
GET /api/anime/{anime_id}/episodes?provider=animecix&season=1
```

**Sorgu Parametreleri:**
- `provider` (opsiyonel): Provider adı (varsayılan olarak ilk yüklenen)
- `season` (opsiyonel): Sezon numarasına göre filtrele

**Yanıt:**
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
      "title": "Giriş: Naruto Uzumaki!",
      "season": 1,
      "url": "https://example.com/episode/1"
    }
  ]
}
```

### Stream'leri Al

Bir bölüm için stream URL'lerini alın:

```http
GET /api/anime/{anime_id}/episodes/{episode_id}/streams?provider=animecix&sort=desc
```

**Sorgu Parametreleri:**
- `provider` (opsiyonel): Provider adı (varsayılan olarak ilk yüklenen)
- `sort` (opsiyonel): Kaliteye göre sırala (`asc` veya `desc`, varsayılan `desc`)

**Yanıt:**
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

## Docker Dağıtımı

### Docker Compose Kullanarak

```bash
docker-compose -f docs/docker-compose.restful.yml up -d
```

### Inline Dockerfile Kullanarak

```dockerfile
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir weeb-cli[serve-restful]
EXPOSE 8080
CMD ["weeb-cli", "serve", "restful"]
```

Container'ı çalıştırın:

```bash
docker run -d \
  --name weeb-cli-restful \
  -p 8080:8080 \
  -e RESTFUL_PORT=8080 \
  -e RESTFUL_HOST=0.0.0.0 \
  -e RESTFUL_CORS=true \
  weeb-cli-restful
```

### Ortam Değişkenleri

Sunucuyu ortam değişkenleri ile yapılandırın:

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

## Hata Yönetimi

Tüm endpoint'ler tutarlı hata yanıtları döndürür:

```json
{
  "success": false,
  "error": "Hata mesajı açıklaması"
}
```

**Yaygın HTTP Durum Kodları:**
- `200`: Başarılı
- `400`: Hatalı istek (eksik/geçersiz parametreler)
- `404`: Kaynak bulunamadı
- `500`: Sunucu hatası

## CORS Desteği

CORS varsayılan olarak etkindir ve herhangi bir origin'den gelen isteklere izin verir. Devre dışı bırakmak için:

```bash
weeb-cli serve restful --no-cors
```

Veya ortam değişkeni ile:

```bash
export RESTFUL_CORS=false
```

## Örnek Kullanım

### cURL

```bash
# Anime ara
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"

# Bölümleri al
curl "http://localhost:8080/api/anime/12345/episodes?season=1"

# Stream'leri al
curl "http://localhost:8080/api/anime/12345/episodes/ep-1/streams?sort=desc"
```

### Python

```python
import requests

# Anime ara
response = requests.get(
    "http://localhost:8080/api/search",
    params={"q": "naruto", "provider": "animecix"}
)
results = response.json()

# Stream'leri al
response = requests.get(
    f"http://localhost:8080/api/anime/{anime_id}/episodes/{episode_id}/streams",
    params={"provider": "animecix", "sort": "desc"}
)
streams = response.json()
```

### JavaScript

```javascript
// Anime ara
const response = await fetch(
  'http://localhost:8080/api/search?q=naruto&provider=animecix'
);
const data = await response.json();

// Stream'leri al
const streamResponse = await fetch(
  `http://localhost:8080/api/anime/${animeId}/episodes/${episodeId}/streams?sort=desc`
);
const streams = await streamResponse.json();
```

## Üretim Dağıtımı

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

### Systemd Servisi

`/etc/systemd/system/weeb-cli-restful.service` oluşturun:

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

Etkinleştir ve başlat:

```bash
sudo systemctl enable weeb-cli-restful
sudo systemctl start weeb-cli-restful
```

## Güvenlik Hususları

1. **Kimlik Doğrulama**: API yerleşik kimlik doğrulama içermez. Herkese açık olarak sunuluyorsa, kimlik doğrulama ile bir reverse proxy (Nginx, Traefik) kullanın.

2. **Hız Sınırlama**: Kötüye kullanımı önlemek için reverse proxy seviyesinde hız sınırlama uygulayın.

3. **HTTPS**: Üretimde her zaman HTTPS kullanın. SSL/TLS'yi reverse proxy seviyesinde yapılandırın.

4. **Güvenlik Duvarı**: Mümkünse erişimi güvenilir IP'lerle sınırlayın.

## Sorun Giderme

### Port Zaten Kullanımda

```bash
# Portu kullanan uygulamayı kontrol et
lsof -i :8080

# Farklı bir port kullan
weeb-cli serve restful --port 9000
```

### Provider Bulunamadı

Provider adının doğru ve mevcut olduğundan emin olun:

```bash
# Mevcut provider'ları listele
weeb-cli api providers

# API isteğinde doğru provider adını kullan
curl "http://localhost:8080/api/search?q=naruto&provider=animecix"
```

### CORS Sorunları

CORS sorunları yaşıyorsanız, CORS'un etkin olduğundan emin olun:

```bash
weeb-cli serve restful --cors
```

## Ayrıca Bakınız

- [Torznab Sunucu Modu](serve-mode.tr.md)
- [API Komutları](api-mode.tr.md)
- [Mevcut Provider'lar](../api/providers/registry.tr.md)
