# API Commands

Nieinteraktywne polecenia JSON API.

## Przegląd

Polecenia API zapewniają wyjście JSON dla:
- Skryptów i automatyzacji
- Integracji z narzędziami
- Operacji bezgłowych

## Polecenia

### providers

Wyświetl wszystkich dostawców.

```bash
weeb-cli api providers
```

### search

Wyszukaj anime.

```bash
weeb-cli api search "query" --provider animecix
```

### episodes

Pobierz listę odcinków.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

### streams

Pobierz adresy URL strumieni.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

## Implementacja

Wszystkie polecenia w `weeb_cli/commands/api.py`.

## Następne kroki

- [Przewodnik trybu API](../../cli/api-mode.md): Szczegółowe użycie
- [Dokumentacja poleceń](../../cli/commands.md): Wszystkie polecenia
