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

    def play(self, url, title=None, start_time=None):
        if not self.mpv_path:
            console.print("[red]MPV not found. Please install mpv player.[/red]")
            return False

        # Build command
        # --save-position-on-quit handled by mpv automatic logic usually, 
        # but we can enforce config or use watch-later feature.
        # User said "otomatik olacak". 
        # MPV saves position for URL if it can hash it.
        # We also pass title.
        
        cmd = [self.mpv_path, url]
        if title:
            cmd.extend([f"--force-media-title={title}"])
        
        # Enable save position on quit explicitly
        cmd.append("--save-position-on-quit")
        
        # If we had a specific start time managed by us, we would add --start=...
        # But we rely on MPV's internal watch-later feature for now as requested.
        
        try:
            # Run blocking
            subprocess.run(cmd)
            return True
        except Exception as e:
            console.print(f"[red]Error running player: {e}[/red]")
            return False

player = Player()
