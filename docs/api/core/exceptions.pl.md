# Moduł wyjątków

::: weeb_cli.exceptions
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Przegląd

Niestandardowa hierarchia wyjątków dla strukturalnej obsługi błędów w całym Weeb CLI. Wszystkie wyjątki dziedziczą z klasy bazowej `WeebCLIError`.

## Hierarchia wyjątków

```
WeebCLIError (bazowy)
├── ProviderError
├── DownloadError
├── NetworkError
├── AuthenticationError
├── DatabaseError
├── ValidationError
└── DependencyError
```

## Przykłady użycia

### Wyrzucanie wyjątków

```python
from weeb_cli.exceptions import ProviderError, DownloadError

# Tylko z wiadomością
raise ProviderError("Nie udało się pobrać szczegółów anime")

# Z kodem błędu
raise ProviderError("Wyszukiwanie nie powiodło się", code="PROVIDER_001")

# Błędy pobierania
raise DownloadError("Niewystarczająca przestrzeń dyskowa", code="DISK_FULL")
```

### Łapanie wyjątków

```python
from weeb_cli.exceptions import (
    ProviderError, 
    NetworkError, 
    WeebCLIError
)

try:
    provider.search("anime")
except ProviderError as e:
    print(f"Błąd dostawcy: {e.message} ({e.code})")
except NetworkError as e:
    print(f"Błąd sieci: {e.message}")
except WeebCLIError as e:
    print(f"Ogólny błąd: {e}")
```

### Specyficzna obsługa wyjątków

```python
from weeb_cli.exceptions import (
    AuthenticationError,
    DatabaseError,
    ValidationError
)

# Uwierzytelnianie
try:
    tracker.authenticate()
except AuthenticationError as e:
    print(f"Uwierzytelnianie nie powiodło się: {e.message}")
    # Ponowne uwierzytelnienie

# Baza danych
try:
    db.save_progress()
except DatabaseError as e:
    print(f"Błąd bazy danych: {e.code}")
    # Ponów próbę lub utwórz kopię zapasową

# Walidacja
try:
    validate_input(user_input)
except ValidationError as e:
    print(f"Nieprawidłowe dane wejściowe: {e.message}")
    # Zapytaj ponownie
```

## Typy wyjątków

### WeebCLIError

Bazowy wyjątek dla wszystkich błędów Weeb CLI. Zapewnia strukturalną obsługę błędów z opcjonalnymi kodami błędów.

**Atrybuty:**
- `message` (str): Czytelna dla człowieka wiadomość o błędzie
- `code` (str): Opcjonalny kod błędu do kategoryzacji

### ProviderError

Wyrzucany dla błędów związanych z dostawcą anime:
- Niepowodzenia wyszukiwania
- Nie udało się pobrać szczegółów anime
- Lista odcinków niedostępna
- Błędy ekstrakcji strumienia

### DownloadError

Wyrzucany dla niepowodzeń operacji pobierania:
- Problemy sieciowe podczas pobierania
- Niewystarczająca przestrzeń dyskowa
- Nieprawidłowe adresy URL strumieni
- Błędy Aria2/yt-dlp

### NetworkError

Wyrzucany dla problemów z połączeniem sieciowym:
- Niepowodzenia żądań HTTP
- Przekroczenia limitu czasu połączenia
- Błędy rozwiązywania DNS
- Sieć niedostępna

### AuthenticationError

Wyrzucany dla niepowodzeń uwierzytelniania trackera:
- Błędy przepływu OAuth
- Nieprawidłowe poświadczenia
- Wygaśnięcie tokenu
- Niepowodzenia uwierzytelniania API

### DatabaseError

Wyrzucany dla błędów operacji bazy danych:
- Błędy SQLite
- Uszkodzenie bazy danych
- Niepowodzenia migracji
- Błędy zapytań

### ValidationError

Wyrzucany dla niepowodzeń walidacji danych wejściowych:
- Nieprawidłowe wartości konfiguracji
- Źle sformatowane dane wejściowe użytkownika
- Nieprawidłowe ścieżki plików
- Błędy walidacji URL

### DependencyError

Wyrzucany dla problemów z zależnościami zewnętrznymi:
- Brakujące wymagane narzędzia (FFmpeg, MPV, Aria2)
- Niepowodzenia wykonania narzędzi
- Niezgodności wersji
- Błędy instalacji

## Kody błędów

Typowe kody błędów używane w całej aplikacji:

| Kod | Wyjątek | Opis |
|-----|---------|------|
| `PROVIDER_001` | ProviderError | Wyszukiwanie nie powiodło się |
| `PROVIDER_002` | ProviderError | Pobieranie szczegółów nie powiodło się |
| `PROVIDER_003` | ProviderError | Ekstrakcja strumienia nie powiodła się |
| `DOWNLOAD_001` | DownloadError | Niewystarczająca przestrzeń dyskowa |
| `DOWNLOAD_002` | DownloadError | Pobieranie nie powiodło się |
| `NETWORK_001` | NetworkError | Przekroczenie limitu czasu połączenia |
| `AUTH_001` | AuthenticationError | OAuth nie powiodło się |
| `DB_001` | DatabaseError | Zapytanie nie powiodło się |
| `VALIDATION_001` | ValidationError | Nieprawidłowe dane wejściowe |
| `DEP_001` | DependencyError | Brakujące narzędzie |

## Najlepsze praktyki

1. **Używaj specyficznych wyjątków**: Łap specyficzne wyjątki przed ogólnymi
2. **Dołączaj kody błędów**: Używaj kodów błędów do logowania i debugowania
3. **Zapewnij kontekst**: Dołącz istotne informacje w wiadomościach o błędach
4. **Obsługuj łagodnie**: Zapewnij zachowanie awaryjne, gdy to możliwe
5. **Loguj błędy**: Loguj wyjątki z pełnym kontekstem do debugowania

## Dokumentacja API

::: weeb_cli.exceptions.WeebCLIError
::: weeb_cli.exceptions.ProviderError
::: weeb_cli.exceptions.DownloadError
::: weeb_cli.exceptions.NetworkError
::: weeb_cli.exceptions.AuthenticationError
::: weeb_cli.exceptions.DatabaseError
::: weeb_cli.exceptions.ValidationError
::: weeb_cli.exceptions.DependencyError
