# Plugin Geliştirme Rehberi

Weeb CLI, uygulamayı özel sağlayıcılar, takipçiler ve servislerle genişletmenize olanak tanıyan sağlam bir eklenti mimarisi sunar. Eklentiler güvenli, taşınabilir bir ortamda izole edilir ve standartlaştırılmış bir klasör yapısını takip eder.

## Eklenti Yapısı

Standart bir eklenti klasörü `data/` dizininde saklanmalı ve şu yapıyı içermelidir:

```
data/
  eklentim/
    plugin.weeb        (Ana kod giriş noktası)
    manifest.json      (Metadata ve yapılandırma)
    README.md          (Detaylı dökümantasyon)
    screenshots/       (Galeri için en az bir ekran görüntüsü)
      ss1.png
    assets/            (İkonlar ve diğer varlıklar)
      icon.png
```

### manifest.json

Manifest, eklentiniz hakkında zorunlu ve isteğe bağlı meta verileri içerir:

```json
{
    "id": "eklentim",
    "name": "Eklenti Adı",
    "version": "1.0.0",
    "description": "Eklentinizin açıklaması.",
    "author": "Adınız",
    "entry_point": "plugin.weeb",
    "min_weeb_version": "1.0.0",
    "dependencies": [],
    "permissions": ["network", "storage"],
    "tags": ["anime", "tr"],
    "icon": "assets/icon.png",
    "homepage": "https://example.com",
    "repository_url": "https://github.com/user/repo",
    "license": "MIT"
}
```

### plugin.weeb

Giriş noktası, bir `register()` fonksiyonu tanımlaması gereken bir Python betiğidir. Güvenli bir builtin alt kümesine ve `weeb_cli` API'lerine erişimi olan kısıtlı bir sandbox ortamında çalışır.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("ozel_saglayicim", lang="tr", region="TR")
    class MyProvider(BaseProvider):
        def search(self, query: str):
            # Uygulama...
            pass
```

## Derleme ve Paketleme

Yeni eklentiler oluşturmak veya paketlemek için sağlanan builder betiğini kullanın:

```bash
# Yeni bir eklenti şablonu oluştur
python3 weeb_cli/utils/plugin_builder.py create yeni-eklentim --id "yeni-id" --name "Yeni İsim"

# Dağıtım için bir eklentiyi paketle (.weeb_pkg)
python3 weeb_cli/utils/plugin_builder.py build data/eklentim -o eklentim.weeb_pkg
```

## Kurulum

1. Weeb CLI'yı açın.
2. **Ayarlar** > **Eklentiler** bölümüne gidin.
3. **Eklenti Yükle** seçeneğini seçin.
4. Eklenti klasörünün yerel yolunu veya `.weeb_pkg` dosyasını belirtin.

## Test ve Kalite

Eklentilerin resmi galeriye kabul edilmesi için en az **%80 test kapsamına (coverage)** sahip olması gerekir. Otomatik testler, eklenti klasörü içindeki bir `tests/` dizinine yerleştirilmelidir.

CI/CD hattımız şunları doğrular:
- **Manifest bütünlüğü**: Zorunlu alanlar (id, isim, versiyon vb.) mevcut olmalıdır.
- **Güvenlik**: Yaygın güvenlik açıkları için Bandit ile taranır.
- **Kod Kalitesi**: Ruff ile kontrol edilir.
- **İşlevsellik**: Testler çalıştırılır ve kapsam kontrol edilir.

## Galeri Üzerinden Paylaşım

Eklenti klasörünüzü `data/` dizinine ekleyen bir Pull Request gönderin. Onaylandıktan sonra otomatik olarak [Eklenti Galerisi](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html) sayfasında görünecektir.
