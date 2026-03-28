# Local Library Service

Lokalne indeksowanie i zarządzanie anime.

## Przegląd

Usługa Local Library zapewnia:
- Automatyczne skanowanie anime
- Wykrywanie odcinków
- Obsługę dysków zewnętrznych
- Synchronizację z trackerami

## Funkcje

### Automatyczne skanowanie

Skanuje katalogi w poszukiwaniu anime:
- Wykrywa tytuły anime
- Liczy odcinki
- Dopasowuje z trackerami

### Wzorce plików

Obsługiwane wzorce nazewnictwa:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Group] Anime Name - 01.mp4`

### Dyski zewnętrzne

- Rejestruj dyski USB
- Skanuj zewnętrzne dyski HDD
- Przenośna biblioteka

## Użycie

```python
from weeb_cli.services.local_library import library

# Skanuj katalog
library.scan_directory("/path/to/anime")

# Pobierz zaindeksowane anime
anime_list = library.get_all_anime()

# Przeszukaj bibliotekę
results = library.search("Naruto")
```

## Wirtualna biblioteka

Dodaj zakładki do anime online:
- Nie wymaga pobierania
- Szybki dostęp
- Zorganizowana kolekcja

## Następne kroki

- [Przewodnik biblioteki](../../user-guide/library.md): Przewodnik użytkownika
- [Konfiguracja](../../getting-started/configuration.md): Ustawienia
