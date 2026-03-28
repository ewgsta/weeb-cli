# Anime Yayını

Medya oynatıcınızda doğrudan anime yayını yapmayı öğrenin.

## Yayın Başlatma

### Arama Sonuçlarından

1. Anime arayın
2. Sonuçlardan anime seçin
3. "İzle" seçeneğini seçin
4. Bölüm seçin
5. Kalite/sunucu seçin
6. Video MPV oynatıcıda açılır

### İzleme Listesinden

1. Ana Menü → İzleme Listesi
2. Anime seçin
3. Bölüm seçin
4. Yayın başlar

## Oynatıcı Kontrolleri

### MPV Klavye Kısayolları

- Boşluk: Oynat/Duraklat
- Sol/Sağ Ok: 5 saniye geri/ileri sar
- Yukarı/Aşağı Ok: 1 dakika geri/ileri sar
- [ / ]: Oynatma hızını azalt/artır
- m: Sesi kapat/aç
- f: Tam ekranı aç/kapat
- q: Oynatıcıdan çık
- s: Ekran görüntüsü al
- j: Altyazıları değiştir

### İlerleme Takibi

Weeb CLI otomatik olarak:
- Konumunuzu her 15 saniyede bir kaydeder
- Bölümü %80 tamamlandığında izlendi olarak işaretler
- İlerlemeyi izleyicilerle senkronize eder (yapılandırılmışsa)

### İzlemeye Devam Et

Bir bölümü yeniden açtığınızda:
- Otomatik olarak son konumdan devam eder
- Sona yakınsa devam et istemi gösterir
- Tamamlandıktan sonra konumu temizler

## Kalite Seçimi

### Mevcut Kaliteler

Sağlayıcıya ve sunucuya bağlıdır:
- 1080p (Full HD)
- 720p (HD)
- 480p (SD)
- 360p (Düşük)
- Otomatik (uyarlanabilir)

### Kalite Seçme

1. Bölüm seçtikten sonra
2. Mevcut kalitelerden seçin
3. Daha yüksek kalite daha hızlı bağlantı gerektirir

### Kalite Sorunları

Tamponlama olursa:
1. Daha düşük kalite seçin
2. İnternet hızını kontrol edin
3. Farklı sunucu deneyin

## Sunucu Seçimi

### Birden Fazla Sunucu

Çoğu sağlayıcı birden fazla sunucu sunar:
- Birincil sunucu (genellikle en hızlı)
- Yedek sunucular
- Farklı barındırma hizmetleri

### Sunucu Değiştirme

Yayın başarısız olursa:
1. Bölüm seçimine geri dönün
2. Farklı sunucu deneyin
3. Farklı sunucuların farklı kaliteleri olabilir

## Altyazılar

### Altyazı Desteği

- Gömülü altyazılar (varsa)
- Harici altyazı dosyaları
- Çoklu dil desteği

### Altyazı Kontrolleri

MPV'de:
- j: Altyazı parçaları arasında geçiş yap
- v: Altyazı görünürlüğünü aç/kapat
- z/x: Altyazı gecikmesini ayarla

## Yayın Sorunları

### Video Oynatılmıyor

1. MPV kurulumunu kontrol edin
2. Farklı kalite/sunucu deneyin
3. İnternet bağlantısını kontrol edin
4. Yayın URL'sinin geçerli olduğunu doğrulayın

### Tamponlama

1. Kalite ayarını düşürün
2. Duraklatın ve tamponlanmasını bekleyin
3. Ağ hızını kontrol edin
4. Farklı sunucu deneyin

### Ses/Video Senkronizasyonu

1. Ayarlamak için z/x tuşlarını kullanın
2. Farklı sunucu deneyin
3. Kalıcıysa sorunu bildirin

### Altyazı Yok

1. Sağlayıcının altyazı sunup sunmadığını kontrol edin
2. Farklı sunucu deneyin
3. Altyazı parçaları arasında geçiş yapmak için j tuşunu kullanın

## Gelişmiş Özellikler

### Discord Rich Presence

Etkinleştirilirse Discord'da gösterir:
- Şu anda izlenen anime
- Bölüm numarası
- Geçen süre

Etkinleştir: Ayarlar → Entegrasyonlar → Discord RPC

### İzleme İstatistikleri

İstatistiklerinizi görüntüleyin:
- Toplam izleme süresi
- İzlenen bölümler
- Favori anime
- İzleme geçmişi

Erişim: Ana Menü → İzleme Listesi → İstatistikler

## İpuçları

1. En iyi deneyim için tam ekran kullanın (f tuşu)
2. Oynatma hızını [ ] tuşlarıyla ayarlayın
3. s tuşuyla ekran görüntüsü alın
4. Hızlı arama için ok tuşlarını kullanın
5. Arkadaşlarınızla paylaşmak için Discord RPC'yi etkinleştirin

## Sonraki Adımlar

- [İndirme Kılavuzu](downloading.md): Çevrimdışı izleme için indirin
- [İzleyici Entegrasyonu](trackers.md): İlerlemenizi senkronize edin
- [Yerel Kütüphane](library.md): İndirilen animeleri yönetin
