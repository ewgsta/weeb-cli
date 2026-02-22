import questionary
from pathlib import Path
from rich.console import Console
from rich.table import Table
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.progress import progress_tracker

console = Console()

def show_watchlist():
    while True:
        console.clear()
        show_header(i18n.t("menu.options.watchlist"))
        
        stats = progress_tracker.get_stats()
        
        console.print(f"[cyan]{i18n.t('watchlist.total_anime')}:[/cyan] {stats['total_anime']}", justify="left")
        console.print(f"[cyan]{i18n.t('watchlist.total_episodes')}:[/cyan] {stats['total_episodes']}", justify="left")
        console.print(f"[cyan]{i18n.t('watchlist.total_hours')}:[/cyan] {stats['total_hours']}h", justify="left")
        
        if stats['last_watched']:
            last = stats['last_watched']
            console.print(f"\n[dim]{i18n.t('watchlist.last_watched')}:[/dim] {last['title']} - {i18n.t('details.episode')} {last['last_watched']}", justify="left")
        
        console.print("")
        
        opt_completed = i18n.t("watchlist.completed")
        opt_in_progress = i18n.t("watchlist.in_progress")
        
        try:
            choice = questionary.select(
                i18n.t("watchlist.select_category"),
                choices=[opt_in_progress, opt_completed],
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if choice is None:
                return
            
            if choice == opt_completed:
                show_completed_list()
            elif choice == opt_in_progress:
                show_in_progress_list()
                
        except KeyboardInterrupt:
            return

def show_completed_list():
    console.clear()
    show_header(i18n.t("watchlist.completed"))
    
    completed = progress_tracker.get_completed_anime()
    
    if not completed:
        console.print(f"[dim]{i18n.t('watchlist.no_completed')}[/dim]")
        try:
            input(i18n.t("common.continue_key"))
        except KeyboardInterrupt:
            pass
        return
    
    table = Table(show_header=True, header_style="bold cyan")
    table.add_column("#", width=4)
    table.add_column(i18n.t("watchlist.anime_title"), width=40)
    table.add_column(i18n.t("watchlist.episodes_watched"), width=15, justify="center")
    
    for i, anime in enumerate(completed, 1):
        watched = len(anime.get("completed", []))
        total = anime.get("total_episodes", watched)
        table.add_row(
            str(i),
            anime.get("title", anime["slug"]),
            f"[green]{watched}/{total}[/green]"
        )
    
    console.print(table)
    
    try:
        input(i18n.t("common.continue_key"))
    except KeyboardInterrupt:
        pass

def show_in_progress_list():
    from weeb_cli.commands.search.anime_details import show_anime_details
    from weeb_cli.commands.downloads import show_anime_episodes
    from weeb_cli.services.local_library import local_library
    
    console.clear()
    show_header(i18n.t("watchlist.in_progress"))
    
    in_progress = progress_tracker.get_in_progress_anime()
    
    if not in_progress:
        console.print(f"[dim]{i18n.t('watchlist.no_in_progress')}[/dim]")
        try:
            input(i18n.t("common.continue_key"))
        except KeyboardInterrupt:
            pass
        return
    
    indexed_anime = {a["title"].lower(): a for a in local_library.get_indexed_anime()}
    
    choices = []
    for anime in in_progress:
        watched = len(anime.get("completed", []))
        total = anime.get("total_episodes", 0)
        total_str = str(total) if total > 0 else "?"
        title = anime.get("title", anime["slug"])
        next_ep = anime.get("last_watched", 0) + 1
        
        is_local = title.lower() in indexed_anime
        prefix = "[dim]●[/dim] " if is_local else ""
        
        choices.append(questionary.Choice(
            title=f"{title} [{watched}/{total_str}] - {i18n.t('watchlist.next')}: {next_ep}",
            value={"anime": anime, "is_local": is_local, "local_data": indexed_anime.get(title.lower())}
        ))
    
    try:
        selected = questionary.select(
            i18n.t("watchlist.select_anime"),
            choices=choices,
            pointer=">",
            use_shortcuts=False
        ).ask()
        
        if selected:
            if selected["is_local"] and selected["local_data"]:
                local_data = selected["local_data"]
                anime_path = local_data["folder_path"]
                anime_info = {
                    "title": local_data["title"],
                    "path": anime_path,
                    "episodes": local_library._scan_anime_folder(Path(anime_path)),
                    "episode_count": local_data["episode_count"],
                    "source": local_data["source_name"]
                }
                show_anime_episodes(anime_info)
            else:
                anime = selected["anime"]
                anime_data = {
                    "id": anime["slug"],
                    "slug": anime["slug"],
                    "title": anime.get("title", anime["slug"]),
                    "name": anime.get("title", anime["slug"])
                }
                show_anime_details(anime_data)
            
    except KeyboardInterrupt:
        pass
