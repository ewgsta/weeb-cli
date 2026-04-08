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
  <a href="#źródła">Źródła</a> •
  <a href="https://ewgsta.github.io/weeb-cli/">Dokumentacja</a>
</p>

---

## Funkcje

### System Wtyczek
- **Niestandardowy format .weeb**: Pakuj i udostępniaj własnych dostawców
- **Bezpieczna Piaskownica**: Uruchamiaj wtyczki bezpiecznie z ograniczonymi uprawnieniami
- **Plugin Builder**: Łatwy w użyciu skrypt do pakowania wtyczek
- **Galeria Wtyczek**: Przeglądaj i instaluj wtyczki społeczności z [Galerii](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html)
- **Automatyczne Wykrywanie**: Wtyczki są ładowane automatycznie przy starcie

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
```

---

## Licencja

Ten projekt jest objęty licencją **Powszechna Licencja Publiczna GNU, wersja 3.0**.  
Zajrzyj do pliku [LICENSE](../../LICENSE) dla wyświetlenia pełnej treści licencji.

Weeb-CLI (C) 2026
