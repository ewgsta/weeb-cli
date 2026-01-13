<div align="center">
  <img src="https://raw.githubusercontent.com/ewgsta/weeb-cli/refs/heads/main/weeb_landing/logo/256x256.webp" alt="Weeb CLI Logo" width="200" height="200" />
  <h1>Weeb CLI</h1>
  <p>
    <b>Tarayıcı yok, reklam yok, dikkat dağıtıcı unsur yok. Sadece siz ve eşsiz bir anime izleme deneyimi.</b>
  </p>
  
  <p>
    <a href="./README-EN.md">Read in English</a>
  </p>

  <p>
    <a href="https://pypi.org/project/weeb-cli/">
      <img src="https://img.shields.io/pypi/v/weeb-cli?style=flat-square&color=blue" alt="PyPI Sürümü" />
    </a>
    <a href="https://aur.archlinux.org/packages/weeb-cli">
      <img src="https://img.shields.io/aur/version/weeb-cli?style=flat-square&color=magenta" alt="AUR Sürümü" />
    </a>
    <img src="https://img.shields.io/github/license/ewgsta/weeb-cli?style=flat-square" alt="Lisans" />
    <img src="https://img.shields.io/badge/platform-win%20%7C%20linux%20%7C%20macos-lightgrey?style=flat-square" alt="Platform" />
  </p>
</div>

Weeb CLI, anime severler için tasarlanmış güçlü, platformlar arası bir komut satırı aracıdır. Favori anime serilerinizi doğrudan terminalinizden arayın, izleyin ve indirin.

---

## Özellikler

- **Gelişmiş Arama**: Hızlı ve detaylı meta verilerle anime arama.
- **Kesintisiz İzleme**: **MPV** entegrasyonu ile HLS/MP4 yayınlarını yüksek kalitede anında izleyin.
- **Akıllı İndirici**:
  - **Aria2** entegrasyonu ile çoklu bağlantılı yüksek hızlı indirmeler.
  - Karmaşık yayınlar için **yt-dlp** desteği.
  - Eşzamanlı indirme yönetimi ve kuyruk sistemi.
  - Akıllı dosya isimlendirme (Örn: `Anime Adı - S1B1.mp4`).
- **İzleme Geçmişi**: İlerlemenizi otomatik takip eder. Kaldığınız yeri (`●`) ve tamamlanan bölümleri (`✓`) işaretler.
- **Çoklu Dil**: Tam Türkçe ve İngilizce arayüz desteği.
- **Çoklu Kaynak**: HiAnime, AllAnime (İngilizce), Animecix, Anizle, Turkanime, Weeb (Yerel Kaynak) (Türkçe)
- **Otomatik Kurulum**: Gerekli araçları (MPV, FFmpeg, Aria2, yt-dlp) eksikse otomatik tespit eder ve kurar.

## Kurulum

### PyPI (Evrensel)
```bash
pip install weeb-cli
```

### AUR (Arch Linux)
```bash
yay -S weeb-cli
```

### Homebrew (macOS/Linux)
```bash
brew tap ewgsta/tap
brew install weeb-cli
```

### Scoop (Windows)
```bash
scoop bucket add weeb-cli https://github.com/ewgsta/scoop-bucket
scoop install weeb-cli
```

### Chocolatey (Windows)
```bash
choco install weeb-cli
```


---

## Kullanım

Aracı terminalden başlatmak için:

```bash
weeb-cli
```

### Kontroller
- **Ok Tuşları**: Menülerde gezinme.
- **Enter**: Seçim yapma.
- **Ctrl+C**: Geri gel / Çıkış.

---

## Yol Haritası (To-Do)

- [x] Temel Arama ve Detaylar
- [x] MPV ile İzleme
- [x] Yerel İzleme Geçmişi ve İlerleme Takibi
- [x] İndirme Yöneticisi (Aria2/yt-dlp Entegrasyonu)
- [x] İnteraktif Ayarlar Menüsü
- [ ] **Anilist / MAL Entegrasyonu** (Listeleri senkronize etme)
- [ ] **Torrent Desteği** (Webtorrent ile izleme ve indirme)
- [ ] **Özel Temalar** (Renk düzenini değiştirme)
- [ ] **Bildirim Sistemi** (Yeni bölüm uyarıları)
- [ ] **Toplu İndirme** (Tek tıkla tüm sezonu indirme)
- [ ] **Discord RPC** (Ne izlediğini gösterme)

---

## Ayarlar

Yapılandırma dosyası `~/.weeb-cli/config.json` konumunda saklanır. Uygulama içindeki **Ayarlar** menüsünden de yönetilebilir.

| Ayar | Açıklama | Varsayılan |
|------|----------|------------|
| `aria2_enabled` | Hızlı indirme için Aria2 kullanımı | `true` |
| `max_concurrent_downloads` | Eşzamanlı indirme sayısı | `3` |
| `download_dir` | İndirme klasörü | `./weeb-downloads` |

---

## Yıldız Geçmişi :3

<a href="https://www.star-history.com/#ewgsta/weeb-cli&type=date&legend=top-left">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=ewgsta/weeb-cli&type=date&theme=dark&legend=top-left" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=ewgsta/weeb-cli&type=date&legend=top-left" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=ewgsta/weeb-cli&type=date&legend=top-left" />
 </picture>
</a>

---

## Lisans

Bu proje Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International Lisansı (CC BY-NC-ND 4.0) ile lisanslanmıştır.
Detaylar için [LICENSE](LICENSE) dosyasına bakınız.

---
