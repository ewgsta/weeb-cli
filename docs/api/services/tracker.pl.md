# Tracker Service

Integracja z AniList, MyAnimeList i Kitsu.

## Przegląd

Usługa Tracker zapewnia:
- Uwierzytelnianie OAuth
- Synchronizację postępu
- Kolejkę offline
- Automatyczne dopasowywanie

## Obsługiwane trackery

### AniList

- OAuth 2.0
- GraphQL API
- Manga i anime

### MyAnimeList

- OAuth 2.0
- REST API
- Kompleksowa baza danych

### Kitsu

- E-mail/hasło
- JSON API
- Nowoczesny interfejs

## Użycie

```python
from weeb_cli.services.tracker import tracker

# Uwierzytelnij
tracker.authenticate_anilist()

# Zaktualizuj postęp
tracker.update_progress(
    anime_id="123",
    episode=5,
    status="CURRENT"
)

# Synchronizuj kolejkę offline
tracker.sync_offline_queue()
```

## Funkcje

- Automatyczna synchronizacja postępu
- Kolejka offline dla aktualizacji
- Inteligentne dopasowywanie anime
- Obsługa wielu trackerów

## Następne kroki

- [Przewodnik trackerów](../../user-guide/trackers.md): Przewodnik użytkownika
- [Konfiguracja](../../getting-started/configuration.md): Konfiguracja
