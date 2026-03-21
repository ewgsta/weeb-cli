import time
import questionary
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from weeb_cli.i18n import i18n
from weeb_cli.config import config

console = Console()

SELECT_STYLE = questionary.Style([
    ('pointer', 'fg:cyan bold'),
    ('highlighted', 'fg:cyan'),
    ('selected', 'fg:cyan bold'),
])


def plugins_menu():
    from weeb_cli.plugins.manager import plugin_manager
    
    while True:
        console.clear()
        
        plugins = plugin_manager.list_plugins()
        _show_plugins_header(plugins)
        
        opt_install = i18n.t("plugins.install", "Install Plugin")
        
        choices = [opt_install]
        
        plugin_choices = {}
        for p in plugins:
            state = i18n.t("common.enabled", "Enabled") if p["enabled"] else i18n.t("common.disabled", "Disabled")
            loaded = "+" if p["loaded"] else "-"
            label = f"  {loaded} {p['display_name']} v{p['version']} [{state}]"
            choices.append(label)
            plugin_choices[label] = p
        
        try:
            answer = questionary.select(
                i18n.t("plugins.title", "Plugin Manager"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=SELECT_STYLE
            ).ask()
        except KeyboardInterrupt:
            return
        
        if answer is None:
            return
        
        if answer == opt_install:
            _install_plugin_flow()
        elif answer in plugin_choices:
            _plugin_detail_menu(plugin_choices[answer])


def _show_plugins_header(plugins):
    total = len(plugins)
    active = sum(1 for p in plugins if p["enabled"])
    
    header_text = f"[bold cyan]{i18n.t('plugins.title', 'Plugin Manager')}[/bold cyan]\n"
    header_text += f"[dim]{i18n.t('plugins.total', 'Total')}: {total} | "
    header_text += f"{i18n.t('common.enabled', 'Enabled')}: {active}[/dim]"
    
    console.print(Panel(header_text, border_style="cyan"))
    console.print()


def _install_plugin_flow():
    from weeb_cli.plugins.manager import plugin_manager
    
    console.print(f"\n[cyan]{i18n.t('plugins.install_hint', 'Enter the path to a .weeb-plugin file.')}[/cyan]")
    console.print(f"[dim]{i18n.t('plugins.install_example', 'Example: /home/user/my-source.weeb-plugin')}[/dim]\n")
    
    try:
        path = questionary.text(
            i18n.t("plugins.file_path", "File path") + ":",
        ).ask()
    except KeyboardInterrupt:
        return
    
    if not path:
        return
    
    path = path.strip().strip("'\"")
    
    with console.status(f"[cyan]{i18n.t('plugins.installing', 'Installing...')}[/cyan]", spinner="dots"):
        success, message = plugin_manager.install_plugin(path)
    
    if success:
        console.print(f"\n[green]{message}[/green]")
    else:
        console.print(f"\n[red]{message}[/red]")
    
    time.sleep(1.5)


def _plugin_detail_menu(plugin_info: dict):
    from weeb_cli.plugins.manager import plugin_manager
    
    while True:
        console.clear()
        
        table = Table(
            title=f"[bold]{plugin_info['display_name']}[/bold]",
            show_header=False,
            border_style="cyan",
            pad_edge=True,
        )
        table.add_column("Key", style="dim", width=16)
        table.add_column("Value")
        
        table.add_row(i18n.t("plugins.name", "Name"), plugin_info["name"])
        table.add_row(i18n.t("plugins.version_label", "Version"), plugin_info["version"])
        table.add_row(i18n.t("plugins.author", "Author"), plugin_info.get("author", "-"))
        table.add_row(i18n.t("plugins.lang_label", "Language"), plugin_info.get("lang", "-").upper())
        
        desc = plugin_info.get("description", "")
        if desc:
            table.add_row(i18n.t("plugins.description", "Description"), desc)
        
        state = i18n.t("common.enabled", "Enabled") if plugin_info["enabled"] else i18n.t("common.disabled", "Disabled")
        state_color = "green" if plugin_info["enabled"] else "red"
        table.add_row(i18n.t("plugins.status", "Status"), f"[{state_color}]{state}[/{state_color}]")
        
        loaded_text = "+" if plugin_info["loaded"] else "-"
        loaded_color = "green" if plugin_info["loaded"] else "red"
        table.add_row(i18n.t("plugins.loaded", "Loaded"), f"[{loaded_color}]{loaded_text}[/{loaded_color}]")
        
        if plugin_info.get("installed_at"):
            table.add_row(i18n.t("plugins.installed_at", "Installed At"), plugin_info["installed_at"])
        
        console.print(table)
        console.print()
        
        if plugin_info["enabled"]:
            opt_toggle = i18n.t("plugins.disable", "Disable")
        else:
            opt_toggle = i18n.t("plugins.enable", "Enable")
        
        opt_uninstall = i18n.t("plugins.uninstall", "Uninstall")
        
        choices = [opt_toggle, opt_uninstall]
        
        try:
            action = questionary.select(
                i18n.t("plugins.action", "Select Action"),
                choices=choices,
                pointer=">",
                use_shortcuts=False,
                style=SELECT_STYLE
            ).ask()
        except KeyboardInterrupt:
            return
        
        if action is None:
            return
        
        if action == opt_toggle:
            if plugin_info["enabled"]:
                ok, msg = plugin_manager.disable_plugin(plugin_info["name"])
                plugin_info["enabled"] = False
                plugin_info["loaded"] = False
            else:
                ok, msg = plugin_manager.enable_plugin(plugin_info["name"])
                plugin_info["enabled"] = True
                plugin_info["loaded"] = True
            
            color = "green" if ok else "red"
            console.print(f"[{color}]{msg}[/{color}]")
            time.sleep(1)
        
        elif action == opt_uninstall:
            try:
                confirm = questionary.confirm(
                    i18n.t("plugins.confirm_uninstall", "Are you sure you want to uninstall this plugin?"),
                    default=False
                ).ask()
            except KeyboardInterrupt:
                continue
            
            if confirm:
                ok, msg = plugin_manager.uninstall_plugin(plugin_info["name"])
                color = "green" if ok else "red"
                console.print(f"[{color}]{msg}[/{color}]")
                time.sleep(1)
                return
