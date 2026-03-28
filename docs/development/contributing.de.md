# Zu Weeb CLI beitragen

Vielen Dank für Ihr Interesse, zu Weeb CLI beizutragen! Dieser Leitfaden hilft Ihnen beim Einstieg.

## Entwicklungssetup

### Voraussetzungen

- Python 3.8 oder höher
- Git
- pip oder pipenv

### Klonen und Installieren

```bash
# Repository klonen
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Im bearbeitbaren Modus installieren
pip install -e .

# Entwicklungsabhängigkeiten installieren
pip install -r requirements.txt
```

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Mit Coverage ausführen
pytest --cov=weeb_cli --cov-report=html

# Spezifische Testdatei ausführen
pytest tests/test_providers.py
```

## Code-Stil

### Python-Stil-Leitfaden

Wir folgen PEP 8 mit einigen Änderungen:

- Zeilenlänge: 100 Zeichen (nicht 79)
- Verwenden Sie Typ-Hinweise für alle Funktionssignaturen
- Verwenden Sie Docstrings (Google-Stil) für alle öffentlichen Funktionen und Klassen

### Typ-Hinweise

Alle Funktionen sollten Typ-Hinweise haben:

```python
def search(self, query: str) -> List[AnimeResult]:
    """Nach Anime nach Abfrage suchen.
    
    Args:
        query: Suchabfrage-String.
    
    Returns:
        Liste der Anime-Suchergebnisse.
    """
    pass
```

### Docstrings

Verwenden Sie Google-Stil-Docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """Kurze Beschreibung.
    
    Längere Beschreibung bei Bedarf.
    
    Args:
        param1: Beschreibung von param1.
        param2: Beschreibung von param2.
    
    Returns:
        Beschreibung des Rückgabewerts.
    
    Raises:
        ValueError: Wenn param1 ungültig ist.
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

## Neuen Anbieter hinzufügen

### 1. Anbieter-Datei erstellen

Neue Datei im entsprechenden Sprachverzeichnis erstellen:

```
weeb_cli/providers/<lang>/<anbieter_name>.py
```

### 2. Anbieter-Klasse implementieren

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.providers.registry import register_provider
from typing import List, Optional

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    """Anbieter für MyAnimeSource.com.
    
    Bietet Anime-Inhalte von MyAnimeSource mit Suche,
    Details und Stream-Extraktion.
    """
    
    BASE_URL = "https://myanimesource.com"
    
    def search(self, query: str) -> List[AnimeResult]:
        """Nach Anime suchen."""
        # Implementierung
        pass
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Anime-Details abrufen."""
        # Implementierung
        pass
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Episodenliste abrufen."""
        # Implementierung
        pass
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Stream-URLs extrahieren."""
        # Implementierung
        pass
```

### 3. Tests hinzufügen

Testdatei in `tests/` erstellen:

```python
import pytest
from weeb_cli.providers import get_provider

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
    assert results[0].title is not None
```

### 4. Dokumentation aktualisieren

Anbieter-Dokumentation in `docs/api/providers/` hinzufügen.

## Pull-Request-Prozess

### 1. Branch erstellen

```bash
git checkout -b feature/mein-neues-feature
```

### 2. Änderungen vornehmen

- Code nach Stil-Richtlinien schreiben
- Typ-Hinweise und Docstrings hinzufügen
- Tests für neue Funktionalität schreiben
- Dokumentation aktualisieren

### 3. Änderungen testen

```bash
# Tests ausführen
pytest

# Code-Stil prüfen
flake8 weeb_cli/

# Typ-Prüfung (optional)
mypy weeb_cli/
```

### 4. Änderungen committen

Verwenden Sie konventionelle Commit-Nachrichten:

```bash
git commit -m "feat: neuen Anbieter für XYZ hinzufügen"
git commit -m "fix: Stream-Extraktionsproblem beheben"
git commit -m "docs: Installationsleitfaden aktualisieren"
```

Commit-Typen:
- `feat`: Neues Feature
- `fix`: Fehlerbehebung
- `docs`: Dokumentationsänderungen
- `style`: Code-Stil-Änderungen (Formatierung)
- `refactor`: Code-Refactoring
- `test`: Tests hinzufügen oder aktualisieren
- `chore`: Wartungsaufgaben

### 5. Pushen und PR erstellen

```bash
git push origin feature/mein-neues-feature
```

Dann einen Pull Request auf GitHub erstellen mit:
- Klarer Beschreibung der Änderungen
- Verweis auf zugehörige Issues
- Screenshots (bei UI-Änderungen)

## Code-Review

Alle Einreichungen erfordern eine Überprüfung. Wir werden Ihren PR überprüfen und möglicherweise Änderungen anfordern. Bitte seien Sie geduldig und reagieren Sie auf Feedback.

## Community-Richtlinien

- Seien Sie respektvoll und konstruktiv
- Helfen Sie anderen in Diskussionen
- Melden Sie Fehler mit detaillierten Informationen
- Schlagen Sie Features mit klaren Anwendungsfällen vor

## Fragen?

- Öffnen Sie ein Issue für Fehler oder Feature-Anfragen
- Starten Sie eine Diskussion für Fragen
- Überprüfen Sie bestehende Issues, bevor Sie neue erstellen

Vielen Dank für Ihren Beitrag zu Weeb CLI!
