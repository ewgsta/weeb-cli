# Współtworzenie Weeb CLI

<div align="center">
  <a href="../../CONTRIBUTING.md">English</a> | <a href="../tr/CONTRIBUTING.md">Türkçe</a> | <a href="../de/CONTRIBUTING.md">Deutsch</a> | <a href="CONTRIBUTING.md">Polski</a>
</div>
<br>

Na wstępie bardzo dziękujemy za rozważenie wkładu w Weeb CLI! Twoja pomoc jest niezwykle cenna.

Jeśli lubisz anime, przydatne narzędzia i terminal, jesteś we właściwym miejscu.

## Pierwsze kroki

1. **Sforkuj repozytorium** na GitHubie.
2. **Sklonuj swojego forka** lokalnie:
   ```bash
   git clone https://github.com/ewgsta/weeb-cli.git
   cd weeb-cli
   ```
3. **Zainstaluj zależności** w trybie edytowalnym:
   ```bash
   pip install -e .
   ```

## Przepływ pracy (Workflow)

1. Utwórz nową gałąź (branch) dla swojej nowej funkcji lub poprawki błędu:
   ```bash
   git checkout -b feature/nazwa-twojej-funkcji
   ```
2. Wprowadź zmiany w kodzie.
3. Aby przetestować zmiany CLI lokalnie, możesz uruchomić `weeb-cli`, który powinien wskazywać na skrypt twojego aktywnego środowiska.
4. Postaraj się napisać testy. Znajdują się one w katalogu `tests/`.
   ```bash
   pytest
   ```
5. Zatwierdź (commit) swoje zmiany. Upewnij się, że opisy commitów jasno określają wprowadzone zmiany.
6. Wypchnij zmiany do swojego forka i prześlij Pull Request do gałęzi `main`.

## Pull Requests

- Ograniczaj swoje Pull Requesty do pojedynczej zmiany, nowej funkcji lub poprawki błędu. Ułatwi to i przyspieszy proces ich weryfikacji.
- Podlinkuj powiązane zgłoszenia (issues) do PR-a, aby ułatwić zarządzającym zrozumienie kontekstu.
- Stosuj się do aktualnego stylu kodowania (używaj Black/Flake8 w komponentach Python).
- Aktualizuj dokumentację (`README.md`, `md/tr/README.md`, itp.), jeśli edytowany kod modyfikuje działanie aplikacji i ma to wpływ na użytkowników.

## Problemy (Issues)

Jeśli znajdziesz błąd lub masz propozycję, otwórz nowe zgłoszenie (issue):
- Przed dodaniem nowego zgłoszenia **Przeszukaj istniejące issues**, aby uniknąć duplikatów.
- Zapewnij najwięcej informacji jak to możliwe, w tym system operacyjny, wersję Pythona oraz aktualną wersję Weeb CLI.
- Jeśli przypadek tego wymaga, warto uwzględnić możliwe sposoby jego zreprodukowania, pliki logów czy zrzuty ekranu.

## Tłumaczenia i i18n
Weeb CLI wspiera różne języki:
- Wszystkie funkcje czy nowe mechaniki dodające nowe teksty wyświetlane w aplikacji, powinny równocześnie uwzględniać odpowiednie pliki JSON zlokalizowane w folderze `locales/` (`en.json`, `tr.json`, `de.json`, `pl.json` itd.).

---

Jeszcze raz dziękujemy Ci za twój cenny wkład!
