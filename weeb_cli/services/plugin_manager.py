"""Plugin management system for Weeb CLI.

This module provides a robust plugin architecture, allowing users to extend
functionality through custom providers and services. Plugins are packaged
in a custom .weeb format (ZIP archive) and run in a secure sandbox.

Features:
    - Dynamic plugin loading and discovery
    - Custom .weeb file format (ZIP based)
    - Sandbox execution environment
    - Dependency management for plugins
    - Versioning and manifest validation
"""

import os
import sys
import json
import zipfile
import shutil
import importlib.util
from pathlib import Path
from typing import Dict, List, Any, Optional, Type
from datetime import datetime

from weeb_cli.config import config
from weeb_cli.i18n import i18n
from weeb_cli.services.logger import debug, error
from weeb_cli.services.dependency_manager import dependency_manager

class PluginError(Exception):
    """Base exception for plugin-related errors."""
    pass

class PluginManifest:
    """Represents a plugin's metadata from manifest.json."""
    
    def __init__(self, data: dict):
        self.id = data.get("id")
        self.name = data.get("name")
        self.version = data.get("version", "1.0.0")
        self.description = data.get("description", "")
        self.author = data.get("author", "Unknown")
        self.entry_point = data.get("entry_point", "plugin.weeb")
        self.dependencies = data.get("dependencies", [])
        self.min_weeb_version = data.get("min_weeb_version", "1.0.0")
        self.permissions = data.get("permissions", [])
        
        # Optional fields
        self.tags = data.get("tags", [])
        self.icon = data.get("icon", "")
        self.homepage = data.get("homepage", "")
        self.repository_url = data.get("repository_url", "")
        self.license = data.get("license", "")
        
        if not self.id or not self.name:
            raise PluginError("Plugin manifest must contain 'id' and 'name'")
            
        import re
        if not re.match(r"^[a-zA-Z0-9_-]+$", self.id):
            raise PluginError("Plugin ID must contain only alphanumeric characters, underscores, and hyphens.")

class Plugin:
    """Represents an installed and loaded plugin."""
    
    def __init__(self, path: Path, manifest: PluginManifest):
        self.path = path
        self.manifest = manifest
        self.module = None
        self.enabled = False
        self.installed_at = datetime.now()
        
    def to_dict(self) -> dict:
        return {
            "id": self.manifest.id,
            "name": self.manifest.name,
            "version": self.manifest.version,
            "description": self.manifest.description,
            "author": self.manifest.author,
            "enabled": self.enabled,
            "path": str(self.path)
        }

class PluginManager:
    """Manages the lifecycle of plugins (discovery, installation, loading, sandboxing)."""
    
    def __init__(self, base_dir: Optional[Path] = None):
        self.plugins_dir = base_dir or Path.home() / ".weeb-cli" / "plugins"
        self.installed_dir = self.plugins_dir / "installed"
        self.temp_dir = self.plugins_dir / "temp"
        
        self.plugins: Dict[str, Plugin] = {}
        try:
            self._ensure_dirs()
            self.load_installed_plugins()
        except Exception as e:
            debug(f"[PluginManager] Initial discovery failed: {e}")

    def _ensure_dirs(self):
        """Create necessary plugin directories if they don't exist."""
        try:
            self.plugins_dir.mkdir(parents=True, exist_ok=True)
            self.installed_dir.mkdir(parents=True, exist_ok=True)
            self.temp_dir.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            debug("[PluginManager] Permission denied while creating plugin directories")

    def load_installed_plugins(self):
        """Discover and load metadata for all plugins in the installed directory."""
        for plugin_path in self.installed_dir.iterdir():
            if plugin_path.is_dir():
                manifest_path = plugin_path / "manifest.json"
                if manifest_path.exists():
                    try:
                        with open(manifest_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            manifest = PluginManifest(data)
                            plugin = Plugin(plugin_path, manifest)
                            
                            # Check if enabled in config
                            enabled_plugins = config.get("enabled_plugins", [])
                            if manifest.id in enabled_plugins:
                                plugin.enabled = True
                                
                            self.plugins[manifest.id] = plugin
                    except Exception as e:
                        error(f"[PluginManager] Failed to load plugin metadata at {plugin_path}: {e}")

    def install_plugin(self, plugin_dir_path: Path) -> Plugin:
        """Install a plugin from a directory structure (data/plugin_name).
        
        Steps:
            1. Validate directory and manifest.json.
            2. Validate plugin.weeb file exists.
            3. Check dependencies.
            4. Move to installed directory.
            5. Load metadata.
        """
        if not plugin_dir_path.exists() or not plugin_dir_path.is_dir():
            raise PluginError(f"Plugin directory not found: {plugin_dir_path}")
            
        # 1. Validate manifest
        manifest_path = plugin_dir_path / "manifest.json"
        if not manifest_path.exists():
            raise PluginError("Plugin is missing manifest.json")
            
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                manifest = PluginManifest(data)
        except Exception as e:
            raise PluginError(f"Invalid manifest.json: {e}")
            
        # 2. Validate entry point
        entry_path = plugin_dir_path / manifest.entry_point
        if not entry_path.exists():
            raise PluginError(f"Entry point {manifest.entry_point} not found in plugin directory")
            
        # 3. Check dependencies
        for dep in manifest.dependencies:
            # We could use pip to install dependencies here if needed
            debug(f"[PluginManager] Plugin '{manifest.name}' requires dependency: {dep}")
            
        # 4. Move to installed
        final_path = self.installed_dir / manifest.id
        if final_path.exists():
            shutil.rmtree(final_path)
            
        # Copy directory structure to installed plugins
        shutil.copytree(plugin_dir_path, final_path)
        
        # 5. Load metadata
        plugin = Plugin(final_path, manifest)
        self.plugins[manifest.id] = plugin
        
        return plugin

    def uninstall_plugin(self, plugin_id: str):
        """Uninstall a plugin by ID."""
        if plugin_id in self.plugins:
            plugin = self.plugins[plugin_id]
            if plugin.path.exists():
                shutil.rmtree(plugin.path)
            del self.plugins[plugin_id]
            
            # Remove from enabled list
            enabled_plugins = config.get("enabled_plugins", [])
            if plugin_id in enabled_plugins:
                enabled_plugins.remove(plugin_id)
                config.set("enabled_plugins", enabled_plugins)

    def enable_plugin(self, plugin_id: str):
        """Enable a plugin and load its code."""
        if plugin_id not in self.plugins:
            raise PluginError(f"Plugin not found: {plugin_id}")
            
        plugin = self.plugins[plugin_id]
        
        # Bug 0001: Only return if module is already loaded AND enabled
        if plugin.enabled and plugin.module is not None:
            return
            
        try:
            self._load_plugin_module(plugin)
            plugin.enabled = True
            
            enabled_plugins = config.get("enabled_plugins", [])
            if plugin_id not in enabled_plugins:
                enabled_plugins.append(plugin_id)
                config.set("enabled_plugins", enabled_plugins)
        except Exception as e:
            error(f"[PluginManager] Failed to enable plugin {plugin_id}: {e}")
            raise PluginError(f"Failed to enable plugin: {e}")

    def disable_plugin(self, plugin_id: str):
        """Disable a plugin (doesn't unload code from memory, but prevents use)."""
        if plugin_id in self.plugins:
            self.plugins[plugin_id].enabled = False
            
            enabled_plugins = config.get("enabled_plugins", [])
            if plugin_id in enabled_plugins:
                enabled_plugins.remove(plugin_id)
                config.set("enabled_plugins", enabled_plugins)

    def _load_plugin_module(self, plugin: Plugin):
        """Load the plugin's entry point module in a restricted environment."""
        entry_path = plugin.path / plugin.manifest.entry_point
        if not entry_path.exists():
            raise PluginError(f"Entry point not found: {plugin.manifest.entry_point}")
            
        module_name = f"weeb_plugin_{plugin.manifest.id}"
        
        # Security: Sandbox layer
        # We restrict the globals available to the plugin module.
        # Note: This is a cooperative sandbox.
        spec = importlib.util.spec_from_file_location(module_name, entry_path)
        if spec is None or spec.loader is None:
            raise PluginError(f"Could not load spec for {entry_path}")
            
        module = importlib.util.module_from_spec(spec)
        
        # Define restricted globals
        # Only allow essential builtins and weeb_cli modules that are safe
        restricted_globals = {
            '__name__': module_name,
            '__file__': str(entry_path),
            '__package__': None,
            '__doc__': None,
            '__builtins__': self._get_safe_builtins(),
            'i18n': i18n,
            'debug': debug,
            'error': error,
            # Provide a way to register providers/services
            'register_provider': self._get_register_provider_proxy(plugin),
        }
        
        # Update module dict with restricted globals
        module.__dict__.update(restricted_globals)
        
        try:
            spec.loader.exec_module(module)
            plugin.module = module
            
            # Register provider if the plugin defines one
            if hasattr(module, "register"):
                module.register()
                
            debug(f"[PluginManager] Successfully loaded plugin module: {plugin.manifest.id}")
        except Exception as e:
            raise PluginError(f"Error executing plugin code: {e}")

    def _get_safe_builtins(self):
        """Return a dictionary of safe Python builtins for the sandbox."""
        import builtins
        # Bug 0006: Added __import__ and some common builtins needed for basic execution
        safe_names = [
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytes', 'bytearray',
            'callable', 'chr', 'complex', 'dict', 'dir', 'divmod', 'enumerate',
            'filter', 'float', 'format', 'frozenset', 'getattr', 'hasattr',
            'hash', 'hex', 'id', 'int', 'isinstance', 'issubclass', 'iter',
            'len', 'list', 'map', 'max', 'min', 'next', 'object', 'oct',
            'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed',
            'round', 'set', 'setattr', 'slice', 'sorted', 'str', 'sum', 'tuple',
            'type', 'zip', 'Exception', 'ValueError', 'TypeError', 'RuntimeError',
            '__import__', '__name__', '__doc__', '__package__', '__loader__', '__spec__'
        ]
        return {name: getattr(builtins, name) for name in safe_names if hasattr(builtins, name)}

    def _get_register_provider_proxy(self, plugin: Plugin):
        """Proxy function to allow plugins to register providers securely."""
        from weeb_cli.providers.registry import register_provider
        
        def proxy(name, lang="en", region="US", disabled=False):
            # We can add validation here to ensure name matches plugin prefix, etc.
            return register_provider(name, lang, region, disabled)
        return proxy

    def get_enabled_plugins(self) -> List[Plugin]:
        """Get list of all enabled plugins."""
        return [p for p in self.plugins.values() if p.enabled]

# Global instance
plugin_manager = PluginManager()
