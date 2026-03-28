# Hızlı Başlangıç Kılavuzu

Bu kılavuz, Weeb CLI ile sadece birkaç dakika içinde başlamanıza yardımcı olacaktır.

## İlk Çalıştırma

Weeb CLI'yi ilk kez çalıştırdığınızda, bir kurulum sihirbazı ile karşılaşacaksınız:

```bash
weeb-cli
```

### Kurulum Sihirbazı

1. **Dil Seçimi**: Tercih ettiğiniz dili seçin (Türkçe, İngilizce, Almanca veya Lehçe)
2. **İndirme Dizini**: Anime dosyalarının nereye indirileceğini ayarlayın
3. **Sağlayıcı Seçimi**: Varsayılan anime kaynağınızı seçin
4. **İsteğe Bağlı Ayarlar**: Takipçileri, Discord RPC'yi vb. yapılandırın

## Temel Kullanım

### Anime Arama

1. Ana menüden "Anime Ara"yı seçin
2. Anime adını girin
3. Arama sonuçlarına göz atın
4. Detayları görmek için bir anime seçin

### Akış

1. Bir anime seçtikten sonra "İzle"yi seçin
2. Bir bölüm seçin
3. Akış kalitesini seçin
4. Video MPV oynatıcıda açılacak

### İndirme

1. Bir anime seçtikten sonra "İndir"i seçin
2. İndirilecek bölümleri seçin (tekli, aralık veya tümü)
3. İndirmeler kuyruğa eklenir
4. "İndirmeler" menüsünden ilerlemeyi izleyin

### İndirmeleri Yönetme

İndirmeler menüsüne erişerek:

- İlerlemeli aktif indirmeleri görüntüleyin
- İndirmeleri duraklatın/devam ettirin
- Başarısız indirmeleri yeniden deneyin
- Tamamlanan indirmeleri temizleyin

## Yaygın Görevler

### İzleme Geçmişini Görüntüleme

```
Ana Menü → İzleme Listesi → Geçmişi Görüntüle
```

İzleme geçmişiniz şunları gösterir:
- Son izlenen animeler
- Bölüm ilerlemesi
- Tamamlanma durumu

### Takipçileri Yapılandırma

```
Ana Menü → Ayarlar → Takipçiler
```

Hesaplarınızı bağlayın:
- AniList (OAuth)
- MyAnimeList (OAuth)
- Kitsu (E-posta/Şifre)

İlerleme, izlerken veya indirirken otomatik olarak senkronize edilir.

### Yerel Kütüphaneyi Yönetme

```
Ana Menü → Kütüphane → Kütüphaneyi Tara
```

Weeb CLI, indirilen animelerinizi indeksleyebilir:
- Dosya adlarından animeleri otomatik algılama
- Takipçilerle senkronizasyon
- Çevrimdışı içeriğe göz atma

## Klavye Kısayolları

- `Ctrl+C`: Mevcut işlemi iptal et / Geri dön
- `↑/↓`: Menülerde gezin
- `Enter`: Seçeneği seç
- `Boşluk`: Seçimi değiştir (çoklu seçim)

## API Modu

Betik yazma ve otomasyon için:

```bash
# Anime ara
weeb-cli api search "One Piece" --provider animecix

# Bölümleri al
weeb-cli api episodes <anime-id> --provider animecix

# Akış bağlantılarını al
weeb-cli api streams <anime-id> <episode-id> --provider animecix
```

Çıktı, kolay ayrıştırma için JSON formatındadır.

## İpuçları

1. **İzlemeye Devam Et**: Weeb CLI konumunuzu otomatik olarak kaydeder. Devam etmek için aynı bölümü seçmeniz yeterlidir.

2. **Kalite Seçimi**: Daha yüksek kaliteli akışlar yavaş bağlantılarda tamponlanabilir. Sorun yaşıyorsanız daha düşük bir kalite deneyin.

3. **İndirme Kuyruğu**: Birden fazla anime ve bölümü kuyruğa alabilirsiniz. Ayarlarınıza göre eşzamanlı olarak indirileceklerdir.

4. **Harici Sürücüler**: USB sürücülerden veya harici HDD'lerden anime taramak için ayarlarda harici sürücüler ekleyin.

5. **Çevrimdışı Mod**: İndirilen animeler ve yerel kütüphane internet bağlantısı olmadan çalışır.

## Sorun Giderme

### Video Oynatılmıyor
- MPV'nin kurulu olduğundan emin olun (ilk çalıştırmada otomatik kurulur)
- İnternet bağlantınızı kontrol edin
- Farklı bir akış kalitesi veya sunucu deneyin

### İndirme Başarısız Oluyor
- Kullanılabilir disk alanını kontrol edin
- İnternet bağlantısını doğrulayın
- Farklı bir sağlayıcı deneyin
- İndirme ayarlarını kontrol edin (Aria2/yt-dlp)

### Takipçi Senkronize Olmuyor
- Ayarlar → Takipçiler'de yeniden kimlik doğrulayın
- İnternet bağlantısını kontrol edin
- Anime başlığının takipçi veritabanıyla eşleştiğini doğrulayın

## Sonraki Adımlar

- [Yapılandırma Kılavuzu](configuration.md): Weeb CLI'yi özelleştirin
- [Kullanım Kılavuzu](../user-guide/searching.md): Ayrıntılı özellik dokümantasyonu
- [CLI Referansı](../cli/commands.md): Komut satırı seçenekleri
