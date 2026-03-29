"""RESTful API server for weeb-cli.

Provides HTTP endpoints that mirror the 'weeb-cli api' commands.
All endpoints return JSON responses identical to the CLI API mode.

Requires: pip install weeb-cli[serve-restful]
Usage:  weeb-cli serve restful --port 8080
"""
import logging
import sys
from typing import Optional

import typer

log = logging.getLogger("weeb-cli-restful")

restful_app = typer.Typer(
    name="restful",
    help="Start a RESTful API server (HTTP version of 'weeb-cli api' commands).",
    add_completion=False,
    invoke_without_command=True,
)


def _quality_score(q: str) -> int:
    """Calculate quality score for stream sorting."""
    q = (q or "").lower()
    if "4k" in q or "2160" in q:
        return 5
    if "1080" in q:
        return 4
    if "720" in q:
        return 3
    if "480" in q:
        return 2
    if "360" in q:
        return 1
    return 0


@restful_app.callback(invoke_without_command=True)
def serve_restful(
    ctx: typer.Context,
    port: int = typer.Option(8080, "--port", envvar="RESTFUL_PORT", help="HTTP port"),
    host: str = typer.Option("0.0.0.0", "--host", envvar="RESTFUL_HOST", help="Bind host"),
    enable_cors: bool = typer.Option(True, "--cors/--no-cors", envvar="RESTFUL_CORS", help="Enable CORS"),
    debug: bool = typer.Option(False, "--debug", envvar="RESTFUL_DEBUG", help="Enable debug mode"),
):
    """Start RESTful API server.
    
    Provides HTTP endpoints that mirror 'weeb-cli api' commands:
    - GET /api/providers -> weeb-cli api providers
    - GET /api/search -> weeb-cli api search
    - GET /api/episodes -> weeb-cli api episodes
    - GET /api/streams -> weeb-cli api streams
    - GET /api/details -> weeb-cli api details
    - POST /api/download -> weeb-cli api download
    """
    try:
        from flask import Flask, request, jsonify
    except ImportError:
        typer.echo(
            "Flask is required for serve restful mode. Install with: pip install weeb-cli[serve-restful]",
            err=True,
        )
        raise typer.Exit(1)

    # Setup headless mode
    from weeb_cli.config import config as weeb_config
    weeb_config.set_headless(True)

    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    # Import provider functions
    from weeb_cli.providers.registry import get_provider, list_providers as list_all_providers

    # Create Flask app
    flask_app = Flask(__name__)
    
    if enable_cors:
        try:
            from flask_cors import CORS
            CORS(flask_app)
            log.info("CORS enabled")
        except ImportError:
            log.warning("flask-cors not installed, CORS disabled")

    # Helper function
    def _get_provider(name: str):
        provider = get_provider(name)
        if provider is None:
            return None
        return provider

    # Health check endpoint
    @flask_app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        all_providers = list_all_providers()
        # Only show enabled providers in health check
        enabled_providers = [p["name"] for p in all_providers if not p.get("disabled", False)]
        return jsonify({
            "status": "ok",
            "service": "weeb-cli-restful",
            "providers": enabled_providers,
        })

    # GET /api/providers - List all available providers
    @flask_app.route("/api/providers", methods=["GET"])
    def api_providers():
        """List all available providers.
        
        Equivalent to: weeb-cli api providers
        """
        try:
            providers = list_all_providers()
            return jsonify(providers)
        except Exception as e:
            log.error(f"Error listing providers: {e}")
            return jsonify({"error": str(e)}), 500

    # GET /api/search?query=...&provider=... - Search anime
    @flask_app.route("/api/search", methods=["GET"])
    def api_search():
        """Search anime.
        
        Query params:
            query: Search query (required)
            provider: Provider name (default: animecix)
        
        Equivalent to: weeb-cli api search "query" --provider animecix
        """
        query = request.args.get("query", "").strip()
        provider_name = request.args.get("provider", "animecix").strip()

        if not query:
            return jsonify({"error": "Missing query parameter"}), 400

        provider = _get_provider(provider_name)
        if provider is None:
            return jsonify({"error": f"Unknown provider: {provider_name}"}), 404

        try:
            results = provider.search(query)
            return jsonify([
                {"id": r.id, "title": r.title, "type": r.type, "cover": r.cover, "year": r.year}
                for r in results
            ])
        except Exception as e:
            log.error(f"Search error: {e}")
            return jsonify({"error": str(e)}), 500

    # GET /api/episodes?anime_id=...&provider=...&season=... - Get episodes
    @flask_app.route("/api/episodes", methods=["GET"])
    def api_episodes():
        """Get anime episodes.
        
        Query params:
            anime_id: Anime ID (required)
            provider: Provider name (default: animecix)
            season: Filter by season number (optional)
        
        Equivalent to: weeb-cli api episodes <anime_id> --provider animecix --season 1
        """
        anime_id = request.args.get("anime_id", "").strip()
        provider_name = request.args.get("provider", "animecix").strip()
        season_filter = request.args.get("season")

        if not anime_id:
            return jsonify({"error": "Missing anime_id parameter"}), 400

        provider = _get_provider(provider_name)
        if provider is None:
            return jsonify({"error": f"Unknown provider: {provider_name}"}), 404

        try:
            eps = provider.get_episodes(anime_id)
            
            if season_filter is not None:
                try:
                    season_num = int(season_filter)
                    eps = [e for e in eps if e.season == season_num]
                except ValueError:
                    return jsonify({"error": "Invalid season number"}), 400

            return jsonify([
                {"id": e.id, "number": e.number, "title": e.title, "season": e.season, "url": e.url}
                for e in eps
            ])
        except Exception as e:
            log.error(f"Episodes error: {e}")
            return jsonify({"error": str(e)}), 500

    # GET /api/streams?anime_id=...&season=...&episode=...&provider=... - Get streams
    @flask_app.route("/api/streams", methods=["GET"])
    def api_streams():
        """Get episode streams.
        
        Query params:
            anime_id: Anime ID (required)
            season: Season number (default: 1)
            episode: Episode number (required)
            provider: Provider name (default: animecix)
        
        Equivalent to: weeb-cli api streams <anime_id> --season 1 --episode 1 --provider animecix
        """
        anime_id = request.args.get("anime_id", "").strip()
        provider_name = request.args.get("provider", "animecix").strip()
        
        try:
            season = int(request.args.get("season", "1"))
            episode = int(request.args.get("episode", "0"))
        except ValueError:
            return jsonify({"error": "Invalid season or episode number"}), 400

        if not anime_id:
            return jsonify({"error": "Missing anime_id parameter"}), 400
        if episode == 0:
            return jsonify({"error": "Missing episode parameter"}), 400

        provider = _get_provider(provider_name)
        if provider is None:
            return jsonify({"error": f"Unknown provider: {provider_name}"}), 404

        try:
            eps = provider.get_episodes(anime_id)
            target = [e for e in eps if e.season == season and e.number == episode]
            
            if not target:
                return jsonify({"error": f"Episode S{season:02d}E{episode:02d} not found"}), 404

            ep = target[0]
            links = provider.get_streams(anime_id, ep.id)
            
            return jsonify([
                {"url": s.url, "quality": s.quality, "server": s.server, "headers": s.headers, "subtitles": s.subtitles}
                for s in links
            ])
        except Exception as e:
            log.error(f"Streams error: {e}")
            return jsonify({"error": str(e)}), 500

    # GET /api/details?anime_id=...&provider=... - Get anime details
    @flask_app.route("/api/details", methods=["GET"])
    def api_details():
        """Get anime details.
        
        Query params:
            anime_id: Anime ID (required)
            provider: Provider name (default: animecix)
        
        Equivalent to: weeb-cli api details <anime_id> --provider animecix
        """
        anime_id = request.args.get("anime_id", "").strip()
        provider_name = request.args.get("provider", "animecix").strip()

        if not anime_id:
            return jsonify({"error": "Missing anime_id parameter"}), 400

        provider = _get_provider(provider_name)
        if provider is None:
            return jsonify({"error": f"Unknown provider: {provider_name}"}), 404

        try:
            d = provider.get_details(anime_id)
            if d is None:
                return jsonify({"error": "Not found"}), 404

            return jsonify({
                "id": d.id, "title": d.title, "description": d.description, "cover": d.cover,
                "genres": d.genres, "year": d.year, "status": d.status, "total_episodes": d.total_episodes,
                "episodes": [
                    {"id": e.id, "number": e.number, "title": e.title, "season": e.season}
                    for e in d.episodes
                ],
            })
        except Exception as e:
            log.error(f"Details error: {e}")
            return jsonify({"error": str(e)}), 500

    # POST /api/download - Download episode
    @flask_app.route("/api/download", methods=["POST"])
    def api_download():
        """Download episode.
        
        JSON body:
            anime_id: Anime ID (required)
            season: Season number (default: 1)
            episode: Episode number (required)
            provider: Provider name (default: animecix)
            output: Output directory (default: ".")
        
        Equivalent to: weeb-cli api download <anime_id> --season 1 --episode 1 --provider animecix --output .
        """
        from weeb_cli.services.headless_downloader import download_episode

        data = request.get_json() or {}
        
        anime_id = data.get("anime_id", "").strip()
        provider_name = data.get("provider", "animecix").strip()
        season = data.get("season", 1)
        episode_num = data.get("episode", 0)
        output = data.get("output", ".")

        if not anime_id:
            return jsonify({"status": "error", "message": "Missing anime_id"}), 400
        if episode_num == 0:
            return jsonify({"status": "error", "message": "Missing episode"}), 400

        provider = _get_provider(provider_name)
        if provider is None:
            return jsonify({"status": "error", "message": f"Unknown provider: {provider_name}"}), 404

        try:
            eps = provider.get_episodes(anime_id)
            target = [e for e in eps if e.season == season and e.number == episode_num]
            
            if not target:
                return jsonify({"status": "error", "message": f"Episode S{season:02d}E{episode_num:02d} not found"}), 404

            ep = target[0]
            stream_links = provider.get_streams(anime_id, ep.id)
            
            if not stream_links:
                return jsonify({"status": "error", "message": "No streams available"}), 404

            stream_links.sort(key=lambda s: _quality_score(s.quality), reverse=True)

            # Try to get the anime title for the filename
            d = provider.get_details(anime_id)
            title = d.title if d else anime_id

            for stream in stream_links:
                result = download_episode(
                    stream_url=stream.url,
                    series_title=title,
                    season=season,
                    episode=episode_num,
                    download_dir=output,
                )
                if result:
                    return jsonify({"status": "ok", "path": result, "anime": title, "quality": stream.quality})

            return jsonify({"status": "error", "message": "All streams failed"}), 500

        except Exception as e:
            log.error(f"Download error: {e}")
            return jsonify({"status": "error", "message": str(e)}), 500

    # Error handlers
    @flask_app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Endpoint not found"}), 404

    @flask_app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    # Start server
    log.info("=" * 60)
    log.info("weeb-cli RESTful API starting")
    log.info("=" * 60)
    log.info(f"  Host: {host}")
    log.info(f"  Port: {port}")
    log.info(f"  CORS: {'enabled' if enable_cors else 'disabled'}")
    log.info(f"  Debug: {'enabled' if debug else 'disabled'}")
    log.info("=" * 60)
    log.info("  Endpoints (mirror 'weeb-cli api' commands):")
    log.info("    GET  /health")
    log.info("    GET  /api/providers")
    log.info("    GET  /api/search?query=...&provider=...")
    log.info("    GET  /api/episodes?anime_id=...&provider=...&season=...")
    log.info("    GET  /api/streams?anime_id=...&season=...&episode=...&provider=...")
    log.info("    GET  /api/details?anime_id=...&provider=...")
    log.info("    POST /api/download (JSON body)")
    log.info("=" * 60)

    flask_app.run(host=host, port=port, debug=debug)
