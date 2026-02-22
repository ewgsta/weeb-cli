import os
import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.config import config
from weeb_cli.services.dependency_manager import dependency_manager

console = Console()

def toggle_config(key, name):
    current = config.get(key)
    new_val = not current
    
    if new_val:
        dep_name = name.lower()
        if "aria2" in dep_name:
            dep_name = "aria2"
        elif "yt-dlp" in dep_name:
            dep_name = "yt-dlp"
        
        path = dependency_manager.check_dependency(dep_name)
        if not path:
            console.print(f"[cyan]{i18n.t('setup.downloading', tool=name)}...[/cyan]")
            if not dependency_manager.install_dependency(dep_name):
                console.print(f"[red]{i18n.t('setup.failed', tool=name)}[/red]")
                time.sleep(1)
                return

    config.set(key, new_val)
    
    msg_key = "settings.toggle_on" if new_val else "settings.toggle_off"
    console.print(f"[green]{i18n.t(msg_key, tool=name)}[/green]")
    time.sleep(0.5)

def download_settings_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.download_settings"))
        
        curr_dir = config.get("download_dir")
        console.print(f"[dim]Current: {curr_dir}[/dim]\n", justify="left")
        
        curr_concurrent = config.get("max_concurrent_downloads", 3)
        curr_retries = config.get("download_max_retries", 3)
        curr_delay = config.get("download_retry_delay", 10)
        
        opt_name = i18n.t("settings.change_folder_name")
        opt_path = i18n.t("settings.change_full_path")
        opt_concurrent = f"{i18n.t('settings.concurrent_downloads')} [{curr_concurrent}]"
        opt_retries = f"{i18n.t('settings.max_retries')} [{curr_retries}]"
        opt_delay = f"{i18n.t('settings.retry_delay')} [{curr_delay}s]"
        
        try:
            sel = questionary.select(
                i18n.t("settings.download_settings"),
                choices=[opt_name, opt_path, opt_concurrent, opt_retries, opt_delay],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_name:
                _change_folder_name()
            elif sel == opt_path:
                _change_full_path(curr_dir)
            elif sel == opt_concurrent:
                _change_concurrent_downloads(curr_concurrent)
            elif sel == opt_retries:
                _change_max_retries(curr_retries)
            elif sel == opt_delay:
                _change_retry_delay(curr_delay)
                
        except KeyboardInterrupt:
            return

def _change_folder_name():
    default_name = i18n.t("downloads.default_folder_name", "weeb-downloads")
    val = questionary.text(i18n.t("settings.folder_name_prompt"), default=default_name).ask()
    if val:
        new_path = os.path.join(os.getcwd(), val)
        config.set("download_dir", new_path)

def _change_full_path(curr_dir):
    val = questionary.text(i18n.t("settings.full_path_prompt"), default=curr_dir).ask()
    if val:
        config.set("download_dir", val)

def _change_concurrent_downloads(curr_concurrent):
    val = questionary.text(i18n.t("settings.enter_concurrent"), default=str(curr_concurrent)).ask()
    if val and val.isdigit():
        n = int(val)
        if 1 <= n <= 5:
            config.set("max_concurrent_downloads", n)

def _change_max_retries(curr_retries):
    val = questionary.text(i18n.t("settings.enter_max_retries"), default=str(curr_retries)).ask()
    if val and val.isdigit():
        n = int(val)
        if 0 <= n <= 10:
            config.set("download_max_retries", n)

def _change_retry_delay(curr_delay):
    val = questionary.text(i18n.t("settings.enter_retry_delay"), default=str(curr_delay)).ask()
    if val and val.isdigit():
        config.set("download_retry_delay", int(val))

def aria2_settings_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.aria2_config"))
        
        curr_conn = config.get("aria2_max_connections", 16)
        opt_conn = f"{i18n.t('settings.max_conn')} [{curr_conn}]"
        
        try:
            sel = questionary.select(
                i18n.t("settings.aria2_config"),
                choices=[opt_conn],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_conn:
                val = questionary.text(f"{i18n.t('settings.enter_conn')}:", default=str(curr_conn)).ask()
                if val and val.isdigit():
                    config.set("aria2_max_connections", int(val))
            elif sel is None:
                return
        except KeyboardInterrupt:
            return

def ytdlp_settings_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.ytdlp_config"))
        
        curr_fmt = config.get("ytdlp_format", "best")
        opt_fmt = f"{i18n.t('settings.format')} [{curr_fmt}]"
        
        try:
            sel = questionary.select(
                i18n.t("settings.ytdlp_config"),
                choices=[opt_fmt],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel == opt_fmt:
                val = questionary.text(f"{i18n.t('settings.enter_format')}:", default=curr_fmt).ask()
                if val:
                    config.set("ytdlp_format", val)
            elif sel is None:
                return
        except KeyboardInterrupt:
            return
