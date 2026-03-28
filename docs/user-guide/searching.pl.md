# Wyszukiwanie anime

Dowiedz się, jak wyszukiwać anime u wielu dostawców i znajdować to, co chcesz obejrzeć.

## Podstawowe wyszukiwanie

### Z menu głównego

1. Uruchom Weeb CLI: `weeb-cli`
2. Wybierz "Szukaj anime" z menu głównego
3. Wprowadź zapytanie wyszukiwania
4. Przeglądaj wyniki

### Wskazówki dotyczące wyszukiwania

- Używaj angielskich lub rodzimych tytułów
- Spróbuj alternatywnych pisowni, jeśli nie znaleziono
- Używaj częściowych tytułów dla szerszych wyników
- Wyszukiwanie nie rozróżnia wielkości liter

## Wyniki wyszukiwania

Wyniki wyświetlają:
- Tytuł anime
- Typ (Serial, Film, OVA itp.)
- Rok wydania
- Obraz okładki (jeśli terminal obsługuje)
- Źródło dostawcy

### Nawigacja w wynikach

- Użyj klawiszy strzałek do nawigacji
- Naciśnij Enter, aby wybrać
- Naciśnij Ctrl+C, aby wrócić

## Wybór dostawcy

### Domyślny dostawca

Domyślny dostawca jest oparty na ustawieniu języka:
- Turecki: Animecix
- Angielski: HiAnime
- Niemiecki: AniWorld
- Polski: Docchi

### Zmiana dostawcy

1. Przejdź do Ustawienia → Konfiguracja
2. Wybierz "Domyślny dostawca"
3. Wybierz spośród dostępnych dostawców

### Wyszukiwanie specyficzne dla dostawcy

Różni dostawcy mogą mieć różną zawartość:
- Spróbuj wielu dostawców, jeśli nie znaleziono
- Niektórzy dostawcy mają ekskluzywną zawartość
- Jakość i dostępność się różnią

## Historia wyszukiwania

### Wyświetlanie historii

1. Z menu głównego wybierz "Szukaj anime"
2. Naciśnij strzałkę w górę, aby zobaczyć ostatnie wyszukiwania
3. Wybierz z historii, aby powtórzyć wyszukiwanie

### Czyszczenie historii

Ustawienia → Pamięć podręczna → Wyczyść historię wyszukiwania

## Zaawansowane wyszukiwanie

### Tryb API

Do skryptowania i automatyzacji:

```bash
# Wyszukiwanie z określonym dostawcą
weeb-cli api search "One Piece" --provider animecix

# Wyjście jest w formacie JSON
weeb-cli api search "Naruto" --provider hianime | jq
```

### Filtrowanie wyników

Obecnie filtrowanie odbywa się przez dostawcę. Przyszłe wersje mogą zawierać:
- Filtrowanie gatunków
- Filtrowanie roku
- Filtrowanie typu (Serial/Film/OVA)

## Rozwiązywanie problemów

### Nie znaleziono wyników

1. Sprawdź pisownię
2. Spróbuj alternatywnego tytułu (angielski/japoński/rodzimy)
3. Spróbuj innego dostawcy
4. Sprawdź połączenie internetowe

### Wolne wyszukiwanie

1. Sprawdź prędkość sieci
2. Spróbuj innego dostawcy
3. Wyczyść pamięć podręczną: Ustawienia → Pamięć podręczna → Wyczyść pamięć podręczną dostawcy

### Błędy dostawcy

Jeśli dostawca zawiedzie:
1. Spróbuj innego dostawcy
2. Sprawdź, czy strona dostawcy jest dostępna
3. Zgłoś problem na GitHub, jeśli się utrzymuje

## Następne kroki

- [Przewodnik streamingu](streaming.md): Dowiedz się, jak oglądać anime
- [Przewodnik pobierania](downloading.md): Dowiedz się, jak pobierać anime
- [Integracja trackerów](trackers.md): Synchronizuj swój postęp
