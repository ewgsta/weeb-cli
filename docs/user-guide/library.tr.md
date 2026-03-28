# Yerel Kütüphane Yönetimi

Weeb CLI'ın yerel kütüphane özellikleriyle indirilen anime koleksiyonunuzu yönetin.

## Genel Bakış

Yerel kütüphane şunları yapmanızı sağlar:
- İndirilen animeleri dizinle
- Çevrimdışı içeriğe göz at
- İzleyicilerle senkronize et
- Harici sürücüleri yönet

## Kütüphaneyi Tarama

### Otomatik Tarama

Weeb CLI indirme dizininizi otomatik olarak tarar:

1. Ana Menü → Kütüphane
2. "Kütüphaneyi Tara"yı seçin
3. Taramanın tamamlanmasını bekleyin

### Tarama Sonuçları

Gösterir:
- Algılanan anime başlıkları
- Bölüm sayıları
- Kaynak konum
- İzleyici eşleşme durumu

### Dosya Formatı

En iyi sonuçlar için bu formatı kullanın:

```
Anime Adı - S1E1.mp4
Anime Adı - S1E2.mp4
Anime Adı - S2E1.mp4
```

Desteklenen desenler:
- `Anime Adı - S1E1.mp4`
- `Anime Adı - 01.mp4`
- `Anime Adı - Bölüm 1.mp4`
- `[Grup] Anime Adı - 01.mp4`

## Harici Sürücüler

### Sürücü Ekleme

USB sürücüler veya harici HDD'ler ekleyin:

1. Ayarlar → Harici Sürücüler
2. "Sürücü Ekle"yi seçin
3. Sürücü yolunu girin
4. Bir isim verin

### Sürücüleri Tarama

1. Kütüphane → Harici Sürücüler
2. Sürücü seçin
3. "Sürücüyü Tara"yı seçin

### Sürücü Yönetimi

- Tüm kayıtlı sürücüleri görüntüle
- Sürücüleri kaldır
- Sürücüleri yeniden adlandır
- Tek tek sürücüleri tara

## Sanal Kütüphane

### Sanal Kütüphane Nedir?

Hızlı erişim için çevrimiçi animeleri yer imlerine ekleyin:
- İndirme gerekmez
- Favorilere hızlı erişim
- Organize koleksiyon

### Sanal Kütüphaneye Ekleme

1. Anime arayın
2. Detayları görüntüleyin
3. "Kütüphaneye Ekle"yi seçin

### Sanal Kütüphaneye Erişim

1. Ana Menü → Kütüphane
2. "Sanal Kütüphane"yi seçin
3. Yer imlerine eklenen animelere göz atın

## Kütüphanede Gezinme

### Yerel Animeler

İndirilen animeleri görüntüleyin:
- Başlığa göre sıralanmış
- Bölüm sayısını gösterir
- Tamamlanma durumunu belirtir

### Kütüphaneden Oynatma

1. Anime seçin
2. Bölüm seçin
3. MPV'de oynatılır

### Kütüphane İstatistikleri

İstatistikleri görüntüleyin:
- Toplam anime sayısı
- Toplam bölümler
- Kullanılan toplam depolama
- En çok izlenen

## İzleyici Senkronizasyonu

### Otomatik Senkronizasyon

Kütüphane taranırken:
- Animeleri izleyici veritabanıyla eşleştirir
- İzleme ilerlemesini senkronize eder
- Tamamlanma durumunu günceller

### Manuel Senkronizasyon

Senkronizasyonu zorla:
1. Kütüphane → Ayarlar
2. "İzleyicilerle Senkronize Et"i seçin

### Eşleşme Doğruluğu

Eşleşmeyi iyileştirin:
- Standart dosya adlandırma kullanın
- Sezon numaralarını dahil edin
- Tam anime başlıklarını kullanın

## Kütüphane Organizasyonu

### Klasör Yapısı

Önerilen yapı:

```
downloads/
├── Anime 1/
│   ├── S1E1.mp4
│   ├── S1E2.mp4
│   └── ...
├── Anime 2/
│   ├── S1E1.mp4
│   └── ...
```

### Temizleme

Animeleri dizinden kaldırın:
1. Kütüphane → Yönet
2. Anime seçin
3. "Dizinden Kaldır"ı seçin

Not: Bu sadece dizinden kaldırır, dosyaları silmez.

## Gelişmiş Özellikler

### Çoklu Kaynak Kütüphane

Şunlardan animeleri birleştirin:
- İndirme dizini
- Harici sürücüler
- Ağ paylaşımları (bağlıysa)

### Kütüphanede Arama

Kütüphanede hızlı arama:
1. Kütüphane menüsü
2. Aramak için yazın
3. Sonuçları gerçek zamanlı filtreler

### Kütüphaneyi Dışa Aktar

Kütüphane listesini dışa aktarın:
1. Kütüphane → Dışa Aktar
2. Format seçin (JSON/CSV)
3. Dosyaya kaydedin

## Sorun Giderme

### Anime Algılanmadı

1. Dosya adlandırma formatını kontrol edin
2. Dosyaların indirme dizininde olduğundan emin olun
3. Kütüphaneyi yeniden tarayın
4. Dosya uzantılarını kontrol edin (.mp4, .mkv)

### Yanlış Bölüm Sayısı

1. Dosya adlandırmasını doğrulayın
2. Yinelenen dosyaları kontrol edin
3. Kütüphaneyi yeniden tarayın

### İzleyici Eşleşmiyor

1. Tam anime başlığını kullanın
2. Klasör adına yılı dahil edin
3. İzleyici ayarlarında manuel eşleştirme

### Harici Sürücü Bulunamadı

1. Sürücünün bağlı olduğunu doğrulayın
2. Yolun doğru olduğunu kontrol edin
3. Ayarlarda sürücüyü yeniden ekleyin

## En İyi Uygulamalar

1. Tutarlı dosya adlandırma kullanın
2. Anime klasörlerine göre organize edin
3. Sezon numaralarını dahil edin
4. İndirmeler tamamlandıktan sonra tarayın
5. Kütüphane veritabanını düzenli olarak yedekleyin

## Sonraki Adımlar

- [İzleyici Entegrasyonu](trackers.md): Çevrimiçi izleyicilerle senkronize edin
- [İndirme Kılavuzu](downloading.md): Daha fazla anime indirin
- [Yapılandırma](../getting-started/configuration.md): Kütüphane ayarları
