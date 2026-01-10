import time
from rich.console import Console
import questionary
from weeb_cli.i18n import i18n

console = Console()

def say_hello():
    with console.status(f"[bold green]{i18n.get('common.processing')}") as status:
        time.sleep(1)
        console.print(f"[green]{i18n.get('hello.greeting')}[/green] 🚀")
        
    console.print(f"[blue]{i18n.get('hello.response', name='User')}[/blue]")
    console.print()
    
    questionary.text(
        i18n.get('common.continue_key'),
        qmark="⌨️",
        style=questionary.Style([('qmark', 'fg:cyan')])
    ).ask()
