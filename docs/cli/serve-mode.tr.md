# Serve Modu - Torznab Sunucusu

Sonarr ve diğer *arr uygulamalarıyla entegrasyon için Weeb CLI'yi Torznab sunucusu olarak çalıştırın.

## Genel Bakış

Serve modu, *arr uygulamalarının Weeb CLI sağlayıcıları aracılığıyla anime aramasına ve indirmesine olanak tanıyan Torznab uyumlu bir API sunucusu sağlar.

## Sunucuyu Başlatma

```bash
weeb-cli serve [SEÇENEKLER]
```

Seçenekler:
- `--host`: Bağlanılacak host (varsayılan: 127.0.0.1)
- `--port`: Dinlenecek port (varsayılan: 8080)
- `--api-key`: Kimlik doğrulama için API anahtarı

Örnek:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080 --api-key apianahtarim123
```

## Sonarr Entegrasyonu

### İndeksleyici Ekleme

1. Sonarr → Ayarlar → İndeksleyiciler
2. Ekle → Torznab → Özel
3. Yapılandır:
   - İsim: Weeb CLI
   - URL: http://localhost:8080
   - API Anahtarı: (anahtarınız)
   - Kategoriler: 5070 (Anime)

### Bağlantıyı Test Etme

1. Sonarr'da "Test"e tıklayın
2. Başarılı göstermeli
3. İndeksleyiciyi kaydedin

## API Uç Noktaları

### Yetenekler

```
GET /api?t=caps
```

Torznab yetenekleri XML'ini döndürür.

### Arama

```
GET /api?t=search&q=SORGU&apikey=ANAHTAR
```

Başlığa göre anime arayın.

### TV Araması

```
GET /api?t=tvsearch&q=SORGU&season=1&ep=1&apikey=ANAHTAR
```

Belirli bir bölümü arayın.

## Yapılandırma

### API Anahtarı

Güvenli API anahtarı oluşturun:
```bash
openssl rand -hex 16
```

Serve komutunda ve Sonarr yapılandırmasında kullanın.

### Ağ Erişimi

Uzaktan erişim için:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080
```

Uyarı: Güvenlik duvarının düzgün yapılandırıldığından emin olun.

## Sınırlamalar

- Salt okunur (indirme yönetimi yok)
- Yalnızca arama (RSS beslemeleri yok)
- Örnek başına tek sağlayıcı
- API anahtarının ötesinde kimlik doğrulama yok

## Sonraki Adımlar

- [API Modu](api-mode.md): JSON API
- [Komutlar](commands.md): CLI referansı
