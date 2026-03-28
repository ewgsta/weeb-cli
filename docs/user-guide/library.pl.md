# Zarządzanie lokalną biblioteką

Zarządzaj swoją kolekcją pobranych anime za pomocą funkcji lokalnej biblioteki Weeb CLI.

## Przegląd

Lokalna biblioteka pozwala na:
- Indeksowanie pobranych anime
- Przeglądanie treści offline
- Synchronizację z trackerami
- Zarządzanie dyskami zewnętrznymi

## Skanowanie biblioteki

### Automatyczne skanowanie

Weeb CLI automatycznie skanuje katalog pobierania:

1. Menu główne → Biblioteka
2. Wybierz "Skanuj bibliotekę"
3. Poczekaj na zakończenie skanowania

### Wyniki skanowania

Pokazuje:
- Wykryte tytuły anime
- Liczby odcinków
- Lokalizację źródłową
- Status dopasowania trackera

### Format pliku

Dla najlepszych wyników użyj tego formatu:

```
Nazwa Anime - S1E1.mp4
Nazwa Anime - S1E2.mp4
Nazwa Anime - S2E1.mp4
```

Obsługiwane wzorce:
- `Nazwa Anime - S1E1.mp4`
- `Nazwa Anime - 01.mp4`
- `Nazwa Anime - Odcinek 1.mp4`
- `[Grupa] Nazwa Anime - 01.mp4`

## Dyski zewnętrzne

### Dodawanie dysków

Dodaj dyski USB lub zewnętrzne HDD:

1. Ustawienia → Dyski zewnętrzne
2. Wybierz "Dodaj dysk"
3. Wprowadź ścieżkę dysku
4. Nadaj nazwę

### Skanowanie dysków

1. Biblioteka → Dyski zewnętrzne
2. Wybierz dysk
3. Wybierz "Skanuj dysk"

### Zarządzanie dyskami

- Wyświetl wszystkie zarejestrowane dyski
- Usuń dyski
- Zmień nazwy dysków
- Skanuj pojedyncze dyski

## Wirtualna biblioteka

### Czym jest wirtualna biblioteka?

Dodaj zakładki do anime online dla szybkiego dostępu:
- Nie wymaga pobierania
- Szybki dostęp do ulubionych
- Zorganizowana kolekcja

### Dodawanie do wirtualnej biblioteki

1. Wyszukaj anime
2. Wyświetl szczegóły
3. Wybierz "Dodaj do biblioteki"

### Dostęp do wirtualnej biblioteki

1. Menu główne → Biblioteka
2. Wybierz "Wirtualna biblioteka"
3. Przeglądaj anime z zakładkami

## Przeglądanie biblioteki

### Lokalne anime

Wyświetl pobrane anime:
- Posortowane według tytułu
- Pokazuje liczbę odcinków
- Wskazuje status ukończenia

### Odtwarzanie z biblioteki

1. Wybierz anime
2. Wybierz odcinek
3. Odtwarza w MPV

### Statystyki biblioteki

Wyświetl statystyki:
- Całkowita liczba anime
- Całkowita liczba odcinków
- Całkowite użyte miejsce
- Najczęściej oglądane

## Synchronizacja trackerów

### Automatyczna synchronizacja

Podczas skanowania biblioteki:
- Dopasowuje anime z bazą danych trackera
- Synchronizuje postęp oglądania
- Aktualizuje status ukończenia

### Ręczna synchronizacja

Wymuś synchronizację:
1. Biblioteka → Ustawienia
2. Wybierz "Synchronizuj z trackerami"

### Dokładność dopasowania

Popraw dopasowanie:
- Używaj standardowego nazewnictwa plików
- Dołącz numery sezonów
- Używaj pełnych tytułów anime

## Organizacja biblioteki

### Struktura folderów

Zalecana struktura:

```
downloads/
├── Anime 1/
│   ├── S1E1.mp4
│   ├── S1E2.mp4
│   └── ...
├── Anime 2/
│   ├── S1E1.mp4
│   └── ...
```

### Czyszczenie

Usuń anime z indeksu:
1. Biblioteka → Zarządzaj
2. Wybierz anime
3. Wybierz "Usuń z indeksu"

Uwaga: To usuwa tylko z indeksu, nie pliki.

## Zaawansowane funkcje

### Biblioteka wieloźródłowa

Połącz anime z:
- Katalogu pobierania
- Dysków zewnętrznych
- Udziałów sieciowych (jeśli zamontowane)

### Przeszukiwanie biblioteki

Szybkie wyszukiwanie w bibliotece:
1. Menu biblioteki
2. Wpisz, aby wyszukać
3. Filtruje wyniki w czasie rzeczywistym

### Eksportowanie biblioteki

Eksportuj listę biblioteki:
1. Biblioteka → Eksportuj
2. Wybierz format (JSON/CSV)
3. Zapisz do pliku

## Rozwiązywanie problemów

### Anime nie wykryte

1. Sprawdź format nazewnictwa plików
2. Upewnij się, że pliki są w katalogu pobierania
3. Ponownie przeskanuj bibliotekę
4. Sprawdź rozszerzenia plików (.mp4, .mkv)

### Nieprawidłowa liczba odcinków

1. Zweryfikuj nazewnictwo plików
2. Sprawdź duplikaty plików
3. Ponownie przeskanuj bibliotekę

### Tracker nie pasuje

1. Użyj dokładnego tytułu anime
2. Dołącz rok w nazwie folderu
3. Ręczne dopasowanie w ustawieniach trackera

### Dysk zewnętrzny nie znaleziony

1. Sprawdź, czy dysk jest zamontowany
2. Sprawdź, czy ścieżka jest poprawna
3. Ponownie dodaj dysk w ustawieniach

## Najlepsze praktyki

1. Używaj spójnego nazewnictwa plików
2. Organizuj według folderów anime
3. Dołączaj numery sezonów
4. Skanuj po zakończeniu pobierania
5. Regularnie twórz kopie zapasowe bazy danych biblioteki

## Następne kroki

- [Integracja trackerów](trackers.md): Synchronizuj z trackerami online
- [Przewodnik pobierania](downloading.md): Pobierz więcej anime
- [Konfiguracja](../getting-started/configuration.md): Ustawienia biblioteki
