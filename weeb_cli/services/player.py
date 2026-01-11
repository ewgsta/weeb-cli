import subprocess
import shutil
import sys
from rich.console import Console

from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.i18n import i18n

console = Console()

class Player:
    def __init__(self):
        self.mpv_path = dependency_manager.check_dependency("mpv")
    
    def is_installed(self):
        return self.mpv_path is not None

    def play(self, url, title=None, start_time=None, headers=None):
        if not self.mpv_path:
            console.print(f"[yellow]{i18n.get('player.installing_mpv')}[/yellow]")
            if dependency_manager.install_dependency("mpv"):
                self.mpv_path = dependency_manager.check_dependency("mpv")
            
        if not self.mpv_path:
            console.print(f"[red]{i18n.get('player.install_failed')}[/red]")
            return False

        cmd = [self.mpv_path, url]
        if title:
            cmd.extend([f"--force-media-title={title}"])
        
        if headers:
            header_strs = [f"{k}: {v}" for k, v in headers.items()]
            cmd.append(f"--http-header-fields={','.join(header_strs)}")
        
        cmd.append("--fs")

        cmd.append("--save-position-on-quit")
            
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except Exception as e:
            console.print(f"[red]Error running player: {e}[/red]")
            return False

player = Player()
