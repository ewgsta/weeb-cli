<p align="center">
  <img src="https://8upload.com/image/a6cdd79fc5a25c99/wl-512x512.jpg" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>Bez przeglądarki, bez reklam, bez rozpraszania uwagi. Tylko Ty i niezrównane wrażenia z oglądania anime.</strong>
</p>

<div align="center">
  <a href="../../README.md">English</a> | <a href="../tr/README.md">Türkçe</a> | <a href="../de/README.md">Deutsch</a> | <a href="README.md">Polski</a>
</div>
<br>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/ewgsta/weeb-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/ewgsta/weeb-cli/tests.yml?style=flat-square" alt="Tests"></a>
</p>

<p align="center">
  <a href="#instalacja">Instalacja</a> •
  <a href="#funkcje">Funkcje</a> •
  <a href="#użycie">Użycie</a> •
  <a href="#źródła">Źródła</a>
</p>

---

## Funkcje

### Wiele źródeł
- **Turecki**: Animecix, Turkanime, Anizle, Weeb
- **Angielski**: HiAnime, AllAnime
- **Niemiecki**: AniWorld
- **Polski**: Docchi

### Inteligentne przesyłanie strumieniowe
- Wysokiej jakości odtwarzanie HLS/MP4 przy użyciu MPV
- Wznawianie od miejsca, w którym skończyłeś (na podstawie znaczników czasu)
- Historia oglądania i statystyki
- Znaczniki odcinków ukończonych (✓) i w trakcie oglądania (●)

### Potężny system pobierania
- **Aria2** do szybkiego pobierania przy użyciu wielu połączeń
- **yt-dlp** dla obsługi złożonych strumieni
- System kolejkowania z jednoczesnym pobieraniem
- Wznawianie przerwanych pobierań
- Inteligentne nazewnictwo plików (`Anime Name - S1E1.mp4`)

### Śledzenie i synchronizacja
- Integracja z **AniList** za pomocą OAuth
- Integracja z **MyAnimeList** za pomocą OAuth
- Integracja z **Kitsu** (email/hasło)
- Automatyczna synchronizacja postępów oglądania (online i offline)
- Kolejka offline dla oczekujących aktualizacji
- Inteligentne dopasowywanie tytułów anime na podstawie nazw plików

### Biblioteka lokalna
- Automatyczne skanowanie pobranych anime
- Obsługa dysków zewnętrznych (USB, HDD)
- Indeksowanie anime offline z automatyczną synchronizacją z trackerem
- Szukaj we wszystkich źródłach
- **Zalecany format**: `Anime Name - S1E1.mp4` – zapewnia najlepszą kompatybilność z trackerem

### Dodatkowe funkcje
- Baza danych SQLite (szybka i niezawodna)
- Powiadomienia systemowe o zakończeniu pobierania
- Integracja z Discord RPC (Pokaż na Discordzie, co teraz oglądasz)
- Historia wyszukiwania
- Tryb debugowania i logowanie
- Automatyczne sprawdzanie aktualizacji
- Nieniektywny tryb API JSON do skryptów i AI
- Tryb serwera Torznab do integracji z Sonarr/*arr

---

## Instalacja

### PyPI (Uniwersalne)
```bash
pip install weeb-cli
```

### Arch Linux (AUR)
```bash
yay -S weeb-cli
```

### Portable
Pobierz odpowiedni plik dla swojej platformy z zakładki [Releases](https://github.com/ewgsta/weeb-cli/releases).

### Dla deweloperów
```bash
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli
pip install -e .
```

---

## Użycie

```bash
weeb-cli
```

### Tryb API (Nieniektywny)

Dla potrzeb pisania skryptów, automatyzacji i agentów AI, weeb-cli udostępnia komendy API JSON, które działają w tle (headless) bez konieczności obsługi bazy danych czy TUI:

```bash
# Wyświetl dostępne źródła
weeb-cli api providers

# Wyszukiwanie anime (zwraca ID)
weeb-cli api search "Angel Beats"
# Zwraca: [{"id": "12345", "title": "Angel Beats!", ...}]

# Lista odcinków (użyj ID z wyszukiwarki)
weeb-cli api episodes 12345 --season 1

# Pobierz adresy URL streamów dla odcinka
weeb-cli api streams 12345 --season 1 --episode 1

# Szczegóły anime
weeb-cli api details 12345

# Pobierz odcinek
weeb-cli api download 12345 --season 1 --episode 1 --output ./downloads
```

Wszystkie komendy API zwracają JSON na standardowe wyjście (stdout).

### Integracja z Sonarr/*arr (Tryb Serve)

weeb-cli może działać jako serwer zgodny z Torznab dla aplikacji Sonarr i podobnych z rodziny *arr:

```bash
pip install weeb-cli[serve]

weeb-cli serve --port 9876 \
  --watch-dir /downloads/watch \
  --completed-dir /downloads/completed \
  --sonarr-url http://sonarr:8989 \
  --sonarr-api-key TWÓJ_KLUCZ
```

Następnie w Sonarr dodaj `http://weeb-cli-host:9876` jako Torznab instancję w kategorii 5070 (TV/Anime). Serwer zawiera komponent `blackhole` pobierający wykryte odcinki automatycznie.

**Wsparcie Docker:**
```bash
docker-compose -f docs/docker-compose.torznab.yml up -d
```

Zobacz [Dokumentacja Serwera Torznab](https://ewgsta.github.io/weeb-cli/cli/serve-mode.pl/) dla pełnych szczegółów.

### Serwer RESTful API

### Serwer RESTful API

Dla aplikacji webowych/mobilnych i niestandardowych integracji, weeb-cli udostępnia serwer RESTful API:

```bash
pip install weeb-cli[serve-restful]

weeb-cli serve restful --port 8080 --cors
```

**Punkty końcowe API:**
- `GET /health` - Sprawdzenie stanu
- `GET /api/providers` - Lista dostępnych dostawców
- `GET /api/search?q=naruto&provider=animecix` - Wyszukaj anime
- `GET /api/anime/{id}?provider=animecix` - Pobierz szczegóły anime
- `GET /api/anime/{id}/episodes?season=1` - Lista odcinków
- `GET /api/anime/{id}/episodes/{ep_id}/streams` - Pobierz adresy URL strumieni

Wszyscy dostępni dostawcy są ładowani automatycznie. Wybierz, którego dostawcy użyć, za pomocą parametru zapytania `provider`.

**Wsparcie Docker:**
```bash
docker-compose -f docs/docker-compose.restful.yml up -d
```

Zobacz [Dokumentacja RESTful API](https://ewgsta.github.io/weeb-cli/cli/restful-api.pl/) dla pełnych szczegółów.

### Sterowanie klawiaturą
| Klawisz | Akcja |
|---------|-------|
| `↑` `↓` | Nawigacja w menu |
| `Enter` | Wybierz |
| `s` | Wyszukaj Anime (Menu główne) |
| `d` | Pobrane (Menu główne) |
| `w` | Do obejrzenia (Menu główne) |
| `c` | Ustawienia (Menu główne) |
| `q` | Wyjście (Menu główne) |
| `Ctrl+C` | Wróć / Wyjdź |

**Uwaga:** Wszystkie skróty klawiaturowe można zmienić w sekcji: Ustawienia > Skróty klawiaturowe.

---

## Źródła

| Źródło | Język |
|--------|-------|
| Animecix | Turecki |
| Turkanime | Turecki |
| Anizle | Turecki |
| Weeb | Turecki |
| HiAnime | Angielski |
| AllAnime | Angielski |
| AniWorld | Niemiecki |
| Docchi | Polski |

---

## Konfiguracja

Lokalizacja pliku konfiguracyjnego: `~/.weeb-cli/weeb.db` (SQLite)

### Dostępne ustawienia

| Ustawienie | Opis | Domyślne | Typ |
|------------|------|----------|-----|
| `language` | Język interfejsu (tr/en/de/pl) | `null` (pyta przy pierszym uruchomieniu) | string |
| `scraping_source` | Aktywne źródło anime | `animecix` | string |
| `aria2_enabled` | Użyj Aria2 podczas pobierania | `true` | boolean |
| `aria2_max_connections` | Max. połączeń na pobieranie | `16` | integer |
| `ytdlp_enabled` | Użyj yt-dlp dla streamów HLS | `true` | boolean |
| `ytdlp_format` | yt-dlp łańcuch formatujący | `bestvideo+bestaudio/best` | string |
| `max_concurrent_downloads` | Jednoczesne pobierania | `3` | integer |
| `download_dir` | Ścieżka folderu pobierania | `./weeb-downloads` | string |
| `download_max_retries` | Ponowne próby pobierania po błędzie | `3` | integer |
| `download_retry_delay` | Opóźnienie między próbami (sekundy) | `10` | integer |
| `show_description` | Wyświetl zarys fabuły anime | `true` | boolean |
| `discord_rpc_enabled` | Integracja logowania Discord | `false` | boolean |
| `shortcuts_enabled` | Skróty klawiaturowe | `true` | boolean |
| `debug_mode` | Tryb podglądu debugowania | `false` | boolean |

### Ustawienia Trackerów (zapisywane osobno)
- `anilist_token` - OAuth token do AniList
- `anilist_user_id` - ID użytkownika AniList
- `mal_token` - OAuth token do MyAnimeList
- `mal_refresh_token` - Odświeżający token MAL
- `mal_username` - Nazwa użytkownika MAL

### Dyski Zewnętrzne
Zarządzane przez menu 'Ustawienia > Dyski Zewnętrzne'. Zapisy dla każdego dysku:
- Ścieżka (np., `D:\Anime`)
- Niestandardowa nazwa/pseudonim
- Godzina dodania

Wszystkie ustawienia mogą być modyfikowane poprzez interaktywne menu Ustawienia.

---

## Plan rozwoju (Roadmap)

### Ukończone
- [x] Wsparcie dla wielu źródeł (TR/EN/DE/PL)
- [x] Odtwarzanie MPV
- [x] Historia i śledzenie postępów
- [x] Integracja pobierania Aria2/yt-dlp
- [x] Lokalne napędy zewnętrzne i biblioteka własna
- [x] Baza danych SQLite
- [x] System powiadomień
- [x] Tryb debugowania
- [x] Integracja MAL/AniList
- [x] Kopia zapasowa / Przywracanie kopii bazy danych
- [x] Skróty klawiszowe
- [x] Bezobsługowe i nieniektywne JSON API (format wyjściowy)
- [x] Serwer Torznab do integracji Sonarr/*arr

### Planowane
- [ ] Rekomendacje anime
- [ ] Działania wsadowe
- [ ] Statystyki (wykresy)
- [ ] Obsługa stylów
- [ ] Pobieranie nowych napisów
- [ ] Obsługa torrent (nyaa.si)
- [ ] Wspólne oglądanie

---

## Struktura projektu
*Szczegółowa struktura znajduje się w angielskiej (lub tureckiej) wersji README.*

---

## Licencja

Ten projekt jest objęty licencją **Powszechna Licencja Publiczna GNU, wersja 3.0**.  
Zajrzyj do pliku [LICENSE](LICENSE) dla wyświetlenia pełnej treści licencji.

Weeb-CLI (C) 2026
