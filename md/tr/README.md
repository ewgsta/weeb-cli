<p align="center">
  <img src="https://8upload.com/image/a6cdd79fc5a25c99/wl-512x512.jpg" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>Tarayıcı yok, reklam yok, dikkat dağıtıcı unsur yok. Sadece siz ve eşsiz bir anime izleme deneyimi.</strong>
</p>

<div align="center">
  <a href="../../README.md">English</a> | <a href="README.md">Türkçe</a> | <a href="../de/README.md">Deutsch</a> | <a href="../pl/README.md">Polski</a>
</div>
<br>

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
  <a href="https://ewgsta.github.io/weeb-cli/">Dokümantasyon</a>
</p>

---

## Özellikler

### Eklenti Sistemi
- **Özel .weeb formatı**: Kendi sağlayıcılarınızı paketleyin ve paylaşın
- **Güvenli Sandbox**: Eklentileri kısıtlı izinlerle güvenli bir şekilde çalıştırın
- **Eklenti Oluşturucu**: Eklentileri paketlemek için kullanımı kolay betik
- **Eklenti Galerisi**: Topluluk eklentilerine [Galeri](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html) üzerinden göz atın ve yükleyin
- **Otomatik Keşif**: Eklentiler başlangıçta otomatik olarak yüklenir

### Çoklu Kaynak Desteği
- **Türkçe**: Animecix, Turkanime, Anizle, Weeb
- **İngilizce**: HiAnime, AllAnime
- **Almanca**: AniWorld
- **Lehçe**: Docchi

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

### İzleme Takibi ve Senkronizasyon
- **AniList** entegrasyonu (OAuth)
- **MyAnimeList** entegrasyonu (OAuth)
- **Kitsu** entegrasyonu (email/şifre)
- Online ve offline izleme için otomatik ilerleme senkronizasyonu
- Bekleyen güncellemeler için çevrimdışı kuyruk
- Dosya adlarından akıllı anime başlığı eşleştirme

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

---

## Kullanım

```bash
weeb-cli
```

### API Modu (Etkileşimsiz)

Scriptler, otomasyon ve yapay zeka ajanları için weeb-cli, veritabanı veya TUI gerektirmeden headless çalışan JSON API komutları sunar:

```bash
# Mevcut sağlayıcıları listele
weeb-cli api providers

# Anime ara (ID'leri döndürür)
weeb-cli api search "Angel Beats"
```

---

## Lisans

Bu proje **GNU Genel Kamu Lisansı v3.0** altında lisanslanmıştır.  
Lisansın tam metni için [LICENSE](../../LICENSE) dosyasına bakın.

Weeb-CLI (C) 2026
