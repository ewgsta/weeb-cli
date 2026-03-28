# Local Library Service

Yerel anime indeksleme ve yönetimi.

## Genel Bakış

Local library servisi şunları sağlar:
- Otomatik anime tarama
- Bölüm algılama
- Harici sürücü desteği
- Tracker senkronizasyonu

## Özellikler

### Otomatik Tarama

Anime için dizinleri tarar:
- Anime başlıklarını algılar
- Bölümleri sayar
- Tracker'larla eşleştirir

### Dosya Desenleri

Desteklenen adlandırma desenleri:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Group] Anime Name - 01.mp4`

### Harici Sürücüler

- USB sürücüleri kaydet
- Harici HDD'leri tara
- Taşınabilir kütüphane

## Kullanım

```python
from weeb_cli.services.local_library import library

# Dizini tara
library.scan_directory("/path/to/anime")

# İndekslenmiş anime'leri al
anime_list = library.get_all_anime()

# Kütüphanede ara
results = library.search("Naruto")
```

## Sanal Kütüphane

Çevrimiçi anime'leri yer imlerine ekle:
- İndirme gerekmez
- Hızlı erişim
- Düzenli koleksiyon

## Sonraki Adımlar

- [Kütüphane Rehberi](../../user-guide/library.md): Kullanıcı rehberi
- [Yapılandırma](../../getting-started/configuration.md): Ayarlar
