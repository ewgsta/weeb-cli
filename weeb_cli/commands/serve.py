"""Built-in Torznab-compatible server for Sonarr/*arr integration.

Requires: pip install weeb-cli[serve]
Usage:  weeb-cli serve --port 9876 --watch-dir /downloads/watch --completed-dir /downloads/completed
"""
import json
import time
import base64
import hashlib
import logging
import re
import sys
import threading
from difflib import SequenceMatcher
from pathlib import Path
from datetime import datetime, timezone
from xml.etree.ElementTree import Element, SubElement, tostring

import typer

log = logging.getLogger("weeb-cli")

serve_app = typer.Typer(
    name="serve",
    help="Start a Torznab-compatible server for Sonarr/*arr integration.",
    add_completion=False,
)


# -- Helpers ------------------------------------------------------------------

def _sanitize_for_release(name: str) -> str:
    name = re.sub(r'[<>:"/\\|?*]', "", name)
    name = re.sub(r"[\s]+", ".", name).strip(".")
    return name


def _quality_score(q: str) -> int:
    q = (q or "").lower()
    if "1080" in q:
        return 3
    if "720" in q:
        return 2
    if "480" in q:
        return 1
    return 0


def _make_guid(anime_id: str, season: int, episode: int, release_name: str) -> str:
    raw = f"{anime_id}-{season}-{episode}-{release_name}"
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def _encode_download_id(data: dict) -> str:
    return base64.urlsafe_b64encode(json.dumps(data).encode()).decode()


def _decode_download_id(encoded: str) -> dict:
    return json.loads(base64.urlsafe_b64decode(encoded.encode()).decode())


# -- Sonarr integration -------------------------------------------------------

def _sonarr_get_series_title(q: str, sonarr_url: str, sonarr_api_key: str) -> str | None:
    if not sonarr_url or not sonarr_api_key:
        return None
    try:
        import requests
        resp = requests.get(
            f"{sonarr_url}/api/v3/series",
            headers={"X-Api-Key": sonarr_api_key},
            timeout=5,
        )
        if resp.status_code != 200:
            return None
        series_list = resp.json()
        q_lower = q.lower().strip()
        q_stripped = re.sub(r"\s+\d+$", "", q_lower).strip()
        q_variants = list(dict.fromkeys([q_lower, q_stripped]))

        for q_try in q_variants:
            q_clean = re.sub(r"[^a-z0-9]", "", q_try)
            for series in series_list:
                title = series.get("title", "")
                if title.lower() == q_try:
                    return title
                clean_title = series.get("cleanTitle", "")
                if clean_title and clean_title == q_clean:
                    return title
                for alt in series.get("alternateTitles", []):
                    alt_title = alt.get("title", "").lower()
                    alt_clean = re.sub(r"[^a-z0-9]", "", alt_title)
                    if alt_title == q_try or alt_clean == q_clean:
                        return title
        return None
    except Exception as e:
        log.debug(f"Sonarr lookup failed: {e}")
        return None


# -- Torznab XML builders -----------------------------------------------------

def _torznab_error(code: int, description: str):
    from flask import Response
    root = Element("error", code=str(code), description=description)
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode")
    return Response(xml, mimetype="application/xml")


def _torznab_caps_xml() -> str:
    root = Element("caps")
    SubElement(root, "server", version="1.0", title="weeb-cli")
    SubElement(root, "limits", max="100", default="50")
    searching = SubElement(root, "searching")
    SubElement(searching, "search", available="yes", supportedParams="q")
    SubElement(searching, "tv-search", available="yes", supportedParams="q,season,ep")
    SubElement(searching, "movie-search", available="no")
    categories = SubElement(root, "categories")
    cat = SubElement(categories, "category", id="5000", name="TV")
    SubElement(cat, "subcat", id="5030", name="TV/SD")
    SubElement(cat, "subcat", id="5040", name="TV/HD")
    SubElement(cat, "subcat", id="5070", name="TV/Anime")
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode")


def _build_torznab_rss(items: list) -> str:
    root = Element("rss", version="2.0")
    root.set("xmlns:torznab", "http://torznab.com/schemas/2015/feed")
    root.set("xmlns:atom", "http://www.w3.org/2005/Atom")
    channel = SubElement(root, "channel")
    SubElement(channel, "title").text = "weeb-cli"

    for it in items:
        item = SubElement(channel, "item")
        SubElement(item, "title").text = it["title"]
        SubElement(item, "guid").text = it["guid"]
        SubElement(item, "link").text = it["link"]
        SubElement(item, "pubDate").text = datetime.now(timezone.utc).strftime(
            "%a, %d %b %Y %H:%M:%S +0000"
        )
        SubElement(item, "category").text = "5070"
        enc = SubElement(item, "enclosure")
        enc.set("url", it["link"])
        enc.set("length", str(it.get("size", 0)))
        enc.set("type", "application/x-bittorrent")

        for attr_name, attr_val in it.get("attrs", {}).items():
            a = SubElement(item, "torznab:attr")
            a.set("name", attr_name)
            a.set("value", str(attr_val))

    return '<?xml version="1.0" encoding="UTF-8"?>\n' + tostring(root, encoding="unicode")


# -- Stream download helper ---------------------------------------------------

def _try_streams(streams, sonarr_title, season, episode_num, completed_dir) -> bool:
    from weeb_cli.services.headless_downloader import download_episode
    if not streams:
        return False
    streams_sorted = sorted(streams, key=lambda s: _quality_score(s.quality), reverse=True)
    for stream in streams_sorted:
        log.info(f"  Trying stream: {stream.quality} @ {stream.server}")
        result = download_episode(
            stream_url=stream.url,
            series_title=sonarr_title,
            season=season,
            episode=episode_num,
            download_dir=completed_dir,
        )
        if result:
            return True
        log.warning(f"  Stream failed, trying next...")
    return False


def _get_fallback_streams(fallback_providers, sonarr_title, season, episode_num):
    for fp in fallback_providers:
        try:
            log.info(f"  Fallback: trying {fp.name} for {sonarr_title} S{season:02d}E{episode_num:02d}")
            results = fp.search(sonarr_title)
            if not results:
                continue
            best = max(results, key=lambda r: SequenceMatcher(
                None, sonarr_title.lower(), r.title.lower()
            ).ratio())
            log.info(f"  Fallback: {fp.name} matched '{best.title}' (id={best.id})")
            episodes = fp.get_episodes(best.id)
            target = [e for e in episodes if e.number == episode_num]
            if not target:
                continue
            ep = target[0]
            streams = fp.get_streams(best.id, ep.id)
            if streams:
                log.info(f"  Fallback: {fp.name} returned {len(streams)} stream(s)")
                return streams
        except Exception as e:
            log.error(f"  Fallback: {fp.name} error: {e}")
    return []


# -- Main serve command -------------------------------------------------------

@serve_app.callback(invoke_without_command=True)
def serve(
    ctx: typer.Context,
    port: int = typer.Option(9876, "--port", envvar="FLASK_PORT", help="HTTP port"),
    watch_dir: str = typer.Option("/downloads/weeb-cli/watch", "--watch-dir", envvar="WATCH_DIR", help="Blackhole watch directory"),
    completed_dir: str = typer.Option("/downloads/weeb-cli/completed", "--completed-dir", envvar="COMPLETED_DIR", help="Completed downloads directory"),
    config_dir: str = typer.Option("/config", "--config-dir", envvar="CONFIG_DIR", help="Config directory for mappings"),
    poll_interval: int = typer.Option(5, "--poll-interval", envvar="POLL_INTERVAL", help="Blackhole poll interval in seconds"),
    sonarr_url: str = typer.Option("", "--sonarr-url", envvar="SONARR_URL", help="Sonarr base URL"),
    sonarr_api_key: str = typer.Option("", "--sonarr-api-key", envvar="SONARR_API_KEY", help="Sonarr API key"),
    provider_names: str = typer.Option("animecix,anizle,turkanime", "--providers", envvar="PROVIDERS", help="Comma-separated provider names (first is primary)"),
):
    """Start a Torznab-compatible HTTP server for Sonarr/*arr integration."""
    try:
        from flask import Flask, request, Response
    except ImportError:
        typer.echo(
            "Flask is required for serve mode. Install with: pip install weeb-cli[serve]",
            err=True,
        )
        raise typer.Exit(1)

    import yaml
    from weeb_cli.config import config as weeb_config
    weeb_config.set_headless(True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )

    # Load providers
    from weeb_cli.providers.registry import get_provider
    all_providers = []
    for name in provider_names.split(","):
        name = name.strip()
        p = get_provider(name)
        if p:
            all_providers.append(p)
            log.info(f"Loaded provider: {name}")
        else:
            log.warning(f"Provider not found: {name}")

    if not all_providers:
        log.error("No providers loaded, exiting.")
        raise typer.Exit(1)

    primary = all_providers[0]
    fallbacks = all_providers[1:]

    # Config loader
    def _load_mappings() -> dict:
        config_path = Path(config_dir) / "config.yml"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    cfg = yaml.safe_load(f) or {}
                return cfg.get("mappings", {}) or {}
            except Exception:
                pass
        return {}

    # Flask app
    flask_app = Flask(__name__)

    @flask_app.route("/api", methods=["GET"])
    def torznab_api():
        t = request.args.get("t", "")
        if t == "caps":
            return Response(_torznab_caps_xml(), mimetype="application/xml")

        if t in ("search", "tvsearch"):
            q = request.args.get("q", "").strip()
            season = request.args.get("season")
            ep = request.args.get("ep")

            if not q:
                return Response(_build_torznab_rss([]), mimetype="application/xml")

            mappings = _load_mappings()
            search_term = mappings.get(q, q)
            log.info(f"Torznab search: q={q} season={season} ep={ep} (search_term={search_term})")

            results = primary.search(search_term)
            if not results:
                log.info(f"  No results for '{search_term}'")
                return Response(_build_torznab_rss([]), mimetype="application/xml")

            best = results[0]
            log.info(f"  Best match: {best.title} (id={best.id})")

            eps = primary.get_episodes(best.id)
            if not eps:
                return Response(_build_torznab_rss([]), mimetype="application/xml")

            if season:
                try:
                    s_num = int(season)
                    eps = [e for e in eps if e.season == s_num]
                except ValueError:
                    pass
            if ep:
                try:
                    e_num = int(ep)
                    eps = [e for e in eps if e.number == e_num]
                except ValueError:
                    pass

            items = []
            base_url = request.host_url.rstrip("/")
            s_title = _sonarr_get_series_title(q, sonarr_url, sonarr_api_key) or q
            release_series = _sanitize_for_release(s_title)

            for episode in eps:
                release_name = (
                    f"{release_series}.S{episode.season:02d}E{episode.number:02d}"
                    f".{primary.name}.1080p.WEB-DL.TR-WEEBCLI"
                )
                download_data = {
                    "episode_url": episode.id,
                    "anime_id": best.id,
                    "sonarr_title": s_title,
                    "season": episode.season,
                    "episode": episode.number,
                    "release_name": release_name,
                }
                dl_id = _encode_download_id(download_data)
                dl_link = f"{base_url}/download?id={dl_id}"
                guid = _make_guid(best.id, episode.season, episode.number, release_name)
                items.append({
                    "title": release_name,
                    "guid": guid,
                    "link": dl_link,
                    "size": 2_000_000_000,
                    "attrs": {
                        "category": "5070",
                        "seeders": "1",
                        "leechers": "0",
                        "peers": "1",
                        "size": "2000000000",
                        "minimumratio": "0",
                        "minimumseedtime": "0",
                    },
                })

            log.info(f"  Returning {len(items)} result(s)")
            return Response(_build_torznab_rss(items), mimetype="application/xml")

        return _torznab_error(202, f"Unsupported function: {t}")

    @flask_app.route("/download", methods=["GET"])
    def download_stub():
        dl_id = request.args.get("id", "")
        if not dl_id:
            return "Missing id", 400
        try:
            data = _decode_download_id(dl_id)
        except Exception:
            return "Invalid id", 400

        stub = {
            "weeb-cli": True,
            "episode_url": data.get("episode_url", ""),
            "anime_id": data.get("anime_id", ""),
            "sonarr_title": data.get("sonarr_title", ""),
            "season": data["season"],
            "episode": data["episode"],
            "release_name": data.get("release_name", ""),
            "created_at": time.time(),
        }

        wd = Path(watch_dir)
        wd.mkdir(parents=True, exist_ok=True)
        stub_name = f"{data.get('release_name', 'download')}.torrent"
        stub_path = wd / stub_name
        with open(stub_path, "w") as f:
            json.dump(stub, f)
        log.info(f"Created stub: {stub_path}")

        torrent_bytes = json.dumps(stub).encode()
        return Response(
            torrent_bytes,
            mimetype="application/x-bittorrent",
            headers={"Content-Disposition": f"attachment; filename={stub_name}"},
        )

    # Blackhole worker
    def blackhole_worker():
        log.info(f"Blackhole worker started (watch={watch_dir}, completed={completed_dir})")
        watch = Path(watch_dir)
        completed = Path(completed_dir)
        watch.mkdir(parents=True, exist_ok=True)
        completed.mkdir(parents=True, exist_ok=True)

        while True:
            try:
                for failed_file in watch.glob("*.failed"):
                    try:
                        age = time.time() - failed_file.stat().st_mtime
                        if age > 300:
                            retried = failed_file.with_suffix(".torrent")
                            failed_file.rename(retried)
                            log.info(f"Retrying: {retried.name}")
                    except Exception:
                        pass

                for stub_file in watch.glob("*.torrent"):
                    try:
                        with open(stub_file) as f:
                            stub = json.load(f)
                        if not stub.get("weeb-cli"):
                            continue

                        episode_url = stub.get("episode_url", "")
                        anime_id = stub.get("anime_id", "")
                        s_title = stub.get("sonarr_title", "")
                        s = stub["season"]
                        ep_num = stub["episode"]
                        release_name = stub.get("release_name", "")
                        log.info(f"Processing stub: {release_name}")

                        # Primary provider
                        primary_streams = primary.get_streams(anime_id, episode_url)
                        success = _try_streams(primary_streams, s_title, s, ep_num, str(completed))

                        # Fallback providers
                        if not success and fallbacks:
                            log.info(f"Primary failed, trying fallback providers...")
                            fb_streams = _get_fallback_streams(fallbacks, s_title, s, ep_num)
                            success = _try_streams(fb_streams, s_title, s, ep_num, str(completed))

                        if success:
                            stub_file.unlink(missing_ok=True)
                            log.info(f"Completed: {release_name}")
                        else:
                            stub_file.rename(stub_file.with_suffix(".failed"))
                            log.error(f"Failed: {release_name}")

                    except Exception as e:
                        log.error(f"Error processing {stub_file.name}: {e}")
                        try:
                            stub_file.rename(stub_file.with_suffix(".failed"))
                        except Exception:
                            pass

            except Exception as e:
                log.error(f"Blackhole worker error: {e}")

            time.sleep(poll_interval)

    log.info("weeb-cli serve starting")
    log.info(f"  Port: {port}")
    log.info(f"  Watch dir: {watch_dir}")
    log.info(f"  Completed dir: {completed_dir}")

    worker = threading.Thread(target=blackhole_worker, daemon=True)
    worker.start()

    flask_app.run(host="0.0.0.0", port=port, debug=False)
