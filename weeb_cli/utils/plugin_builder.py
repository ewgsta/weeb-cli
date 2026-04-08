import os
import sys
import json
import zipfile
import argparse
from pathlib import Path

def build_plugin(source_dir: Path, output_file: Path = None):
    """Package a plugin directory into a .weeb file."""
    if not source_dir.is_dir():
        print(f"Error: {source_dir} is not a directory")
        return False
        
    manifest_path = source_dir / "manifest.json"
    if not manifest_path.exists():
        print(f"Error: manifest.json not found in {source_dir}")
        return False
        
    try:
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            plugin_id = manifest.get("id")
            if not plugin_id:
                print("Error: Plugin ID missing in manifest.json")
                return False
    except Exception as e:
        print(f"Error reading manifest: {e}")
        return False
        
    if output_file is None:
        output_file = Path(f"{plugin_id}.weeb")
        
    print(f"Building plugin '{plugin_id}'...")
    
    with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                file_path = Path(root) / file
                # Skip already built .weeb files and some other patterns
                if file.endswith(".weeb") or file.startswith("."):
                    continue
                
                rel_path = file_path.relative_to(source_dir)
                zipf.write(file_path, rel_path)
                
    print(f"Successfully created {output_file}")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Weeb CLI Plugin Builder")
    parser.add_argument("source", help="Source directory of the plugin")
    parser.add_argument("-o", "--output", help="Output .weeb file path")
    
    args = parser.parse_args()
    source_path = Path(args.source)
    output_path = Path(args.output) if args.output else None
    
    if build_plugin(source_path, output_path):
        sys.exit(0)
    else:
        sys.exit(1)
