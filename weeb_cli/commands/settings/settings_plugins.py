import questionary
import time
import json
import requests
from pathlib import Path
from rich.console import Console
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
            i18n.t("settings.check_updates"),
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
        elif answer == i18n.t("settings.check_updates"):
            _check_updates_flow()
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
            i18n.t("settings.load_plugin") + " (URL or local path):"
        ).ask()
        
        if not path_str:
            return
            
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

def _check_updates_flow():
    console.print(f"[cyan]{i18n.t('settings.checking_updates')}[/cyan]")
    # In a real scenario, this would query the gallery API
    # For now, we just simulate the process
    time.sleep(1)
    
    plugins = plugin_manager.plugins
    updates_available = []
    
    for p_id, plugin in plugins.items():
        # Mock check: if version is 1.0.0, an update is available
        if plugin.manifest.version == "1.0.0":
            updates_available.append(plugin)
            
    if not updates_available:
        console.print(f"[green]{i18n.t('settings.up_to_date')}[/green]")
        time.sleep(1)
        return
        
    console.print(f"\n[yellow]{i18n.t('settings.updates_available', count=len(updates_available))}[/yellow]")
    for p in updates_available:
        console.print(f"- {p.manifest.name}: v{p.manifest.version} -> v1.1.0")
        
    try:
        if questionary.confirm(i18n.t('settings.update_prompt')).ask():
            console.print(f"[cyan]{i18n.t('settings.updating')}[/cyan]")
            time.sleep(2)
            console.print(f"[green]{i18n.t('settings.update_success')}[/green]")
    except KeyboardInterrupt:
        pass
        
    time.sleep(1)
