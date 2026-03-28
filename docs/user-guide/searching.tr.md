# Anime Arama

Birden fazla sağlayıcıda anime aramayı ve izlemek istediğiniz içeriği bulmayı öğrenin.

## Temel Arama

### Ana Menüden

1. Weeb CLI'ı başlatın: `weeb-cli`
2. Ana menüden "Anime Ara"yı seçin
3. Arama sorgunuzu girin
4. Sonuçlara göz atın

### Arama İpuçları

- İngilizce veya yerel dil başlıklarını kullanın
- Bulunamazsa alternatif yazılışları deneyin
- Daha geniş sonuçlar için kısmi başlıklar kullanın
- Arama büyük/küçük harf duyarlı değildir

## Arama Sonuçları

Sonuçlar şunları gösterir:
- Anime başlığı
- Tür (Dizi, Film, OVA, vb.)
- Yayın yılı
- Kapak resmi (terminal destekliyorsa)
- Sağlayıcı kaynağı

### Sonuçlarda Gezinme

- Gezinmek için ok tuşlarını kullanın
- Seçmek için Enter'a basın
- Geri dönmek için Ctrl+C'ye basın

## Sağlayıcı Seçimi

### Varsayılan Sağlayıcı

Varsayılan sağlayıcı dil ayarınıza göre belirlenir:
- Türkçe: Animecix
- İngilizce: HiAnime
- Almanca: AniWorld
- Lehçe: Docchi

### Sağlayıcıyı Değiştirme

1. Ayarlar → Yapılandırma'ya gidin
2. "Varsayılan Sağlayıcı"yı seçin
3. Mevcut sağlayıcılardan birini seçin

### Sağlayıcıya Özel Arama

Farklı sağlayıcıların farklı içerikleri olabilir:
- Bulunamazsa birden fazla sağlayıcı deneyin
- Bazı sağlayıcıların özel içeriği vardır
- Kalite ve kullanılabilirlik değişir

## Arama Geçmişi

### Geçmişi Görüntüleme

1. Ana menüden "Anime Ara"yı seçin
2. Son aramaları görmek için Yukarı ok tuşuna basın
3. Aramayı tekrarlamak için geçmişten seçin

### Geçmişi Temizleme

Ayarlar → Önbellek → Arama Geçmişini Temizle

## Gelişmiş Arama

### API Modu

Betik ve otomasyon için:

```bash
# Belirli sağlayıcıyla arama
weeb-cli api search "One Piece" --provider animecix

# Çıktı JSON formatındadır
weeb-cli api search "Naruto" --provider hianime | jq
```

### Sonuçları Filtreleme

Şu anda filtreleme sağlayıcı tarafından yapılır. Gelecek sürümler şunları içerebilir:
- Tür filtreleme
- Yıl filtreleme
- Tip filtreleme (Dizi/Film/OVA)

## Sorun Giderme

### Sonuç Bulunamadı

1. Yazımı kontrol edin
2. Alternatif başlığı deneyin (İngilizce/Japonca/Yerel)
3. Farklı sağlayıcı deneyin
4. İnternet bağlantısını kontrol edin

### Yavaş Arama

1. Ağ hızını kontrol edin
2. Farklı sağlayıcı deneyin
3. Önbelleği temizleyin: Ayarlar → Önbellek → Sağlayıcı Önbelleğini Temizle

### Sağlayıcı Hataları

Bir sağlayıcı başarısız olursa:
1. Başka bir sağlayıcı deneyin
2. Sağlayıcı web sitesinin erişilebilir olup olmadığını kontrol edin
3. Kalıcıysa GitHub'da sorun bildirin

## Sonraki Adımlar

- [Yayın Kılavuzu](streaming.md): Anime izlemeyi öğrenin
- [İndirme Kılavuzu](downloading.md): Anime indirmeyi öğrenin
- [İzleyici Entegrasyonu](trackers.md): İlerlemenizi senkronize edin
