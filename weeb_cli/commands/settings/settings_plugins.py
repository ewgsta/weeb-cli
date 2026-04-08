import time
import questionary
from rich.console import Console
from pathlib import Path
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.plugin_manager import plugin_manager, PluginError

console = Console()

SELECT_STYLE = questionary.Style([
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan'),
    ('selected', 'fg:cyan bold'),
])

def plugins_menu():
    while True:
        console.clear()
        show_header(i18n.t("settings.plugins"))
        
        plugins = plugin_manager.plugins
        choices = []
        
        for p_id, plugin in plugins.items():
            state = "[ON]" if plugin.enabled else "[OFF]"
            choices.append(f"{plugin.manifest.name} v{plugin.manifest.version} {state}")
            
        choices.extend([
            i18n.t("settings.load_plugin"),
            i18n.t("shortcut_back")
        ])
        
        try:
            answer = questionary.select(
                i18n.t("settings.plugin_management"),
                choices=choices,
                pointer=">",
                style=SELECT_STYLE
            ).ask()
        except KeyboardInterrupt:
            return

        if answer is None or answer == i18n.t("shortcut_back"):
            return
            
        if answer == i18n.t("settings.load_plugin"):
            _load_plugin_flow()
        else:
            # Toggle plugin
            plugin_name = answer.rsplit(' v', 1)[0]
            for p_id, plugin in plugins.items():
                if plugin.manifest.name == plugin_name:
                    _toggle_plugin(p_id)
                    break

def _load_plugin_flow():
    try:
        path_str = questionary.text(
            i18n.t("settings.load_plugin") + " (.weeb path):"
        ).ask()
        
        if path_str:
            path = Path(path_str).expanduser().resolve()
            if not path.exists():
                console.print(f"[red]{i18n.t('settings.drive_not_found')}[/red]")
                time.sleep(1)
                return
                
            plugin = plugin_manager.install_plugin(path)
            console.print(f"[green]Plugin installed: {plugin.manifest.name}[/green]")
            time.sleep(1)
    except Exception as e:
        console.print(f"[red]{i18n.t('settings.plugin_error', error=str(e))}[/red]")
        time.sleep(2)

def _toggle_plugin(plugin_id: str):
    plugin = plugin_manager.plugins.get(plugin_id)
    if not plugin:
        return
        
    try:
        if plugin.enabled:
            plugin_manager.disable_plugin(plugin_id)
            console.print(f"[yellow]{i18n.t('settings.plugin_disabled')}[/yellow]")
        else:
            plugin_manager.enable_plugin(plugin_id)
            console.print(f"[green]{i18n.t('settings.plugin_enabled')}[/green]")
    except Exception as e:
        console.print(f"[red]{i18n.t('settings.plugin_error', error=str(e))}[/red]")
    
    time.sleep(1)
