# Ayarlar Rehberi

Weeb CLI'yi tercihlerinize göre yapılandırmak için eksiksiz rehber.

## Ayarlara Erişim

Ana Menü → Ayarlar

## Genel Ayarlar

### Dil

Arayüz dilini değiştirin:
- Türkçe
- English (İngilizce)
- Deutsch (Almanca)
- Polski (Lehçe)

Yol: Ayarlar → Yapılandırma → Dil

### Varsayılan Sağlayıcı

Tercih edilen anime kaynağını ayarlayın:
- Dilinize göre belirlenir
- Manuel olarak değiştirilebilir

Yol: Ayarlar → Yapılandırma → Varsayılan Sağlayıcı

### Açıklamaları Göster

Aramada anime açıklamalarını göster/gizle:
- Açık: Tam özeti gösterir
- Kapalı: Kompakt görünüm

Yol: Ayarlar → Yapılandırma → Açıklamaları Göster

### Hata Ayıklama Modu

Detaylı günlük kaydını etkinleştirin:
- Günlükler ~/.weeb-cli/logs/ dizinine kaydedilir
- Sorun giderme için kullanışlıdır
- Performansı etkileyebilir

Yol: Ayarlar → Yapılandırma → Hata Ayıklama Modu

## İndirme Ayarları

### İndirme Dizini

Anime dosyalarının kaydedileceği yeri ayarlayın:
- Varsayılan: ./weeb-downloads
- Yazılabilir herhangi bir yol olabilir
- Göreceli ve mutlak yolları destekler

Yol: Ayarlar → İndirmeler → İndirme Dizini

### Aria2 Ayarları

Aria2 indiriciyi yapılandırın:
- Aria2'yi Etkinleştir/Devre Dışı Bırak
- Maksimum bağlantı sayısı (1-32)
- Varsayılan: 16 bağlantı

Yol: Ayarlar → İndirmeler → Aria2

### yt-dlp Ayarları

yt-dlp'yi yapılandırın:
- yt-dlp'yi Etkinleştir/Devre Dışı Bırak
- Format dizesi
- Varsayılan: bestvideo+bestaudio/best

Yol: Ayarlar → İndirmeler → yt-dlp

### Eşzamanlı İndirmeler

Maksimum eşzamanlı indirme sayısı:
- Aralık: 1-10
- Varsayılan: 3
- Yüksek değerler daha fazla bant genişliği kullanır

Yol: Ayarlar → İndirmeler → Eşzamanlı

### Yeniden Deneme Ayarları

İndirme yeniden denemelerini yapılandırın:
- Maksimum deneme: 0-10
- Deneme gecikmesi: 1-60 saniye
- Üstel geri çekilme

Yol: Ayarlar → İndirmeler → Yeniden Deneme

## İzleyici Ayarları

### AniList

AniList entegrasyonunu yapılandırın:
- OAuth ile kimlik doğrulama
- Bağlantı durumunu görüntüleme
- Hesap bağlantısını kesme

Yol: Ayarlar → İzleyiciler → AniList

### MyAnimeList

MAL entegrasyonunu yapılandırın:
- OAuth ile kimlik doğrulama
- Senkronizasyon durumunu görüntüleme
- Hesap bağlantısını kesme

Yol: Ayarlar → İzleyiciler → MyAnimeList

### Kitsu

Kitsu entegrasyonunu yapılandırın:
- E-posta/şifre ile giriş
- Bağlantı durumunu görüntüleme
- Çıkış yapma

Yol: Ayarlar → İzleyiciler → Kitsu

## Entegrasyon Ayarları

### Discord Rich Presence

Discord'da ne izlediğinizi gösterin:
- Etkinleştir/Devre Dışı Bırak
- Anime başlığını gösterir
- Bölüm numarasını gösterir
- Geçen süreyi gösterir

Yol: Ayarlar → Entegrasyonlar → Discord RPC

### Klavye Kısayolları

Global klavye kısayolları (deneysel):
- Etkinleştir/Devre Dışı Bırak
- Kısayolları yapılandır
- Sistem çapında kontroller

Yol: Ayarlar → Entegrasyonlar → Kısayollar

## Önbellek Ayarları

### Önbellek İstatistiklerini Görüntüle

Önbellek bilgilerini görün:
- Bellek girdileri
- Dosya girdileri
- Toplam boyut

Yol: Ayarlar → Önbellek → İstatistikler

### Önbelleği Temizle

Önbelleğe alınmış verileri kaldırın:
- Tüm önbelleği temizle
- Sağlayıcı önbelleğini temizle
- Arama geçmişini temizle

Yol: Ayarlar → Önbellek → Temizle

### Önbellek Temizliği

Eski önbellek girdilerini kaldırın:
- Maksimum yaşı ayarla
- Otomatik temizlik
- Manuel temizlik

Yol: Ayarlar → Önbellek → Temizlik

## Harici Sürücüler

### Sürücü Ekle

Harici sürücüleri kaydedin:
1. Ayarlar → Harici Sürücüler
2. "Sürücü Ekle"yi seçin
3. Yolu girin
4. İsim verin

### Sürücüleri Yönet

- Tüm sürücüleri görüntüle
- Sürücüleri kaldır
- Sürücüleri yeniden adlandır
- Sürücüleri tara

Yol: Ayarlar → Harici Sürücüler

## Yedekleme ve Geri Yükleme

### Yedek Oluştur

Verilerinizi yedekleyin:
- Yapılandırma
- İzleme ilerlemesi
- İndirme kuyruğu
- Kütüphane dizini

Yol: Ayarlar → Yedekleme → Yedek Oluştur

### Yedeği Geri Yükle

Yedekten geri yükleyin:
1. Ayarlar → Yedekleme → Geri Yükle
2. Yedek dosyasını seçin
3. Geri yüklemeyi onaylayın

Uyarı: Mevcut verilerin üzerine yazar

## Gelişmiş Ayarlar

### Ayarları Sıfırla

Varsayılanlara sıfırlayın:
1. Ayarlar → Gelişmiş
2. "Tüm Ayarları Sıfırla"yı seçin
3. Sıfırlamayı onaylayın

Uyarı: Geri alınamaz

### Ayarları Dışa Aktar

Yapılandırmayı dışa aktarın:
- JSON formatı
- Tüm ayarları içerir
- Kimlik bilgilerini hariç tutar

Yol: Ayarlar → Gelişmiş → Dışa Aktar

### Ayarları İçe Aktar

Yapılandırmayı içe aktarın:
1. Ayarlar → Gelişmiş → İçe Aktar
2. JSON dosyasını seçin
3. İçe aktarmayı onaylayın

## Yapılandırma Dosyası

Ayarlar şurada saklanır:
```
~/.weeb-cli/weeb.db
```

Tablolar içeren SQLite veritabanı:
- config
- progress
- download_queue
- external_drives
- anime_index

## İpuçları

1. Büyük değişikliklerden önce yedek alın
2. Ayarları tek bir indirme ile test edin
3. Sorun giderme için hata ayıklamayı etkinleştirin
4. Büyük koleksiyonlar için harici sürücüler kullanın
5. İzleyicileri düzenli olarak senkronize edin

## Sonraki Adımlar

- [Yapılandırma Rehberi](../getting-started/configuration.md): Detaylı yapılandırma seçenekleri
- [İndirme Rehberi](downloading.md): İndirmeleri optimize edin
- [İzleyici Rehberi](trackers.md): İzleyicileri kurun
