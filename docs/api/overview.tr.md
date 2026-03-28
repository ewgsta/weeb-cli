# API Referans Genel Bakış

Weeb CLI API referans dokümantasyonuna hoş geldiniz. Bu bölüm, kod tabanındaki tüm modüller, sınıflar ve fonksiyonlar için detaylı dokümantasyon sağlar.

## Organizasyon

API dokümantasyonu pakete göre düzenlenmiştir:

### Temel Modüller

Temel işlevsellik sağlayan önemli modüller:

- **[Config](core/config.md)**: Yapılandırma yönetim sistemi
- **[I18n](core/i18n.md)**: Uluslararasılaştırma ve yerelleştirme
- **[Exceptions](core/exceptions.md)**: Özel istisna hiyerarşisi

### Sağlayıcılar

Anime kaynak sağlayıcı uygulamaları:

- **[Temel Sağlayıcı](providers/base.md)**: Soyut temel sınıf ve veri yapıları
- **[Kayıt](providers/registry.md)**: Sağlayıcı keşfi ve yönetimi
- **[Türkçe Sağlayıcılar](providers/turkish.md)**: Animecix, Turkanime, Anizle, Weeb
- **[İngilizce Sağlayıcılar](providers/english.md)**: HiAnime, AllAnime
- **[Almanca Sağlayıcılar](providers/german.md)**: AniWorld
- **[Lehçe Sağlayıcılar](providers/polish.md)**: Docchi

### Servisler

İş mantığı ve temel işlevsellik:

- **[Veritabanı](services/database.md)**: SQLite veritabanı yönetimi
- **[İndirici](services/downloader.md)**: Kuyruk tabanlı indirme sistemi
- **[İzleyici](services/tracker.md)**: AniList, MAL, Kitsu entegrasyonu
- **[Oynatıcı](services/player.md)**: MPV oynatıcı entegrasyonu
- **[Önbellek](services/cache.md)**: Önbellekleme sistemi
- **[Yerel Kütüphane](services/local_library.md)**: Yerel anime yönetimi

### Komutlar

CLI komut uygulamaları:

- **[API Komutları](commands/api.md)**: Etkileşimsiz JSON API
- **[Arama](commands/search.md)**: Anime arama işlevselliği
- **[İndirmeler](commands/downloads.md)**: İndirme yönetimi
- **[İzleme Listesi](commands/watchlist.md)**: İzleme geçmişi ve ilerleme

### UI Bileşenleri

Terminal kullanıcı arayüzü öğeleri:

- **[Menü](ui/menu.md)**: Etkileşimli menü sistemi
- **[İstem](ui/prompt.md)**: Kullanıcı girişi istemleri
- **[Başlık](ui/header.md)**: Uygulama başlığı gösterimi

## Hızlı Bağlantılar

### Yaygın Görevler

- [Sağlayıcı Uygulama](../development/adding-providers.md)
- [Önbellek Sistemini Kullanma](services/cache.md)
- [Veritabanı İşlemleri](services/database.md)
- [Hata İşleme](core/exceptions.md)

### Tip İpuçları

Tüm modüller daha iyi IDE desteği ve kod netliği için kapsamlı tip ipuçları kullanır:

```python
from typing import List, Optional, Dict

def search(query: str) -> List[AnimeResult]:
    """Tam tip bilgisi ile arama."""
    pass
```

### Docstring Stili

Her yerde Google stili docstring'ler kullanıyoruz:

```python
def function(param: str) -> bool:
    """Kısa açıklama.
    
    Args:
        param: Parametre açıklaması.
    
    Returns:
        Dönüş değeri açıklaması.
    
    Example:
        >>> function("test")
        True
    """
    pass
```

## Navigasyon

API dokümantasyonunda gezinmek için kenar çubuğunu kullanın. Her sayfa şunları içerir:

- Modül genel bakışı
- Sınıf ve fonksiyon imzaları
- Detaylı açıklamalar
- Kullanım örnekleri
- Tip bilgisi

## Katkıda Bulunma

Dokümantasyonda bir sorun mu buldunuz? Lütfen [bir sorun açın](https://github.com/ewgsta/weeb-cli/issues) veya bir pull request gönderin.
