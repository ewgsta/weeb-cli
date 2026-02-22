import time
import questionary
from pathlib import Path
from datetime import datetime
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header

console = Console()

def backup_restore_menu():
    from weeb_cli.services.database import db
    
    while True:
        console.clear()
        show_header(i18n.t("settings.backup_restore"))
        
        db_size = db.db_path.stat().st_size / 1024
        console.print(f"[dim]{i18n.t('settings.db_location')}: {db.db_path}[/dim]")
        console.print(f"[dim]{i18n.t('settings.db_size')}: {db_size:.2f} KB[/dim]\n")
        
        opt_backup = i18n.t("settings.create_backup")
        opt_restore = i18n.t("settings.restore_backup")
        
        try:
            sel = questionary.select(
                i18n.t("downloads.action_prompt"),
                choices=[opt_backup, opt_restore],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if sel is None:
                return
            
            if sel == opt_backup:
                create_backup()
            elif sel == opt_restore:
                restore_backup()
                
        except KeyboardInterrupt:
            return

def create_backup():
    from weeb_cli.services.database import db
    
    default_name = f"weeb-backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}.db"
    
    try:
        path = questionary.text(
            i18n.t("settings.backup_path"),
            default=default_name,
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        backup_path = Path(path)
        if not backup_path.suffix:
            backup_path = backup_path.with_suffix('.db')
        
        with console.status(i18n.t("common.processing"), spinner="dots"):
            success = db.backup_database(backup_path)
        
        if success:
            console.print(f"[green]{i18n.t('settings.backup_success')}[/green]")
            console.print(f"[dim]{backup_path.absolute()}[/dim]")
        else:
            console.print(f"[red]{i18n.t('settings.backup_failed')}[/red]")
        
        time.sleep(2)
        
    except KeyboardInterrupt:
        pass

def restore_backup():
    from weeb_cli.services.database import db
    
    try:
        path = questionary.text(
            i18n.t("settings.restore_path"),
            qmark=">"
        ).ask()
        
        if not path:
            return
        
        backup_path = Path(path)
        
        if not backup_path.exists():
            console.print(f"[red]{i18n.t('settings.backup_not_found')}[/red]")
            time.sleep(1.5)
            return
        
        confirm = questionary.confirm(
            i18n.t("settings.restore_confirm"),
            default=False
        ).ask()
        
        if not confirm:
            return
        
        with console.status(i18n.t("common.processing"), spinner="dots"):
            success = db.restore_database(backup_path)
        
        if success:
            console.print(f"[green]{i18n.t('settings.restore_success')}[/green]")
            console.print(f"[yellow]{i18n.t('settings.restart_required')}[/yellow]")
        else:
            console.print(f"[red]{i18n.t('settings.restore_failed')}[/red]")
        
        time.sleep(2)
        
    except KeyboardInterrupt:
        pass
