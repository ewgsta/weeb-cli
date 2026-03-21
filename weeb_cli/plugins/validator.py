import ast
import json
import re
from typing import Tuple, Optional, List
from packaging.version import Version, InvalidVersion


REQUIRED_MANIFEST_FIELDS = [
    "name", "version", "lang", "entry_point", "entry_class"
]

OPTIONAL_MANIFEST_FIELDS = [
    "display_name", "author", "description", "region",
    "min_weeb_version", "permissions", "homepage"
]

VALID_PERMISSIONS = ["http"]

ALLOWED_IMPORTS = {
    "json", "re", "time", "urllib", "urllib.request", "urllib.parse",
    "requests", "bs4", "BeautifulSoup", "hashlib", "base64", "html",
    "typing", "dataclasses", "lxml", "math", "string", "collections",
    "html.parser", "xml", "xml.etree", "xml.etree.ElementTree",
    "weeb_cli.providers.base", "weeb_cli.providers.registry",
    "weeb_cli.services.logger",
}

BLOCKED_PATTERNS = [
    r'\bos\.system\b',
    r'\bos\.popen\b',
    r'\bos\.exec\w*\b',
    r'\bos\.spawn\w*\b',
    r'\bsubprocess\b',
    r'\beval\s*\(',
    r'\bexec\s*\(',
    r'\bcompile\s*\(',
    r'\b__import__\s*\(',
    r'\bopen\s*\(',
    r'\bsocket\b',
    r'\bctypes\b',
    r'\bcffi\b',
    r'\bsys\.exit\b',
    r'\bshutil\b',
    r'\bglobals\s*\(\)',
    r'\blocals\s*\(\)',
    r'\bsetattr\s*\(',
    r'\bdelattr\s*\(',
]


def validate_manifest(manifest: dict) -> Tuple[bool, Optional[str]]:
    for field in REQUIRED_MANIFEST_FIELDS:
        if field not in manifest:
            return False, f"Missing required field: '{field}'"
    
    name = manifest.get("name", "")
    if not re.match(r'^[a-z0-9][a-z0-9\-_]{1,48}[a-z0-9]$', name):
        return False, (
            f"Invalid plugin name: '{name}'. "
            "Must be 3-50 chars, lowercase, digits, hyphens and underscores."
        )
    
    try:
        Version(manifest["version"])
    except InvalidVersion:
        return False, f"Invalid version: '{manifest['version']}'"
    
    if "min_weeb_version" in manifest:
        try:
            Version(manifest["min_weeb_version"])
        except InvalidVersion:
            return False, f"Invalid min_weeb_version: '{manifest['min_weeb_version']}'"
    
    lang = manifest.get("lang", "")
    if not re.match(r'^[a-z]{2}$', lang):
        return False, f"Invalid language code: '{lang}'. Must be 2-letter ISO 639-1."
    
    entry_point = manifest.get("entry_point", "")
    if not entry_point.endswith(".py"):
        return False, f"entry_point must be a Python file: '{entry_point}'"
    if ".." in entry_point or entry_point.startswith("/"):
        return False, f"entry_point must be a safe path: '{entry_point}'"
    
    permissions = manifest.get("permissions", [])
    if not isinstance(permissions, list):
        return False, "permissions must be a list."
    for perm in permissions:
        if perm not in VALID_PERMISSIONS:
            return False, f"Invalid permission: '{perm}'. Allowed: {VALID_PERMISSIONS}"
    
    return True, None


def check_version_compatibility(manifest: dict, current_version: str) -> Tuple[bool, Optional[str]]:
    min_version = manifest.get("min_weeb_version")
    if not min_version:
        return True, None
    
    try:
        if Version(current_version) < Version(min_version):
            return False, (
                f"This plugin requires weeb-cli {min_version}+. "
                f"Current version: {current_version}"
            )
    except InvalidVersion:
        return True, None
    
    return True, None


def validate_code(source_code: str) -> Tuple[bool, Optional[str], List[str]]:
    warnings = []
    
    try:
        ast.parse(source_code)
    except SyntaxError as e:
        return False, f"Syntax error (line {e.lineno}): {e.msg}", []
    
    for pattern in BLOCKED_PATTERNS:
        matches = re.finditer(pattern, source_code, re.MULTILINE)
        for match in matches:
            line_num = source_code[:match.start()].count('\n') + 1
            matched_text = match.group()
            
            line = source_code.split('\n')[line_num - 1].strip()
            if line.startswith('#'):
                continue
            
            return False, (
                f"Security violation (line {line_num}): "
                f"'{matched_text}' is not allowed."
            ), []
    
    tree = ast.parse(source_code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if not _is_allowed_import(alias.name):
                    return False, (
                        f"Disallowed import (line {node.lineno}): '{alias.name}'"
                    ), []
        
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if not _is_allowed_import(module):
                return False, (
                    f"Disallowed import (line {node.lineno}): '{module}'"
                ), []
    
    has_base_provider = False
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseProvider":
                    has_base_provider = True
                elif isinstance(base, ast.Attribute):
                    attr_str = _get_attribute_string(base)
                    if attr_str and "BaseProvider" in attr_str:
                        has_base_provider = True
    
    if not has_base_provider:
        return False, "Plugin must contain at least one BaseProvider subclass.", []
    
    return True, None, warnings


def _is_allowed_import(module_name: str) -> bool:
    if module_name in ALLOWED_IMPORTS:
        return True
    
    for allowed in ALLOWED_IMPORTS:
        if module_name.startswith(allowed + "."):
            return True
    
    return False


def _get_attribute_string(node: ast.Attribute) -> Optional[str]:
    parts = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    parts.reverse()
    return ".".join(parts) if parts else None


def validate_entry_class(source_code: str, entry_class: str) -> Tuple[bool, Optional[str]]:
    tree = ast.parse(source_code)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == entry_class:
            has_base = False
            for base in node.bases:
                if isinstance(base, ast.Name) and base.id == "BaseProvider":
                    has_base = True
                elif isinstance(base, ast.Attribute):
                    attr_str = _get_attribute_string(base)
                    if attr_str and "BaseProvider" in attr_str:
                        has_base = True
            
            if has_base:
                return True, None
            else:
                return False, (
                    f"'{entry_class}' does not extend BaseProvider."
                )
    
    return False, f"'{entry_class}' class not found in source."
