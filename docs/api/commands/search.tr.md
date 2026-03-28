# Search Command

Etkileşimli anime arama işlevselliği.

## Genel Bakış

Search komutu şunları sağlar:
- Çoklu sağlayıcı arama
- Etkileşimli sonuçlar
- Arama geçmişi
- Hızlı erişim

## Uygulama

`weeb_cli/commands/search/` içinde bulunur:
- `search_handlers.py`: Arama mantığı
- `anime_details.py`: Detay görüntüleme
- `episode_utils.py`: Bölüm seçimi
- `stream_utils.py`: Yayın seçimi
- `watch_flow.py`: İzleme iş akışı
- `download_flow.py`: İndirme iş akışı

## Özellikler

- Sağlayıcı seçimi
- Sonuç filtreleme
- Geçmiş takibi
- Hızlı gezinme

## Sonraki Adımlar

- [Arama Rehberi](../../user-guide/searching.md): Kullanıcı rehberi
- [API Referansı](../overview.md): Tam API dokümanları
