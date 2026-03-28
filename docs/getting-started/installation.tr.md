# Kurulum

Weeb CLI, platformunuza ve tercihlerinize bağlı olarak birden fazla yöntemle kurulabilir.

## PyPI (Evrensel)

Weeb CLI'yi kurmanın en kolay yolu pip üzerinden:

```bash
pip install weeb-cli
```

En son sürüme güncellemek için:

```bash
pip install --upgrade weeb-cli
```

## Arch Linux (AUR)

Arch Linux kullanıcıları için Weeb CLI, AUR'da mevcuttur:

```bash
yay -S weeb-cli
```

Veya başka bir AUR yardımcısı kullanarak:

```bash
paru -S weeb-cli
```

## Taşınabilir Çalıştırılabilir Dosyalar

Windows, macOS ve Linux için önceden oluşturulmuş taşınabilir çalıştırılabilir dosyalar [Releases](https://github.com/ewgsta/weeb-cli/releases) sayfasından edinilebilir.

1. Platformunuz için uygun dosyayı indirin
2. Arşivi çıkarın
3. Çalıştırılabilir dosyayı çalıştırın

## Geliştirici Kurulumu

Geliştirme veya projeye katkıda bulunmak için:

```bash
# Depoyu klonlayın
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Düzenlenebilir modda kurun
pip install -e .

# Geliştirme bağımlılıklarını kurun
pip install -r requirements.txt
```

## Bağımlılıklar

Weeb CLI, ilk çalıştırmada aşağıdaki bağımlılıkları otomatik olarak indirir ve kurar:

- **FFmpeg**: Video işleme ve dönüştürme
- **MPV**: Akış için medya oynatıcı
- **Aria2**: Hızlı çoklu bağlantı indirmeleri
- **yt-dlp**: Akış çıkarma ve indirme

Bu araçlar `~/.weeb-cli/bin/` dizinine indirilir ve otomatik olarak yönetilir.

## Doğrulama

Kurulumdan sonra, Weeb CLI'nin doğru şekilde kurulduğunu doğrulayın:

```bash
weeb-cli --version
```

Sürüm numarasını görmelisiniz.

## Sonraki Adımlar

- [Hızlı Başlangıç Kılavuzu](quickstart.md): Weeb CLI ile başlayın
- [Yapılandırma](configuration.md): Tercihlerinizi yapılandırın
