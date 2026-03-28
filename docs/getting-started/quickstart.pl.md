# Przewodnik szybkiego startu

Ten przewodnik pomoże Ci rozpocząć pracę z Weeb CLI w zaledwie kilka minut.

## Pierwsze uruchomienie

Gdy uruchomisz Weeb CLI po raz pierwszy, zostaniesz przeprowadzony przez kreatora konfiguracji:

```bash
weeb-cli
```

### Kreator konfiguracji

1. **Wybór języka**: Wybierz preferowany język (turecki, angielski, niemiecki lub polski)
2. **Katalog pobierania**: Ustaw, gdzie będą pobierane pliki anime
3. **Wybór dostawcy**: Wybierz domyślne źródło anime
4. **Ustawienia opcjonalne**: Skonfiguruj trackery, Discord RPC itp.

## Podstawowe użycie

### Wyszukiwanie anime

1. Z menu głównego wybierz "Szukaj anime"
2. Wprowadź nazwę anime
3. Przeglądaj wyniki wyszukiwania
4. Wybierz anime, aby zobaczyć szczegóły

### Streaming

1. Po wybraniu anime wybierz "Oglądaj"
2. Wybierz odcinek
3. Wybierz jakość strumienia
4. Wideo otworzy się w odtwarzaczu MPV

### Pobieranie

1. Po wybraniu anime wybierz "Pobierz"
2. Wybierz odcinki do pobrania (pojedynczy, zakres lub wszystkie)
3. Pobierania są dodawane do kolejki
4. Monitoruj postęp z menu "Pobierania"

### Zarządzanie pobieraniami

Uzyskaj dostęp do menu pobierania, aby:

- Wyświetlić aktywne pobierania z postępem
- Wstrzymać/wznowić pobierania
- Ponowić nieudane pobierania
- Wyczyścić ukończone pobierania

## Typowe zadania

### Przeglądanie historii oglądania

```
Menu główne → Lista obserwowanych → Wyświetl historię
```

Twoja historia oglądania pokazuje:
- Ostatnio oglądane anime
- Postęp odcinków
- Status ukończenia

### Konfigurowanie trackerów

```
Menu główne → Ustawienia → Trackery
```

Połącz swoje konta:
- AniList (OAuth)
- MyAnimeList (OAuth)
- Kitsu (Email/Hasło)

Postęp synchronizuje się automatycznie podczas oglądania lub pobierania.

### Zarządzanie lokalną biblioteką

```
Menu główne → Biblioteka → Skanuj bibliotekę
```

Weeb CLI może indeksować pobrane anime:
- Automatyczne wykrywanie anime z nazw plików
- Synchronizacja z trackerami
- Przeglądanie treści offline

## Skróty klawiszowe

- `Ctrl+C`: Anuluj bieżącą operację / Wróć
- `↑/↓`: Nawiguj po menu
- `Enter`: Wybierz opcję
- `Spacja`: Przełącz zaznaczenie (wielokrotny wybór)

## Tryb API

Do skryptowania i automatyzacji:

```bash
# Szukaj anime
weeb-cli api search "One Piece" --provider animecix

# Pobierz odcinki
weeb-cli api episodes <anime-id> --provider animecix

# Pobierz linki do strumieni
weeb-cli api streams <anime-id> <episode-id> --provider animecix
```

Wyjście jest w formacie JSON dla łatwego parsowania.

## Wskazówki

1. **Wznów oglądanie**: Weeb CLI automatycznie zapisuje Twoją pozycję. Po prostu wybierz ten sam odcinek, aby kontynuować.

2. **Wybór jakości**: Strumienie wyższej jakości mogą buforować się na wolniejszych połączeniach. Spróbuj niższej jakości, jeśli występują problemy.

3. **Kolejka pobierania**: Możesz kolejkować wiele anime i odcinków. Będą pobierane równocześnie na podstawie Twoich ustawień.

4. **Dyski zewnętrzne**: Dodaj dyski zewnętrzne w ustawieniach, aby skanować anime z dysków USB lub zewnętrznych HDD.

5. **Tryb offline**: Pobrane anime i lokalna biblioteka działają bez połączenia internetowego.

## Rozwiązywanie problemów

### Wideo nie odtwarza się
- Upewnij się, że MPV jest zainstalowany (automatycznie instalowany przy pierwszym uruchomieniu)
- Sprawdź połączenie internetowe
- Spróbuj innej jakości strumienia lub serwera

### Pobieranie nie powiodło się
- Sprawdź dostępne miejsce na dysku
- Zweryfikuj połączenie internetowe
- Spróbuj innego dostawcy
- Sprawdź ustawienia pobierania (Aria2/yt-dlp)

### Tracker nie synchronizuje się
- Ponownie uwierzytelnij w Ustawienia → Trackery
- Sprawdź połączenie internetowe
- Zweryfikuj, czy tytuł anime pasuje do bazy danych trackera

## Następne kroki

- [Przewodnik konfiguracji](configuration.md): Dostosuj Weeb CLI
- [Przewodnik użytkownika](../user-guide/searching.md): Szczegółowa dokumentacja funkcji
- [Dokumentacja CLI](../cli/commands.md): Opcje wiersza poleceń
