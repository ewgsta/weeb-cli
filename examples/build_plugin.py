#!/usr/bin/env python3
"""
Build a .weeb-plugin package from a plugin directory.

Usage:
    python build_plugin.py <plugin_dir> [output_path]

Example:
    python build_plugin.py examples/sample-plugin/
    python build_plugin.py examples/sample-plugin/ my-plugin.weeb-plugin
"""

import sys
import json
import zipfile
from pathlib import Path


def build_plugin(plugin_dir: str, output_path: str = None):
    plugin_dir = Path(plugin_dir)
    
    if not plugin_dir.exists():
        print(f"Error: Directory not found: {plugin_dir}")
        sys.exit(1)
    
    manifest_path = plugin_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: manifest.json not found: {manifest_path}")
        sys.exit(1)
    
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)
    
    name = manifest.get("name", "plugin")
    version = manifest.get("version", "0.0.0")
    
    if output_path is None:
        output_path = f"{name}-v{version}.weeb-plugin"
    
    print(f"Building plugin: {name} v{version}")
    print(f"Source: {plugin_dir}")
    print()
    
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file_path in plugin_dir.rglob("*"):
            if file_path.is_file():
                if file_path.name.startswith(".") or "__pycache__" in str(file_path):
                    continue
                
                arcname = file_path.relative_to(plugin_dir)
                zf.write(file_path, arcname)
                print(f"  + {arcname}")
    
    file_size = Path(output_path).stat().st_size
    print(f"\nDone: {output_path} ({file_size} bytes)")
    print(f"  Name:    {manifest.get('display_name', name)}")
    print(f"  Version: {version}")
    print(f"  Lang:    {manifest.get('lang', '?')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_plugin.py <plugin_dir> [output_path]")
        sys.exit(1)
    
    plugin_dir = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else None
    
    build_plugin(plugin_dir, output)
