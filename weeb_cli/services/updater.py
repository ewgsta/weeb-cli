import requests
from packaging import version
from weeb_cli import __version__
from rich.console import Console
import questionary
from weeb_cli.i18n import i18n
import sys
import os
import platform
import subprocess
import tempfile

console = Console()

def get_install_method():
    if getattr(sys, 'frozen', False):
        return "exe"
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "weeb-cli"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            return "pip"
    except Exception:
        pass
    
    return "standalone"

def get_platform_info():
    system = platform.system().lower()
    machine = platform.machine().lower()
    
    if system == "windows":
        return "windows", "exe"
    elif system == "darwin":
        return "macos", "macos" if "arm" in machine else "macos-intel"
    elif system == "linux":
        return "linux", "linux"
    else:
        return system, system

def check_for_updates():
    try:
        url = "https://api.github.com/repos/ewgsta/weeb-cli/releases/latest"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            latest_tag = data.get("tag_name", "").lstrip("v")
            assets = data.get("assets", [])
            
            if not latest_tag:
                return False, None, None
                
            current_ver = version.parse(__version__)
            latest_ver = version.parse(latest_tag)
            
            if latest_ver > current_ver:
                return True, latest_tag, assets
                
    except Exception:
        pass
        
    return False, None, None

def find_asset_for_platform(assets):
    system, platform_key = get_platform_info()
    
    for asset in assets:
        name = asset.get("name", "").lower()
        download_url = asset.get("browser_download_url", "")
        
        if system == "windows" and name.endswith(".exe"):
            return download_url, name
        elif system == "darwin" and ("macos" in name or "darwin" in name):
            return download_url, name
        elif system == "linux" and "linux" in name:
            return download_url, name
    
    return None, None

def download_exe(url, filename):
    try:
        console.print(f"[cyan]{i18n.get('update.downloading')}...[/cyan]")
        
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        
        if getattr(sys, 'frozen', False):
            current_exe = sys.executable
            download_dir = os.path.dirname(current_exe)
            new_exe_path = os.path.join(download_dir, f"weeb-cli-new.exe")
        else:
            download_dir = tempfile.gettempdir()
            new_exe_path = os.path.join(download_dir, filename)
        
        downloaded = 0
        with open(new_exe_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = int((downloaded / total_size) * 100)
                        console.print(f"\r[cyan]İndiriliyor: {percent}%[/cyan]", end="")
        
        console.print(f"\n[green]{i18n.get('update.downloaded')}[/green]")
        console.print(f"[dim]Konum: {new_exe_path}[/dim]")
        
        if getattr(sys, 'frozen', False):
            batch_content = f'''@echo off
timeout /t 2 /nobreak >nul
del "{current_exe}"
move "{new_exe_path}" "{current_exe}"
start "" "{current_exe}"
del "%~f0"
'''
            batch_path = os.path.join(download_dir, "update.bat")
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            
            console.print(f"[green]{i18n.get('update.restarting')}...[/green]")
            subprocess.Popen(['cmd', '/c', batch_path], 
                           creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0)
            sys.exit(0)
        
        return True
        
    except Exception as e:
        console.print(f"[red]{i18n.get('update.error')}: {e}[/red]")
        return False

def update_via_pip():
    try:
        console.print(f"[cyan]{i18n.get('update.updating_pip')}...[/cyan]")
        
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "weeb-cli"],
            capture_output=True, text=True, timeout=120
        )
        
        if result.returncode == 0:
            console.print(f"[green]{i18n.get('update.success')}[/green]")
            console.print(f"[dim]{i18n.get('update.restart_required')}[/dim]")
            return True
        else:
            console.print(f"[red]{i18n.get('update.error')}[/red]")
            console.print(f"[dim]{result.stderr}[/dim]")
            return False
            
    except Exception as e:
        console.print(f"[red]{i18n.get('update.error')}: {e}[/red]")
        return False

from weeb_cli.config import config
import time

def update_prompt():
    last_check = float(config.get("last_update_check") or 0)
    if time.time() - last_check < 86400: # 24 hours
        return

    is_available, latest_ver, assets = check_for_updates()
    config.set("last_update_check", str(time.time()))
    
    if not is_available:
        return
    
    console.clear()
    console.print(f"\n[green bold]{i18n.get('update.available')} (v{latest_ver})[/green bold]")
    console.print(f"[dim]{i18n.get('update.current')}: v{__version__}[/dim]\n")
    
    should_update = questionary.confirm(
        i18n.get("update.prompt"),
        default=True
    ).ask()
    
    if not should_update:
        return
    
    install_method = get_install_method()
    
    if install_method == "exe":
        asset_url, asset_name = find_asset_for_platform(assets or [])
        if asset_url:
            download_exe(asset_url, asset_name)
        else:
            console.print(f"[red]{i18n.get('update.no_asset')}[/red]")
            
    elif install_method == "pip":
        update_via_pip()
        
    else:
        asset_url, asset_name = find_asset_for_platform(assets or [])
        if asset_url:
            system, _ = get_platform_info()
            if system == "windows":
                download_exe(asset_url, asset_name)
            else:
                console.print(f"[cyan]{i18n.get('update.download_url')}:[/cyan]")
                console.print(f"[blue]{asset_url}[/blue]")
        else:
            console.print(f"[yellow]{i18n.get('update.manual_update')}[/yellow]")
            console.print("[blue]pip install --upgrade weeb-cli[/blue]")
