from rich import print
from rich.text import Text
from rich.console import Console
from weeb_cli.config import config
from weeb_cli import __version__

console = Console()

def show_header(title="Weeb CLI", show_version=False, show_source=False):
    console.clear()
    
    text = Text()
    text.append(f" {title} ", style="bold white on blue")
    
    parts = []
    
    if show_source:
        cfg_source = config.get("scraping_source", "local")
        disp_source = "Weeb" if cfg_source == "local" else cfg_source.capitalize()
        parts.append(disp_source)
        
    if show_version:
        parts.append(f"v{__version__}")
        
    if parts:
        joined = " | ".join(parts)
        text.append(f" | {joined}", style="dim white")
    
    console.print(text, justify="left")
    print()
