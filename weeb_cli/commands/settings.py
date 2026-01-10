import questionary
from rich.console import Console
from weeb_cli.i18n import i18n

console = Console()

def open_settings():
    while True:
        choices = [
            i18n.get("settings.language"),
            i18n.get("settings.back")
        ]
        
        answer = questionary.select(
            i18n.get("settings.title"),
            choices=choices,
            use_indicator=True,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan'),
                ('selected', 'fg:cyan bold'),
            ])
        ).ask()
        
        if answer == i18n.get("settings.language"):
            change_language()
        else:
            break

def change_language():
    # Hardcoded list of supported languages
    langs = {
        "Türkçe": "tr",
        "English": "en"
    }
    
    selected = questionary.select(
        "Select Language / Dil Seçiniz:",
        choices=list(langs.keys()),
        use_indicator=True
    ).ask()
    
    if selected:
        code = langs[selected]
        i18n.set_language(code)
        console.print(f"[green]{i18n.get('settings.language_changed')}[/green]")
