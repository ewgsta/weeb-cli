import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.services.downloader import queue_manager
from .episode_utils import get_episodes_safe

console = Console()

def handle_download_flow(slug, details):
    episodes = get_episodes_safe(details)
    if not episodes:
        console.print(f"[yellow]{i18n.t('details.no_episodes')}[/yellow]")
        time.sleep(1.5)
        return

    try:
        selected_eps = _select_episodes_to_download(episodes)
        if not selected_eps:
            return
        
        _add_to_download_queue(slug, details, selected_eps)
        
    except KeyboardInterrupt:
        return

def _select_episodes_to_download(episodes):
    opt_all = i18n.t("details.download_options.all")
    opt_manual = i18n.t("details.download_options.manual")
    opt_range = i18n.t("details.download_options.range")

    mode = questionary.select(
        i18n.t("details.download_options.prompt"),
        choices=[opt_all, opt_manual, opt_range],
        pointer=">",
        use_shortcuts=False
    ).ask()
    
    if mode is None:
        return None
        
    if mode == opt_all:
        return episodes
        
    if mode == opt_manual:
        return _select_episodes_manually(episodes)
        
    if mode == opt_range:
        return _select_episodes_by_range(episodes)
    
    return None

def _select_episodes_manually(episodes):
    choices = []
    for ep in episodes:
        name = f"{i18n.t('details.episode')} {ep.get('number')}"
        choices.append(questionary.Choice(name, value=ep))
    
    return questionary.checkbox(
        "Select Episodes:",
        choices=choices
    ).ask()

def _select_episodes_by_range(episodes):
    r_str = questionary.text(i18n.t("details.download_options.range_input")).ask()
    if not r_str:
        return None
    
    nums = set()
    try:
        parts = r_str.split(',')
        for p in parts:
            p = p.strip()
            if '-' in p:
                s, e = p.split('-')
                for x in range(int(s), int(e) + 1):
                    nums.add(x)
            elif p.isdigit():
                nums.add(int(p))
    except:
        console.print(f"[red]{i18n.t('details.download_options.range_error')}[/red]")
        time.sleep(1)
        return None
    
    return [ep for ep in episodes if int(ep.get('number', -1)) in nums]

def _add_to_download_queue(slug, details, selected_eps):
    anime_title = details.get("title") or "Unknown Anime"
    
    opt_now = i18n.t("downloads.start_now")
    opt_queue = i18n.t("downloads.add_to_queue")
    
    action = questionary.select(
        i18n.t("downloads.action_prompt"),
        choices=[opt_now, opt_queue],
        pointer=">",
        use_shortcuts=False
    ).ask()
    
    if action is None:
        return
    
    added = queue_manager.add_to_queue(anime_title, selected_eps, slug)
    
    if added > 0:
        console.print(f"[green]{i18n.t('downloads.queued', count=added)}[/green]")
        
        if action == opt_now:
            queue_manager.start_queue()
    else:
        console.print(f"[yellow]{i18n.t('downloads.already_in_queue')}[/yellow]")
    
    time.sleep(1)
