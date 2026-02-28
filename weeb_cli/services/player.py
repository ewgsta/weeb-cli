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

    def play(self, url, title=None, start_time=None, headers=None, anime_title=None, episode_number=None, total_episodes=None):
        if not self.mpv_path:
            console.print(f"[yellow]{i18n.t('player.installing_mpv')}[/yellow]")
            if dependency_manager.install_dependency("mpv"):
                self.mpv_path = dependency_manager.check_dependency("mpv")
            
        if not self.mpv_path:
            console.print(f"[red]{i18n.t('player.install_failed')}[/red]")
            return False

        from weeb_cli.services.discord_rpc import discord_rpc
        
        if anime_title and episode_number:
            discord_rpc.update_presence(anime_title, episode_number, total_episodes)

        cmd = [self.mpv_path, url]
        if title:
            cmd.extend([f"--force-media-title={title}"])
        
        if headers:
            header_strs = [f"{k}: {v}" for k, v in headers.items()]
            cmd.append(f"--http-header-fields={','.join(header_strs)}")
        
        cmd.append("--fs")

        cmd.append("--save-position-on-quit")
        cmd.append("--really-quiet")
        cmd.append("--no-terminal")
            
        try:
            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            if result.returncode != 0 and result.stderr:
                console.print(f"[red]{i18n.t('player.error')}: {result.stderr.strip()}[/red]")
            return result.returncode == 0
        except FileNotFoundError:
            console.print(f"[red]{i18n.t('player.error')}: MPV not found at {self.mpv_path}[/red]")
            return False
        except Exception as e:
            console.print(f"[red]{i18n.t('player.error')}: {e}[/red]")
            return False
        finally:
            discord_rpc.clear_presence()

player = Player()
