import traceback
from typing import Optional
from rich.console import Console
from weeb_cli.services.logger import error as log_error
from weeb_cli.config import config
from weeb_cli.i18n import i18n

console = Console()

def handle_error(e: Exception, context: str = "", user_message: Optional[str] = None) -> None:
    is_debug = config.get("debug_mode", False)
    
    if is_debug:
        log_error(f"[{context}] {type(e).__name__}: {str(e)}")
        log_error(traceback.format_exc())
    
    if user_message:
        console.print(f"[red]{user_message}[/red]")
    else:
        error_msg = i18n.t("errors.generic", "An error occurred")
        console.print(f"[red]{error_msg}[/red]")
    
    if is_debug:
        console.print(f"[dim]Check logs for details: ~/.weeb-cli/logs/[/dim]")

def handle_provider_error(e: Exception, provider_name: str = "") -> None:
    context = f"Provider:{provider_name}" if provider_name else "Provider"
    user_message = i18n.t("errors.provider", "Failed to fetch data from source")
    handle_error(e, context, user_message)

def handle_download_error(e: Exception, anime_title: str = "", episode: Optional[int] = None) -> None:
    context = f"Download:{anime_title}"
    if episode:
        context += f":E{episode}"
    user_message = i18n.t("errors.download", "Download failed")
    handle_error(e, context, user_message)

def handle_network_error(e: Exception, url: str = "") -> None:
    context = f"Network:{url[:50]}" if url else "Network"
    user_message = i18n.t("errors.network", "Network connection failed")
    handle_error(e, context, user_message)
