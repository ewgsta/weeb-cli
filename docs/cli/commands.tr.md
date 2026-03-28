# CLI Komutları Referansı

Tüm Weeb CLI komut satırı komutları için eksiksiz referans.

## Ana Komutlar

### Varsayılan (Etkileşimli Mod)

Ana menü ile etkileşimli modu başlatın.

```bash
weeb-cli
```

Alt komut sağlanmadığında bu varsayılan komuttur.

### start

Etkileşimli mod için alternatif komut (varsayılan ile aynı).

```bash
weeb-cli start
```

### api

Betikler ve otomasyon için etkileşimsiz JSON API.

```bash
weeb-cli api [ALTKOMUT]
```

Detaylar için [API Modu](api-mode.md)'na bakın.

### serve

*arr entegrasyonu için Torznab sunucusunu başlatın.

```bash
weeb-cli serve [SEÇENEKLER]
```

Detaylar için [Serve Modu](serve-mode.md)'na bakın.

## API Alt Komutları

### api providers

Tüm mevcut sağlayıcıları listeleyin.

```bash
weeb-cli api providers
```

Çıktı:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  }
]
```

### api search

Anime arayın.

```bash
weeb-cli api search SORGU [SEÇENEKLER]
```

Seçenekler:
- `--provider, -p`: Sağlayıcı adı (varsayılan: animecix)

Örnek:
```bash
weeb-cli api search "One Piece" --provider hianime
```

Çıktı:
```json
[
  {
    "id": "one-piece-100",
    "title": "One Piece",
    "type": "series",
    "cover": "https://...",
    "year": 1999
  }
]
```

### api episodes

Anime için bölüm listesini alın.

```bash
weeb-cli api episodes ANIME_ID [SEÇENEKLER]
```

Seçenekler:
- `--provider, -p`: Sağlayıcı adı (varsayılan: animecix)
- `--season, -s`: Sezon numarasına göre filtrele

Örnek:
```bash
weeb-cli api episodes "one-piece-100" --provider hianime --season 1
```

Çıktı:
```json
[
  {
    "id": "ep-1",
    "number": 1,
    "title": "I'm Luffy! The Man Who Will Become Pirate King!",
    "season": 1
  }
]
```

### api streams

Bölüm için yayın URL'lerini alın.

```bash
weeb-cli api streams ANIME_ID EPISODE_ID [SEÇENEKLER]
```

Seçenekler:
- `--provider, -p`: Sağlayıcı adı (varsayılan: animecix)

Örnek:
```bash
weeb-cli api streams "one-piece-100" "ep-1" --provider hianime
```

Çıktı:
```json
[
  {
    "url": "https://...",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {}
  }
]
```

## Global Seçenekler

### --help

Yardım mesajını göster.

```bash
weeb-cli --help
weeb-cli api --help
weeb-cli api search --help
```

### --version

Sürüm bilgisini göster.

```bash
weeb-cli --version
```

## Ortam Değişkenleri

### WEEB_CLI_CONFIG_DIR

Yapılandırma dizinini geçersiz kıl:

```bash
export WEEB_CLI_CONFIG_DIR="/özel/yol"
weeb-cli
```

### WEEB_CLI_DEBUG

Hata ayıklama modunu etkinleştir:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

## Çıkış Kodları

- 0: Başarılı
- 1: Genel hata
- 2: Geçersiz argümanlar
- 130: Kesintiye uğradı (Ctrl+C)

## Örnekler

### Arama ve Yayın

```bash
# Arama
weeb-cli api search "Naruto" --provider animecix > sonuclar.json

# Sonuçlardan anime ID'sini al
ANIME_ID=$(jq -r '.[0].id' sonuclar.json)

# Bölümleri al
weeb-cli api episodes "$ANIME_ID" --provider animecix > bolumler.json

# Bölüm ID'sini al
EPISODE_ID=$(jq -r '.[0].id' bolumler.json)

# Yayınları al
weeb-cli api streams "$ANIME_ID" "$EPISODE_ID" --provider animecix > yayinlar.json

# mpv ile oynat
STREAM_URL=$(jq -r '.[0].url' yayinlar.json)
mpv "$STREAM_URL"
```

### Toplu İşleme

```bash
#!/bin/bash
# Bir animenin tüm bölümlerini indir

ANIME_ID="one-piece-100"
PROVIDER="hianime"

# Bölümleri al
episodes=$(weeb-cli api episodes "$ANIME_ID" --provider "$PROVIDER")

# Bölümler arasında döngü
echo "$episodes" | jq -c '.[]' | while read episode; do
    ep_id=$(echo "$episode" | jq -r '.id')
    ep_num=$(echo "$episode" | jq -r '.number')
    
    echo "$ep_num. bölüm işleniyor..."
    
    # Yayınları al
    streams=$(weeb-cli api streams "$ANIME_ID" "$ep_id" --provider "$PROVIDER")
    stream_url=$(echo "$streams" | jq -r '.[0].url')
    
    # yt-dlp ile indir
    yt-dlp -o "Bolum-$ep_num.mp4" "$stream_url"
done
```

## Kabuk Tamamlama

### Bash

```bash
eval "$(_WEEB_CLI_COMPLETE=bash_source weeb-cli)"
```

### Zsh

```bash
eval "$(_WEEB_CLI_COMPLETE=zsh_source weeb-cli)"
```

### Fish

```bash
eval (env _WEEB_CLI_COMPLETE=fish_source weeb-cli)
```

## Sonraki Adımlar

- [API Modu Rehberi](api-mode.md): Detaylı API kullanımı
- [Serve Modu Rehberi](serve-mode.md): Torznab sunucusu
- [Kullanıcı Rehberi](../user-guide/searching.md): Etkileşimli mod
