# Tryb Serve - Serwer Torznab

Uruchom Weeb CLI jako serwer Torznab do integracji z Sonarr i innymi aplikacjami *arr.

## Przegląd

Tryb Serve zapewnia serwer API zgodny z Torznab, który umożliwia aplikacjom *arr wyszukiwanie i pobieranie anime przez dostawców Weeb CLI.

## Uruchamianie serwera

```bash
weeb-cli serve [OPCJE]
```

Opcje:
- `--host`: Host do powiązania (domyślnie: 127.0.0.1)
- `--port`: Port do nasłuchiwania (domyślnie: 8080)
- `--api-key`: Klucz API do uwierzytelniania

Przykład:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080 --api-key mojklucz123
```

## Integracja z Sonarr

### Dodawanie indeksera

1. Sonarr → Ustawienia → Indeksery
2. Dodaj → Torznab → Niestandardowy
3. Skonfiguruj:
   - Nazwa: Weeb CLI
   - URL: http://localhost:8080
   - Klucz API: (twój klucz)
   - Kategorie: 5070 (Anime)

### Testowanie połączenia

1. Kliknij "Test" w Sonarr
2. Powinno pokazać sukces
3. Zapisz indekser

## Punkty końcowe API

### Możliwości

```
GET /api?t=caps
```

Zwraca XML możliwości Torznab.

### Wyszukiwanie

```
GET /api?t=search&q=ZAPYTANIE&apikey=KLUCZ
```

Wyszukaj anime według tytułu.

### Wyszukiwanie TV

```
GET /api?t=tvsearch&q=ZAPYTANIE&season=1&ep=1&apikey=KLUCZ
```

Wyszukaj konkretny odcinek.

## Konfiguracja

### Klucz API

Wygeneruj bezpieczny klucz API:
```bash
openssl rand -hex 16
```

Użyj w poleceniu serve i konfiguracji Sonarr.

### Dostęp sieciowy

Dla zdalnego dostępu:
```bash
weeb-cli serve --host 0.0.0.0 --port 8080
```

Ostrzeżenie: Upewnij się, że zapora jest prawidłowo skonfigurowana.

## Ograniczenia

- Tylko do odczytu (brak zarządzania pobieraniem)
- Tylko wyszukiwanie (brak kanałów RSS)
- Jeden dostawca na instancję
- Brak uwierzytelniania poza kluczem API

## Następne kroki

- [Tryb API](api-mode.md): API JSON
- [Polecenia](commands.md): Dokumentacja CLI
