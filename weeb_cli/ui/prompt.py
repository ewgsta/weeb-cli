import sys
import typer
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich.text import Text
from typing import List, Any, Union, Tuple

console = Console()

class Prompt:
    def __init__(self):
        self.console = Console()

    def _get_input(self):
        try:
            return typer.getchar()
        except Exception:
            return sys.stdin.read(1)

    def select(self, title: str, options: List[Union[str, Tuple[str, Any]]], pointer: str = ">", page_size: int = 10) -> Any:
        processed_options = []
        for opt in options:
            if isinstance(opt, tuple):
                processed_options.append(opt)
            else:
                processed_options.append((opt, opt))
        
        current_idx = 0
        total_options = len(processed_options)
        window_start = 0
        
        def generate_table():
            table = Table.grid(padding=(0, 1))
            table.add_column("Pointer", width=2)
            table.add_column("Option")
            
            nonlocal window_start
            if current_idx >= window_start + page_size:
                window_start = current_idx - page_size + 1
            elif current_idx < window_start:
                window_start = current_idx
            
            display_options = processed_options[window_start : window_start + page_size]
            
            if title:
                self.console.print(f"[bold cyan]? {title}[/bold cyan]")
            
            for i, (label, _) in enumerate(display_options):
                abs_idx = window_start + i
                if abs_idx == current_idx:
                    table.add_row(f"[cyan]{pointer}[/cyan]", f"[cyan]{label}[/cyan]")
                else:
                    table.add_row(" ", label)
            
            if total_options > page_size:
                table.add_row(" ", f"[dim]({window_start+1}-{min(window_start+page_size, total_options)} of {total_options})[/dim]")
                
            return table

        
        self.console.print(f"[bold cyan]? {title}[/bold cyan]")
        
        with Live("", refresh_per_second=20, auto_refresh=False, transient=True) as live:
            while True:
                table = Table.grid(padding=(0, 1))
                table.add_column("Pointer", width=2)
                table.add_column("Option")
                
                if current_idx >= window_start + page_size:
                    window_start = current_idx - page_size + 1
                elif current_idx < window_start:
                    window_start = current_idx
                    
                limit = min(window_start + page_size, total_options)
                    
                for idx in range(window_start, limit):
                    label = processed_options[idx][0]
                    if idx == current_idx:
                        table.add_row(f"[cyan]{pointer}[/cyan]", f"[cyan]{label}[/cyan]")
                    else:
                        table.add_row(" ", label)
                        
                if total_options > page_size:
                    progress = f"({window_start+1}-{limit}/{total_options})"
                    table.add_row(" ", f"[dim]{progress}[/dim]")
                
                live.update(table)
                live.refresh()
                
                key = self._get_input()
                
                if key in ["w", "W", "k", "K"] or key == '\x1b[A' or key == '\xe0H': # \xe0H is windows arrow up sometimes
                    current_idx = (current_idx - 1) % total_options
                elif key in ["s", "S", "j", "J"] or key == '\x1b[B' or key == '\xe0P':
                    current_idx = (current_idx + 1) % total_options
                elif key == '\r' or key == '\n':
                    return processed_options[current_idx][1]
                elif key == '\x03':
                    sys.exit(0)
                elif key == '\xe0': 
                    try:
                        next_key = typer.getchar()
                        if next_key == 'H': 
                            current_idx = (current_idx - 1) % total_options
                        elif next_key == 'P': 
                            current_idx = (current_idx + 1) % total_options
                    except: pass
                elif key == '\x1b':
                    try:
                        k2 = typer.getchar()
                        if k2 == '[':
                            k3 = typer.getchar()
                            if k3 == 'A': 
                                current_idx = (current_idx - 1) % total_options
                            elif k3 == 'B': 
                                current_idx = (current_idx + 1) % total_options
                    except: pass

prompt = Prompt()
