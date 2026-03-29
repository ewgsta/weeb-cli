"""RESTful API server for weeb-cli.

Provides a REST API interface for all provider operations including search,
episode listing, stream extraction, and anime details.

Requires: pip install weeb-cli[serve-restful]
Usage:  weeb-cli serve restful --port 8080 --providers animecix,hianime
"""
import json
import logging
import sys
from typing import Optional, List

import typer
from flask import Flask, request, jsonify, Response
from flask_cors import CORS

log = logging.getLogger("weeb-cli-restful")

restful_app = typer.Typer(
    name="restful",
    help="Start a RESTful API server for provider operations.",
    add_completion=False,
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


def _serialize_anime_result(result) -> dict:
    """Serialize AnimeResult to dict."""
    return {
        "id": result.id,
        "title": result.title,
        "type": result.type,
        "cover": result.cover,
        "year": result.year,
    }


def _serialize_episode(episode) -> dict:
    """Serialize Episode to dict."""
    return {
        "id": episode.id,
        "number": episode.number,
        "title": episode.title,
        "season": episode.season,
        "url": episode.url,
    }


def _serialize_stream(stream) -> dict:
    """Serialize StreamLink to dict."""
    return {
        "url": stream.url,
        "quality": stream.quality,
        "server": stream.server,
        "headers": stream.headers,
        "subtitles": stream.subtitles,
    }


def _serialize_anime_details(details) -> dict:
    """Serialize AnimeDetails to dict."""
    return {
        "id": details.id,
        "title": details.title,
        "type": details.type,
        "cover": details.cover,
        "year": details.year,
        "description": details.description,
        "genres": details.genres,
        "status": details.status,
        "episodes": [_serialize_episode(ep) for ep in details.episodes] if details.episodes else [],
    }


@restful_app.callback(invoke_without_command=True)
def serve_restful(
    ctx: typer.Context,
    port: int = typer.Option(8080, "--port", envvar="RESTFUL_PORT", help="HTTP port"),
    host: str = typer.Option("0.0.0.0", "--host", envvar="RESTFUL_HOST", help="Bind host"),
    provider_names: str = typer.Option(
        "animecix,hianime,aniworld,docchi",
        "--providers",
        envvar="RESTFUL_PROVIDERS",
        help="Comma-separated provider names",
    ),
    enable_cors: bool = typer.Option(True, "--cors/--no-cors", envvar="RESTFUL_CORS", help="Enable CORS"),
    debug: bool = typer.Option(False, "--debug", envvar="RESTFUL_DEBUG", help="Enable debug mode"),
):
    """Start RESTful API server."""
    try:
        from flask import Flask
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

    # Load providers
    from weeb_cli.providers.registry import get_provider, list_providers as list_all_providers
    
    providers = {}
    for name in provider_names.split(","):
        name = name.strip()
        p = get_provider(name)
        if p:
            providers[name] = p
            log.info(f"Loaded provider: {name}")
        else:
            log.warning(f"Provider not found: {name}")

    if not providers:
        log.error("No providers loaded, exiting.")
        raise typer.Exit(1)

    # Create Flask app
    flask_app = Flask(__name__)
    
    if enable_cors:
        CORS(flask_app)
        log.info("CORS enabled")

    # Health check endpoint
    @flask_app.route("/health", methods=["GET"])
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "ok",
            "service": "weeb-cli-restful",
            "providers": list(providers.keys()),
        })

    # List all available providers
    @flask_app.route("/api/providers", methods=["GET"])
    def api_providers():
        """List all available providers."""
        try:
            all_providers = list_all_providers()
            return jsonify({
                "success": True,
                "providers": all_providers,
                "loaded": list(providers.keys()),
            })
        except Exception as e:
            log.error(f"Error listing providers: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Search anime
    @flask_app.route("/api/search", methods=["GET"])
    def api_search():
        """Search anime across providers.
        
        Query params:
            q: Search query (required)
            provider: Provider name (optional, defaults to first loaded)
        """
        query = request.args.get("q", "").strip()
        provider_name = request.args.get("provider", "").strip()

        if not query:
            return jsonify({"success": False, "error": "Missing query parameter 'q'"}), 400

        # Select provider
        if provider_name:
            if provider_name not in providers:
                return jsonify({
                    "success": False,
                    "error": f"Provider '{provider_name}' not loaded",
                    "available": list(providers.keys()),
                }), 404
            provider = providers[provider_name]
        else:
            provider = next(iter(providers.values()))
            provider_name = provider.name

        try:
            log.info(f"Search: query='{query}' provider={provider_name}")
            results = provider.search(query)
            
            return jsonify({
                "success": True,
                "provider": provider_name,
                "query": query,
                "count": len(results),
                "results": [_serialize_anime_result(r) for r in results],
            })
        except Exception as e:
            log.error(f"Search error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Get anime details
    @flask_app.route("/api/anime/<anime_id>", methods=["GET"])
    def api_anime_details(anime_id: str):
        """Get anime details.
        
        Query params:
            provider: Provider name (optional, defaults to first loaded)
        """
        provider_name = request.args.get("provider", "").strip()

        # Select provider
        if provider_name:
            if provider_name not in providers:
                return jsonify({
                    "success": False,
                    "error": f"Provider '{provider_name}' not loaded",
                    "available": list(providers.keys()),
                }), 404
            provider = providers[provider_name]
        else:
            provider = next(iter(providers.values()))
            provider_name = provider.name

        try:
            log.info(f"Details: anime_id='{anime_id}' provider={provider_name}")
            details = provider.get_details(anime_id)
            
            if not details:
                return jsonify({
                    "success": False,
                    "error": "Anime not found",
                }), 404

            return jsonify({
                "success": True,
                "provider": provider_name,
                "anime": _serialize_anime_details(details),
            })
        except Exception as e:
            log.error(f"Details error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Get episodes
    @flask_app.route("/api/anime/<anime_id>/episodes", methods=["GET"])
    def api_episodes(anime_id: str):
        """Get anime episodes.
        
        Query params:
            provider: Provider name (optional, defaults to first loaded)
            season: Filter by season number (optional)
        """
        provider_name = request.args.get("provider", "").strip()
        season_filter = request.args.get("season")

        # Select provider
        if provider_name:
            if provider_name not in providers:
                return jsonify({
                    "success": False,
                    "error": f"Provider '{provider_name}' not loaded",
                    "available": list(providers.keys()),
                }), 404
            provider = providers[provider_name]
        else:
            provider = next(iter(providers.values()))
            provider_name = provider.name

        try:
            log.info(f"Episodes: anime_id='{anime_id}' provider={provider_name} season={season_filter}")
            episodes = provider.get_episodes(anime_id)
            
            # Filter by season if requested
            if season_filter:
                try:
                    season_num = int(season_filter)
                    episodes = [ep for ep in episodes if ep.season == season_num]
                except ValueError:
                    return jsonify({"success": False, "error": "Invalid season number"}), 400

            return jsonify({
                "success": True,
                "provider": provider_name,
                "anime_id": anime_id,
                "count": len(episodes),
                "episodes": [_serialize_episode(ep) for ep in episodes],
            })
        except Exception as e:
            log.error(f"Episodes error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Get streams
    @flask_app.route("/api/anime/<anime_id>/episodes/<episode_id>/streams", methods=["GET"])
    def api_streams(anime_id: str, episode_id: str):
        """Get episode streams.
        
        Query params:
            provider: Provider name (optional, defaults to first loaded)
            sort: Sort by quality (asc/desc, optional)
        """
        provider_name = request.args.get("provider", "").strip()
        sort_order = request.args.get("sort", "desc").lower()

        # Select provider
        if provider_name:
            if provider_name not in providers:
                return jsonify({
                    "success": False,
                    "error": f"Provider '{provider_name}' not loaded",
                    "available": list(providers.keys()),
                }), 404
            provider = providers[provider_name]
        else:
            provider = next(iter(providers.values()))
            provider_name = provider.name

        try:
            log.info(f"Streams: anime_id='{anime_id}' episode_id='{episode_id}' provider={provider_name}")
            streams = provider.get_streams(anime_id, episode_id)
            
            # Sort by quality
            if sort_order == "desc":
                streams = sorted(streams, key=lambda s: _quality_score(s.quality), reverse=True)
            elif sort_order == "asc":
                streams = sorted(streams, key=lambda s: _quality_score(s.quality))

            return jsonify({
                "success": True,
                "provider": provider_name,
                "anime_id": anime_id,
                "episode_id": episode_id,
                "count": len(streams),
                "streams": [_serialize_stream(s) for s in streams],
            })
        except Exception as e:
            log.error(f"Streams error: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    # Error handlers
    @flask_app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "error": "Endpoint not found"}), 404

    @flask_app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "error": "Internal server error"}), 500

    # Start server
    log.info("weeb-cli RESTful API starting")
    log.info(f"  Host: {host}")
    log.info(f"  Port: {port}")
    log.info(f"  Providers: {', '.join(providers.keys())}")
    log.info(f"  CORS: {'enabled' if enable_cors else 'disabled'}")
    log.info(f"  Debug: {'enabled' if debug else 'disabled'}")

    flask_app.run(host=host, port=port, debug=debug)
