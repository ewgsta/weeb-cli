# Plugin-Entwicklungsleitfaden

Weeb CLI bietet eine robuste Plugin-Architektur, mit der Sie die Anwendung durch benutzerdefinierte Anbieter, Tracker und Dienste erweitern können. Plugins sind in einer sicheren, portablen Umgebung isoliert und folgen einer standardisierten Verzeichnisstruktur.

## Plugin-Struktur

Ein Standard-Plugin-Ordner muss im Verzeichnis `data/` gespeichert sein und die folgende Struktur aufweisen:

```
data/
  mein-plugin/
    plugin.weeb        (Haupt-Code-Einstiegspunkt)
    manifest.json      (Metadaten und Konfiguration)
    README.md          (Detaillierte Dokumentation)
    screenshots/       (Mindestens ein Screenshot für die Galerie)
      ss1.png
    assets/            (Icons und andere Assets)
      icon.png
```

### manifest.json

Das Manifest enthält obligatorische und optionale Metadaten über Ihr Plugin:

```json
{
    "id": "mein-plugin",
    "name": "Mein Plugin",
    "version": "1.0.0",
    "description": "Eine Beschreibung Ihres Plugins.",
    "author": "Ihr Name",
    "entry_point": "plugin.weeb",
    "min_weeb_version": "1.0.0",
    "dependencies": [],
    "permissions": ["network", "storage"],
    "tags": ["anime", "de"],
    "icon": "assets/icon.png",
    "homepage": "https://example.com",
    "repository_url": "https://github.com/user/repo",
    "license": "MIT"
}
```

### plugin.weeb

Der Einstiegspunkt ist ein Python-Skript, das eine `register()`-Funktion definieren muss. Es läuft in einer eingeschränkten Sandbox-Umgebung mit Zugriff auf eine sichere Untermenge von Builtins und `weeb_cli`-APIs.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("mein_benutzerdefinierter_anbieter", lang="de", region="DE")
    class MyProvider(BaseProvider):
        def search(self, query: str):
            # Implementierung...
            pass
```

## Erstellung und Paketierung

Verwenden Sie das bereitgestellte Builder-Skript, um neue Plugins zu erstellen oder zu paketieren:

```bash
# Erstellen Sie eine neue Plugin-Vorlage
python3 weeb_cli/utils/plugin_builder.py create mein-neues-plugin --id "neue-id" --name "Neuer Name"

# Erstellen/Paketieren Sie ein Plugin für die Verteilung (.weeb_pkg)
python3 weeb_cli/utils/plugin_builder.py build data/mein-plugin -o mein-plugin.weeb_pkg
```

## Installation

1. Öffnen Sie Weeb CLI.
2. Gehen Sie zu **Einstellungen** > **Plugins**.
3. Wählen Sie **Plugin laden**.
4. Geben Sie den lokalen Pfad zum Plugin-Ordner oder dessen `.weeb_pkg` an.

## Testen und Qualität

Plugins müssen eine **Testabdeckung von mindestens 80 %** aufweisen, um in die offizielle Galerie aufgenommen zu werden. Automatisierte Tests sollten in einem Verzeichnis `tests/` innerhalb des Plugin-Ordners platziert werden.

Unsere CI/CD-Pipeline validiert:
- **Manifest-Integrität**: Erforderliche Felder (ID, Name, Version usw.) müssen vorhanden sein.
- **Sicherheit**: Überprüfung durch Bandit auf häufige Schwachstellen.
- **Codequalität**: Überprüfung durch Ruff.
- **Funktionalität**: Tests werden ausgeführt und die Abdeckung wird geprüft.

## Teilen über die Galerie

Reichen Sie einen Pull Request ein, um Ihren Plugin-Ordner zum Verzeichnis `data/` hinzuzufügen. Sobald er genehmigt wurde, erscheint er automatisch in der [Plugin-Galerie](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html).
