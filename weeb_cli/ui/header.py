from rich import print
from rich.text import Text
from rich.console import Console
from weeb_cli.config import config

console = Console()

def show_header(title="Weeb API"):
    console.clear()
    
    source = config.get("scraping_source", "local")
    display_source = "Weeb" if source == "local" else source
    
    text = Text()
    text.append(f" {title} ", style="bold white on blue")
    text.append(f" | {display_source} v0.0.1", style="dim white")
    
    console.print(text, justify="center")
    console.print("[dim italic]> Sadece sen ve anime.[/dim italic]", justify="center")
    print()
