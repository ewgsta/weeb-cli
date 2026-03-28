# Installation

Weeb CLI kann je nach Plattform und Präferenz auf verschiedene Arten installiert werden.

## PyPI (Universal)

Der einfachste Weg, Weeb CLI zu installieren, ist über pip:

```bash
pip install weeb-cli
```

Um auf die neueste Version zu aktualisieren:

```bash
pip install --upgrade weeb-cli
```

## Arch Linux (AUR)

Für Arch Linux-Benutzer ist Weeb CLI im AUR verfügbar:

```bash
yay -S weeb-cli
```

Oder mit einem anderen AUR-Helper:

```bash
paru -S weeb-cli
```

## Portable Executables

Vorgefertigte portable ausführbare Dateien sind für Windows, macOS und Linux auf der [Releases](https://github.com/ewgsta/weeb-cli/releases)-Seite verfügbar.

1. Laden Sie die entsprechende Datei für Ihre Plattform herunter
2. Extrahieren Sie das Archiv
3. Führen Sie die ausführbare Datei aus

## Entwickler-Installation

Für die Entwicklung oder Beiträge zum Projekt:

```bash
# Repository klonen
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Im bearbeitbaren Modus installieren
pip install -e .

# Entwicklungsabhängigkeiten installieren
pip install -r requirements.txt
```

## Abhängigkeiten

Weeb CLI lädt beim ersten Start automatisch die folgenden Abhängigkeiten herunter und installiert sie:

- **FFmpeg**: Videoverarbeitung und -konvertierung
- **MPV**: Mediaplayer für Streaming
- **Aria2**: Schnelle Multi-Verbindungs-Downloads
- **yt-dlp**: Stream-Extraktion und Download

Diese Tools werden nach `~/.weeb-cli/bin/` heruntergeladen und automatisch verwaltet.

## Überprüfung

Überprüfen Sie nach der Installation, ob Weeb CLI korrekt installiert ist:

```bash
weeb-cli --version
```

Sie sollten die Versionsnummer sehen.

## Nächste Schritte

- [Schnellstart-Anleitung](quickstart.md): Erste Schritte mit Weeb CLI
- [Konfiguration](configuration.md): Konfigurieren Sie Ihre Einstellungen
