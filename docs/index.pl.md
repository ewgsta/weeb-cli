# Dokumentacja Weeb CLI

**Bez przeglądarki, bez reklam, bez rozpraszaczy. Tylko Ty i niezrównane doświadczenie oglądania anime.**

## Witamy

Weeb CLI to potężna aplikacja terminalowa do streamingu i pobierania anime, która zapewnia bezprzegladarkowe, wolne od reklam doświadczenie oglądania anime. Dzięki wsparciu dla wielu źródeł anime w różnych językach, zintegrowanym usługom śledzenia i zaawansowanemu zarządzaniu pobieraniem, Weeb CLI jest Twoim kompleksowym towarzyszem anime.

## Główne funkcje

### Wsparcie wielu źródeł
- Turecki: Animecix, Turkanime, Anizle, Weeb
- Angielski: HiAnime, AllAnime
- Niemiecki: AniWorld
- Polski: Docchi

### Inteligentny streaming
- Wysokiej jakości odtwarzanie HLS/MP4 z MPV
- Wznowienie od miejsca, w którym skończyłeś
- Historia oglądania i statystyki
- Śledzenie postępu odcinków

### Zaawansowane pobieranie
- Szybkie pobieranie wielopołączeniowe z Aria2
- Obsługa złożonych strumieni z yt-dlp
- System kolejki z równoczesnymi pobieraniami
- Wznawianie przerwanych pobierań
- Inteligentne nazewnictwo plików

### Integracja z trackerami
- Wsparcie dla AniList, MyAnimeList i Kitsu
- Uwierzytelnianie OAuth
- Automatyczna synchronizacja postępu
- Kolejka offline dla oczekujących aktualizacji

### Lokalna biblioteka
- Automatyczne skanowanie pobranych anime
- Obsługa dysków zewnętrznych (USB, HDD)
- Indeksowanie anime offline
- Inteligentne dopasowywanie tytułów

### Dodatkowe funkcje
- System wtyczek (Plugin System) z bezpieczną piaskownicą
- Plugin Builder do łatwego pakowania wtyczek
- Strona galerii wtyczek (Plugin Gallery)
- Wsparcie wielu języków (TR, EN, DE, PL)
- Discord Rich Presence
- Powiadomienia systemowe
- Nieinteraktywne API JSON
- Serwer Torznab dla integracji *arr

## Szybki start

```bash
# Instalacja przez pip
pip install weeb-cli

# Tryb interaktywny
weeb-cli

# Tryb API
weeb-cli api search "nazwa anime"
```

## Struktura dokumentacji

- **Rozpoczęcie**: Instalacja i wstępna konfiguracja
- **Przewodnik użytkownika**: Szczegółowe instrukcje użytkowania
- **Dokumentacja API**: Pełna dokumentacja API
- **Rozwój**: Przewodnik po wkładzie i rozwoju
- **Dokumentacja CLI**: Dokumentacja interfejsu wiersza poleceń

## Wsparcie

- GitHub: [ewgsta/weeb-cli](https://github.com/ewgsta/weeb-cli)
- Problemy: [Zgłoś błąd](https://github.com/ewgsta/weeb-cli/issues)
- PyPI: [weeb-cli](https://pypi.org/project/weeb-cli/)

## Licencja

Weeb CLI jest licencjonowany na licencji GPL-3.0. Zobacz [LICENSE](https://github.com/ewgsta/weeb-cli/blob/main/LICENSE) dla szczegółów.
