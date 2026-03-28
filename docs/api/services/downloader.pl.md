# Downloader Service

Menedżer pobierania oparty na kolejce z wieloma metodami pobierania.

## Przegląd

Usługa Downloader zapewnia:
- Zarządzanie pobieraniem oparte na kolejce
- Współbieżne pobieranie
- Wiele metod pobierania (Aria2, yt-dlp, FFmpeg)
- Automatyczne ponawianie z wycofywaniem
- Śledzenie postępu

## QueueManager

Główny menedżer kolejki pobierania.

### Metody

- `start_queue()`: Uruchom workery pobierania
- `stop_queue()`: Zatrzymaj wszystkie pobierania
- `add_to_queue()`: Dodaj odcinki do kolejki
- `retry_failed()`: Ponów nieudane pobierania
- `clear_completed()`: Usuń ukończone elementy

## Metody pobierania

### Kolejność priorytetów

1. Aria2 (najszybszy, wielopołączeniowy)
2. yt-dlp (złożone strumienie)
3. FFmpeg (konwersja HLS)
4. Generic HTTP (zapasowy)

## Użycie

```python
from weeb_cli.services.downloader import queue_manager

# Uruchom kolejkę
queue_manager.start_queue()

# Dodaj do kolejki
queue_manager.add_to_queue(
    anime_title="Nazwa anime",
    episodes=[episode_data],
    slug="anime-slug"
)

# Sprawdź status
if queue_manager.is_running():
    print("Kolejka aktywna")
```

## Konfiguracja

- Maksymalna liczba współbieżnych pobrań
- Połączenia Aria2
- Próby ponawiania
- Opóźnienie ponawiania

## Następne kroki

- [Przewodnik pobierania](../../user-guide/downloading.md): Przewodnik użytkownika
- [Konfiguracja](../../getting-started/configuration.md): Ustawienia
