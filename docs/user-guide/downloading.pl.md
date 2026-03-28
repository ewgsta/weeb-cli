# Zarządzanie pobieraniem

Dowiedz się, jak pobierać anime do oglądania offline za pomocą potężnego systemu pobierania Weeb CLI.

## Rozpoczynanie pobierania

### Z wyszukiwania

1. Wyszukaj anime
2. Wybierz anime
3. Wybierz opcję "Pobierz"
4. Wybierz odcinki:
   - Pojedynczy odcinek
   - Zakres odcinków (np. 1-12)
   - Wszystkie odcinki
5. Pobierania dodane do kolejki

### Z listy obserwowanych

1. Menu główne → Lista obserwowanych
2. Wybierz anime
3. Wybierz "Pobierz odcinki"
4. Wybierz odcinki

## Kolejka pobierania

### Wyświetlanie kolejki

Menu główne → Pobierania

Pokazuje:
- Aktywne pobierania z postępem
- Oczekujące pobierania
- Ukończone pobierania
- Nieudane pobierania

### Informacje o kolejce

Dla każdego pobierania:
- Tytuł anime i odcinek
- Procent postępu
- Prędkość pobierania
- Szacowany czas
- Status (oczekujące/przetwarzanie/ukończone/nieudane)

## Zarządzanie pobieraniami

### Wstrzymaj/Wznów

Kolejka może być:
- Wstrzymana: Zatrzymuje wszystkie aktywne pobierania
- Wznowiona: Kontynuuje od miejsca zatrzymania

### Ponów nieudane

Jeśli pobierania się nie powiodą:
1. Przejdź do menu Pobierania
2. Wybierz "Ponów nieudane"
3. Nieudane pobierania się restartują

### Wyczyść ukończone

Usuń ukończone pobierania z kolejki:
1. Menu Pobierania
2. Wybierz "Wyczyść ukończone"

## Metody pobierania

Weeb CLI używa wielu metod pobierania z automatycznym fallbackiem:

### 1. Aria2 (Najszybsza)

- Pobierania wielopołączeniowe
- Obsługa wznawiania
- Śledzenie postępu
- Domyślnie: 16 połączeń

Konfiguruj: Ustawienia → Pobierania → Ustawienia Aria2

### 2. yt-dlp

- Obsługa złożonych strumieni
- Wybór formatu
- Pobieranie napisów
- Fallback dla strumieni HLS

Konfiguruj: Ustawienia → Pobierania → Ustawienia yt-dlp

### 3. FFmpeg

- Konwersja strumieni HLS
- Konwersja formatu
- Metoda fallback

### 4. Ogólny HTTP

- Proste pobierania HTTP
- Ostatnia deska ratunku

## Ustawienia pobierania

### Równoczesne pobierania

Maksymalna liczba jednoczesnych pobierań:
- Domyślnie: 3
- Zakres: 1-10
- Wyższe = szybsze, ale więcej zasobów

Ustawienia → Pobierania → Równoczesne pobierania

### Katalog pobierania

Ustaw, gdzie pliki są zapisywane:
- Domyślnie: `./weeb-downloads`
- Może być dowolnym zapisywalnym katalogiem

Ustawienia → Pobierania → Katalog pobierania

### Ustawienia ponownych prób

Skonfiguruj zachowanie ponownych prób:
- Maks. ponownych prób: 0-10 (domyślnie: 3)
- Opóźnienie ponownej próby: 1-60 sekund (domyślnie: 10)

Ustawienia → Pobierania → Ustawienia ponownych prób

## Nazewnictwo plików

### Format domyślny

```
Nazwa Anime - S1E1.mp4
Nazwa Anime - S1E2.mp4
```

### Niestandardowe nazewnictwo

Pliki są automatycznie nazywane:
- Oczyszczone dla systemu plików
- Numery sezonu i odcinka
- Rozszerzenie .mp4

## Problemy z pobieraniem

### Niewystarczające miejsce na dysku

Weeb CLI sprawdza dostępne miejsce przed pobieraniem:
- Wymaga minimum 1GB wolnego
- Pokazuje błąd, jeśli niewystarczające
- Zwolnij miejsce lub zmień katalog

### Pobieranie się nie powiodło

Częste przyczyny:
1. Przerwanie sieci
2. Nieprawidłowy URL strumienia
3. Problemy z dostawcą
4. Miejsce na dysku

Rozwiązania:
1. Ponów pobieranie
2. Spróbuj innej jakości
3. Spróbuj innego dostawcy
4. Sprawdź logi dla szczegółów

### Wolne pobierania

Popraw prędkość:
1. Włącz Aria2
2. Zwiększ maks. połączenia
3. Sprawdź prędkość sieci
4. Spróbuj innego serwera

### Wznów przerwane

Pobierania automatycznie się wznawiają:
- Aria2 obsługuje wznawianie
- Częściowe pliki są zachowane
- Kontynuuje od ostatniego bajtu

## Zaawansowane funkcje

### Pobierania wsadowe

Pobierz wiele anime:
1. Wyszukaj i dodaj do kolejki
2. Powtórz dla innych anime
3. Wszystkie pobierają się równocześnie

### Preferencja jakości

Weeb CLI automatycznie wybiera:
- Najwyższą dostępną jakość
- Najlepszy dostępny serwer
- Fallback na niższą jakość w razie potrzeby

### Powiadomienia o postępie

Powiadomienia systemowe gdy:
- Pobieranie się kończy
- Pobieranie się nie powiodło
- Kolejka się kończy

Włącz: Ustawienia → Powiadomienia

## Monitorowanie pobierań

### Postęp w czasie rzeczywistym

Menu Pobierania pokazuje:
- Bieżącą prędkość (MB/s)
- Pobrano rozmiar / Całkowity rozmiar
- Pasek postępu
- Szacowany czas

### Statystyki pobierania

Po ukończeniu:
- Całkowicie pobrano
- Średnia prędkość
- Zajęty czas
- Wskaźnik sukcesu

## Wskazówki

1. Włącz Aria2 dla najszybszych pobierań
2. Pobieraj poza godzinami szczytu
3. Używaj zakresów odcinków dla pobierań wsadowych
4. Regularnie monitoruj miejsce na dysku
5. Ponów nieudane pobierania przed rezygnacją

## Następne kroki

- [Lokalna biblioteka](library.md): Zarządzaj pobranymi anime
- [Integracja trackerów](trackers.md): Synchronizuj postęp pobierania
- [Konfiguracja](../getting-started/configuration.md): Optymalizuj ustawienia
