<p align="center">
  <img src="weeb_landing/logo/512x512.webp" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>Anime severler için güçlü, platformlar arası komut satırı aracı</strong>
</p>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/ewgsta/weeb-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/ewgsta/weeb-cli/tests.yml?style=flat-square" alt="Tests"></a>
</p>

<p align="center">
  <a href="#kurulum">Kurulum</a> •
  <a href="#özellikler">Özellikler</a> •
  <a href="#kullanım">Kullanım</a> •
  <a href="#kaynaklar">Kaynaklar</a> •
  <a href="README-EN.md">English</a>
</p>

---

## Demo

### 🎬 Anime Arama ve İzleme
![Anime Search Demo](./demo-search.gif)

### 📋 Ana Menü ve Navigasyon
![Main Menu Demo](./demo-menu.gif)

### ⚡ Tam Özellik Gösterimi
![Full Feature Demo](./demo-full.gif)

> Demo kayıtları [VHS](https://github.com/charmbracelet/vhs) ile oluşturulmuştur. Kendi demo'nuzu oluşturmak için [README-DEMO.md](./README-DEMO.md) dosyasına bakın.

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

| Ayar | Açıklama | Varsayılan |
|------|----------|------------|
| `aria2_enabled` | Aria2 kullanımı | `true` |
| `max_concurrent_downloads` | Eşzamanlı indirme | `3` |
| `download_dir` | İndirme klasörü | `./weeb-downloads` |
| `discord_rpc_enabled` | Discord RPC | `false` |
| `debug_mode` | Debug loglama | `false` |

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
- [ ] Torrent desteği
- [ ] Watch party
- [ ] Mobile app entegrasyonu

---

## Lisans

Bu proje [CC BY-NC-ND 4.0](LICENSE) lisansı ile lisanslanmıştır.

---

<p align="center">
  <a href="https://weeb-cli.ewgsta.me">Website</a> •
  <a href="https://github.com/ewgsta/weeb-cli/issues">Sorun Bildir</a>
</p>
