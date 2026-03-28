# Przegląd architektury

Ten dokument zapewnia ogólny przegląd architektury i decyzji projektowych Weeb CLI.

## Architektura systemu

```
┌─────────────────────────────────────────────────────────┐
│                  Warstwa CLI (Typer)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Wyszukiw. │  │Pobieranie│  │Lista     │  │Ustawienia│ │
│  │          │  │          │  │oglądania │  │         │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                   Warstwa serwisów                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Pobieracz │  │ Tracker  │  │  Odtwarz.│  │  Cache  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Baza danych│  │ Scraper  │  │  Logger  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                 Warstwa dostawców                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ Tureccy  │  │Angielscy │  │ Niemieccy│  │ Polscy  │ │
│  │Dostawcy  │  │Dostawcy  │  │Dostawcy  │  │Dostawcy │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Warstwa danych                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  SQLite  │  │   Cache  │  │   Logi   │              │
│  │Baza danych│  │  Pliki   │  │  Pliki   │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## Wzorce projektowe

### 1. Wzorzec rejestru (Dostawcy)

Dostawcy są automatycznie wykrywani i rejestrowane za pomocą dekoratorów:

```python
@register_provider("animecix", lang="tr", region="TR")
class AnimecixProvider(BaseProvider):
    pass
```

**Korzyści:**
- Łatwe dodawanie nowych dostawców
- Nie wymaga ręcznej rejestracji
- Automatyczne wykrywanie z systemu plików

### 2. Leniwe ładowanie (Serwisy)

Serwisy używają leniwego ładowania do odroczenia inicjalizacji:

```python
@property
def db(self):
    if self._db is None:
        from weeb_cli.services.database import db
        self._db = db
    return self._db
```

**Korzyści:**
- Szybszy czas uruchamiania
- Zmniejszone zużycie pamięci
- Unikanie cyklicznych importów

### 3. Wzorzec singletona (Instancje globalne)

Globalne instancje dla współdzielonych zasobów:

```python
config = Config()
i18n = I18n()
cache = CacheManager()
```

**Korzyści:**
- Pojedyncze źródło prawdy
- Łatwy dostęp w całej aplikacji
- Spójny stan

### 4. Wzorzec strategii (Metody pobierania)

Wiele strategii pobierania z awaryjnością:

```python
def _try_download(self, url, path, item):
    strategies = [
        self._download_aria2,
        self._download_ytdlp,
        self._download_ffmpeg,
        self._download_generic
    ]
    for strategy in strategies:
        if strategy(url, path, item):
            return True
    return False
```

**Korzyści:**
- Łagodna degradacja
- Elastyczne metody pobierania
- Łatwe dodawanie nowych strategii

## Główne komponenty

### Warstwa CLI

**Technologia:** Typer + Rich + Questionary

**Odpowiedzialności:**
- Parsowanie argumentów wiersza poleceń
- Wyświetlanie interaktywnych menu
- Obsługa wprowadzania użytkownika
- Pokazywanie wskaźników postępu

### Warstwa serwisów

**Główne serwisy:**

1. **Database**: SQLite z trybem WAL
   - Przechowywanie konfiguracji
   - Śledzenie postępu
   - Kolejka pobierania
   - Indeks lokalnej biblioteki

2. **Downloader**: Menedżer pobierania oparty na kolejce
   - Równoczesne pobieranie
   - Wiele metod pobierania
   - Logika ponownych prób
   - Śledzenie postępu

3. **Tracker**: Integracja śledzenia anime
   - Uwierzytelnianie OAuth
   - Synchronizacja postępu
   - Kolejka offline

4. **Player**: Integracja MPV
   - Komunikacja IPC
   - Monitorowanie postępu
   - Funkcja wznowienia

5. **Cache**: Dwupoziomowe buforowanie
   - Cache pamięci
   - Cache plików
   - Obsługa TTL

### Warstwa dostawców

**Struktura:**
- Katalogi zorganizowane według języka
- Interfejs bazowego dostawcy
- System rejestru
- Ekstraktory strumieni

**Cykl życia dostawcy:**
1. Wykrywanie (skanowanie systemu plików)
2. Rejestracja (dekorator)
3. Instancjacja (na żądanie)
4. Buforowanie (wyniki)

### Warstwa danych

**Przechowywanie:**
- Baza danych SQLite (~/.weeb-cli/weeb.db)
- Pliki cache (~/.weeb-cli/cache/)
- Pliki logów (~/.weeb-cli/logs/)
- Pobrane pliki binarne (~/.weeb-cli/bin/)

## Przepływ danych

### Przepływ wyszukiwania

```
Wprowadzenie użytkownika → CLI → Scraper → Dostawca → Cache → API
                                              ↓
                                          Wyniki
                                              ↓
                                       Wyświetlenie CLI
```

### Przepływ pobierania

```
Wybór użytkownika → Menedżer kolejki → Worker pobierania
                                            ↓
                                    Wypróbuj strategie
                                            ↓
                         ┌─────────────────────────┐
                         │  Aria2 → yt-dlp →       │
                         │  FFmpeg → Ogólny        │
                         └─────────────────────────┘
                                            ↓
                                    Aktualizuj postęp
                                            ↓
                                    Zapisz do bazy danych
```

### Przepływ oglądania

```
Wybór użytkownika → Ekstrakcja strumienia → Odtwarzacz (MPV)
                                                ↓
                                           Monitor IPC
                                                ↓
                                          Zapisz postęp
                                                ↓
                                        Synchronizuj tracker
```

## Bezpieczeństwo wątków

### Strategia blokowania

1. **Database**: RLock dla zarządzania połączeniami
2. **Kolejka pobierania**: Lock dla operacji kolejki
3. **Cache**: Brak blokowania (dostęp jednowątkowy)

### Operacje równoczesne

- Workery pobierania działają w oddzielnych wątkach
- Monitor MPV działa w wątku demona
- Synchronizacja trackera działa w tle

## Obsługa błędów

### Hierarchia wyjątków

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

### Odzyskiwanie po błędach

1. **Logika ponownych prób**: Wykładniczy backoff dla błędów przejściowych
2. **Awaryjność**: Alternatywne metody, gdy podstawowa zawiedzie
3. **Łagodna degradacja**: Kontynuuj z ograniczoną funkcjonalnością
4. **Powiadomienie użytkownika**: Jasne komunikaty o błędach z i18n

## Optymalizacje wydajności

### 1. Buforowanie

- Wyniki wyszukiwania buforowane przez 1 godzinę
- Szczegóły buforowane przez 6 godzin
- Dwupoziomowe (pamięć + plik) dla szybkości

### 2. Leniwe ładowanie

- Serwisy ładowane przy pierwszym użyciu
- Dostawcy wykrywani na żądanie
- Pooling połączeń bazy danych

### 3. Równoczesne pobieranie

- Wiele pobierań równolegle
- Konfigurowalny limit równoczesności
- Planowanie świadome zasobów

### 4. Optymalizacja bazy danych

- Tryb WAL dla równoczesnego dostępu
- Przygotowane instrukcje
- Indeksowane zapytania
- Operacje wsadowe

## Względy bezpieczeństwa

### 1. Sanityzacja wejścia

- Sanityzacja nazw plików
- Walidacja URL
- Zapobieganie wstrzykiwaniu SQL (zapytania parametryzowane)

### 2. Przechowywanie poświadczeń

- Tokeny OAuth w bazie danych
- Brak haseł w postaci zwykłego tekstu
- Bezpieczne odświeżanie tokenów

### 3. Bezpieczeństwo sieci

- HTTPS dla wywołań API
- Weryfikacja certyfikatów
- Limity czasu

## Rozszerzalność

### Dodawanie nowych funkcji

1. **Nowy dostawca**: Zaimplementuj interfejs BaseProvider
2. **Nowy tracker**: Zaimplementuj interfejs TrackerBase
3. **Nowe polecenie**: Dodaj polecenie Typer
4. **Nowy serwis**: Postępuj zgodnie ze wzorcem serwisu

### System wtyczek

Obecnie nie zaimplementowany, ale architektura obsługuje:
- Wtyczki dostawców
- Wtyczki ekstraktorów
- Wtyczki poleceń

## Przyszłe ulepszenia

1. **System wtyczek**: Dynamiczne ładowanie wtyczek
2. **Serwer API**: REST API do zdalnego sterowania
3. **Interfejs webowy**: Interfejs oparty na przeglądarce
4. **Aplikacja mobilna**: Towarzysząca aplikacja mobilna
5. **Synchronizacja w chmurze**: Synchronizacja między urządzeniami
