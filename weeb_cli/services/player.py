import subprocess
import threading
import time
import socket
import json
import os
import platform
import tempfile
from typing import Optional, Dict, Callable
from rich.console import Console
from weeb_cli.services.logger import debug as log_debug, error as log_error

from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.services.error_handler import handle_error
from weeb_cli.i18n import i18n

console = Console()

class Player:
    def __init__(self) -> None:
        self.mpv_path: Optional[str] = dependency_manager.check_dependency("mpv")
        self._ipc_path: Optional[str] = None
        self._monitor_thread: Optional[threading.Thread] = None
        self._stop_monitor = threading.Event()
        self._current_anime_data: Dict = {}
    
    def is_installed(self) -> bool:
        return self.mpv_path is not None

    def _get_ipc_path(self) -> str:
        if platform.system() == "Windows":
            return r"\\.\pipe\mpv-ipc-" + str(os.getpid())
        else:
            return os.path.join(tempfile.gettempdir(), f"mpv-ipc-{os.getpid()}.sock")

    def _send_ipc_command(self, sock: socket.socket, command: list) -> Optional[Dict]:
        try:
            req = json.dumps({"command": command}) + "\n"
            sock.sendall(req.encode("utf-8"))
            
            # Read response (simple line-based)
            data = b""
            while not data.endswith(b"\n"):
                chunk = sock.recv(1024)
                if not chunk: break
                data += chunk
            
            if data:
                return json.loads(data.decode("utf-8"))
        except Exception:
            pass
        return None

    def _monitor_mpv(self, ipc_path: str, slug: str, anime_title: str, on_watched: Optional[Callable]):
        log_debug(f"[Player] Monitor started for {slug}")
        self._stop_monitor.clear()
        
        # Give MPV a moment to start and create the socket
        time.sleep(2)
        
        from weeb_cli.services.database import db
        
        sock = None
        last_save_time = time.time()
        watched_triggered = False
        
        try:
            if platform.system() == "Windows":
                # For Windows, we'd need a different approach for named pipes if using standard socket
                # For now, we'll focus on Unix-like socket or skip monitor on Windows if complex
                log_debug("[Player] IPC Monitor on Windows is currently limited")
                return
            
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.connect(ipc_path)
            sock.settimeout(2)
            
            while not self._stop_monitor.is_set():
                # Get current position and duration
                pos_resp = self._send_ipc_command(sock, ["get_property", "time-pos"])
                dur_resp = self._send_ipc_command(sock, ["get_property", "duration"])
                
                if pos_resp and dur_resp and "data" in pos_resp and "data" in dur_resp:
                    curr_pos = pos_resp["data"]
                    duration = dur_resp["data"]
                    
                    if duration > 0:
                        progress = (curr_pos / duration) * 100
                        
                        # Auto-mark as watched at 80%
                        if progress >= 80 and not watched_triggered:
                            log_debug(f"[Player] Auto-mark triggered for {slug} (%{progress:.1f})")
                            if on_watched:
                                on_watched()
                            watched_triggered = True
                        
                        # Periodic save (every 15s)
                        if time.time() - last_save_time > 15:
                            db.save_progress(
                                slug, 
                                anime_title, 
                                self._current_anime_data.get("episode_number", 0),
                                self._current_anime_data.get("total_episodes", 0),
                                db.get_progress(slug).get("completed", []),
                                datetime.now().isoformat(),
                                current_time=curr_pos,
                                duration=duration
                            )
                            last_save_time = time.time()
                            log_debug(f"[Player] Progress saved: {curr_pos:.1f}/{duration:.1f}")
                
                time.sleep(5)
                
        except Exception as e:
            log_debug(f"[Player] Monitor error: {e}")
        finally:
            if sock:
                try:
                    # Final save before closing
                    if 'curr_pos' in locals() and 'duration' in locals():
                        db.save_progress(
                            slug, 
                            anime_title, 
                            self._current_anime_data.get("episode_number", 0),
                            self._current_anime_data.get("total_episodes", 0),
                            db.get_progress(slug).get("completed", []),
                            datetime.now().isoformat(),
                            current_time=curr_pos,
                            duration=duration
                        )
                    sock.close()
                except Exception:
                    pass
            if os.path.exists(ipc_path) and platform.system() != "Windows":
                try: os.unlink(ipc_path)
                except Exception: pass

    def play(self, url: str, title: Optional[str] = None, start_time: Optional[int] = None, 
             headers: Optional[Dict[str, str]] = None, anime_title: Optional[str] = None, 
             episode_number: Optional[int] = None, total_episodes: Optional[int] = None,
             slug: Optional[str] = None, on_watched: Optional[Callable] = None) -> bool:
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

        self._current_anime_data = {
            "slug": slug,
            "anime_title": anime_title,
            "episode_number": episode_number,
            "total_episodes": total_episodes
        }

        ipc_path = self._get_ipc_path()
        cmd = [self.mpv_path, url]
        
        if platform.system() != "Windows":
            cmd.append(f"--input-ipc-server={ipc_path}")
        
        if title:
            cmd.extend([f"--force-media-title={title}"])
        
        # Priority: explicit start_time > DB saved time
        if start_time:
            cmd.append(f"--start={start_time}")
        elif slug:
            from weeb_cli.services.database import db
            prog = db.get_progress(slug)
            if prog and prog.get("current_time", 0) > 0:
                # If duration is known and we are near the end, don't resume
                if not (prog.get("duration", 0) > 0 and prog["current_time"] > prog["duration"] * 0.95):
                    cmd.append(f"--start={int(prog['current_time'])}")
                    log_debug(f"[Player] Resuming from {prog['current_time']}s")
        
        if headers:
            for k, v in headers.items():
                cmd.append(f"--http-header-fields={k}: {v}")
        
        cmd.append("--fs")
        cmd.append("--save-position-on-quit")
        cmd.append("--really-quiet")
        cmd.append("--no-terminal")
        
        log_debug(f"[Player] MPV cmd: {' '.join(cmd[:5])}... ({len(cmd)} args)")
            
        try:
            if slug and platform.system() != "Windows":
                self._monitor_thread = threading.Thread(
                    target=self._monitor_mpv, 
                    args=(ipc_path, slug, anime_title or "Anime", on_watched),
                    daemon=True
                )
                self._monitor_thread.start()

            result = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
            
            if self._monitor_thread:
                self._stop_monitor.set()
                self._monitor_thread.join(timeout=1)

            if result.returncode != 0 and result.stderr:
                console.print(f"[red]{i18n.t('player.error')}: {result.stderr.strip()}[/red]")
            return result.returncode == 0
        except FileNotFoundError as e:
            handle_error(e, "Player:MPV", f"{i18n.t('player.error')}: MPV not found at {self.mpv_path}")
            return False
        except Exception as e:
            handle_error(e, "Player:MPV")
            return False
        finally:
            discord_rpc.clear_presence()

player = Player()
