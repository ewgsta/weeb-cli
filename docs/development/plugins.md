# Plugin Development Guide

Weeb CLI provides a robust plugin architecture that allows you to extend the application with custom providers, trackers, and services. Plugins are isolated in a secure, portable environment and follow a standardized directory structure.

## Plugin Structure

A standard plugin folder must be stored in the `data/` directory and contain the following structure:

```
data/
  my-plugin/
    plugin.weeb        (Main code entry point)
    manifest.json      (Metadata and configuration)
    README.md          (Detailed documentation)
    screenshots/       (At least one screenshot for the gallery)
      ss1.png
    assets/            (Icons and other assets)
      icon.png
```

### manifest.json

The manifest contains mandatory and optional metadata about your plugin:

```json
{
    "id": "my-plugin",
    "name": "My Plugin",
    "version": "1.0.0",
    "description": "A description of your plugin.",
    "author": "Your Name",
    "entry_point": "plugin.weeb",
    "min_weeb_version": "1.0.0",
    "dependencies": [],
    "permissions": ["network", "storage"],
    "tags": ["anime", "en"],
    "icon": "assets/icon.png",
    "homepage": "https://example.com",
    "repository_url": "https://github.com/user/repo",
    "license": "MIT"
}
```

### plugin.weeb

The entry point is a Python script that must define a `register()` function. It runs in a restricted sandbox environment with access to a safe subset of builtins and `weeb_cli` APIs.

```python
def register():
    from weeb_cli.providers.registry import register_provider
    from weeb_cli.providers.base import BaseProvider
    
    @register_provider("my_custom_provider", lang="en", region="US")
    class MyProvider(BaseProvider):
        def search(self, query: str):
            # Implementation...
            pass
```

## Building and Packaging

Use the provided builder script to package or create new plugins:

```bash
# Create a new plugin template
python3 weeb_cli/utils/plugin_builder.py create my-new-plugin --id "new-id" --name "New Name"

# Build/Package a plugin for distribution (.weeb_pkg)
python3 weeb_cli/utils/plugin_builder.py build data/my-plugin -o my-plugin.weeb_pkg
```

## Installation

1. Open Weeb CLI.
2. Go to **Settings** > **Plugins**.
3. Select **Load Plugin**.
4. Provide the local path to the plugin folder or its `.weeb_pkg`.

## Testing and Quality

Plugins must maintain at least **80% test coverage** to be accepted into the official gallery. Automated tests should be placed in a `tests/` directory within the plugin folder.

Our CI/CD pipeline validates:
- **Manifest integrity**: Required fields (id, name, version, etc.) must be present.
- **Security**: Scanned via Bandit for common vulnerabilities.
- **Code Quality**: Linted via Ruff.
- **Functionality**: Tests are executed, and coverage is checked.

## Sharing via Gallery

Submit a Pull Request adding your plugin folder to the `data/` directory. Once approved, it will automatically appear in the [Plugin Gallery](https://ewgsta.github.io/weeb-cli/plugin_gallery/index.html).
