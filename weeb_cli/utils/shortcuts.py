"""Desktop shortcut creation utilities.

Creates platform-specific shortcuts for easy application access:
- Linux: .desktop file in ~/.local/share/applications/
- macOS: .app alias in /Applications/
- Windows: Start Menu shortcut
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional


def get_executable_path() -> str:
    """Get the path to the weeb-cli executable.
    
    Returns:
        Path to the executable or python script.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys.executable
    else:
        # Running as Python script
        return shutil.which('weeb-cli') or sys.executable


def get_icon_path() -> Optional[str]:
    """Get the path to the application icon if available.
    
    Returns:
        Path to icon file or None.
    """
    # Try to find icon in package
    try:
        import weeb_cli
        package_dir = Path(weeb_cli.__file__).parent
        icon_path = package_dir / 'assets' / 'icon.png'
        if icon_path.exists():
            return str(icon_path)
    except Exception:
        pass
    return None


def create_linux_desktop_file() -> bool:
    """Create .desktop file for Linux.
    
    Creates a desktop entry in ~/.local/share/applications/
    following the freedesktop.org specification.
    
    Returns:
        True if successful, False otherwise.
    """
    try:
        apps_dir = Path.home() / '.local' / 'share' / 'applications'
        apps_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_file = apps_dir / 'weeb-cli.desktop'
        
        # Don't recreate if it already exists
        if desktop_file.exists():
            return True
        
        executable = get_executable_path()
        icon = get_icon_path() or 'utilities-terminal'
        
        content = f"""[Desktop Entry]
Version=1.0
Type=Application
Name=Weeb CLI
Comment=Terminal-based anime streaming application
Exec={executable}
Icon={icon}
Terminal=true
Categories=AudioVideo;Video;Player;
Keywords=anime;streaming;video;
StartupNotify=false
"""
        
        desktop_file.write_text(content)
        desktop_file.chmod(0o755)
        
        return True
    except Exception:
        return False


def create_macos_alias() -> bool:
    """Create application alias for macOS.
    
    Creates a symbolic link in /Applications/ if user has permissions,
    otherwise creates in ~/Applications/.
    
    Returns:
        True if successful, False otherwise.
    """
    try:
        executable = get_executable_path()
        
        # Try system Applications first, fallback to user Applications
        for apps_dir in [Path('/Applications'), Path.home() / 'Applications']:
            apps_dir.mkdir(parents=True, exist_ok=True)
            
            link_path = apps_dir / 'Weeb CLI'
            
            # Don't recreate if it already exists
            if link_path.exists():
                return True
            
            try:
                # Create symbolic link
                link_path.symlink_to(executable)
                return True
            except PermissionError:
                # Try next location
                continue
        
        return False
    except Exception:
        return False


def create_windows_shortcut() -> bool:
    """Create Start Menu shortcut for Windows.
    
    Creates a shortcut in the Start Menu using Windows COM API.
    
    Returns:
        True if successful, False otherwise.
    """
    try:
        import winshell
        from win32com.client import Dispatch
        
        start_menu = Path(winshell.start_menu())
        programs = start_menu / 'Programs'
        programs.mkdir(parents=True, exist_ok=True)
        
        shortcut_path = programs / 'Weeb CLI.lnk'
        
        # Don't recreate if it already exists
        if shortcut_path.exists():
            return True
        
        executable = get_executable_path()
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(str(shortcut_path))
        shortcut.TargetPath = executable
        shortcut.WorkingDirectory = str(Path.home())
        shortcut.Description = 'Terminal-based anime streaming application'
        
        icon = get_icon_path()
        if icon:
            shortcut.IconLocation = icon
        
        shortcut.save()
        
        return True
    except ImportError:
        # winshell or pywin32 not available
        return False
    except Exception:
        return False


def should_create_shortcuts() -> bool:
    """Check if shortcuts should be created.
    
    Returns:
        True if this is first run or shortcuts are missing.
    """
    from weeb_cli.config import CONFIG_DIR
    
    marker_file = CONFIG_DIR / '.shortcuts_created'
    
    # If marker exists, check if shortcuts still exist
    if marker_file.exists():
        if sys.platform == 'linux':
            desktop_file = Path.home() / '.local' / 'share' / 'applications' / 'weeb-cli.desktop'
            return not desktop_file.exists()
        elif sys.platform == 'darwin':
            for apps_dir in [Path('/Applications'), Path.home() / 'Applications']:
                if (apps_dir / 'Weeb CLI').exists():
                    return False
            return True
        elif sys.platform == 'win32':
            try:
                import winshell
                start_menu = Path(winshell.start_menu())
                shortcut = start_menu / 'Programs' / 'Weeb CLI.lnk'
                return not shortcut.exists()
            except ImportError:
                return False
    
    return True


def create_shortcuts() -> bool:
    """Create platform-specific shortcuts.
    
    Automatically detects the platform and creates appropriate shortcuts.
    Only runs on first launch or if shortcuts are missing.
    
    Returns:
        True if shortcuts were created successfully.
    """
    if not should_create_shortcuts():
        return True
    
    success = False
    
    if sys.platform == 'linux':
        success = create_linux_desktop_file()
    elif sys.platform == 'darwin':
        success = create_macos_alias()
    elif sys.platform == 'win32':
        success = create_windows_shortcut()
    
    # Mark as created even if failed to avoid repeated attempts
    if success:
        from weeb_cli.config import CONFIG_DIR
        marker_file = CONFIG_DIR / '.shortcuts_created'
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        marker_file.touch()
    
    return success


def remove_shortcuts() -> bool:
    """Remove all platform-specific shortcuts.
    
    Returns:
        True if shortcuts were removed successfully.
    """
    try:
        if sys.platform == 'linux':
            desktop_file = Path.home() / '.local' / 'share' / 'applications' / 'weeb-cli.desktop'
            if desktop_file.exists():
                desktop_file.unlink()
        
        elif sys.platform == 'darwin':
            for apps_dir in [Path('/Applications'), Path.home() / 'Applications']:
                link_path = apps_dir / 'Weeb CLI'
                if link_path.exists():
                    link_path.unlink()
        
        elif sys.platform == 'win32':
            try:
                import winshell
                start_menu = Path(winshell.start_menu())
                shortcut = start_menu / 'Programs' / 'Weeb CLI.lnk'
                if shortcut.exists():
                    shortcut.unlink()
            except ImportError:
                pass
        
        # Remove marker
        from weeb_cli.config import CONFIG_DIR
        marker_file = CONFIG_DIR / '.shortcuts_created'
        if marker_file.exists():
            marker_file.unlink()
        
        return True
    except Exception:
        return False
