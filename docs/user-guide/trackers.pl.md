# Integracja trackerów

Synchronizuj postęp oglądania anime z AniList, MyAnimeList i Kitsu.

## Obsługiwane trackery

### AniList

- Uwierzytelnianie OAuth
- Automatyczna synchronizacja postępu
- Śledzenie mangi i anime
- Funkcje społecznościowe

### MyAnimeList

- Uwierzytelnianie OAuth
- Kompleksowa baza danych
- Funkcje społecznościowe
- Rekomendacje

### Kitsu

- Uwierzytelnianie email/hasło
- Nowoczesny interfejs
- Funkcje społecznościowe
- Śledzenie postępu

## Konfigurowanie trackerów

### Konfiguracja AniList

1. Ustawienia → Trackery → AniList
2. Wybierz "Uwierzytelnij"
3. Przeglądarka otwiera się dla OAuth
4. Autoryzuj aplikację
5. Wróć do CLI (automatyczne wykrywanie)

### Konfiguracja MyAnimeList

1. Ustawienia → Trackery → MyAnimeList
2. Wybierz "Uwierzytelnij"
3. Przeglądarka otwiera się dla OAuth
4. Autoryzuj aplikację
5. Wróć do CLI

### Konfiguracja Kitsu

1. Ustawienia → Trackery → Kitsu
2. Wprowadź email
3. Wprowadź hasło
4. Dane uwierzytelniające są bezpiecznie zapisywane

## Synchronizacja postępu

### Automatyczna synchronizacja

Postęp synchronizuje się automatycznie:
- Podczas oglądania anime (przy 80% ukończenia)
- Podczas pobierania odcinków
- Podczas skanowania lokalnej biblioteki
- Podczas uruchamiania aplikacji

### Ręczna synchronizacja

Wymuś synchronizację:
1. Ustawienia → Trackery
2. Wybierz tracker
3. Wybierz "Synchronizuj teraz"

### Kolejka offline

Gdy offline:
- Aktualizacje są kolejkowane lokalnie
- Synchronizowane po przywróceniu połączenia
- Żaden postęp nie jest tracony

## Dopasowywanie anime

### Automatyczne dopasowanie

Weeb CLI automatycznie dopasowuje:
- Według tytułu anime
- Według alternatywnych tytułów
- Według roku i typu

### Dokładność dopasowania

Popraw dopasowanie:
- Używaj dokładnych tytułów
- Dołącz rok w wyszukiwaniu
- Używaj angielskich tytułów, gdy to możliwe

### Ręczne dopasowanie

Jeśli automatyczne dopasowanie zawiedzie:
1. Lista obserwowanych → Wybierz anime
2. Wybierz "Połącz z trackerem"
3. Przeszukaj bazę danych trackera
4. Wybierz prawidłowe dopasowanie

## Zarządzanie trackerami

### Wyświetl status

Sprawdź status trackera:
- Status uwierzytelnienia
- Czas ostatniej synchronizacji
- Oczekujące aktualizacje
- Błędy synchronizacji

Dostęp: Ustawienia → Trackery → Status

### Rozłącz

Usuń tracker:
1. Ustawienia → Trackery
2. Wybierz tracker
3. Wybierz "Rozłącz"
4. Potwierdź usunięcie

### Ponowne uwierzytelnienie

Jeśli token wygaśnie:
1. Ustawienia → Trackery
2. Wybierz tracker
3. Wybierz "Ponownie uwierzytelnij"

## Funkcje trackerów

### Aktualizacje postępu

Automatycznie aktualizuje:
- Bieżący odcinek
- Status oglądania (oglądanie/ukończone/porzucone)
- Ocena (jeśli ustawiona)
- Liczba obejrzeń

### Zarządzanie statusem

Ustaw status anime:
- Oglądanie
- Ukończone
- Wstrzymane
- Porzucone
- Planowane do obejrzenia

### Ocenianie

Oceń anime:
- Skala 1-10 (AniList/Kitsu)
- Skala 1-10 (MyAnimeList)
- Aktualizuje na trackerze

## Prywatność

### Udostępniane dane

Udostępnia tylko:
- Postęp oglądania
- Numery odcinków
- Status ukończenia
- Oceny (jeśli ustawione)

### Nieudostępniane dane

Nigdy nie udostępnia:
- Pobrane pliki
- Źródła strumieni
- Historia wyszukiwania
- Lokalne ścieżki

## Rozwiązywanie problemów

### Uwierzytelnienie nie powiodło się

1. Sprawdź połączenie internetowe
2. Zweryfikuj dane uwierzytelniające
3. Spróbuj ponownie uwierzytelnić
4. Sprawdź status strony trackera

### Postęp się nie synchronizuje

1. Sprawdź połączenie z trackerem
2. Zweryfikuj, czy anime jest dopasowane
3. Sprawdź kolejkę offline
4. Ręczna synchronizacja

### Nieprawidłowe anime dopasowane

1. Odłącz bieżące dopasowanie
2. Ręcznie przeszukaj tracker
3. Wybierz prawidłowe anime
4. Potwierdź dopasowanie

### Błędy synchronizacji

Sprawdź logi:
```bash
~/.weeb-cli/logs/debug.log
```

Włącz tryb debugowania:
Ustawienia → Konfiguracja → Tryb debugowania

## Wiele trackerów

### Używanie wielu

Możesz używać wszystkich trzech trackerów jednocześnie:
- Postęp synchronizuje się ze wszystkimi
- Niezależne uwierzytelnianie
- Oddzielne kolejki offline

### Priorytet synchronizacji

W przypadku konfliktów:
1. Najnowsza aktualizacja wygrywa
2. Ręczne aktualizacje nadpisują automatyczne
3. Sprawdź każdy tracker osobno

## Najlepsze praktyki

1. Uwierzytelnij się we wszystkich używanych trackerach
2. Używaj spójnych tytułów anime
3. Regularnie sprawdzaj status synchronizacji
4. Okresowo czyść kolejkę offline
5. Ponownie uwierzytelnij, jeśli problemy się utrzymują

## Następne kroki

- [Przewodnik listy obserwowanych](../cli/commands.md): Zarządzaj historią oglądania
- [Przewodnik biblioteki](library.md): Synchronizacja lokalnej biblioteki
- [Konfiguracja](../getting-started/configuration.md): Ustawienia trackerów
