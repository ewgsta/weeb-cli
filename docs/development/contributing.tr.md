# Weeb CLI'ye Katkıda Bulunma

Weeb CLI'ye katkıda bulunmak istediğiniz için teşekkür ederiz! Bu rehber başlamanıza yardımcı olacaktır.

## Geliştirme Kurulumu

### Ön Gereksinimler

- Python 3.8 veya üzeri
- Git
- pip veya pipenv

### Klonlama ve Kurulum

```bash
# Depoyu klonlayın
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Düzenlenebilir modda kurun
pip install -e .

# Geliştirme bağımlılıklarını kurun
pip install -r requirements.txt
```

### Testleri Çalıştırma

```bash
# Tüm testleri çalıştır
pytest

# Kapsam ile çalıştır
pytest --cov=weeb_cli --cov-report=html

# Belirli test dosyasını çalıştır
pytest tests/test_providers.py
```

## Kod Stili

### Python Stil Rehberi

Bazı değişikliklerle PEP 8'i takip ediyoruz:

- Satır uzunluğu: 100 karakter (79 değil)
- Tüm fonksiyon imzaları için tip ipuçları kullanın
- Tüm genel fonksiyonlar ve sınıflar için docstring'ler (Google stili) kullanın

### Tip İpuçları

Tüm fonksiyonlar tip ipuçlarına sahip olmalıdır:

```python
def search(self, query: str) -> List[AnimeResult]:
    """Sorguya göre anime ara.
    
    Args:
        query: Arama sorgu dizesi.
    
    Returns:
        Anime arama sonuçlarının listesi.
    """
    pass
```

### Docstring'ler

Google stili docstring'ler kullanın:

```python
def function_name(param1: str, param2: int) -> bool:
    """Kısa açıklama.
    
    Gerekirse daha uzun açıklama.
    
    Args:
        param1: param1'in açıklaması.
        param2: param2'nin açıklaması.
    
    Returns:
        Dönüş değerinin açıklaması.
    
    Raises:
        ValueError: param1 geçersiz olduğunda.
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

## Yeni Sağlayıcı Ekleme

### 1. Sağlayıcı Dosyası Oluştur

Uygun dil dizininde yeni bir dosya oluşturun:

```
weeb_cli/providers/<lang>/<sağlayıcı_adı>.py
```

### 2. Sağlayıcı Sınıfını Uygula

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.providers.registry import register_provider
from typing import List, Optional

@register_provider("mysaglayi ci", lang="en", region="US")
class MyProvider(BaseProvider):
    """MyAnimeSource.com için sağlayıcı.
    
    Arama, detaylar ve yayın çıkarma ile MyAnimeSource'tan
    anime içeriği sağlar.
    """
    
    BASE_URL = "https://myanimesource.com"
    
    def search(self, query: str) -> List[AnimeResult]:
        """Anime ara."""
        # Uygulama
        pass
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Anime detaylarını al."""
        # Uygulama
        pass
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Bölüm listesini al."""
        # Uygulama
        pass
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Yayın URL'lerini çıkar."""
        # Uygulama
        pass
```

### 3. Testler Ekle

`tests/` içinde test dosyası oluşturun:

```python
import pytest
from weeb_cli.providers import get_provider

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
    assert results[0].title is not None
```

### 4. Dokümantasyonu Güncelle

`docs/api/providers/` içine sağlayıcı dokümantasyonu ekleyin.

## Pull Request Süreci

### 1. Dal Oluştur

```bash
git checkout -b feature/yeni-ozelligim
```

### 2. Değişiklik Yap

- Stil yönergelerini takip ederek kod yazın
- Tip ipuçları ve docstring'ler ekleyin
- Yeni işlevsellik için testler yazın
- Dokümantasyonu güncelleyin

### 3. Değişikliklerinizi Test Edin

```bash
# Testleri çalıştır
pytest

# Kod stilini kontrol et
flake8 weeb_cli/

# Tip kontrolü (isteğe bağlı)
mypy weeb_cli/
```

### 4. Değişiklikleri Commit Et

Geleneksel commit mesajları kullanın:

```bash
git commit -m "feat: XYZ için yeni sağlayıcı ekle"
git commit -m "fix: yayın çıkarma sorununu çöz"
git commit -m "docs: kurulum rehberini güncelle"
```

Commit türleri:
- `feat`: Yeni özellik
- `fix`: Hata düzeltmesi
- `docs`: Dokümantasyon değişiklikleri
- `style`: Kod stili değişiklikleri (biçimlendirme)
- `refactor`: Kod yeniden düzenleme
- `test`: Test ekleme veya güncelleme
- `chore`: Bakım görevleri

### 5. Push ve PR Oluştur

```bash
git push origin feature/yeni-ozelligim
```

Ardından GitHub'da şunlarla bir Pull Request oluşturun:
- Değişikliklerin net açıklaması
- İlgili sorunlara referans
- Ekran görüntüleri (UI değişiklikleri varsa)

## Kod İncelemesi

Tüm gönderimler inceleme gerektirir. PR'ınızı inceleyeceğiz ve değişiklik talep edebiliriz. Lütfen sabırlı olun ve geri bildirimlere yanıt verin.

## Topluluk Yönergeleri

- Saygılı ve yapıcı olun
- Tartışmalarda başkalarına yardım edin
- Hataları detaylı bilgilerle bildirin
- Özellikleri net kullanım senaryolarıyla önerin

## Sorular?

- Hatalar veya özellik istekleri için bir sorun açın
- Sorular için bir tartışma başlatın
- Yeni sorun oluşturmadan önce mevcut sorunları kontrol edin

Weeb CLI'ye katkıda bulunduğunuz için teşekkür ederiz!
