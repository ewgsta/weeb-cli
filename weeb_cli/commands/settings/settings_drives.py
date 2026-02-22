import os
import time
import questionary
from pathlib import Path
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header

console = Console()

def external_drives_menu():
    from weeb_cli.services.local_library import local_library
    
    while True:
        console.clear()
        show_header(i18n.t("settings.external_drives"))
        
        drives = local_library.get_external_drives()
        
        opt_add = i18n.t("settings.add_drive")
        choices = [questionary.Choice(opt_add, value="add")]
        
        for drive in drives:
            path = Path(drive["path"])
            status = "● " if path.exists() else "○ "
            choices.append(questionary.Choice(
                f"{status}{drive['name']} ({drive['path']})",
                value=drive
            ))
        
        try:
            sel = questionary.select(
                i18n.t("settings.external_drives"),
                choices=choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == "add":
                add_external_drive()
            else:
                manage_drive(sel)
                
        except KeyboardInterrupt:
            return

def add_external_drive():
    from weeb_cli.services.local_library import local_library
    
    try:
        path = questionary.text(
            i18n.t("settings.enter_drive_path"),
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        if not Path(path).exists():
            console.print(f"[yellow]{i18n.t('settings.drive_not_found')}[/yellow]")
            time.sleep(1)
            return
        
        name = questionary.text(
            i18n.t("settings.enter_drive_name"),
            default=os.path.basename(path) or path,
            qmark=">"
        ).ask()
        
        if name:
            local_library.add_external_drive(path, name)
            console.print(f"[green]{i18n.t('settings.drive_added')}[/green]")
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        pass

def manage_drive(drive):
    from weeb_cli.services.local_library import local_library
    
    while True:
        console.clear()
        show_header(drive["name"])
        
        console.print(f"[dim]{drive['path']}[/dim]\n")
        
        opt_rename = i18n.t("settings.rename_drive")
        opt_remove = i18n.t("settings.remove_drive")
        
        try:
            sel = questionary.select(
                i18n.t("downloads.action_prompt"),
                choices=[opt_rename, opt_remove],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_rename:
                new_name = questionary.text(
                    i18n.t("settings.enter_drive_name"),
                    default=drive["name"],
                    qmark=">"
                ).ask()
                if new_name:
                    local_library.rename_external_drive(drive["path"], new_name)
                    drive["name"] = new_name
                    console.print(f"[green]{i18n.t('settings.drive_renamed')}[/green]")
                    time.sleep(0.5)
                    
            elif sel == opt_remove:
                confirm = questionary.confirm(
                    i18n.t("settings.confirm_remove"),
                    default=False
                ).ask()
                if confirm:
                    local_library.remove_external_drive(drive["path"])
                    console.print(f"[green]{i18n.t('settings.drive_removed')}[/green]")
                    time.sleep(0.5)
                    return
                    
        except KeyboardInterrupt:
            return
