# Python SDK

Programowe API do bezpośredniej integracji funkcjonalności Weeb CLI w aplikacjach Python.

## Przegląd

Weeb CLI SDK zapewnia natywny interfejs Python dla wszystkich funkcji streamowania i pobierania anime. W przeciwieństwie do trybu CLI API, który wymaga tworzenia procesów i parsowania JSON, SDK oferuje:

- **Bezpośrednie API Python** - Brak narzutu subprocess
- **Bezpieczeństwo typów** - Pełne wskazówki typów dla wsparcia IDE
- **Bezpieczne wątkowo** - Bezpieczne dla operacji współbieżnych
- **Tryb Headless** - Brak zależności od bazy danych lub TUI
- **Te same funkcje** - Wszystkie funkcje CLI dostępne

## Instalacja

SDK jest dołączony do weeb-cli:

```bash
pip install weeb-cli
```

## Szybki start

```python
from weeb_cli import WeebSDK

# Inicjalizacja SDK
sdk = WeebSDK(default_provider="hianime")

# Wyszukiwanie anime
results = sdk.search("One Piece")
print(f"Znaleziono {len(results)} wyników")

# Pobierz pierwszy wynik
anime = results[0]
print(f"{anime.title} ({anime.year})")

# Pobierz odcinki
episodes = sdk.get_episodes(anime.id, season=1)
print(f"Sezon 1 ma {len(episodes)} odcinków")

# Pobierz adresy URL strumieni
streams = sdk.get_streams(
    anime_id=anime.id,
    episode_id=episodes[0].id
)
print(f"Dostępne w {len(streams)} jakościach")

# Pobierz odcinek
path = sdk.download_episode(
    anime_id=anime.id,
    season=1,
    episode=1,
    output_dir="./downloads"
)
print(f"Pobrano do: {path}")
```

## Dokumentacja API

### Klasa WeebSDK

Główny interfejs SDK dla wszystkich operacji.

#### Konstruktor

```python
WeebSDK(headless: bool = True, default_provider: Optional[str] = None)
```

**Parametry:**
- `headless` (bool): Uruchom w trybie headless (bez bazy danych/TUI). Domyślnie: `True`
- `default_provider` (str, opcjonalnie): Domyślny dostawca do użycia. Domyślnie: `"animecix"`

**Przykład:**
```python
# Headless z domyślnym dostawcą
sdk = WeebSDK()

# Niestandardowy domyślny dostawca
sdk = WeebSDK(default_provider="hianime")

# Z dostępem do bazy danych (dla historii oglądania itp.)
sdk = WeebSDK(headless=False)
```

#### search()

Wyszukaj anime według ciągu zapytania.

```python
def search(
    query: str, 
    provider: Optional[str] = None
) -> List[AnimeResult]
```

**Parametry:**
- `query` (str): Zapytanie wyszukiwania (tytuł anime lub słowa kluczowe)
- `provider` (str, opcjonalnie): Dostawca do użycia. Używa `default_provider`, jeśli nie określono

**Zwraca:** Lista obiektów `AnimeResult`

**Przykład:**
```python
results = sdk.search("Naruto", provider="hianime")
for anime in results:
    print(f"{anime.title} - {anime.type} ({anime.year})")
```

#### get_episodes()

Pobierz listę dostępnych odcinków dla anime.

```python
def get_episodes(
    anime_id: str, 
    season: Optional[int] = None,
    provider: Optional[str] = None
) -> List[Episode]
```

**Parametry:**
- `anime_id` (str): Unikalny identyfikator anime
- `season` (int, opcjonalnie): Filtruj według numeru sezonu
- `provider` (str, opcjonalnie): Dostawca do użycia

**Zwraca:** Lista obiektów `Episode`

**Przykład:**
```python
# Pobierz wszystkie odcinki
episodes = sdk.get_episodes("anime-id", provider="hianime")

# Tylko sezon 2
season2 = sdk.get_episodes("anime-id", season=2, provider="hianime")

for ep in season2:
    print(f"S{ep.season:02d}E{ep.number:02d}: {ep.title}")
```

#### download_episode()

Pobierz odcinek do lokalnego magazynu.

```python
def download_episode(
    anime_id: str,
    season: int,
    episode: int,
    provider: Optional[str] = None,
    output_dir: str = ".",
    anime_title: Optional[str] = None
) -> Optional[str]
```

**Parametry:**
- `anime_id` (str): Unikalny identyfikator anime
- `season` (int): Numer sezonu
- `episode` (int): Numer odcinka
- `provider` (str, opcjonalnie): Dostawca do użycia
- `output_dir` (str): Katalog do zapisania pliku. Domyślnie: bieżący katalog
- `anime_title` (str, opcjonalnie): Niestandardowy tytuł dla nazwy pliku. Pobierany automatycznie, jeśli nie podano

**Zwraca:** Ścieżka do pobranego pliku lub `None` w przypadku błędu

**Przykład:**
```python
# Podstawowe pobieranie
path = sdk.download_episode(
    anime_id="anime-id",
    season=1,
    episode=1,
    provider="hianime"
)

# Niestandardowy katalog wyjściowy i tytuł
path = sdk.download_episode(
    anime_id="anime-id",
    season=2,
    episode=5,
    provider="hianime",
    output_dir="/media/anime",
    anime_title="Moje ulubione anime"
)
print(f"Pobrano do: {path}")
```

## Zaawansowane użycie

### Wyszukiwanie u wielu dostawców

Wyszukaj u wielu dostawców i połącz wyniki:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK()
query = "One Piece"

# Wyszukaj u wielu dostawców
providers = ["hianime", "animecix", "aniworld"]
all_results = []

for provider in providers:
    try:
        results = sdk.search(query, provider=provider)
        all_results.extend(results)
        print(f"{provider}: {len(results)} wyników")
    except Exception as e:
        print(f"{provider} nie powiódł się: {e}")

print(f"Razem: {len(all_results)} wyników")
```

### Pobieranie wsadowe

Pobierz wiele odcinków:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK(default_provider="hianime")

# Wyszukaj i pobierz anime
results = sdk.search("Naruto")
anime_id = results[0].id

# Pobierz sezon 1
for episode_num in range(1, 26):
    try:
        path = sdk.download_episode(
            anime_id=anime_id,
            season=1,
            episode=episode_num,
            output_dir="./naruto_s1"
        )
        print(f"✓ Odcinek {episode_num}: {path}")
    except Exception as e:
        print(f"✗ Odcinek {episode_num}: {e}")
```

## Przykłady integracji

### Flask Web API

```python
from flask import Flask, jsonify, request
from weeb_cli import WeebSDK

app = Flask(__name__)
sdk = WeebSDK()

@app.route('/api/search')
def search():
    query = request.args.get('q')
    provider = request.args.get('provider', 'hianime')
    
    results = sdk.search(query, provider=provider)
    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'year': r.year,
            'cover': r.cover
        }
        for r in results
    ])

if __name__ == '__main__':
    app.run(port=5000)
```

### Bot Discord

```python
import discord
from discord.ext import commands
from weeb_cli import WeebSDK

bot = commands.Bot(command_prefix='!')
sdk = WeebSDK(default_provider="hianime")

@bot.command()
async def anime(ctx, *, query):
    """Wyszukaj anime"""
    results = sdk.search(query)
    
    if not results:
        await ctx.send("Nie znaleziono wyników")
        return
    
    anime = results[0]
    embed = discord.Embed(
        title=anime.title,
        description=f"Rok: {anime.year}"
    )
    if anime.cover:
        embed.set_thumbnail(url=anime.cover)
    
    await ctx.send(embed=embed)

bot.run('TOKEN')
```

## Najlepsze praktyki

1. **Ponowne użycie instancji SDK**: Utwórz jedną instancję SDK i używaj jej ponownie
2. **Obsługa błędów**: Zawsze opakowuj wywołania SDK w bloki try-except
3. **Wybór dostawcy**: Pozwól użytkownikom wybrać dostawcę lub użyj odpowiednich dla języka wartości domyślnych
4. **Operacje współbieżne**: Użyj wątków dla operacji wsadowych
5. **Buforowanie**: SDK używa tej samej pamięci podręcznej co CLI - wyniki są automatycznie buforowane
6. **Tryb Headless**: Zachowaj headless=True dla aplikacji bezstanowych

## Ograniczenia

- **Brak historii oglądania**: Tryb headless nie śledzi postępu oglądania
- **Brak synchronizacji trackera**: Synchronizacja AniList/MAL wymaga trybu nie-headless
- **Brak powiadomień**: Powiadomienia systemowe niedostępne w trybie headless
- **Brak Discord RPC**: Integracja Discord wymaga trybu nie-headless

Dla tych funkcji zainicjuj SDK z `headless=False` i upewnij się, że baza danych jest dostępna.

## Następne kroki

- [Dokumentacja trybu API](../cli/api-mode.pl.md): CLI JSON API
- [Rozwój dostawcy](../development/adding-providers.pl.md): Tworzenie niestandardowych dostawców
- [Architektura](../development/architecture.pl.md): Przegląd projektu systemu
