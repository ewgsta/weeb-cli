# API Commands

Nicht-interaktive JSON-API-Befehle.

## Übersicht

API-Befehle bieten JSON-Ausgabe für:
- Skripte und Automatisierung
- Integration mit Tools
- Headless-Betrieb

## Befehle

### providers

Alle Provider auflisten.

```bash
weeb-cli api providers
```

### search

Nach Anime suchen.

```bash
weeb-cli api search "query" --provider animecix
```

### episodes

Episodenliste abrufen.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

### streams

Stream-URLs abrufen.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

## Implementierung

Alle Befehle in `weeb_cli/commands/api.py`.

## Nächste Schritte

- [API-Modus-Anleitung](../../cli/api-mode.md): Detaillierte Verwendung
- [Befehlsreferenz](../../cli/commands.md): Alle Befehle
