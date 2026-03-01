import time
import questionary
from rich.console import Console
from weeb_cli.i18n import i18n
from weeb_cli.ui.header import show_header
from weeb_cli.services.watch import get_streams
from weeb_cli.services.player import player
from weeb_cli.services.progress import progress_tracker
from weeb_cli.services.scraper import scraper
from .episode_utils import get_episodes_safe, group_episodes_by_season, make_season_episode_id
from .stream_utils import sort_streams, extract_streams_from_response

console = Console()

def handle_watch_flow(slug, details):
    episodes = get_episodes_safe(details)
    if not episodes:
        console.print(f"[yellow]{i18n.t('details.no_episodes')}[/yellow]")
        time.sleep(1.5)
        return

    seasons = group_episodes_by_season(episodes)
    season_numbers = sorted(seasons.keys())
    
    if len(season_numbers) <= 1:
        _handle_single_season_watch(slug, details, episodes, season=1)
        return
    
    _handle_multi_season_watch(slug, details, seasons, season_numbers)

def _handle_multi_season_watch(slug, details, seasons, season_numbers):
    prog_data = progress_tracker.get_anime_progress(slug)
    completed_ids = set(prog_data.get("completed", []))
    
    while True:
        console.clear()
        show_header(details.get("title", "Anime"))
        
        season_choices = _build_season_choices(seasons, season_numbers, completed_ids)
        
        try:
            selected_season = questionary.select(
                i18n.t("details.select_season", "Sezon Seçin") + ":",
                choices=season_choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected_season is None:
                return
            
            _handle_single_season_watch(slug, details, seasons[selected_season], season=selected_season)
            
        except KeyboardInterrupt:
            return

def _build_season_choices(seasons, season_numbers, completed_ids):
    season_choices = []
    for s_num in season_numbers:
        s_episodes = seasons[s_num]
        total_in_season = len(s_episodes)
        
        watched_in_season = sum(
            1 for ep in s_episodes
            if make_season_episode_id(s_num, int(ep.get('number') or ep.get('ep_num') or 0)) in completed_ids
        )
        
        if watched_in_season >= total_in_season:
            status = " [✓]"
        elif watched_in_season > 0:
            status = f" [{watched_in_season}/{total_in_season}]"
        else:
            status = f" [0/{total_in_season}]"
        
        label = f"{i18n.t('details.season', 'Sezon')} {s_num}{status}"
        season_choices.append(questionary.Choice(label, value=s_num))
    
    return season_choices

def _handle_single_season_watch(slug, details, episodes, season=1):
    prog_data = progress_tracker.get_anime_progress(slug)
    completed_ids = set(prog_data.get("completed", []))
    
    next_ep_num = _calculate_next_episode(completed_ids, season, prog_data)

    while True:
        ep_choices = _build_episode_choices(episodes, season, completed_ids, next_ep_num)
        
        try:
            selected_ep = questionary.select(
                i18n.t("details.select_episode") + ":",
                choices=ep_choices,
                pointer=">",
                use_shortcuts=False
            ).ask()
            
            if selected_ep is None:
                return

            success = _play_episode(slug, selected_ep, details, season, episodes)
            
            if success:
                ep_num = selected_ep.get("number") or selected_ep.get("ep_num")
                if _mark_episode_watched(slug, details, ep_num, season, episodes, completed_ids):
                    next_ep_num = int(ep_num) + 1
            
        except KeyboardInterrupt:
            return

def _calculate_next_episode(completed_ids, season, prog_data):
    last_watched_in_season = 0
    for ep_id in completed_ids:
        if ep_id >= season * 1000 and ep_id < (season + 1) * 1000:
            ep_num = ep_id % 1000
            if ep_num > last_watched_in_season:
                last_watched_in_season = ep_num
    
    if season == 1 and not any(cid >= 1000 for cid in completed_ids):
        last_watched_in_season = prog_data.get("last_watched", 0)
    
    return last_watched_in_season + 1

def _build_episode_choices(episodes, season, completed_ids, next_ep_num):
    ep_choices = []
    for ep in episodes:
        num_val = ep.get('number') or ep.get('ep_num')
        try:
            num = int(num_val)
        except:
            num = -1
        
        ep_progress_id = make_season_episode_id(season, num)
        
        prefix = "   "
        if ep_progress_id in completed_ids or (season == 1 and num in completed_ids):
            prefix = "✓  "
        elif num == next_ep_num:
            prefix = "●  "
        
        name = f"{prefix}{i18n.t('details.episode')} {num_val}"
        ep_choices.append(questionary.Choice(name, value=ep))
    
    return ep_choices

def _play_episode(slug, selected_ep, details, season, episodes):
    ep_id = selected_ep.get("id")
    ep_num = selected_ep.get("number") or selected_ep.get("ep_num")
    
    if not ep_id:
        console.print(f"[red]{i18n.t('details.invalid_ep_id')}[/red]")
        time.sleep(1)
        return False

    with console.status(i18n.t("common.processing"), spinner="dots"):
        stream_resp = get_streams(slug, ep_id)
    
    streams_list = extract_streams_from_response(stream_resp)
    
    if not streams_list:
        error_msg = i18n.t('details.stream_not_found')
        if scraper.last_error:
            error_msg += f" [{scraper.last_error}]"
        console.print(f"[red]{error_msg}[/red]")
        time.sleep(1.5)
        return False
    
    from weeb_cli.services.stream_validator import stream_validator
    
    console.print(f"[dim]{i18n.t('details.validating_streams', 'Validating streams')}...[/dim]")
    valid_streams = []
    for stream in streams_list:
        is_valid, error = stream_validator.validate_url(stream.get("url"), timeout=3)
        if is_valid:
            valid_streams.append(stream)
    
    if not valid_streams:
        console.print(f"[red]{i18n.t('details.no_valid_streams', 'No valid streams found')}[/red]")
        time.sleep(1.5)
        return False
    
    if len(valid_streams) < len(streams_list):
        console.print(f"[dim]{len(valid_streams)}/{len(streams_list)} {i18n.t('details.streams_valid', 'streams valid')}[/dim]")
    
    streams_list = sort_streams(valid_streams)
    
    selected_stream = _select_stream(streams_list)
    if selected_stream is None:
        return False
    
    stream_url = selected_stream.get("url")
    if not stream_url:
        console.print(f"[red]{i18n.t('details.stream_not_found')}[/red]")
        time.sleep(1.5)
        return False
    
    console.print(f"[green]{i18n.t('details.player_starting')}[/green]")
    title = f"{details.get('title', 'Anime')} - S{season}E{ep_num}"
    
    headers = {}
    if details.get("source") == "hianime":
        headers["Referer"] = "https://hianime.to"
    
    return player.play(
        stream_url,
        title=title,
        headers=headers,
        anime_title=details.get('title', 'Anime'),
        episode_number=int(ep_num) if ep_num else None,
        total_episodes=details.get("total_episodes") or len(episodes)
    )

def _select_stream(streams_list):
    if len(streams_list) == 1:
        return streams_list[0]
    
    stream_choices = []
    for s in streams_list:
        server = s.get("server", "Unknown")
        quality = s.get("quality", "auto")
        label = f"{server} ({quality})"
        stream_choices.append(questionary.Choice(label, value=s))
    
    return questionary.select(
        i18n.t("details.select_source"),
        choices=stream_choices,
        pointer=">",
        use_shortcuts=False
    ).ask()

def _mark_episode_watched(slug, details, ep_num, season, episodes, completed_ids):
    try:
        ans = questionary.confirm(i18n.t("details.mark_watched")).ask()
        if not ans:
            return False
        
        n = int(ep_num)
        total_eps = details.get("total_episodes") or len(episodes)
        
        season_ep_id = make_season_episode_id(season, n)
        progress_tracker.mark_watched(
            slug,
            season_ep_id,
            title=details.get("title"),
            total_episodes=total_eps
        )
        console.print(f"[green]✓ {i18n.t('details.marked_watched')}[/green]")
        
        _update_trackers(details, slug)
        
        completed_ids.add(season_ep_id)
        return True
    except:
        return False

def _update_trackers(details, slug):
    from weeb_cli.services.tracker import anilist_tracker, mal_tracker, kitsu_tracker
    
    updated_prog = progress_tracker.get_anime_progress(slug)
    total_watched = len(updated_prog.get("completed", []))
    total_eps = details.get("total_episodes", 0)
    
    updated = []
    pending = []
    
    for name, tracker in [("AniList", anilist_tracker), ("MAL", mal_tracker), ("Kitsu", kitsu_tracker)]:
        if tracker.is_authenticated():
            result = tracker.update_progress(
                details.get("title"),
                total_watched,
                total_eps
            )
            if result:
                updated.append(name)
            else:
                pending.append(name)
    
    # Show combined message
    if updated:
        trackers_str = ", ".join(updated)
        console.print(f"[green]✓ {trackers_str} {i18n.t('watchlist.tracker_updated')}[/green]")
    if pending:
        trackers_str = ", ".join(pending)
        console.print(f"[yellow]⏳ {trackers_str}: {i18n.t('watchlist.tracker_pending')}[/yellow]")
