# Przewodnik po ustawieniach

Kompletny przewodnik po konfigurowaniu Weeb CLI według własnych preferencji.

## Dostęp do ustawień

Menu główne → Ustawienia

## Ustawienia ogólne

### Język

Zmień język interfejsu:
- Türkçe (turecki)
- English (angielski)
- Deutsch (niemiecki)
- Polski

Ścieżka: Ustawienia → Konfiguracja → Język

### Domyślny dostawca

Ustaw preferowane źródło anime:
- Na podstawie Twojego języka
- Można zmienić ręcznie

Ścieżka: Ustawienia → Konfiguracja → Domyślny dostawca

### Pokaż opisy

Przełącz opisy anime w wyszukiwaniu:
- Włączone: Pokazuje pełne streszczenie
- Wyłączone: Widok kompaktowy

Ścieżka: Ustawienia → Konfiguracja → Pokaż opisy

### Tryb debugowania

Włącz szczegółowe logowanie:
- Logi zapisywane w ~/.weeb-cli/logs/
- Przydatne do rozwiązywania problemów
- Może wpłynąć na wydajność

Ścieżka: Ustawienia → Konfiguracja → Tryb debugowania

## Ustawienia pobierania

### Katalog pobierania

Ustaw, gdzie zapisywane są pliki anime:
- Domyślnie: ./weeb-downloads
- Może być dowolna zapisywalna ścieżka
- Obsługuje ścieżki względne i bezwzględne

Ścieżka: Ustawienia → Pobieranie → Katalog pobierania

### Ustawienia Aria2

Skonfiguruj program pobierający Aria2:
- Włącz/Wyłącz Aria2
- Maks. połączenia (1-32)
- Domyślnie: 16 połączeń

Ścieżka: Ustawienia → Pobieranie → Aria2

### Ustawienia yt-dlp

Skonfiguruj yt-dlp:
- Włącz/Wyłącz yt-dlp
- Ciąg formatu
- Domyślnie: bestvideo+bestaudio/best

Ścieżka: Ustawienia → Pobieranie → yt-dlp

### Równoczesne pobieranie

Maks. jednoczesne pobieranie:
- Zakres: 1-10
- Domyślnie: 3
- Wyższe zużywa więcej przepustowości

Ścieżka: Ustawienia → Pobieranie → Równoczesne

### Ustawienia ponownych prób

Skonfiguruj ponowne próby pobierania:
- Maks. ponownych prób: 0-10
- Opóźnienie ponownej próby: 1-60 sekund
- Wykładniczy backoff

Ścieżka: Ustawienia → Pobieranie → Ponowna próba

## Ustawienia trackerów

### AniList

Skonfiguruj integrację AniList:
- Uwierzytelnij za pomocą OAuth
- Zobacz status połączenia
- Rozłącz konto

Ścieżka: Ustawienia → Trackery → AniList

### MyAnimeList

Skonfiguruj integrację MAL:
- Uwierzytelnij za pomocą OAuth
- Zobacz status synchronizacji
- Rozłącz konto

Ścieżka: Ustawienia → Trackery → MyAnimeList

### Kitsu

Skonfiguruj integrację Kitsu:
- Zaloguj się za pomocą e-mail/hasła
- Zobacz status połączenia
- Wyloguj się

Ścieżka: Ustawienia → Trackery → Kitsu

## Ustawienia integracji

### Discord Rich Presence

Pokaż na Discordzie, co oglądasz:
- Włącz/Wyłącz
- Pokazuje tytuł anime
- Pokazuje numer odcinka
- Pokazuje upłynięty czas

Ścieżka: Ustawienia → Integracje → Discord RPC

### AniSkip Auto Pomijanie

Automatycznie pomijaj czołówki i napisy końcowe anime:
- Włącz/Wyłącz
- Używa API AniSkip
- Pobiera czasy pomijania z MyAnimeList
- Automatycznie przewija podczas odtwarzania
- Obsługuje typy OP, ED i mixed-OP

Ścieżka: Ustawienia → Integracje → Auto Pomijanie

### Skróty klawiszowe

Globalne skróty klawiszowe (eksperymentalne):
- Włącz/Wyłącz
- Skonfiguruj skróty
- Sterowanie systemowe

Ścieżka: Ustawienia → Integracje → Skróty

## Ustawienia pamięci podręcznej

### Zobacz statystyki pamięci podręcznej

Zobacz informacje o pamięci podręcznej:
- Wpisy w pamięci
- Wpisy w plikach
- Całkowity rozmiar

Ścieżka: Ustawienia → Pamięć podręczna → Statystyki

### Wyczyść pamięć podręczną

Usuń dane z pamięci podręcznej:
- Wyczyść całą pamięć podręczną
- Wyczyść pamięć podręczną dostawcy
- Wyczyść historię wyszukiwania

Ścieżka: Ustawienia → Pamięć podręczna → Wyczyść

### Czyszczenie pamięci podręcznej

Usuń stare wpisy pamięci podręcznej:
- Ustaw maksymalny wiek
- Automatyczne czyszczenie
- Ręczne czyszczenie

Ścieżka: Ustawienia → Pamięć podręczna → Czyszczenie

## Dyski zewnętrzne

### Dodaj dysk

Zarejestruj dyski zewnętrzne:
1. Ustawienia → Dyski zewnętrzne
2. Wybierz "Dodaj dysk"
3. Wprowadź ścieżkę
4. Nadaj nazwę

### Zarządzaj dyskami

- Zobacz wszystkie dyski
- Usuń dyski
- Zmień nazwę dysków
- Skanuj dyski

Ścieżka: Ustawienia → Dyski zewnętrzne

## Kopia zapasowa i przywracanie

### Utwórz kopię zapasową

Utwórz kopię zapasową swoich danych:
- Konfiguracja
- Postęp oglądania
- Kolejka pobierania
- Indeks biblioteki

Ścieżka: Ustawienia → Kopia zapasowa → Utwórz kopię zapasową

### Przywróć kopię zapasową

Przywróć z kopii zapasowej:
1. Ustawienia → Kopia zapasowa → Przywróć
2. Wybierz plik kopii zapasowej
3. Potwierdź przywracanie

Ostrzeżenie: Nadpisuje bieżące dane

## Ustawienia zaawansowane

### Resetuj ustawienia

Przywróć domyślne:
1. Ustawienia → Zaawansowane
2. Wybierz "Resetuj wszystkie ustawienia"
3. Potwierdź reset

Ostrzeżenie: Nie można cofnąć

### Eksportuj ustawienia

Eksportuj konfigurację:
- Format JSON
- Zawiera wszystkie ustawienia
- Wyklucza dane uwierzytelniające

Ścieżka: Ustawienia → Zaawansowane → Eksportuj

### Importuj ustawienia

Importuj konfigurację:
1. Ustawienia → Zaawansowane → Importuj
2. Wybierz plik JSON
3. Potwierdź import

## Plik konfiguracyjny

Ustawienia przechowywane w:
```
~/.weeb-cli/weeb.db
```

Baza danych SQLite z tabelami:
- config
- progress
- download_queue
- external_drives
- anime_index

## Wskazówki

1. Utwórz kopię zapasową przed większymi zmianami
2. Testuj ustawienia z pojedynczym pobieraniem
3. Włącz debugowanie do rozwiązywania problemów
4. Używaj dysków zewnętrznych dla dużych kolekcji
5. Regularnie synchronizuj trackery

## Następne kroki

- [Przewodnik konfiguracji](../getting-started/configuration.md): Szczegółowe opcje konfiguracji
- [Przewodnik pobierania](downloading.md): Optymalizuj pobieranie
- [Przewodnik trackerów](trackers.md): Skonfiguruj trackery
