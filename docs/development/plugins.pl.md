# Przewodnik po tworzeniu wtyczek

Weeb CLI zapewnia solidną architekturę wtyczek, która pozwala na rozszerzenie aplikacji o niestandardowych dostawców, trackery i usługi. Wtyczki są izolowane w bezpiecznym, przenośnym środowisku i postępują zgodnie ze standardową strukturą katalogów.

## Struktura wtyczki

Standardowy folder wtyczki musi być przechowywany w katalogu `data/` i zawierać następującą strukturę:

```
data/
  moja-wtyczka/
    plugin.weeb        (Główny punkt wejścia kodu)
    manifest.json      (Metadane i konfiguracja)
    README.md          (Szczegółowa dokumentacja)
    screenshots/       (Przynajmniej jeden zrzut ekranu do galerii)
      ss1.png
    assets/            (Ikony i inne zasoby)
      icon.png
```

### manifest.json

Manifest zawiera obowiązkowe i opcjonalne metadane dotyczące Twojej wtyczki:

```json
{
    "id": "moja-wtyczka",
    "name": "Moja Wtyczka",
    "version": "1.0.0",
    "description": "Opis Twojej wtyczki.",
    "author": "Twoje Imię",
    "entry_point": "plugin.weeb",
    "min_weeb_version": "1.0.0",
    "dependencies": [],
    "permissions": ["network", "storage"],
    "tags": ["anime", "pl"],
    "icon": "assets/icon.png",
    "homepage": "https://example.com",
    "repository_url": "https://github.com/user/repo",
    "license": "MIT"
}
```

### plugin.weeb

Punkt wejścia to skrypt w języku Python, który musi definiować funkcję `register()`. Działa on w ograniczonym środowisku piaskownicy z dostępem do bezpiecznego podzbioru wbudowanych funkcji i interfejsów API `weeb_cli`.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("moj_niestandardowy_dostawca", lang="pl", region="PL")
    class MojDostawca(BaseProvider):
        def search(self, query: str):
            # Implementacja...
            pass
```

## Budowanie i Pakowanie

Użyj dostarczonego skryptu budującego, aby utworzyć lub spakować nowe wtyczki:

```bash
# Utwórz nowy szablon wtyczki
python3 weeb_cli/utils/plugin_builder.py create moja-nowa-wtyczka --id "nowe-id" --name "Nowa Nazwa"

# Zbuduj/Spakuj wtyczkę do dystrybucji (.weeb_pkg)
python3 weeb_cli/utils/plugin_builder.py build data/moja-wtyczka -o moja-wtyczka.weeb_pkg
```

## Instalacja

1. Otwórz Weeb CLI.
2. Przejdź do **Ustawienia** > **Wtyczki**.
3. Wybierz **Załaduj Wtyczkę**.
4. Podaj ścieżkę lokalną do folderu wtyczki lub jej pliku `.weeb_pkg`.

## Testowanie i Jakość

Wtyczki muszą utrzymywać co najmniej **80% pokrycia testami**, aby zostały zaakceptowane w oficjalnej galerii. Automatyczne testy powinny być umieszczone w katalogu `tests/` wewnątrz folderu wtyczki.

Nasz potok CI/CD weryfikuje:
- **Integralność manifestu**: Wymagane pola (id, nazwa, wersja itp.) muszą być obecne.
- **Bezpieczeństwo**: Skanowanie za pomocą Bandit w poszukiwaniu typowych luk.
- **Jakość kodu**: Linting za pomocą Ruff.
- **Funkcjonalność**: Testy są wykonywane i sprawdzane jest pokrycie.

## Udostępnianie przez Galerię

Prześlij Pull Request dodający folder Twojej wtyczki do katalogu `data/`. Po zatwierdzeniu automatycznie pojawi się on w [Galerii Wtyczek](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html).
