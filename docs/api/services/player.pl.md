# Player Service

Integracja odtwarzacza MPV z monitorowaniem IPC.

## Przegląd

Usługa Player zapewnia:
- Integrację odtwarzacza MPV
- Komunikację przez gniazdo IPC
- Monitorowanie postępu
- Funkcję wznowienia

## Klasa Player

Główny menedżer odtwarzacza.

### Metody

- `play()`: Rozpocznij odtwarzanie
- `is_installed()`: Sprawdź instalację MPV

## Funkcje

### Śledzenie postępu

- Zapisuje pozycję co 15 sekund
- Automatycznie oznacza jako obejrzane przy 80%
- Synchronizuje z trackerami

### Obsługa wznowienia

- Automatycznie wznawia od ostatniej pozycji
- Czyści pozycję po zakończeniu

## Użycie

```python
from weeb_cli.services.player import player

# Odtwórz strumień
player.play(
    url="https://stream-url.m3u8",
    title="Anime - Odcinek 1",
    anime_title="Nazwa anime",
    episode_number=1,
    slug="anime-slug"
)
```

## Monitorowanie IPC

Monitoruje MPV przez gniazdo IPC:
- Bieżąca pozycja
- Czas trwania
- Status odtwarzania

## Następne kroki

- [Przewodnik streamingu](../../user-guide/streaming.md): Przewodnik użytkownika
- [Konfiguracja](../../getting-started/configuration.md): Ustawienia
