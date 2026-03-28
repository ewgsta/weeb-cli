# Database Service

Kalıcı depolama için SQLite veritabanı yönetimi.

## Genel Bakış

Database servisi şunlar için thread-safe SQLite işlemleri sağlar:
- Yapılandırma depolama
- İzleme ilerleme takibi
- İndirme kuyruğu yönetimi
- Yerel kütüphane indeksleme
- Sanal kütüphane yer imleri

## Veritabanı Konumu

```
~/.weeb-cli/weeb.db
```

## Tablolar

- `config`: Anahtar-değer yapılandırması
- `progress`: İzleme ilerlemesi ve zaman damgaları
- `search_history`: Son aramalar
- `download_queue`: İndirme kuyruğu öğeleri
- `external_drives`: Harici sürücü yolları
- `anime_index`: Yerel anime indeksi
- `virtual_library`: Çevrimiçi anime yer imleri

## Kullanım

```python
from weeb_cli.services.database import db

# Yapılandırma
db.set_config("key", "value")
value = db.get_config("key")

# İlerleme
db.save_progress(slug, title, episode, total)
progress = db.get_progress(slug)

# Kuyruk
db.add_to_queue(item)
queue = db.get_queue()
```

## Thread Güvenliği

Veritabanı şunları kullanır:
- Thread güvenliği için RLock
- Eşzamanlı erişim için WAL modu
- Bağlantı havuzu
- Meşgul durumunda otomatik yeniden deneme

## Sonraki Adımlar

- [API Referansı](../overview.md): Tam API dokümanları
- [Yapılandırma](../../getting-started/configuration.md): Yapılandırma rehberi
