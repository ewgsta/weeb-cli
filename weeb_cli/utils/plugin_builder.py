import os
import sys
import json
import zipfile
import argparse
import shutil
from pathlib import Path

def validate_plugin_structure(source_dir: Path):
    """Validate that the plugin directory has the required structure."""
    required_files = ["plugin.weeb", "manifest.json", "README.md"]
    required_dirs = ["screenshots"]
    
    for file in required_files:
        if not (source_dir / file).exists():
            print(f"Error: Required file '{file}' not found in {source_dir}")
            return False
            
    for d in required_dirs:
        if not (source_dir / d).is_dir():
            print(f"Error: Required directory '{d}/' not found in {source_dir}")
            return False
            
    # Validate manifest.json
    try:
        with open(source_dir / "manifest.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
            required_fields = ["id", "name", "version", "description", "author", "dependencies"]
            for field in required_fields:
                if field not in manifest:
                    print(f"Error: Required field '{field}' missing in manifest.json")
                    return False
    except json.JSONDecodeError:
        print("Error: manifest.json is not valid JSON")
        return False
    except Exception as e:
        print(f"Error reading manifest.json: {e}")
        return False
        
    return True

def create_plugin_template(target_dir: Path, plugin_id: str, plugin_name: str):
    """Create a new plugin template structure."""
    if target_dir.exists():
        print(f"Error: Target directory {target_dir} already exists")
        return False
        
    try:
        # Create directories
        target_dir.mkdir(parents=True)
        (target_dir / "screenshots").mkdir()
        (target_dir / "assets").mkdir()
        
        # Create manifest.json
        manifest = {
            "id": plugin_id,
            "name": plugin_name,
            "version": "1.0.0",
            "description": "A new Weeb CLI plugin",
            "author": "Your Name",
            "entry_point": "plugin.weeb",
            "min_weeb_version": "1.0.0",
            "dependencies": [],
            "tags": [],
            "icon": "assets/icon.png",
            "homepage": "",
            "repository_url": "",
            "license": "MIT"
        }
        with open(target_dir / "manifest.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
            
        # Create plugin.weeb (python code)
        with open(target_dir / "plugin.weeb", "w", encoding="utf-8") as f:
            f.write('def register():\n    print("Plugin registered!")\n')
            
        # Create README.md
        with open(target_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(f"# {plugin_name}\n\n{manifest['description']}")
            
        # Create placeholder images
        with open(target_dir / "assets/icon.png", "w") as f:
            f.write("")
        with open(target_dir / "screenshots/preview.png", "w") as f:
            f.write("")
            
        print(f"Successfully created plugin template at {target_dir}")
        return True
    except Exception as e:
        print(f"Error creating template: {e}")
        if target_dir.exists():
            shutil.rmtree(target_dir)
        return False

def build_plugin(source_dir: Path, output_file: Path = None):
    """Package a plugin directory into a .weeb_pkg zip file for distribution."""
    if not source_dir.is_dir():
        print(f"Error: {source_dir} is not a directory")
        return False
        
    if not validate_plugin_structure(source_dir):
        return False
        
    with open(source_dir / "manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)
        plugin_id = manifest["id"]
        
    if output_file is None:
        output_file = Path(f"{plugin_id}.weeb_pkg")
        
    print(f"Building plugin package '{plugin_id}'...")
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                # Skip .weeb_pkg files and hidden files/dirs
                if file.endswith(".weeb_pkg") or file.startswith("."):
                    continue
                if any(p.startswith(".") for p in file_path.parts):
                    continue
                
                rel_path = file_path.relative_to(source_dir)
                zipf.write(file_path, rel_path)
                
    print(f"Successfully created {output_file}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weeb CLI Plugin Builder")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build a plugin package")
    build_parser.add_argument("source", help="Source directory of the plugin")
    build_parser.add_argument("-o", "--output", help="Output .weeb_pkg file path")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new plugin template")
    create_parser.add_argument("directory", help="Target directory for the new plugin")
    create_parser.add_argument("--id", required=True, help="Plugin ID (e.g., my-plugin)")
    create_parser.add_argument("--name", required=True, help="Plugin Name")
    
    args = parser.parse_args()
    
    if args.command == "build":
        source_path = Path(args.source)
        output_path = Path(args.output) if args.output else None
        if build_plugin(source_path, output_path):
            sys.exit(0)
        else:
            sys.exit(1)
    elif args.command == "create":
        target_path = Path(args.directory)
        if create_plugin_template(target_path, args.id, args.name):
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)
