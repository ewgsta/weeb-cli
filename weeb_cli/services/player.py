import subprocess
import shutil
import sys
from rich.console import Console

console = Console()

class Player:
    def __init__(self):
        self.mpv_path = shutil.which("mpv")
    
    def is_installed(self):
        return self.mpv_path is not None

    def play(self, url, title=None, start_time=None, headers=None):
        if not self.mpv_path:
            console.print("[red]MPV not found. Please install mpv player.[/red]")
            return False

        
        cmd = [self.mpv_path, url]
        if title:
            cmd.extend([f"--force-media-title={title}"])
        
        if headers:
            header_strs = [f"{k}: {v}" for k, v in headers.items()]
            cmd.append(f"--http-header-fields={','.join(header_strs)}")
        
        # Start in fullscreen
        cmd.append("--fs")

        # Enable save position on quit explicitly
        cmd.append("--save-position-on-quit")
            
        try:
            subprocess.run(cmd)
            return True
        except Exception as e:
            console.print(f"[red]Error running player: {e}[/red]")
            return False

player = Player()
