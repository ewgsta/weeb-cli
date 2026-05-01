# API Modu

Betikler, otomasyon ve diğer araçlarla entegrasyon için etkileşimsiz JSON API.

## Genel Bakış

API modu tüm işlemler için JSON çıktısı sağlar, bu sayede kolayca:
- Betiklerle entegre olun
- İş akışlarını otomatikleştirin
- Özel arayüzler oluşturun
- Diğer araçlarla bağlantı kurun

**Tüm API komutları sağlayıcı seçimini destekler** `--provider` (veya `-p`) seçeneği ile. Bu, her işlem için hangi anime kaynağını kullanacağınızı seçmenize olanak tanır.

## Sağlayıcı Seçimi

### Mevcut Sağlayıcılar

Tüm mevcut sağlayıcıları görmek için `providers` komutunu kullanın:

```bash
weeb-cli api providers
```

Yanıt:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider",
    "disabled": false
  },
  {
    "name": "hianime",
    "lang": "en",
    "region": "US",
    "class": "HiAnimeProvider",
    "disabled": false
  },
  {
    "name": "aniworld",
    "lang": "de",
    "region": "DE",
    "class": "AniWorldProvider",
    "disabled": false
  },
  {
    "name": "docchi",
    "lang": "pl",
    "region": "PL",
    "class": "DocchiProvider",
    "disabled": false
  }
]
```

### Sağlayıcı Kategorileri

**Türkçe Sağlayıcılar:**
- `animecix` - Varsayılan Türkçe sağlayıcı
- `turkanime` - Alternatif Türkçe kaynak
- `anizle` - Türkçe anime akışı
- `weeb` - Türkçe anime kaynağı

**İngilizce Sağlayıcılar:**
- `hianime` - Yüksek kaliteli İngilizce anime
- `allanime` - Kapsamlı İngilizce kaynak

**Almanca Sağlayıcılar:**
- `aniworld` - Almanca anime akışı

**Lehçe Sağlayıcılar:**
- `docchi` - Lehçe anime kaynağı

### Sağlayıcıları Kullanma

Tüm komutlar `--provider` veya `-p` seçeneğini kabul eder:

```bash
# Belirli bir sağlayıcı ile ara
weeb-cli api search "Naruto" --provider hianime

# Türkçe kaynaktan bölümleri al
weeb-cli api episodes "anime-id" --provider turkanime

# Almanca sağlayıcıdan indir
weeb-cli api download "anime-id" -s 1 -e 1 --provider aniworld
```

**Varsayılan Sağlayıcı:** `--provider` belirtilmezse, varsayılan olarak `animecix` kullanılır.

## Temel Kullanım

Tüm API komutları bu kalıbı takip eder:

```bash
weeb-cli api [KOMUT] [ARGÜMANLAR] [SEÇENEKLER]
```

Çıktı her zaman geçerli JSON'dur.

## Komutlar

### providers

Tüm mevcut sağlayıcıları meta verilerle listeleyin.

```bash
weeb-cli api providers
```

Yanıt:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  },
  {
    "name": "hianime",
    "lang": "en",
    "region": "US",
    "class": "HiAnimeProvider"
  }
]
```

### search

Sağlayıcılar arasında anime arayın.

```bash
weeb-cli api search "anime adı" --provider animecix
```

Yanıt:
```json
[
  {
    "id": "anime-slug",
    "title": "Anime Başlığı",
    "type": "series",
    "cover": "https://kapak-url.jpg",
    "year": 2024
  }
]
```

### episodes

Bir anime için bölüm listesini alın.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

İsteğe bağlı: Sezona göre filtrele
```bash
weeb-cli api episodes "anime-id" --season 2 --provider animecix
```

Yanıt:
```json
[
  {
    "id": "episode-id",
    "number": 1,
    "title": "Bölüm Başlığı",
    "season": 1,
    "url": "https://bolum-url"
  }
]
```

### streams

Bir bölüm için yayın URL'lerini alın.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

Yanıt:
```json
[
  {
    "url": "https://yayin-url.m3u8",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {
      "Referer": "https://..."
    },
    "subtitles": null
  }
]
```

## Hata İşleme

### Hata Yanıtı

Hatalar stderr'e JSON olarak döndürülür:

```json
{
  "error": "Sağlayıcı bulunamadı: geçersiz-sağlayıcı"
}
```

Hata durumunda çıkış kodu sıfır değildir.

### Hataları Kontrol Etme

```bash
if weeb-cli api search "anime" --provider geçersiz 2>/dev/null; then
    echo "Başarılı"
else
    echo "Başarısız"
fi
```

## Entegrasyon Örnekleri

### Python Betiği

```python
import subprocess
import json

def search_anime(query, provider="animecix"):
    result = subprocess.run(
        ["weeb-cli", "api", "search", query, "--provider", provider],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        error = json.loads(result.stderr)
        raise Exception(error["error"])

# Kullanım
results = search_anime("One Piece", "hianime")
for anime in results:
    print(f"{anime['title']} ({anime['year']})")
```

### Bash Betiği

```bash
#!/bin/bash

PROVIDER="animecix"
QUERY="Naruto"

# Arama
results=$(weeb-cli api search "$QUERY" --provider "$PROVIDER")

# jq ile ayrıştır
echo "$results" | jq -r '.[] | "\(.title) - \(.year)"'

# İlk sonucun ID'sini al
anime_id=$(echo "$results" | jq -r '.[0].id')

# Bölümleri al
episodes=$(weeb-cli api episodes "$anime_id" --provider "$PROVIDER")
echo "$episodes" | jq -r '.[] | "Bölüm \(.number): \(.title)"'
```

### Node.js Betiği

```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function searchAnime(query, provider = 'animecix') {
    const cmd = `weeb-cli api search "${query}" --provider ${provider}`;
    const { stdout } = await execPromise(cmd);
    return JSON.parse(stdout);
}

// Kullanım
searchAnime('One Piece', 'hianime')
    .then(results => {
        results.forEach(anime => {
            console.log(`${anime.title} (${anime.year})`);
        });
    })
    .catch(console.error);
```

## Gelişmiş Kullanım

### Sonuçları Yönlendirme

```bash
# jq ile arama ve filtreleme
weeb-cli api search "anime" --provider animecix | \
    jq '.[] | select(.year >= 2020)'

# Tüm bölümleri al ve say
weeb-cli api episodes "anime-id" --provider animecix | \
    jq 'length'

# En iyi kaliteli yayını al
weeb-cli api streams "anime-id" "ep-id" --provider animecix | \
    jq -r '.[0].url'
```

### Komutları Zincirleme

```bash
# Ara, ilk sonucu al, bölümleri al
ANIME_ID=$(weeb-cli api search "Naruto" --provider animecix | jq -r '.[0].id')
weeb-cli api episodes "$ANIME_ID" --provider animecix
```

### Hata İşleme

```bash
# Hataları yakala
if ! output=$(weeb-cli api search "anime" --provider geçersiz 2>&1); then
    echo "Hata oluştu: $output"
    exit 1
fi
```

## Performans

### Önbellekleme

API modu etkileşimli mod ile aynı önbelleği kullanır:
- Arama sonuçları 1 saat önbelleğe alınır
- Detaylar 6 saat önbelleğe alınır
- Yayınlar önbelleğe alınmaz

### Headless Modu

API modu headless modda çalışır:
- TUI bağımlılıkları yüklenmez
- Daha hızlı başlangıç
- Daha düşük bellek kullanımı

## Sınırlamalar

### Etkileşimli Özellikler Yok

API modu şunları desteklemez:
- Menüler ve istemler
- İlerleme çubukları
- Kullanıcı girişi
- Renkli çıktı

### Durum Yönetimi Yok

Her komut bağımsızdır:
- Oturum durumu yok
- İzleme geçmişi güncellemeleri yok
- İlerleme takibi yok

Bu özellikler için etkileşimli modu kullanın.

## En İyi Uygulamalar

1. Sağlayıcıyı her zaman açıkça belirtin
2. Hataları düzgün bir şekilde işleyin
3. JSON'u uygun araçlarla ayrıştırın (jq, Python json)
4. Mümkün olduğunda sonuçları önbelleğe alın
5. Uygun zaman aşımları kullanın

## Sonraki Adımlar

- [Komutlar Referansı](commands.md): Tüm CLI komutları
- [Serve Modu](serve-mode.md): Torznab sunucusu
- [Geliştirme](../development/contributing.md): API geliştirme
