# Plugin Development Guide

Weeb CLI provides a robust plugin architecture that allows you to extend the application with custom providers, trackers, and services. Plugins are packaged in a secure, portable `.weeb` format.

## Plugin Structure

A standard plugin folder must contain the following files:

```
my-plugin/
├── manifest.json
├── main.py (Entry point)
├── README.md
└── assets/
    └── logo.png (Optional)
```

### manifest.json

The manifest contains metadata about your plugin:

```json
{
    "id": "my-plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "A description of your plugin.",
    "author": "Your Name",
    "entry_point": "main.py",
    "dependencies": [],
    "min_weeb_version": "1.0.0",
    "permissions": ["network", "storage"]
}
```

### main.py

The entry point must define a `register()` function that will be called when the plugin is enabled.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("my_custom_provider", lang="en", region="US")
    class MyProvider(BaseProvider):
        # Implementation...
        pass
```

## Building a Plugin

Use the provided builder script to package your plugin directory into a `.weeb` file:

```bash
python3 weeb_cli/utils/plugin_builder.py plugins/my-plugin -o my-plugin.weeb
```

## Installing a Plugin

1. Open Weeb CLI.
2. Go to **Settings** > **Plugins**.
3. Select **Load Plugin**.
4. Enter the path to your `.weeb` file.

## Security & Sandboxing

Plugins run in a restricted execution environment. They are only allowed to use a subset of the Python standard library and must request specific permissions in the `manifest.json`.

- **network**: Allows making HTTP requests.
- **storage**: Allows local file access within the plugin's data directory.

## Sharing Plugins

You can share your plugins by submitting a Pull Request to the main repository. 

1. Fork the repository.
2. Create a folder under `plugins/` for your plugin.
3. Add your plugin files.
4. Open a Pull Request using the **Plugin Submission Template**.

Our CI/CD pipeline will automatically validate your plugin for:
- Manifest correctness
- Security vulnerabilities (Bandit)
- Code style (Ruff)
- Structure integrity
