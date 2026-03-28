# İndirme Yönetimi

Weeb CLI'ın güçlü indirme sistemiyle çevrimdışı izleme için anime indirmeyi öğrenin.

## İndirmeleri Başlatma

### Aramadan

1. Anime arayın
2. Anime seçin
3. "İndir" seçeneğini seçin
4. Bölümleri seçin:
   - Tek bölüm
   - Bölüm aralığı (örn. 1-12)
   - Tüm bölümler
5. İndirmeler kuyruğa eklenir

### İzleme Listesinden

1. Ana Menü → İzleme Listesi
2. Anime seçin
3. "Bölümleri İndir"i seçin
4. Bölümleri seçin

## İndirme Kuyruğu

### Kuyruğu Görüntüleme

Ana Menü → İndirmeler

Gösterir:
- İlerleme ile aktif indirmeler
- Bekleyen indirmeler
- Tamamlanan indirmeler
- Başarısız indirmeler

### Kuyruk Bilgisi

Her indirme için:
- Anime başlığı ve bölüm
- İlerleme yüzdesi
- İndirme hızı
- Tahmini süre
- Durum (beklemede/işleniyor/tamamlandı/başarısız)

## İndirmeleri Yönetme

### Duraklat/Devam Et

Kuyruk şunları yapabilir:
- Duraklatıldı: Tüm aktif indirmeleri durdurur
- Devam Ettirildi: Durdurulduğu yerden devam eder

### Başarısızları Yeniden Dene

İndirmeler başarısız olursa:
1. İndirmeler menüsüne gidin
2. "Başarısızları Yeniden Dene"yi seçin
3. Başarısız indirmeler yeniden başlar

### Tamamlananları Temizle

Tamamlanan indirmeleri kuyruktan kaldırın:
1. İndirmeler menüsü
2. "Tamamlananları Temizle"yi seçin

## İndirme Yöntemleri

Weeb CLI otomatik yedekleme ile birden fazla indirme yöntemi kullanır:

### 1. Aria2 (En Hızlı)

- Çoklu bağlantı indirmeleri
- Devam etme desteği
- İlerleme takibi
- Varsayılan: 16 bağlantı

Yapılandır: Ayarlar → İndirmeler → Aria2 Ayarları

### 2. yt-dlp

- Karmaşık akış desteği
- Format seçimi
- Altyazı indirme
- HLS akışları için yedek

Yapılandır: Ayarlar → İndirmeler → yt-dlp Ayarları

### 3. FFmpeg

- HLS akış dönüştürme
- Format dönüştürme
- Yedek yöntem

### 4. Genel HTTP

- Basit HTTP indirmeleri
- Son çare yedek

## İndirme Ayarları

### Eşzamanlı İndirmeler

Maksimum eşzamanlı indirme:
- Varsayılan: 3
- Aralık: 1-10
- Daha yüksek = daha hızlı ama daha fazla kaynak

Ayarlar → İndirmeler → Eşzamanlı İndirmeler

### İndirme Dizini

Dosyaların nereye kaydedileceğini ayarlayın:
- Varsayılan: `./weeb-downloads`
- Herhangi bir yazılabilir dizin olabilir

Ayarlar → İndirmeler → İndirme Dizini

### Yeniden Deneme Ayarları

Yeniden deneme davranışını yapılandırın:
- Maksimum yeniden deneme: 0-10 (varsayılan: 3)
- Yeniden deneme gecikmesi: 1-60 saniye (varsayılan: 10)

Ayarlar → İndirmeler → Yeniden Deneme Ayarları

## Dosya Adlandırma

### Varsayılan Format

```
Anime Adı - S1E1.mp4
Anime Adı - S1E2.mp4
```

### Özel Adlandırma

Dosyalar otomatik olarak adlandırılır:
- Dosya sistemi için temizlenmiş
- Sezon ve bölüm numaraları
- .mp4 uzantısı

## İndirme Sorunları

### Yetersiz Disk Alanı

Weeb CLI indirmeden önce kullanılabilir alanı kontrol eder:
- Minimum 1GB boş alan gerektirir
- Yetersizse hata gösterir
- Alanı temizleyin veya dizini değiştirin

### İndirme Başarısız

Yaygın nedenler:
1. Ağ kesintisi
2. Geçersiz akış URL'si
3. Sağlayıcı sorunları
4. Disk alanı

Çözümler:
1. İndirmeyi yeniden deneyin
2. Farklı kalite deneyin
3. Farklı sağlayıcı deneyin
4. Ayrıntılar için günlükleri kontrol edin

### Yavaş İndirmeler

Hızı artırın:
1. Aria2'yi etkinleştirin
2. Maksimum bağlantıları artırın
3. Ağ hızını kontrol edin
4. Farklı sunucu deneyin

### Kesintiye Uğrayanı Devam Ettir

İndirmeler otomatik olarak devam eder:
- Aria2 devam etmeyi destekler
- Kısmi dosyalar korunur
- Son bayttan devam eder

## Gelişmiş Özellikler

### Toplu İndirmeler

Birden fazla anime indirin:
1. Arayın ve kuyruğa ekleyin
2. Diğer animeler için tekrarlayın
3. Hepsi eşzamanlı olarak indirilir

### Kalite Tercihi

Weeb CLI otomatik olarak seçer:
- En yüksek kullanılabilir kalite
- En iyi kullanılabilir sunucu
- Gerekirse daha düşük kaliteye yedek

### İlerleme Bildirimleri

Sistem bildirimleri:
- İndirme tamamlandığında
- İndirme başarısız olduğunda
- Kuyruk bittiğinde

Etkinleştir: Ayarlar → Bildirimler

## İndirmeleri İzleme

### Gerçek Zamanlı İlerleme

İndirmeler menüsü gösterir:
- Mevcut hız (MB/s)
- İndirilen boyut / Toplam boyut
- İlerleme çubuğu
- Tahmini süre

### İndirme İstatistikleri

Tamamlandıktan sonra:
- Toplam indirilen
- Ortalama hız
- Geçen süre
- Başarı oranı

## İpuçları

1. En hızlı indirmeler için Aria2'yi etkinleştirin
2. Yoğun olmayan saatlerde indirin
3. Toplu indirmeler için bölüm aralıklarını kullanın
4. Disk alanını düzenli olarak izleyin
5. Vazgeçmeden önce başarısız indirmeleri yeniden deneyin

## Sonraki Adımlar

- [Yerel Kütüphane](library.md): İndirilen animeleri yönetin
- [İzleyici Entegrasyonu](trackers.md): İndirme ilerlemesini senkronize edin
- [Yapılandırma](../getting-started/configuration.md): Ayarları optimize edin
