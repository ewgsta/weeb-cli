from rich import print
from rich.panel import Panel
from rich.text import Text
from rich.console import Console
import pyfiglet

console = Console()

def show_header():
    console.clear()
    
    f = pyfiglet.Figlet(font='slant')
    title_text = f.renderText('Weeb CLI')
    
    panel = Panel(
        Text(title_text, justify="center", style="bold cyan"),
        subtitle="v0.0.1",
        subtitle_align="right",
        border_style="blue",
        padding=(1, 5),
        expand=False
    )
    
    console.print(panel, justify="center")
    console.print("[dim italic]> Sadece sen ve anime.[/dim italic]", justify="center")
    print()
