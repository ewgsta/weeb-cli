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
        
        opt_aria2_conf = f"  ↳ {i18n.get('settings.aria2_config')}"
        opt_ytdlp_conf = f"  ↳ {i18n.get('settings.ytdlp_config')}"
        
        choices = [opt_lang, opt_source, opt_aria2]
        if config.get("aria2_enabled"):
            choices.append(opt_aria2_conf)
            
        choices.append(opt_ytdlp)
        if config.get("ytdlp_enabled"):
            choices.append(opt_ytdlp_conf)
        
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
        elif answer == opt_aria2_conf:
            aria2_settings_menu()
        elif answer == opt_ytdlp:
            toggle_config("ytdlp_enabled", "yt-dlp")
        elif answer == opt_ytdlp_conf:
            ytdlp_settings_menu()
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
            save_val = "local" if selected == "Weeb" else selected
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

def aria2_settings_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.aria2_config"))
        
        curr_conn = config.get("aria2_max_connections", 16)
        curr_dir = config.get("aria2_download_dir")
        
        opt_conn = f"{i18n.get('settings.max_conn')} [{curr_conn}]"
        opt_dir = f"{i18n.get('settings.download_dir')} [{curr_dir}]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.aria2_config"),
                choices=[opt_conn, opt_dir],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_conn:
                val = questionary.text(f"{i18n.get('settings.enter_conn')}:", default=str(curr_conn)).ask()
                if val and val.isdigit():
                    config.set("aria2_max_connections", int(val))
            elif sel == opt_dir:
                val = questionary.text(f"{i18n.get('settings.enter_path')}:", default=str(curr_dir)).ask()
                if val:
                    config.set("aria2_download_dir", val)
            elif sel is None:
                return
        except KeyboardInterrupt:
            return

def ytdlp_settings_menu():
    while True:
        console.clear()
        show_header(i18n.get("settings.ytdlp_config"))
        
        curr_fmt = config.get("ytdlp_format", "best")
        opt_fmt = f"{i18n.get('settings.format')} [{curr_fmt}]"
        
        try:
            sel = questionary.select(
                i18n.get("settings.ytdlp_config"), 
                choices=[opt_fmt], 
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_fmt:
                val = questionary.text(f"{i18n.get('settings.enter_format')}:", default=curr_fmt).ask()
                if val:
                    config.set("ytdlp_format", val)
            elif sel is None:
                return
        except KeyboardInterrupt:
            return
