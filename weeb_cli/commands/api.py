import json
import sys
import typer
from typing import Optional

api_app = typer.Typer(
    name="api",
    help="Non-interactive API commands for scripts, agents, and automation.",
    add_completion=False,
    invoke_without_command=True,
)


def _setup_headless():
    from weeb_cli.config import config
    config.set_headless(True)


def _get_provider(name: str):
    from weeb_cli.providers.registry import get_provider
    provider = get_provider(name)
    if provider is None:
        typer.echo(json.dumps({"error": f"Unknown provider: {name}"}), err=True)
        raise typer.Exit(1)
    return provider


def _output(data):
    typer.echo(json.dumps(data, ensure_ascii=False, indent=2))


def _quality_score(q: str) -> int:
    q = (q or "").lower()
    if "1080" in q:
        return 3
    if "720" in q:
        return 2
    if "480" in q:
        return 1
    return 0


@api_app.callback()
def api_callback(ctx: typer.Context):
    _setup_headless()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(0)


@api_app.command()
def providers():
    """List all available providers."""
    from weeb_cli.providers.registry import list_providers
    _output(list_providers())


@api_app.command()
def search(
    query: str = typer.Argument(..., help="Search query"),
    provider: str = typer.Option("animecix", "--provider", "-p", help="Provider name"),
):
    """Search for anime by title. Returns a list with IDs to use in other commands."""
    p = _get_provider(provider)
    results = p.search(query)
    _output([
        {"id": r.id, "title": r.title, "type": r.type, "cover": r.cover, "year": r.year}
        for r in results
    ])


@api_app.command()
def episodes(
    anime_id: str = typer.Argument(..., help="Anime ID from search results"),
    season: Optional[int] = typer.Option(None, "--season", "-s", help="Filter by season number"),
    provider: str = typer.Option("animecix", "--provider", "-p", help="Provider name"),
):
    """List episodes for an anime by ID."""
    p = _get_provider(provider)
    eps = p.get_episodes(anime_id)
    if season is not None:
        eps = [e for e in eps if e.season == season]
    _output([
        {"id": e.id, "number": e.number, "title": e.title, "season": e.season, "url": e.url}
        for e in eps
    ])


@api_app.command()
def streams(
    anime_id: str = typer.Argument(..., help="Anime ID from search results"),
    season: int = typer.Option(1, "--season", "-s", help="Season number"),
    episode: int = typer.Option(..., "--episode", "-e", help="Episode number"),
    provider: str = typer.Option("animecix", "--provider", "-p", help="Provider name"),
):
    """Get stream URLs for a specific episode by anime ID and episode number."""
    p = _get_provider(provider)
    eps = p.get_episodes(anime_id)
    target = [e for e in eps if e.season == season and e.number == episode]
    if not target:
        _output({"error": f"Episode S{season:02d}E{episode:02d} not found"})
        raise typer.Exit(1)
    ep = target[0]
    links = p.get_streams(anime_id, ep.id)
    _output([
        {"url": s.url, "quality": s.quality, "server": s.server, "headers": s.headers, "subtitles": s.subtitles}
        for s in links
    ])


@api_app.command()
def details(
    anime_id: str = typer.Argument(..., help="Anime ID from search results"),
    provider: str = typer.Option("animecix", "--provider", "-p", help="Provider name"),
):
    """Get anime details by ID."""
    p = _get_provider(provider)
    d = p.get_details(anime_id)
    if d is None:
        _output({"error": "Not found"})
        raise typer.Exit(1)
    _output({
        "id": d.id, "title": d.title, "description": d.description, "cover": d.cover,
        "genres": d.genres, "year": d.year, "status": d.status, "total_episodes": d.total_episodes,
        "episodes": [
            {"id": e.id, "number": e.number, "title": e.title, "season": e.season}
            for e in d.episodes
        ],
    })


@api_app.command()
def download(
    anime_id: str = typer.Argument(..., help="Anime ID from search results"),
    season: int = typer.Option(1, "--season", "-s", help="Season number"),
    episode: int = typer.Option(..., "--episode", "-e", help="Episode number"),
    provider: str = typer.Option("animecix", "--provider", "-p", help="Provider name"),
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Download an episode by anime ID and episode number."""
    from weeb_cli.services.headless_downloader import download_episode

    p = _get_provider(provider)
    eps = p.get_episodes(anime_id)
    target = [e for e in eps if e.season == season and e.number == episode]
    if not target:
        _output({"status": "error", "message": f"Episode S{season:02d}E{episode:02d} not found"})
        raise typer.Exit(1)

    ep = target[0]
    stream_links = p.get_streams(anime_id, ep.id)
    if not stream_links:
        _output({"status": "error", "message": "No streams available"})
        raise typer.Exit(1)

    stream_links.sort(key=lambda s: _quality_score(s.quality), reverse=True)

    # Try to get the anime title for the filename
    d = p.get_details(anime_id)
    title = d.title if d else anime_id

    for stream in stream_links:
        result = download_episode(
            stream_url=stream.url,
            series_title=title,
            season=season,
            episode=episode,
            download_dir=output,
        )
        if result:
            _output({"status": "ok", "path": result, "anime": title, "quality": stream.quality})
            return

    _output({"status": "error", "message": "All streams failed"})
    raise typer.Exit(1)


@api_app.command(name="download-url", hidden=True)
def download_url(
    stream_url: str = typer.Argument(..., help="Direct stream URL to download"),
    title: str = typer.Option(..., "--title", "-t", help="Series title for filename"),
    season: int = typer.Option(1, "--season", "-s", help="Season number"),
    episode: int = typer.Option(..., "--episode", "-e", help="Episode number"),
    output: str = typer.Option(".", "--output", "-o", help="Output directory"),
):
    """Download a single episode from a direct stream URL."""
    from weeb_cli.services.headless_downloader import download_episode
    result = download_episode(
        stream_url=stream_url,
        series_title=title,
        season=season,
        episode=episode,
        download_dir=output,
    )
    if result:
        _output({"status": "ok", "path": result})
    else:
        _output({"status": "error", "message": "Download failed"})
        raise typer.Exit(1)
