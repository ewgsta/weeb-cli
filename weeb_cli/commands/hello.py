import time
from rich.console import Console
import questionary

console = Console()

def say_hello():
    with console.status("[bold green]İşlem yapılıyor...") as status:
        time.sleep(1)
        console.print("[green]Selam Weeb![/green] 🚀")
        
    console.print("[blue]Bu Python ile yazılmış örnek bir komut çıktısıdır.[/blue]")
    console.print()
    
    questionary.text(
        "Devam etmek için Enter'a basın...",
        qmark="⌨️",
        style=questionary.Style([('qmark', 'fg:cyan')])
    ).ask()
