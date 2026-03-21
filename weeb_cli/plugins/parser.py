import json
import zipfile
import shutil
from pathlib import Path
from typing import Tuple, Optional, Dict, Any

from weeb_cli.config import CONFIG_DIR
from weeb_cli.services.logger import debug
from weeb_cli.plugins.validator import (
    validate_manifest,
    validate_code,
    validate_entry_class,
    check_version_compatibility,
)

PLUGINS_DIR = CONFIG_DIR / "plugins"


def ensure_plugins_dir() -> Path:
    PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
    return PLUGINS_DIR


def parse_plugin_file(plugin_path: str) -> Tuple[bool, Optional[Dict[str, Any]], Optional[str]]:
    path = Path(plugin_path)
    
    if not path.exists():
        return False, None, f"File not found: {plugin_path}"
    
    if not path.suffix == ".weeb-plugin":
        return False, None, "File extension must be '.weeb-plugin'."
    
    if not zipfile.is_zipfile(path):
        return False, None, "Invalid plugin file. File may be corrupted."
    
    try:
        with zipfile.ZipFile(path, 'r') as zf:
            names = zf.namelist()
            
            if "manifest.json" not in names:
                return False, None, "manifest.json not found in plugin."
            
            manifest_data = json.loads(zf.read("manifest.json").decode("utf-8"))
            
            valid, error = validate_manifest(manifest_data)
            if not valid:
                return False, None, f"Manifest error: {error}"
            
            from weeb_cli import __version__
            compatible, compat_error = check_version_compatibility(manifest_data, __version__)
            if not compatible:
                return False, None, compat_error
            
            entry_point = manifest_data["entry_point"]
            if entry_point not in names:
                return False, None, f"Entry point file not found: {entry_point}"
            
            source_code = zf.read(entry_point).decode("utf-8")
            
            code_valid, code_error, warnings = validate_code(source_code)
            if not code_valid:
                return False, None, f"Code validation error: {code_error}"
            
            entry_class = manifest_data["entry_class"]
            class_valid, class_error = validate_entry_class(source_code, entry_class)
            if not class_valid:
                return False, None, f"Class error: {class_error}"
            
            if warnings:
                for w in warnings:
                    debug(f"[Plugin] Warning: {w}")
            
            return True, manifest_data, None
            
    except json.JSONDecodeError as e:
        return False, None, f"manifest.json parse error: {e}"
    except zipfile.BadZipFile:
        return False, None, "Corrupted ZIP file."
    except Exception as e:
        return False, None, f"Plugin parse error: {e}"


def extract_plugin(plugin_path: str, manifest: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    plugin_name = manifest["name"]
    target_dir = ensure_plugins_dir() / plugin_name
    
    if target_dir.exists():
        try:
            shutil.rmtree(target_dir)
        except Exception as e:
            return False, f"Failed to remove old plugin dir: {e}"
    
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(plugin_path, 'r') as zf:
            for member in zf.namelist():
                safe_path = Path(member)
                if ".." in safe_path.parts:
                    debug(f"[Plugin] Unsafe path skipped: {member}")
                    continue
                
                target_path = target_dir / safe_path
                
                if member.endswith("/"):
                    target_path.mkdir(parents=True, exist_ok=True)
                else:
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                    target_path.write_bytes(zf.read(member))
        
        debug(f"[Plugin] '{plugin_name}' extracted: {target_dir}")
        return True, None
        
    except Exception as e:
        if target_dir.exists():
            shutil.rmtree(target_dir, ignore_errors=True)
        return False, f"Plugin extraction error: {e}"


def remove_plugin_files(plugin_name: str) -> Tuple[bool, Optional[str]]:
    target_dir = PLUGINS_DIR / plugin_name
    
    if not target_dir.exists():
        return True, None
    
    try:
        shutil.rmtree(target_dir)
        debug(f"[Plugin] '{plugin_name}' files removed.")
        return True, None
    except Exception as e:
        return False, f"Failed to remove plugin files: {e}"


def get_plugin_dir(plugin_name: str) -> Optional[Path]:
    target_dir = PLUGINS_DIR / plugin_name
    if target_dir.exists() and target_dir.is_dir():
        return target_dir
    return None


def list_plugin_dirs() -> list:
    if not PLUGINS_DIR.exists():
        return []
    
    dirs = []
    for item in PLUGINS_DIR.iterdir():
        if item.is_dir() and (item / "manifest.json").exists():
            dirs.append(item)
    return dirs
