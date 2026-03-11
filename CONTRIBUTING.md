# Contributing to Weeb CLI

*Looking for the Turkish version? [Türkçe için buraya tıklayın](md/tr/CONTRIBUTING.md).*

First off, thank you for considering contributing to Weeb CLI! Your help is highly appreciated.

If you enjoy anime, tools, and the terminal, you are in the right place.

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/ewgsta/weeb-cli.git
   cd weeb-cli
   ```
3. **Install dependencies** in editable mode:
   ```bash
   pip install -e .
   ```

## Workflow

1. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes in the codebase.
3. To test your CLI changes locally, you can run `weeb-cli` which should point to your active environment's script.
4. Try to write tests. They are located under the `tests/` directory.
   ```bash
   pytest
   ```
5. Commit your changes. Ensure your commit messages clearly describe what changed.
6. Push to your fork and submit a Pull Request to the `main` branch.

## Pull Requests

- Keep your pull requests focused on a single change, feature, or bugfix. This makes the review process smoother.
- Link any related issues to your PR so maintainers have context.
- Adhere to the existing code style (use Black/Flake8 for Python components).
- Update the documentation (`README.md`, `README-TR.md`, etc.) if your changes affect external behavior.

## Issues

If you find a bug or have a suggestion, feel free to open an issue:
- **Search existing issues** before you create a new one to avoid duplicates.
- Provide as much context as possible. Mention the OS, Python version, and Weeb CLI version.
- Include a reproducible example, logs, or screenshots where applicable.

## Translations & i18n

Since Weeb CLI supports Turkish and English (`tr` and `en`):
- Features adding texts to the user interface should modify both `locales/en.json` and `locales/tr.json`.

---

Thank you again for your contribution!
