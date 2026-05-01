# Python SDK

Python uygulamalarına Weeb CLI işlevselliğini doğrudan entegre etmek için programatik API.

## Genel Bakış

Weeb CLI SDK, tüm anime akış ve indirme işlevselliği için yerel bir Python arayüzü sağlar. Süreç oluşturma ve JSON ayrıştırma gerektiren CLI API modunun aksine, SDK şunları sunar:

- **Doğrudan Python API** - Subprocess yükü yok
- **Tip Güvenliği** - IDE desteği için tam tip ipuçları
- **Thread Güvenli** - Eşzamanlı işlemler için güvenli
- **Headless Mod** - Veritabanı veya TUI bağımlılığı yok
- **Aynı Özellikler** - Tüm CLI işlevselliği mevcut

## Kurulum

SDK, weeb-cli ile birlikte gelir:

```bash
pip install weeb-cli
```

## Hızlı Başlangıç

```python
from weeb_cli import WeebSDK

# SDK'yı başlat
sdk = WeebSDK(default_provider="hianime")

# Anime ara
results = sdk.search("One Piece")
print(f"{len(results)} sonuç bulundu")

# İlk sonucu al
anime = results[0]
print(f"{anime.title} ({anime.year})")

# Bölümleri al
episodes = sdk.get_episodes(anime.id, season=1)
print(f"Sezon 1'de {len(episodes)} bölüm var")

# Stream URL'lerini al
streams = sdk.get_streams(
    anime_id=anime.id,
    episode_id=episodes[0].id
)
print(f"{len(streams)} kalitede mevcut")

# Bölüm indir
path = sdk.download_episode(
    anime_id=anime.id,
    season=1,
    episode=1,
    output_dir="./indirilenler"
)
print(f"İndirildi: {path}")
```

## API Referansı

### WeebSDK Sınıfı

Tüm işlemler için ana SDK arayüzü.

#### Constructor

```python
WeebSDK(headless: bool = True, default_provider: Optional[str] = None)
```

**Parametreler:**
- `headless` (bool): Headless modda çalıştır (veritabanı/TUI yok). Varsayılan: `True`
- `default_provider` (str, optional): Kullanılacak varsayılan sağlayıcı. Varsayılan: `"animecix"`

**Örnek:**
```python
# Varsayılan sağlayıcı ile headless
sdk = WeebSDK()

# Özel varsayılan sağlayıcı
sdk = WeebSDK(default_provider="hianime")

# Veritabanı erişimi ile (izleme geçmişi vb. için)
sdk = WeebSDK(headless=False)
```

#### list_providers()

Tüm mevcut anime sağlayıcılarını listele.

```python
def list_providers() -> List[Dict[str, Any]]
```

**Döndürür:** Sağlayıcı meta veri sözlüklerinin listesi:
- `name` (str): Sağlayıcı tanımlayıcısı
- `lang` (str): Dil kodu (en, tr, de, pl)
- `region` (str): Bölge kodu (US, TR, DE, PL)
- `class` (str): Sağlayıcı sınıf adı
- `disabled` (bool): Sağlayıcının devre dışı olup olmadığı

**Örnek:**
```python
providers = sdk.list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']} ({p['region']})")
```

#### search()

Sorgu dizesiyle anime ara.

```python
def search(
    query: str, 
    provider: Optional[str] = None
) -> List[AnimeResult]
```

**Parametreler:**
- `query` (str): Arama sorgusu (anime başlığı veya anahtar kelimeler)
- `provider` (str, optional): Kullanılacak sağlayıcı. Belirtilmezse `default_provider` kullanılır

**Döndürür:** `AnimeResult` nesnelerinin listesi:
- `id` (str): Benzersiz anime tanımlayıcısı
- `title` (str): Anime başlığı
- `type` (str): İçerik türü (series, movie, ova)
- `cover` (str, optional): Kapak resmi URL'si
- `year` (int, optional): Yayın yılı

**Hata Fırlatır:**
- `ProviderError`: Sağlayıcı bulunamazsa veya arama başarısız olursa

**Örnek:**
```python
results = sdk.search("Naruto", provider="hianime")
for anime in results:
    print(f"{anime.title} - {anime.type} ({anime.year})")
```

#### get_episodes()

Bir anime için mevcut bölümlerin listesini al.

```python
def get_episodes(
    anime_id: str, 
    season: Optional[int] = None,
    provider: Optional[str] = None
) -> List[Episode]
```

**Parametreler:**
- `anime_id` (str): Benzersiz anime tanımlayıcısı
- `season` (int, optional): Sezon numarasına göre filtrele
- `provider` (str, optional): Kullanılacak sağlayıcı

**Döndürür:** `Episode` nesnelerinin listesi:
- `id` (str): Bölüm tanımlayıcısı
- `number` (int): Bölüm numarası
- `title` (str, optional): Bölüm başlığı
- `season` (int): Sezon numarası
- `url` (str, optional): Bölüm sayfası URL'si

**Örnek:**
```python
# Tüm bölümleri al
episodes = sdk.get_episodes("anime-id", provider="hianime")

# Sadece 2. sezonu al
season2 = sdk.get_episodes("anime-id", season=2, provider="hianime")

for ep in season2:
    print(f"S{ep.season:02d}E{ep.number:02d}: {ep.title}")
```

#### download_episode()

Bir bölümü yerel depolamaya indir.

```python
def download_episode(
    anime_id: str,
    season: int,
    episode: int,
    provider: Optional[str] = None,
    output_dir: str = ".",
    anime_title: Optional[str] = None
) -> Optional[str]
```

**Parametreler:**
- `anime_id` (str): Benzersiz anime tanımlayıcısı
- `season` (int): Sezon numarası
- `episode` (int): Bölüm numarası
- `provider` (str, optional): Kullanılacak sağlayıcı
- `output_dir` (str): Dosyayı kaydetmek için dizin. Varsayılan: mevcut dizin
- `anime_title` (str, optional): Dosya adı için özel başlık. Sağlanmazsa otomatik alınır

**Döndürür:** İndirilen dosyanın yolu veya başarısız olursa `None`

**Örnek:**
```python
# Temel indirme
path = sdk.download_episode(
    anime_id="anime-id",
    season=1,
    episode=1,
    provider="hianime"
)

# Özel çıktı dizini ve başlık
path = sdk.download_episode(
    anime_id="anime-id",
    season=2,
    episode=5,
    provider="hianime",
    output_dir="/media/anime",
    anime_title="Favori Animem"
)
print(f"İndirildi: {path}")
```

## Gelişmiş Kullanım

### Çoklu Sağlayıcı Arama

Birden fazla sağlayıcıda ara ve sonuçları birleştir:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK()
query = "One Piece"

# Birden fazla sağlayıcıda ara
providers = ["hianime", "animecix", "aniworld"]
all_results = []

for provider in providers:
    try:
        results = sdk.search(query, provider=provider)
        all_results.extend(results)
        print(f"{provider}: {len(results)} sonuç")
    except Exception as e:
        print(f"{provider} başarısız: {e}")

print(f"Toplam: {len(all_results)} sonuç")
```

### Toplu İndirme

Birden fazla bölümü indir:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK(default_provider="hianime")

# Ara ve anime al
results = sdk.search("Naruto")
anime_id = results[0].id

# 1. sezonu indir
for episode_num in range(1, 26):
    try:
        path = sdk.download_episode(
            anime_id=anime_id,
            season=1,
            episode=episode_num,
            output_dir="./naruto_s1"
        )
        print(f"✓ Bölüm {episode_num}: {path}")
    except Exception as e:
        print(f"✗ Bölüm {episode_num}: {e}")
```

### Eşzamanlı İndirmeler

Paralel indirmeler için threading kullan:

```python
from weeb_cli import WeebSDK
from concurrent.futures import ThreadPoolExecutor, as_completed

sdk = WeebSDK(default_provider="hianime")

def download_ep(anime_id, season, episode):
    return sdk.download_episode(
        anime_id=anime_id,
        season=season,
        episode=episode,
        output_dir="./indirilenler"
    )

# 1-10 arası bölümleri eşzamanlı indir
anime_id = "anime-id"
episodes = range(1, 11)

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(download_ep, anime_id, 1, ep): ep 
        for ep in episodes
    }
    
    for future in as_completed(futures):
        ep = futures[future]
        try:
            path = future.result()
            print(f"✓ Bölüm {ep}: {path}")
        except Exception as e:
            print(f"✗ Bölüm {ep}: {e}")
```

## Entegrasyon Örnekleri

### Flask Web API

```python
from flask import Flask, jsonify, request
from weeb_cli import WeebSDK

app = Flask(__name__)
sdk = WeebSDK()

@app.route('/api/search')
def search():
    query = request.args.get('q')
    provider = request.args.get('provider', 'hianime')
    
    results = sdk.search(query, provider=provider)
    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'year': r.year,
            'cover': r.cover
        }
        for r in results
    ])

if __name__ == '__main__':
    app.run(port=5000)
```

### Discord Bot

```python
import discord
from discord.ext import commands
from weeb_cli import WeebSDK

bot = commands.Bot(command_prefix='!')
sdk = WeebSDK(default_provider="hianime")

@bot.command()
async def anime(ctx, *, query):
    """Anime ara"""
    results = sdk.search(query)
    
    if not results:
        await ctx.send("Sonuç bulunamadı")
        return
    
    anime = results[0]
    embed = discord.Embed(
        title=anime.title,
        description=f"Yıl: {anime.year}"
    )
    if anime.cover:
        embed.set_thumbnail(url=anime.cover)
    
    await ctx.send(embed=embed)

bot.run('TOKEN')
```

## En İyi Uygulamalar

1. **SDK Instance'ını Yeniden Kullan**: Bir SDK instance'ı oluştur ve yeniden kullan
2. **Hataları Yönet**: SDK çağrılarını her zaman try-except bloklarına sar
3. **Sağlayıcı Seçimi**: Kullanıcıların sağlayıcı seçmesine izin ver veya dile uygun varsayılanları kullan
4. **Eşzamanlı İşlemler**: Toplu işlemler için threading kullan
5. **Önbellekleme**: SDK, CLI ile aynı önbelleği kullanır - sonuçlar otomatik olarak önbelleğe alınır
6. **Headless Mod**: Durumsuz uygulamalar için headless=True'yu koru

## Sınırlamalar

- **İzleme Geçmişi Yok**: Headless mod izleme ilerlemesini takip etmez
- **Tracker Senkronizasyonu Yok**: AniList/MAL senkronizasyonu headless olmayan mod gerektirir
- **Bildirim Yok**: Sistem bildirimleri headless modda mevcut değil
- **Discord RPC Yok**: Discord entegrasyonu headless olmayan mod gerektirir

Bu özellikler için SDK'yı `headless=False` ile başlatın ve veritabanının erişilebilir olduğundan emin olun.

## Sonraki Adımlar

- [API Modu Dokümantasyonu](../cli/api-mode.tr.md): CLI JSON API
- [Sağlayıcı Geliştirme](../development/adding-providers.tr.md): Özel sağlayıcılar oluştur
- [Mimari](../development/architecture.tr.md): Sistem tasarımına genel bakış
