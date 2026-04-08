import unittest
import os
import json
import zipfile
import shutil
from pathlib import Path
from weeb_cli.services.plugin_manager import PluginManager, PluginManifest, PluginError

class TestPluginManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("tests/temp_plugins").resolve()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.manager = PluginManager(base_dir=self.test_dir)

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if hasattr(self, 'weeb_file') and self.weeb_file.exists():
            os.remove(self.weeb_file)

    def test_manifest_validation(self):
        # Valid manifest
        data = {
            "id": "test-plugin",
            "name": "Test Plugin",
            "version": "1.0.0",
            "entry_point": "plugin.weeb"
        }
        manifest = PluginManifest(data)
        self.assertEqual(manifest.id, "test-plugin")
        self.assertEqual(manifest.name, "Test Plugin")

        # Invalid manifest (missing ID)
        with self.assertRaises(PluginError):
            PluginManifest({"name": "No ID"})

    def test_install_plugin(self):
        # Create a dummy plugin directory structure
        plugin_src = self.test_dir / "src_plugin"
        plugin_src.mkdir()
        
        manifest_data = {
            "id": "my-plugin",
            "name": "My Plugin",
            "version": "1.0.0",
            "entry_point": "plugin.weeb",
            "description": "Test description",
            "author": "Test Author",
            "dependencies": []
        }
        with open(plugin_src / "manifest.json", "w") as f:
            json.dump(manifest_data, f)
            
        with open(plugin_src / "plugin.weeb", "w") as f:
            f.write("def register(): pass")

        # Install plugin
        plugin = self.manager.install_plugin(plugin_src)
        
        self.assertEqual(plugin.manifest.id, "my-plugin")
        self.assertTrue((self.manager.installed_dir / "my-plugin").exists())
        self.assertIn("my-plugin", self.manager.plugins)

    def test_uninstall_plugin(self):
        # Install a dummy plugin first
        plugin_id = "to-remove"
        plugin_path = self.manager.installed_dir / plugin_id
        plugin_path.mkdir(parents=True)
        
        with open(plugin_path / "manifest.json", "w") as f:
            json.dump({"id": plugin_id, "name": "To Remove"}, f)
            
        self.manager.load_installed_plugins()
        self.assertIn(plugin_id, self.manager.plugins)
        
        # Uninstall
        self.manager.uninstall_plugin(plugin_id)
        self.assertNotIn(plugin_id, self.manager.plugins)
        self.assertFalse(plugin_path.exists())

if __name__ == '__main__':
    unittest.main()
