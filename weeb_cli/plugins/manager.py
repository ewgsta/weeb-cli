import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Type
from datetime import datetime

from weeb_cli.config import CONFIG_DIR
from weeb_cli.services.logger import debug
from weeb_cli.providers.base import BaseProvider
from weeb_cli.plugins.parser import (
    parse_plugin_file,
    extract_plugin,
    remove_plugin_files,
    get_plugin_dir,
    list_plugin_dirs,
    ensure_plugins_dir,
    PLUGINS_DIR,
)
from weeb_cli.plugins.sandbox import load_plugin_module, unload_plugin_module


PLUGIN_PREFIX = "plugin:"


class PluginManager:
    def __init__(self):
        self._loaded_providers: Dict[str, Type[BaseProvider]] = {}
        self._plugin_meta: Dict[str, Dict[str, Any]] = {}
        self._initialized = False
    
    def _get_db(self):
        from weeb_cli.services.database import db
        return db
    
    def initialize(self):
        if self._initialized:
            return
        
        self._initialized = True
        self._load_installed_plugins()
    
    def _load_installed_plugins(self):
        plugin_dirs = list_plugin_dirs()
        
        for plugin_dir in plugin_dirs:
            try:
                manifest_path = plugin_dir / "manifest.json"
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                
                plugin_name = manifest.get("name", plugin_dir.name)
                
                if not self._is_plugin_enabled(plugin_name):
                    debug(f"[PluginManager] '{plugin_name}' disabled, skipping.")
                    continue
                
                self._load_single_plugin(plugin_name, plugin_dir, manifest)
                
            except Exception as e:
                debug(f"[PluginManager] Plugin load error ({plugin_dir.name}): {e}")
    
    def _load_single_plugin(self, plugin_name: str, plugin_dir: Path, manifest: dict) -> bool:
        entry_point = manifest.get("entry_point", "provider.py")
        entry_class = manifest.get("entry_class", "")
        
        if not entry_class:
            debug(f"[PluginManager] '{plugin_name}': entry_class not specified.")
            return False
        
        provider_class = load_plugin_module(
            plugin_name, plugin_dir, entry_point, entry_class
        )
        
        if provider_class is None:
            debug(f"[PluginManager] '{plugin_name}' failed to load.")
            return False
        
        provider_class.name = plugin_name
        provider_class.lang = manifest.get("lang", "tr")
        provider_class.region = manifest.get("region", "TR")
        
        registry_name = f"{PLUGIN_PREFIX}{plugin_name}"
        
        self._loaded_providers[registry_name] = provider_class
        self._plugin_meta[registry_name] = {
            "name": registry_name,
            "display_name": manifest.get("display_name", plugin_name),
            "lang": manifest.get("lang", "tr"),
            "region": manifest.get("region", "TR"),
            "class": entry_class,
            "version": manifest.get("version", "0.0.0"),
            "author": manifest.get("author", "Unknown"),
            "description": manifest.get("description", ""),
            "is_plugin": True,
        }
        
        debug(f"[PluginManager] '{plugin_name}' loaded successfully.")
        return True
    
    def install_plugin(self, plugin_path: str) -> tuple[bool, str]:
        success, manifest, error = parse_plugin_file(plugin_path)
        
        if not success:
            return False, error or "Unknown error"
        
        plugin_name = manifest["name"]
        
        extract_ok, extract_error = extract_plugin(plugin_path, manifest)
        if not extract_ok:
            return False, extract_error or "Extraction error"
        
        plugin_dir = get_plugin_dir(plugin_name)
        if not plugin_dir:
            return False, "Plugin directory could not be created."
        
        load_ok = self._load_single_plugin(plugin_name, plugin_dir, manifest)
        if not load_ok:
            remove_plugin_files(plugin_name)
            return False, "Plugin could not be loaded. Code validation may have failed."
        
        try:
            db = self._get_db()
            db.register_plugin(
                name=plugin_name,
                version=manifest.get("version", "0.0.0"),
                author=manifest.get("author", ""),
                lang=manifest.get("lang", "tr"),
                display_name=manifest.get("display_name", plugin_name),
                description=manifest.get("description", ""),
            )
        except Exception as e:
            debug(f"[PluginManager] DB register error: {e}")
        
        self._register_to_provider_registry(plugin_name)
        
        display = manifest.get('display_name', plugin_name)
        return True, f"'{display}' installed successfully."
    
    def uninstall_plugin(self, plugin_name: str) -> tuple[bool, str]:
        registry_name = plugin_name
        if not plugin_name.startswith(PLUGIN_PREFIX):
            registry_name = f"{PLUGIN_PREFIX}{plugin_name}"
        
        bare_name = plugin_name.replace(PLUGIN_PREFIX, "")
        
        if registry_name in self._loaded_providers:
            del self._loaded_providers[registry_name]
        if registry_name in self._plugin_meta:
            del self._plugin_meta[registry_name]
        
        unload_plugin_module(bare_name)
        
        self._unregister_from_provider_registry(bare_name)
        
        remove_ok, remove_error = remove_plugin_files(bare_name)
        if not remove_ok:
            return False, remove_error or "File removal error"
        
        try:
            db = self._get_db()
            db.unregister_plugin(bare_name)
        except Exception as e:
            debug(f"[PluginManager] DB removal error: {e}")
        
        return True, f"'{bare_name}' uninstalled successfully."
    
    def enable_plugin(self, plugin_name: str) -> tuple[bool, str]:
        bare_name = plugin_name.replace(PLUGIN_PREFIX, "")
        
        try:
            db = self._get_db()
            db.set_plugin_enabled(bare_name, True)
        except Exception as e:
            return False, f"DB error: {e}"
        
        plugin_dir = get_plugin_dir(bare_name)
        if plugin_dir:
            manifest_path = plugin_dir / "manifest.json"
            if manifest_path.exists():
                with open(manifest_path, "r", encoding="utf-8") as f:
                    manifest = json.load(f)
                self._load_single_plugin(bare_name, plugin_dir, manifest)
                self._register_to_provider_registry(bare_name)
        
        return True, f"'{bare_name}' enabled."
    
    def disable_plugin(self, plugin_name: str) -> tuple[bool, str]:
        bare_name = plugin_name.replace(PLUGIN_PREFIX, "")
        registry_name = f"{PLUGIN_PREFIX}{bare_name}"
        
        try:
            db = self._get_db()
            db.set_plugin_enabled(bare_name, False)
        except Exception as e:
            return False, f"DB error: {e}"
        
        if registry_name in self._loaded_providers:
            del self._loaded_providers[registry_name]
        if registry_name in self._plugin_meta:
            del self._plugin_meta[registry_name]
        
        self._unregister_from_provider_registry(bare_name)
        unload_plugin_module(bare_name)
        
        return True, f"'{bare_name}' disabled."
    
    def list_plugins(self) -> List[Dict[str, Any]]:
        plugins = []
        
        try:
            db = self._get_db()
            db_plugins = db.get_all_plugins()
            
            for p in db_plugins:
                registry_name = f"{PLUGIN_PREFIX}{p['name']}"
                is_loaded = registry_name in self._loaded_providers
                
                plugins.append({
                    "name": p["name"],
                    "display_name": p.get("display_name", p["name"]),
                    "version": p.get("version", "0.0.0"),
                    "author": p.get("author", ""),
                    "lang": p.get("lang", "tr"),
                    "description": p.get("description", ""),
                    "enabled": p.get("enabled", True),
                    "loaded": is_loaded,
                    "installed_at": p.get("installed_at", ""),
                })
        except Exception as e:
            debug(f"[PluginManager] Plugin list error: {e}")
            
            for dir_path in list_plugin_dirs():
                try:
                    manifest_path = dir_path / "manifest.json"
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    
                    name = manifest.get("name", dir_path.name)
                    registry_name = f"{PLUGIN_PREFIX}{name}"
                    
                    plugins.append({
                        "name": name,
                        "display_name": manifest.get("display_name", name),
                        "version": manifest.get("version", "0.0.0"),
                        "author": manifest.get("author", ""),
                        "lang": manifest.get("lang", "tr"),
                        "description": manifest.get("description", ""),
                        "enabled": True,
                        "loaded": registry_name in self._loaded_providers,
                        "installed_at": "",
                    })
                except Exception:
                    pass
        
        return plugins
    
    def get_plugin_provider(self, name: str) -> Optional[BaseProvider]:
        registry_name = name if name.startswith(PLUGIN_PREFIX) else f"{PLUGIN_PREFIX}{name}"
        
        if registry_name in self._loaded_providers:
            try:
                return self._loaded_providers[registry_name]()
            except Exception as e:
                debug(f"[PluginManager] Provider instance error: {e}")
        return None
    
    def get_plugin_providers(self) -> Dict[str, Type[BaseProvider]]:
        return dict(self._loaded_providers)
    
    def get_plugin_meta(self) -> Dict[str, dict]:
        return dict(self._plugin_meta)
    
    def get_plugins_for_lang(self, lang: str) -> List[str]:
        return [
            name for name, meta in self._plugin_meta.items()
            if meta.get("lang") == lang
        ]
    
    def _is_plugin_enabled(self, plugin_name: str) -> bool:
        try:
            db = self._get_db()
            plugin_data = db.get_plugin(plugin_name)
            if plugin_data:
                return plugin_data.get("enabled", True)
        except Exception:
            pass
        return True
    
    def _register_to_provider_registry(self, plugin_name: str):
        from weeb_cli.providers.registry import _providers, _provider_meta
        
        registry_name = f"{PLUGIN_PREFIX}{plugin_name}"
        
        if registry_name in self._loaded_providers:
            _providers[registry_name] = self._loaded_providers[registry_name]
        
        if registry_name in self._plugin_meta:
            _provider_meta[registry_name] = self._plugin_meta[registry_name]
    
    def _unregister_from_provider_registry(self, plugin_name: str):
        from weeb_cli.providers.registry import _providers, _provider_meta
        
        registry_name = f"{PLUGIN_PREFIX}{plugin_name}"
        
        _providers.pop(registry_name, None)
        _provider_meta.pop(registry_name, None)


plugin_manager = PluginManager()
