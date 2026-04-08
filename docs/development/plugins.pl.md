# Przewodnik po tworzeniu wtyczek

Weeb CLI zapewnia solidną architekturę wtyczek, która pozwala na rozszerzenie aplikacji o niestandardowych dostawców, trackery i usługi. Wtyczki są pakowane w bezpiecznym, przenośnym formacie `.weeb`.

## Struktura wtyczki

Standardowy folder wtyczki musi zawierać następujące pliki:

```
moja-wtyczka/
├── manifest.json
├── main.py (Punkt wejścia)
├── README.md
└── assets/
    └── logo.png (Opcjonalnie)
```

### manifest.json

Manifest zawiera metadane dotyczące Twojej wtyczki:

```json
{
    "id": "moja-wtyczka",
    "name": "Moja Wtyczka",
    "version": "1.0.0",
    "description": "Opis Twojej wtyczki.",
    "author": "Twoje Imię",
    "entry_point": "main.py",
    "dependencies": [],
    "min_weeb_version": "1.0.0",
    "permissions": ["network", "storage"]
}
```

### main.py

Punkt wejścia musi definiować funkcję `register()`, która zostanie wywołana po włączeniu wtyczki.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("moj_dostawca", lang="pl", region="PL")
    class MojDostawca(BaseProvider):
        # Implementacja...
        pass
```

## Budowanie wtyczki

Użyj dostarczonego skryptu budującego, aby spakować katalog wtyczki do pliku `.weeb`:

```bash
python3 weeb_cli/utils/plugin_builder.py plugins/moja-wtyczka -o moja-wtyczka.weeb
```

## Instalowanie wtyczki

1. Otwórz Weeb CLI.
2. Przejdź do **Ustawienia** > **Wtyczki**.
3. Wybierz **Załaduj Wtyczkę**.
4. Wprowadź ścieżkę do pliku `.weeb`.

## Bezpieczeństwo i Piaskownica

Wtyczki działają w ograniczonym środowisku wykonawczym. Mogą korzystać tylko z podzbioru biblioteki standardowej Pythona i muszą prosić o określone uprawnienia w `manifest.json`.

- **network**: Pozwala na wykonywanie żądań HTTP.
- **storage**: Pozwala na dostęp do plików lokalnych w katalogu danych wtyczki.

## Udostępnianie wtyczek

Możesz udostępniać swoje wtyczki, przesyłając Pull Request do głównego repozytorium.

1. Sforkuj repozytorium.
2. Utwórz folder w `plugins/` dla swojej wtyczki.
3. Dodaj pliki wtyczki.
4. Otwórz Pull Request, korzystając z **Szablonu przesyłania wtyczki**.

Nasz potok CI/CD automatycznie zweryfikuje Twoją wtyczkę pod kątem:
- Poprawności manifestu
- Luk w zabezpieczeniach (Bandit)
- Stylu kodu (Ruff)
- Integralności struktury
