import questionary
import time
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.cache import get_cache
from weeb_cli.config import config

console = Console()

SELECT_STYLE = questionary.Style([
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan'),
    ('selected', 'fg:cyan bold'),
])

def cache_settings_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.cache_title"))
        
        cache = get_cache()
        stats = cache.get_stats()
        
        console.print(f"[dim]{i18n.t('settings.cache_memory_entries')}: {stats['memory_entries']}[/dim]")
        console.print(f"[dim]{i18n.t('settings.cache_file_entries')}: {stats['file_entries']}[/dim]")
        console.print(f"[dim]{i18n.t('settings.cache_total_size')}: {stats['total_size_mb']} MB[/dim]\n")
        
        choices = [
            i18n.t("settings.cache_clear_all"),
            i18n.t("settings.cache_clear_provider"),
            i18n.t("settings.cache_cleanup_old"),
        ]
        
        try:
            answer = questionary.select(
                i18n.t("settings.cache_prompt"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=SELECT_STYLE
            ).ask()
        except KeyboardInterrupt:
            return
        
        if answer is None:
            return
        
        if answer == i18n.t("settings.cache_clear_all"):
            confirm = questionary.confirm(
                i18n.t("settings.cache_confirm_clear_all"),
                default=False
            ).ask()
            
            if confirm:
                cache.clear()
                console.print(f"[green]{i18n.t('settings.cache_cleared')}[/green]")
                time.sleep(1)
        
        elif answer == i18n.t("settings.cache_clear_provider"):
            provider = config.get("scraping_source", "None")
            removed = cache.invalidate_provider(provider)
            console.print(f"[green]{i18n.t('settings.cache_provider_cleared')}: {removed} {i18n.t('common.items')}[/green]")
            time.sleep(1)
        
        elif answer == i18n.t("settings.cache_cleanup_old"):
            removed = cache.cleanup(max_age=86400)
            console.print(f"[green]{i18n.t('settings.cache_cleaned')}: {removed} {i18n.t('common.items')}[/green]")
            time.sleep(1)
