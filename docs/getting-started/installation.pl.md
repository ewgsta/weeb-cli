# Instalacja

Weeb CLI można zainstalować na wiele sposobów w zależności od platformy i preferencji.

## PyPI (Uniwersalny)

Najłatwiejszym sposobem instalacji Weeb CLI jest przez pip:

```bash
pip install weeb-cli
```

Aby zaktualizować do najnowszej wersji:

```bash
pip install --upgrade weeb-cli
```

## Arch Linux (AUR)

Dla użytkowników Arch Linux, Weeb CLI jest dostępny w AUR:

```bash
yay -S weeb-cli
```

Lub używając innego helpera AUR:

```bash
paru -S weeb-cli
```

## Przenośne pliki wykonywalne

Wstępnie zbudowane przenośne pliki wykonywalne są dostępne dla Windows, macOS i Linux na stronie [Releases](https://github.com/ewgsta/weeb-cli/releases).

1. Pobierz odpowiedni plik dla swojej platformy
2. Rozpakuj archiwum
3. Uruchom plik wykonywalny

## Instalacja dla deweloperów

Dla rozwoju lub wkładu w projekt:

```bash
# Sklonuj repozytorium
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Zainstaluj w trybie edytowalnym
pip install -e .

# Zainstaluj zależności deweloperskie
pip install -r requirements.txt
```

## Zależności

Weeb CLI automatycznie pobierze i zainstaluje następujące zależności przy pierwszym uruchomieniu:

- **FFmpeg**: Przetwarzanie i konwersja wideo
- **MPV**: Odtwarzacz multimedialny do streamingu
- **Aria2**: Szybkie pobieranie wielopołączeniowe
- **yt-dlp**: Ekstrakcja i pobieranie strumieni

Te narzędzia są pobierane do `~/.weeb-cli/bin/` i zarządzane automatycznie.

## Weryfikacja

Po instalacji sprawdź, czy Weeb CLI jest poprawnie zainstalowany:

```bash
weeb-cli --version
```

Powinieneś zobaczyć numer wersji.

## Następne kroki

- [Przewodnik szybkiego startu](quickstart.md): Rozpocznij pracę z Weeb CLI
- [Konfiguracja](configuration.md): Skonfiguruj swoje preferencje
