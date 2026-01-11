import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.config import config
import time
from weeb_cli.ui.header import show_header

console = Console()

def open_settings():
    while True:
        console.clear()
        show_header(i18n.get("settings.title"))
        
        lang = config.get("language")
        source = config.get("scraping_source", "local")
        display_source = "weeb" if source == "local" else source

        aria2_state = i18n.get("common.enabled") if config.get("aria2_enabled") else i18n.get("common.disabled")
        ytdlp_state = i18n.get("common.enabled") if config.get("ytdlp_enabled") else i18n.get("common.disabled")
        
        opt_lang = i18n.get("settings.language")
        opt_source = f"{i18n.get('settings.source')} [{display_source}]"
        opt_aria2 = f"{i18n.get('settings.aria2')} [{aria2_state}]"
        opt_ytdlp = f"{i18n.get('settings.ytdlp')} [{ytdlp_state}]"
        
        choices = [opt_lang, opt_source, opt_aria2, opt_ytdlp]
        
        try:
            answer = questionary.select(
                i18n.get("settings.title"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=questionary.Style([
                    ('pointer', 'fg:cyan bold'),
                    ('highlighted', 'fg:cyan'),
                    ('selected', 'fg:cyan bold'),
                ])
            ).ask()
        except KeyboardInterrupt:
            return

        if answer == opt_lang:
            change_language()
        elif answer == opt_source:
            change_source()
        elif answer == opt_aria2:
            toggle_config("aria2_enabled", "Aria2")
        elif answer == opt_ytdlp:
            toggle_config("ytdlp_enabled", "yt-dlp")
        elif answer is None:
            return

def change_language():
    langs = {"Türkçe": "tr", "English": "en"}
    try:
        selected = questionary.select(
            "Select Language / Dil Seçiniz:",
            choices=list(langs.keys()),
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected:
            lang_code = langs[selected]
            i18n.set_language(lang_code)
            
            new_source = "local" if lang_code == "tr" else "hianime"
            config.set("scraping_source", new_source)
            
            console.print(f"[green]{i18n.get('settings.language_changed')}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def change_source():
    current_lang = config.get("language")
    
    sources = []
    if current_lang == "tr":
        sources = ["weeb", "animecix", "turkanime", "anizle"]
    else:
        sources = ["hianime", "allanime"]
        
    try:
        selected = questionary.select(
            i18n.get("settings.source"),
            choices=sources,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected:
            save_val = "local" if selected == "weeb" else selected
            config.set("scraping_source", save_val)
            console.print(f"[green]{i18n.t('settings.source_changed', source=selected)}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
        
def toggle_config(key, name):
    current = config.get(key)
    new_val = not current
    config.set(key, new_val)
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=name)}[/green]")
    time.sleep(0.5)
