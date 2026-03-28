# Beitragen zu Weeb CLI

<div align="center">
  <a href="../../CONTRIBUTING.md">English</a> | <a href="../tr/CONTRIBUTING.md">Türkçe</a> | <a href="CONTRIBUTING.md">Deutsch</a> | <a href="../pl/CONTRIBUTING.md">Polski</a>
</div>
<br>

Zunächst einmal vielen Dank, dass du in Erwägung ziehst, zu Weeb CLI beizutragen! Deine Hilfe wird sehr geschätzt.

Wenn du Anime, Tools und das Terminal magst, bist du hier genau richtig.

## Erste Schritte

1. **Forke das Repository** auf GitHub.
2. **Klone deinen Fork** lokal:
   ```bash
   git clone https://github.com/ewgsta/weeb-cli.git
   cd weeb-cli
   ```
3. **Installiere Abhängigkeiten** im bearbeitbaren Modus (editable mode):
   ```bash
   pip install -e .
   ```

## Workflow

1. Erstelle einen neuen Branch für deine Funktion oder deinen Fehlerbehebung (Bugfix):
   ```bash
   git checkout -b feature/ein-guter-name
   ```
2. Nimm deine Änderungen am Code vor.
3. Um deine CLI-Änderungen lokal zu testen, kannst du `weeb-cli` ausführen, welches auf das Skript deiner aktiven Umgebung verweisen sollte.
4. Versuche, Tests zu schreiben. Sie befinden sich im Verzeichnis `tests/`.
   ```bash
   pytest
   ```
5. Führe einen Commit deiner Änderungen durch. Stelle sicher, dass deine Commit-Nachrichten klar beschreiben, was geändert wurde.
6. Pushe auf deinen Fork und eröffne einen Pull Request für den `main`-Branch.

## Pull Requests

- Beschränke deine Pull Requests auf eine einzige Änderung, Funktion oder Fehlerbehebung. Dies macht den Überprüfungsprozess reibungsloser.
- Verlinke zugehörige Issues in deinem PR, damit die Maintainer den Kontext verstehen.
- Halte dich an den bestehenden Code-Stil (verwende Black/Flake8 für Python-Komponenten).
- Aktualisiere die Dokumentation (`README.md`, `md/tr/README.md` usw.), falls deine Änderungen das externe Verhalten beeinflussen.

## Issues

Wenn du einen Fehler findest oder einen Vorschlag hast, kannst du gerne ein Issue eröffnen:
- **Suche nach bestehenden Issues**, bevor du ein neues erstellst, um Duplikate zu vermeiden.
- Gib so viel Kontext wie möglich an. Erwähne das Betriebssystem, die Python-Version und die Weeb CLI-Version.
- Füge ein reproduzierbares Beispiel, Logs oder Screenshots hinzu, wo zutreffend.

## Übersetzungen & i18n

Da Weeb CLI mehrere Sprachen unterstützt:
- Funktionen, die Texte zur Benutzeroberfläche hinzufügen, sollten die entsprechenden JSON-Dateien in `locales/` (`en.json`, `tr.json`, `de.json`, `pl.json` usw.) anpassen.

---

Nochmals vielen Dank für deinen Beitrag!
