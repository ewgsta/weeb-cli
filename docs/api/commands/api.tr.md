# API Commands

Etkileşimsiz JSON API komutları.

## Genel Bakış

API komutları şunlar için JSON çıktısı sağlar:
- Betikler ve otomasyon
- Araçlarla entegrasyon
- Başsız çalışma

## Komutlar

### providers

Tüm sağlayıcıları listele.

```bash
weeb-cli api providers
```

### search

Anime ara.

```bash
weeb-cli api search "query" --provider animecix
```

### episodes

Bölüm listesini al.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

### streams

Yayın URL'lerini al.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

## Uygulama

Tüm komutlar `weeb_cli/commands/api.py` içinde.

## Sonraki Adımlar

- [API Modu Rehberi](../../cli/api-mode.md): Detaylı kullanım
- [Komutlar Referansı](../../cli/commands.md): Tüm komutlar
