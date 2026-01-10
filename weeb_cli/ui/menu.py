import questionary
from rich.console import Console
import sys
from .header import show_header

console = Console()

def show_main_menu(actions):
    console.clear()
    show_header()
    
    choices = list(actions.keys()) + ["Çıkış Yap"]
    
    try:
        answer = questionary.select(
            "Bir işlem seçin:",
            choices=choices,
            use_indicator=True,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan'),
                ('selected', 'fg:cyan bold'),
            ])
        ).ask()
        
        if answer == "Çıkış Yap" or answer is None:
            console.print("[yellow]👋 Görüşmek üzere...[/yellow]")
            sys.exit(0)
            
        action = actions.get(answer)
        if action:
            action()
            
        # Loop back to menu
        show_main_menu(actions)
        
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Görüşmek üzere...[/yellow]")
        sys.exit(0)
