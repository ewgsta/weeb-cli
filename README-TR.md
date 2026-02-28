<p align="center">
  <img src="weeb_landing/logo/512x512.webp" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>Tarayıcı yok, reklam yok, dikkat dağıtıcı unsur yok. Sadece siz ve eşsiz bir anime izleme deneyimi.</strong>
</p>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/ewgsta/weeb-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/ewgsta/weeb-cli/tests.yml?style=flat-square" alt="Tests"></a>
</p>

<p align="center">
  <a href="#kurulum">Kurulum</a> •
  <a href="#özellikler">Özellikler</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#kaynaklar">Kaynaklar</a> •
  <a href="README.md">English</a>
</p>

---

## Özellikler

### Çoklu Kaynak Desteği
- **Türkçe**: Animecix, Turkanime, Anizle
- **İngilizce**: HiAnime, AllAnime

### Akıllı İzleme
- MPV entegrasyonu ile yüksek kaliteli HLS/MP4 yayınları
- Kaldığınız yerden devam etme (dakika bazında)
- İzleme geçmişi ve istatistikler
- Tamamlanan (✓) ve devam eden (●) bölüm işaretleri

### Güçlü İndirme Sistemi
- **Aria2** ile çoklu bağlantılı hızlı indirme
- **yt-dlp** ile karmaşık yayın desteği
- Kuyruk sistemi ve eşzamanlı indirme
- Yarım kalan indirmeleri devam ettirme
- Akıllı dosya isimlendirme (`Anime Adı - S1B1.mp4`)

### Yerel Kütüphane
- İndirilen animeleri otomatik tarama
- Harici disk desteği (USB, HDD)
- Çevrimdışı anime indexleme
- Tüm kaynaklarda arama

### Ek Özellikler
- SQLite veritabanı (hızlı ve güvenilir)
- İndirme tamamlandığında sistem bildirimi
- Discord RPC entegrasyonu (izlediğiniz anime Discord'da görünsün)
- Arama geçmişi
- Debug modu ve loglama
- Otomatik güncelleme kontrolü
- Scriptler ve yapay zeka ajanları için etkileşimsiz JSON API
- Sonarr/*arr entegrasyonu için Torznab sunucu modu

---

## Kurulum

### PyPI (Evrensel)
```bash
pip install weeb-cli
```

### Arch Linux (AUR)
```bash
yay -S weeb-cli
```

### Portable
[Releases](https://github.com/ewgsta/weeb-cli/releases) sayfasından platformunuza uygun dosyayı indirin.

### Geliştirici Kurulumu
```bash
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli
pip install -e .
```

---

## Kullanım

```bash
weeb-cli
```

### API Modu (Etkileşimsiz)

Scriptler, otomasyon ve yapay zeka ajanları icin weeb-cli, veritabanı veya TUI gerektirmeden headless calisan JSON API komutları sunar:

```bash
# Mevcut sağlayıcıları listele
weeb-cli api providers

# Anime ara (ID'leri döndürür)
weeb-cli api search "Angel Beats"
# Döndürür: [{"id": "12345", "title": "Angel Beats!", ...}]

# Bölümleri listele (aramadan gelen ID ile)
weeb-cli api episodes 12345 --season 1

# Stream URL'lerini al
weeb-cli api streams 12345 --season 1 --episode 1

# Anime detaylarını al
weeb-cli api details 12345

# Bir bölüm indir
weeb-cli api download 12345 --season 1 --episode 1 --output ./downloads
```

Tüm API komutları stdout'a JSON çıktı verir.

### Sonarr/*arr Entegrasyonu (Serve Modu)

weeb-cli, Sonarr ve diğer *arr uygulamaları için Torznab uyumlu bir sunucu olarak çalışabilir:

```bash
pip install weeb-cli[serve]

weeb-cli serve --port 9876 \
  --watch-dir /downloads/watch \
  --completed-dir /downloads/completed \
  --sonarr-url http://sonarr:8989 \
  --sonarr-api-key ANAHTARINIZ \
  --providers animecix,anizle,turkanime
```

Ardından Sonarr'da `http://weeb-cli-host:9876` adresini 5070 (TV/Anime) kategorisiyle Torznab indexer olarak ekleyin. Sunucu, yakalanan bölümleri otomatik olarak işleyen bir blackhole indirme worker'ı içerir.

#### Docker

```dockerfile
FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends aria2 ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir weeb-cli[serve] yt-dlp
EXPOSE 9876
CMD ["weeb-cli", "serve", "--port", "9876", "--watch-dir", "/downloads/watch", "--completed-dir", "/downloads/completed"]
```

### Klavye Kontrolleri
| Tuş | İşlev |
|-----|-------|
| `↑` `↓` | Menüde gezinme |
| `Enter` | Seçim yapma |
| `s` | Anime Ara (Ana menüde) |
| `d` | İndirmeler (Ana menüde) |
| `w` | İzlediklerim (Ana menüde) |
| `c` | Ayarlar (Ana menüde) |
| `q` | Çıkış (Ana menüde) |
| `Ctrl+C` | Geri dön / Çıkış |

**Not:** Tüm kısayollar Ayarlar > Klavye Kısayolları menüsünden özelleştirilebilir.

---

## Kaynaklar

| Kaynak | Dil |
|--------|-----|
| Animecix | Türkçe |
| Turkanime | Türkçe |
| Anizle | Türkçe |
| HiAnime | İngilizce |
| AllAnime | İngilizce |

---

## Ayarlar

Yapılandırma: `~/.weeb-cli/weeb.db` (SQLite)

### Mevcut Ayarlar

| Ayar | Açıklama | Varsayılan | Tip |
|------|----------|------------|-----|
| `language` | Arayüz dili (tr/en) | `null` (ilk çalıştırmada sorar) | string |
| `scraping_source` | Aktif anime kaynağı | `animecix` | string |
| `aria2_enabled` | İndirmeler için Aria2 kullan | `true` | boolean |
| `aria2_max_connections` | İndirme başına max bağlantı | `16` | integer |
| `ytdlp_enabled` | HLS yayınlar için yt-dlp kullan | `true` | boolean |
| `ytdlp_format` | yt-dlp format string | `bestvideo+bestaudio/best` | string |
| `max_concurrent_downloads` | Eşzamanlı indirme sayısı | `3` | integer |
| `download_dir` | İndirme klasörü yolu | `./weeb-downloads` | string |
| `download_max_retries` | Başarısız indirmeleri yeniden dene | `3` | integer |
| `download_retry_delay` | Denemeler arası bekleme (saniye) | `10` | integer |
| `show_description` | Anime açıklamalarını göster | `true` | boolean |
| `discord_rpc_enabled` | Discord Rich Presence | `false` | boolean |
| `shortcuts_enabled` | Klavye kısayolları | `true` | boolean |
| `debug_mode` | Debug loglama | `false` | boolean |

### Tracker Ayarları (ayrı saklanır)
- `anilist_token` - AniList OAuth token
- `anilist_user_id` - AniList kullanıcı ID
- `mal_token` - MyAnimeList OAuth token
- `mal_refresh_token` - MAL yenileme token
- `mal_username` - MAL kullanıcı adı

### Harici Diskler
Ayarlar > Harici Diskler menüsünden yönetilir. Her disk şunları saklar:
- Yol (örn. `D:\Anime`)
- Özel isim/takma ad
- Eklenme zamanı

Tüm ayarlar interaktif Ayarlar menüsünden değiştirilebilir.

---

## Yol Haritası

### Tamamlanan
- [x] Çoklu kaynak desteği (TR/EN)
- [x] MPV ile izleme
- [x] İzleme geçmişi ve ilerleme takibi
- [x] Aria2/yt-dlp indirme entegrasyonu
- [x] Harici disk ve yerel kütüphane
- [x] SQLite veritabanı
- [x] Bildirim sistemi
- [x] Debug modu
- [x] MAL/AniList entegrasyonu
- [x] Veritabanı yedekleme/geri yükleme
- [x] Klavye kısayolları
- [x] Etkileşimsiz API modu (JSON çıktı)
- [x] Sonarr/*arr entegrasyonu için Torznab sunucu

## Gelecek Planlar

### v2.6.0 (Planlanan)
- [ ] Async/await refactoring
- [ ] Download strategy pattern
- [ ] Token şifreleme
- [ ] Progress bar iyileştirmesi
- [ ] Plugin sistemi

### v2.7.0 (Planlanan)
- [ ] Anime önerileri
- [ ] Toplu işlemler
- [ ] İzleme istatistikleri (grafik)
- [ ] Tema desteği
- [ ] Altyazı indirme

### v3.0.0 (Uzun Vadeli)
- [ ] Web UI (opsiyonel)
- [ ] Torrent desteği (nyaa.si)
- [ ] Watch party
- [ ] Mobile app entegrasyonu

---

## Proje Yapısı

```
weeb-cli/
├── weeb_cli/                    # Ana uygulama paketi
│   ├── commands/                # CLI komut yöneticileri
│   │   ├── api.py               # Etkileşimsiz JSON API komutları
│   │   ├── downloads.py         # İndirme yönetimi komutları
│   │   ├── search.py            # Anime arama fonksiyonları
│   │   ├── serve.py             # *arr entegrasyonu için Torznab sunucu
│   │   ├── settings.py          # Ayarlar menüsü ve yapılandırma
│   │   ├── setup.py             # İlk kurulum sihirbazı
│   │   └── watchlist.py         # İzleme geçmişi ve ilerleme
│   │
│   ├── providers/               # Anime kaynak entegrasyonları
│   │   ├── extractors/          # Video stream çıkarıcıları
│   │   │   └── megacloud.py     # Megacloud çıkarıcı
│   │   ├── allanime.py          # AllAnime sağlayıcı (EN)
│   │   ├── animecix.py          # Animecix sağlayıcı (TR)
│   │   ├── anizle.py            # Anizle sağlayıcı (TR)
│   │   ├── base.py              # Temel sağlayıcı arayüzü
│   │   ├── hianime.py           # HiAnime sağlayıcı (EN)
│   │   ├── registry.py          # Sağlayıcı kayıt sistemi
│   │   └── turkanime.py         # Turkanime sağlayıcı (TR)
│   │
│   ├── services/                # İş mantığı katmanı
│   │   ├── cache.py             # Dosya tabanlı önbellekleme
│   │   ├── database.py          # SQLite veritabanı yöneticisi
│   │   ├── dependency_manager.py # FFmpeg, MPV otomatik kurulum
│   │   ├── details.py           # Anime detay çekici
│   │   ├── discord_rpc.py       # Discord Rich Presence
│   │   ├── downloader.py        # Kuyruk tabanlı indirme yöneticisi
│   │   ├── error_handler.py     # Global hata yönetimi
│   │   ├── headless_downloader.py # Headless indirme (DB/TUI bağımlılığı yok)
│   │   ├── local_library.py     # Yerel anime indeksleme
│   │   ├── logger.py            # Debug loglama sistemi
│   │   ├── notifier.py          # Sistem bildirimleri
│   │   ├── player.py            # MPV video oynatıcı entegrasyonu
│   │   ├── progress.py          # İzleme ilerleme takibi
│   │   ├── scraper.py           # Sağlayıcı facade
│   │   ├── search.py            # Arama servisi
│   │   ├── shortcuts.py         # Klavye kısayol yöneticisi
│   │   ├── tracker.py           # MAL/AniList entegrasyonu
│   │   ├── updater.py           # Otomatik güncelleme kontrolü
│   │   ├── watch.py             # Yayın servisi
│   │   ├── _base.py             # Temel servis sınıfı
│   │   └── _tracker_base.py     # Temel tracker arayüzü
│   │
│   ├── ui/                      # Terminal UI bileşenleri
│   │   ├── header.py            # Başlık gösterimi
│   │   ├── menu.py              # Ana menü
│   │   └── prompt.py            # Özel promptlar
│   │
│   ├── utils/                   # Yardımcı fonksiyonlar
│   │   └── sanitizer.py         # Dosya adı/yol temizleme
│   │
│   ├── locales/                 # Çoklu dil desteği
│   │   ├── en.json              # İngilizce çeviriler
│   │   └── tr.json              # Türkçe çeviriler
│   │
│   ├── templates/               # HTML şablonları
│   │   ├── anilist_error.html   # AniList OAuth hata sayfası
│   │   ├── anilist_success.html # AniList OAuth başarı sayfası
│   │   ├── mal_error.html       # MAL OAuth hata sayfası
│   │   └── mal_success.html     # MAL OAuth başarı sayfası
│   │
│   ├── config.py                # Yapılandırma yönetimi
│   ├── exceptions.py            # Özel exception hiyerarşisi
│   ├── i18n.py                  # Çoklu dil sistemi
│   ├── main.py                  # CLI giriş noktası
│   └── __main__.py              # Paket çalıştırma giriş noktası
│
├── tests/                       # Test paketi
│   ├── test_api.py              # API komutları ve headless downloader testleri
│   ├── test_cache.py            # Önbellek yöneticisi testleri
│   ├── test_exceptions.py       # Exception testleri
│   ├── test_sanitizer.py        # Sanitizer testleri
│   └── conftest.py              # Pytest fixture'ları
│
├── weeb_landing/                # Landing sayfası varlıkları
│   ├── logo/                    # Logo dosyaları (çeşitli boyutlar)
│   └── index.html               # Landing sayfası
│
├── distribution/                # Build ve dağıtım dosyaları
├── pyproject.toml               # Proje metadata ve bağımlılıklar
├── requirements.txt             # Python bağımlılıkları
├── pytest.ini                   # Pytest yapılandırması
├── LICENSE                      # CC BY-NC-ND 4.0 lisansı
└── README.md                    # Bu dosya
```

---

## Teknoloji Yığını

### Temel Teknolojiler
- **Python 3.8+** - Ana programlama dili
- **Typer** - Zengin terminal desteği ile CLI framework
- **Rich** - Terminal formatlama ve stil
- **Questionary** - İnteraktif promptlar ve menüler
- **SQLite** - Yerel veritabanı (WAL modu)

### Web & Ağ
- **requests** - HTTP istemcisi
- **curl_cffi** - Tarayıcı taklit özellikli gelişmiş HTTP
- **BeautifulSoup4** - HTML ayrıştırma
- **lxml** - Hızlı XML/HTML işleme

### Medya & İndirme
- **FFmpeg** - Video işleme ve dönüştürme
- **MPV** - Yüksek kaliteli video oynatıcı
- **Aria2** - Çoklu bağlantılı indirici
- **yt-dlp** - Karmaşık stream indirici (HLS, DASH)

### Şifreleme & Güvenlik
- **pycryptodome** - Şifreleme/şifre çözme (Turkanime)

### Ek Özellikler
- **pypresence** - Discord Rich Presence
- **py7zr** - 7z arşiv işleme
- **winotify** - Windows bildirimleri
- **pyfiglet** - ASCII art başlıklar
- **packaging** - Versiyon karşılaştırma

### Geliştirme & Test
- **pytest** - Test framework
- **pyinstaller** - Çalıştırılabilir dosya oluşturucu
- **build** - Python paket oluşturucu

### Mimari Desenler
- **Provider Pattern** - Takılabilir anime kaynakları
- **Registry Pattern** - Dinamik sağlayıcı kaydı
- **Service Locator** - Lazy-loaded servisler
- **Queue Pattern** - Thread-safe indirme kuyruğu
- **Decorator Pattern** - Önbellekleme decorator
- **Observer Pattern** - İlerleme takibi
- **Strategy Pattern** - Çoklu indirme stratejileri

---

## 📢 Sosyal Medyada Paylaş

**Weeb-CLI'ı favori platformlarınızda paylaşmak için bu tanıtım metinlerini kopyalayıp yapıştırın:**

---

### Twitter/X, Mastodon

```
🎬 Weeb-CLI - Terminal'den eşsiz anime deneyimi!

✅ Tarayıcı yok, reklam yok, sadece anime
✅ Çoklu kaynak (TR/EN)
✅ Aria2 & yt-dlp ile akıllı indirme
✅ MAL/AniList senkronizasyonu
✅ Discord RPC entegrasyonu

Terminal weeb'leri, bu sizin için! 🔥

pip install weeb-cli

⭐ https://github.com/ewgsta/weeb-cli
```

### Reddit, Discord, Forum

```
**🎬 Weeb-CLI - Terminal Tabanlı Anime İzleme & İndirme**

Selam anime severler! Bu harika CLI aracını paylaşmak istedim:

**Özellikler:**
• 🌐 Çoklu anime kaynakları (Türkçe & İngilizce)
• 📺 MPV ile yüksek kaliteli izleme
• ⬇️ Aria2/yt-dlp ile hızlı indirme
• 📊 İzleme geçmişi & ilerleme takibi
• 🎮 Discord Rich Presence
• 📱 MAL/AniList entegrasyonu
• 🤖 Otomasyon için API modu
• 📡 Sonarr/*arr için Torznab sunucu

**Kurulum:**
pip install weeb-cli

**GitHub:** https://github.com/ewgsta/weeb-cli

Tarayıcı yok, reklam yok, dikkat dağıtıcı yok. Sadece siz ve eşsiz bir anime deneyimi! ⭐
```

### LinkedIn, Profesyonel

```
🚀 Weeb-CLI - Terminal Tabanlı Anime Platformu

Modern yazılım mimari desenlerini sergileyen açık kaynaklı bir Python CLI uygulaması:

📌 Teknik Özellikler:
• Takılabilir anime kaynakları için Provider Pattern
• Aria2/yt-dlp ile kuyruk tabanlı indirme yönetimi
• WAL modunda SQLite veritabanı
• OAuth entegrasyonu (MAL/AniList)
• Otomasyon için etkileşimsiz JSON API
• *arr stack entegrasyonu için Torznab sunucu

🔧 Tech Stack: Python, Typer, Rich, BeautifulSoup4, curl_cffi, SQLite

📦 Kurulum: pip install weeb-cli
🔗 GitHub: https://github.com/ewgsta/weeb-cli

#AçıkKaynak #Python #CLI #Anime #YazılımMimarisi
```

---

## Lisans

Bu proje **GNU Genel Kamu Lisansı v3.0** altında lisanslanmıştır.  
Lisansın tam metni için [LICENSE](LICENSE) dosyasına bakın.

Weeb-CLI (C) 2026

---

<p align="center">
  <a href="https://weeb-cli.ewgsta.me">Website</a> •
  <a href="https://github.com/ewgsta/weeb-cli/issues">Sorun Bildir</a>
</p>
