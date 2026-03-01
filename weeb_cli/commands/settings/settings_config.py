import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.config import config

console = Console()

def toggle_description():
    current = config.get("show_description", True)
    config.set("show_description", not current)
    msg_key = "settings.toggle_on" if not current else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=i18n.t('settings.show_description'))}[/green]")
    time.sleep(0.5)

def toggle_discord_rpc():
    from weeb_cli.services.discord_rpc import discord_rpc
    
    current = config.get("discord_rpc_enabled", False)
    new_val = not current
    config.set("discord_rpc_enabled", new_val)
    
    if new_val:
        discord_rpc.connect()
    else:
        discord_rpc.disconnect()
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool='Discord RPC')}[/green]")
    time.sleep(0.5)

def toggle_shortcuts():
    current = config.get("shortcuts_enabled", True)
    new_val = not current
    config.set("shortcuts_enabled", new_val)
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=i18n.t('settings.shortcuts'))}[/green]")
    time.sleep(0.5)

def change_language():
    from weeb_cli.services.scraper import scraper
    
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
            
            sources = scraper.get_sources_for_lang(lang_code)
            if sources:
                config.set("scraping_source", sources[0])
            
            console.print(f"[green]{i18n.t('settings.language_changed')}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass

def change_source():
    from weeb_cli.services.scraper import scraper
    from weeb_cli.services.cache import get_cache
    
    current_lang = config.get("language", "tr")
    current_source = config.get("scraping_source", "")
    sources = scraper.get_sources_for_lang(current_lang)
    
    if not sources:
        console.print(f"[yellow]{i18n.t('settings.no_sources')}[/yellow]")
        time.sleep(1)
        return
        
    try:
        selected = questionary.select(
            i18n.t("settings.source"),
            choices=sources,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected and selected != current_source:
            cache = get_cache()
            cache.invalidate_provider(current_source)
            
            config.set("scraping_source", selected)
            console.print(f"[green]{i18n.t('settings.source_changed', source=selected)}[/green]")
            time.sleep(1)
    except KeyboardInterrupt:
        pass
