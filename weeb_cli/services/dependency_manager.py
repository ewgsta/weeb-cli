import os
import sys
import platform
import shutil
import requests
import zipfile
import tarfile
import stat
import subprocess
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, DownloadColumn, TransferSpeedColumn
from ..config import config
from ..i18n import i18n

try:
    import py7zr
except ImportError:
    py7zr = None

console = Console()

class DependencyManager:
    def __init__(self):
        self.os_type = platform.system().lower()
        self.arch = platform.machine().lower()
        self.bin_dir = Path.home() / ".weeb-cli" / "bin"
        self._ensure_bin_dir()

        mpv_macos_url = "https://laboratory.stolendata.net/~djinn/mpv_osx/mpv-latest.tar.gz"
        if self.arch == "arm64":
            mpv_macos_url = "https://laboratory.stolendata.net/~djinn/mpv_osx/mpv-arm64-latest.tar.gz"

        self.dependencies = {
            "windows": {
                "yt-dlp": {
                    "url": ["https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp.exe"],
                    "type": "binary",
                    "filename": "yt-dlp.exe",
                    "pkg": {"winget": "yt-dlp", "choco": "yt-dlp", "scoop": "yt-dlp"}
                },
                "ffmpeg": {
                    "url": [
                        "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
                        "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
                    ],
                    "type": "archive",
                    "files": ["ffmpeg.exe", "ffprobe.exe"],
                    "pkg": {"winget": "Gyan.FFmpeg", "choco": "ffmpeg", "scoop": "ffmpeg"}
                },
                "mpv": {
                    "url": [
                        "https://github.com/shinchiro/mpv-winbuild-cmake/releases/download/v20240114/mpv-x86_64-v3-20240114-git-07ec82e.7z", 
                        "https://sourceforge.net/projects/mpv-player-windows/files/64bit/mpv-x86_64-20231224-git-0a30b42.7z/download"
                    ],
                    "type": "archive", 
                    "filename": "mpv.exe",
                    "pkg": {"winget": "MutanteOz.mpv", "choco": "mpv", "scoop": "mpv"}
                },
                "aria2": {
                     "url": ["https://github.com/aria2/aria2/releases/download/release-1.37.0/aria2-1.37.0-win-64bit-build1.zip"],
                     "type": "archive",
                     "files": ["aria2c.exe"],
                     "pkg": {"winget": "aria2", "choco": "aria2", "scoop": "aria2"}
                }
            },
            "linux": {
                "yt-dlp": {
                    "url": ["https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp"],
                    "type": "binary",
                    "filename": "yt-dlp",
                    "pkg": {"brew": "yt-dlp", "yay": "yt-dlp", "pacman": "yt-dlp", "apt": "yt-dlp"}
                },
                "ffmpeg": {
                    "url": ["https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"],
                    "type": "archive",
                    "files": ["ffmpeg", "ffprobe"],
                    "pkg": {"brew": "ffmpeg", "yay": "ffmpeg", "pacman": "ffmpeg", "apt": "ffmpeg"}
                },
                 "aria2": {
                     "url": ["https://github.com/q3aql/aria2-static-builds/releases/download/v1.36.0/aria2-1.36.0-linux-gnu-64bit-build1.tar.bz2"],
                     "type": "archive",
                     "files": ["aria2c"],
                     "pkg": {"brew": "aria2", "yay": "aria2", "pacman": "aria2", "apt": "aria2"}
                },
                "mpv": {
                    "url": ["https://github.com/pkgforge-dev/mpv-AppImage/releases/latest/download/mpv-x86_64.AppImage"],
                    "type": "binary",
                    "filename": "mpv",
                    "pkg": {"brew": "mpv", "yay": "mpv-git", "pacman": "mpv", "apt": "mpv"}
                }
            },
            "darwin": { 
                 "yt-dlp": {
                    "url": ["https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp_macos"],
                    "type": "binary",
                    "filename": "yt-dlp",
                    "pkg": {"brew": "yt-dlp"}
                },
                "ffmpeg": {
                     "url": ["https://evermeet.cx/ffmpeg/getrelease/zip"],
                     "type": "archive",
                     "files": ["ffmpeg", "ffprobe"],
                     "pkg": {"brew": "ffmpeg"}
                },
                "mpv": {
                    "url": [mpv_macos_url],
                    "type": "archive",
                    "files": ["mpv"],
                    "pkg": {"brew": "mpv"}
                }
            }
        }

    def _ensure_bin_dir(self):
        if not self.bin_dir.exists():
            self.bin_dir.mkdir(parents=True, exist_ok=True)
        if str(self.bin_dir) not in os.environ["PATH"]:
            os.environ["PATH"] += os.pathsep + str(self.bin_dir)

    def check_dependency(self, name):
        exe_name = f"{name}.exe" if self.os_type == "windows" else name
        local_path = self.bin_dir / exe_name
        
        if local_path.exists():
            return str(local_path)
            
        system_path = shutil.which(name)
        return system_path

    def install_dependency(self, name):
        if self.os_type not in self.dependencies or name not in self.dependencies[self.os_type]:
            console.print(f"[yellow]{i18n.t('setup.manual_required', tool=name)}[/yellow]")
            return False

        if self._try_package_managers(name):
            return True
            
        return self._install_direct(name)

    def _try_package_managers(self, name):
        info = self.dependencies[self.os_type][name]
        pkg_map = info.get("pkg", {})
        
        managers = {
            "scoop": ["scoop", "install"],
            "choco": ["choco", "install", "-y"],
            "brew": ["brew", "install"],
            "yay": ["yay", "-S", "--noconfirm"],
            "pacman": ["sudo", "pacman", "-S", "--noconfirm"],
            "apt": ["sudo", "apt", "install", "-y"],
            "winget": ["winget", "install", "-e", "--id"],
        }
        
        for mgr, cmd_prefix in managers.items():
            if mgr in pkg_map and shutil.which(mgr):
                pkg_name = pkg_map[mgr]
                console.print(f"[cyan]{i18n.t('setup.pkg_manager_try', manager=mgr)}[/cyan]")
                
                full_cmd = cmd_prefix + [pkg_name]
                try:
                    subprocess.run(full_cmd, check=True, timeout=60)
                    console.print(f"[green]{i18n.t('setup.success', tool=name)}[/green]")
                    return True
                except subprocess.CalledProcessError:
                    continue
        return False

    def _install_direct(self, name):
        info = self.dependencies[self.os_type][name]
        urls = info["url"]
        
        console.print(f"[cyan]{i18n.t('setup.downloading', tool=name)}[/cyan]")
        
        success = False
        downloaded_file = None

        for url in urls:
            try:
                downloaded_file = self._download_file(url, f"temp_{name}")
                success = True
                break
            except Exception as e:
                console.print(f"[red]{i18n.t('common.error')}: {e}[/red]")
                continue
        
        if not success or not downloaded_file:
            console.print(f"[red]{i18n.t('setup.failed', tool=name)}[/red]")
            return False

        try:
            if info["type"] == "binary":
                target = self.bin_dir / info["filename"]
                
                if target.exists():
                    os.remove(target)
                
                shutil.move(downloaded_file, target)
                self._make_executable(target)
            
            elif info["type"] == "archive":
                self._extract_and_install(downloaded_file, info.get("files", []), name)
            
            console.print(f"[green]{i18n.t('setup.success', tool=name)}[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]{i18n.t('setup.failed', tool=name)}: {e}[/red]")
            return False
        finally:
            if downloaded_file and os.path.exists(downloaded_file):
                os.remove(downloaded_file)

    def _get_temp_dir(self):
        temp_dir = self.bin_dir / "temp"
        temp_dir.mkdir(exist_ok=True)
        return temp_dir

    def _download_file(self, url, prefix):
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        filename = url.split("/")[-1]
        temp_path = self._get_temp_dir() / (prefix + "_" + filename)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
        ) as progress:
            task = progress.add_task(f"[cyan]Downloading...", total=total_size)
            
            with open(temp_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))
                    
        return temp_path

    def _extract_and_install(self, archive_path, target_files, tool_name):
        archive_path = str(archive_path)
        
        temp_extract = self._get_temp_dir() / "extract"
        if temp_extract.exists():
            shutil.rmtree(temp_extract)
        temp_extract.mkdir()

        try:
            if archive_path.endswith(".zip"):
                with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_extract)
            elif archive_path.endswith(".7z"):
                if not py7zr:
                    raise Exception("py7zr missing")
                with py7zr.SevenZipFile(archive_path, mode='r') as z:
                    z.extractall(path=temp_extract)
            elif archive_path.endswith((".tar.gz", ".tar.xz", ".tar.bz2", ".tgz")):
                with tarfile.open(archive_path, "r:*") as tar_ref:
                    tar_ref.extractall(temp_extract)
            else:
                raise Exception("Unsupported format")

            found_count = 0
            for root, dirs, files in os.walk(temp_extract):
                for file in files:
                    is_target = False
                    
                    if file in target_files:
                        is_target = True
                    
                    if self.os_type == "windows" and not is_target:
                        simple_name = file.lower().replace(".exe", "")
                        if f"{simple_name}.exe" == file.lower() and \
                           (simple_name in target_files or simple_name == tool_name):
                            is_target = True
                    
                    if self.os_type == "darwin" and tool_name == "mpv" and file == "mpv":
                         if "Contents" in root and "MacOS" in root:
                             is_target = True

                    if is_target:
                         source = Path(root) / file
                         target_name = file
                         target = self.bin_dir / target_name
                         
                         if target.exists():
                             os.remove(target)
                             
                         shutil.move(str(source), str(target))
                         self._make_executable(target)
                         found_count += 1
            
            if found_count == 0:
                for root, dirs, files in os.walk(temp_extract):
                    for file in files:
                        if file.startswith(tool_name) and (file.endswith(".exe") or "." not in file):
                            source = Path(root) / file
                            target = self.bin_dir / file
                            if target.exists():
                                os.remove(target)
                            shutil.move(str(source), str(target))
                            self._make_executable(target)
                            found_count += 1
                            break

            if found_count == 0:
                raise Exception("Binary not found in archive")

        finally:
            if temp_extract.exists():
                shutil.rmtree(temp_extract)

    def _make_executable(self, path):
        if self.os_type != "windows":
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)

dependency_manager = DependencyManager()
