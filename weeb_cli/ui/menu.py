import questionary
from rich.console import Console
import sys
from .header import show_header
from weeb_cli.i18n import i18n

console = Console()

def show_main_menu(action_map):
    """
    Shows the main menu.
    action_map: dict of { "translation_key": function }
    e.g. { "hello": say_hello } -> looks up "menu.options.hello"
    """
    console.clear()
    show_header()
    
    # Build choices mapping: Display Text -> Function
    choices_map = {}
    for key, func in action_map.items():
        display_text = i18n.get(f"menu.options.{key}")
        choices_map[display_text] = func
    
    exit_text = i18n.get("menu.options.exit")
    
    choices = list(choices_map.keys()) + [exit_text]
    
    try:
        answer = questionary.select(
            i18n.get("menu.prompt"),
            choices=choices,
            use_indicator=True,
            style=questionary.Style([
                ('pointer', 'fg:cyan bold'),
                ('highlighted', 'fg:cyan'),
                ('selected', 'fg:cyan bold'),
            ])
        ).ask()
        
        if answer == exit_text or answer is None:
            console.print(f"[yellow]👋 {i18n.get('common.success')}...[/yellow]") # Using success as placeholder for bye or just keep generic
            sys.exit(0)
            
        action = choices_map.get(answer)
        if action:
            action()
            
        # Loop back to menu
        show_main_menu(action_map)
        
    except KeyboardInterrupt:
        sys.exit(0)
