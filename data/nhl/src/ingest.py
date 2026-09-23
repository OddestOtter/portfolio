import argparse
import gzip
import json
import time
from datetime import datetime, timezone
from importlib.metadata import version
from pathlib import Path

from nhlpy import NHLClient
from tenacity import retry, stop_after_attempt, wait_exponential

LANDING = Path("data/landing")
SLEEP = 0.5
FINAL_STATES = {"OFF", "FINAL"}     # finished games; verify against your inspection output
GAME_TYPES = {2, 3}                 # regular season, playoffs
CLIENT_VERSION = version("nhl-api-py")

client = NHLClient(timeout=30)

# endpoint name -> function that takes a game id
GAME_ENDPOINTS = {
    "boxscore": lambda gid: client.game_center.boxscore(game_id=gid),
    "play_by_play": lambda gid: client.game_center.play_by_play(game_id=gid),
    "shift_chart": lambda gid: client.game_center.shift_chart_data(game_id=gid),
}


@retry(stop=stop_after_attempt(5), wait=wait_exponential(min=1, max=30), reraise=True)
def _call(fn, **kwargs):
    return fn(**kwargs)


def fetch_and_land(path: Path, meta: dict, fn, **kwargs):
    """Call the API, then write an envelope atomically. Returns the payload."""
    payload = _call(fn, **kwargs)
    envelope = {
        **meta,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "client_version": CLIENT_VERSION,
        "payload": payload,                          # untouched
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + ".tmp")
    with gzip.open(tmp, "wt") as f:
        json.dump(envelope, f, default=str)
    tmp.rename(path)                                 # no half-written files
    time.sleep(SLEEP)
    return payload


def read_payload(path: Path):
    with gzip.open(path, "rt") as f:
        return json.load(f)["payload"]


def team_abbrs() -> list[str]:
    teams = _call(client.teams.teams)
    return sorted({t.get("abbr") or t.get("triCode") for t in teams})


def final_game_ids(season: str, refresh: bool = False) -> list[int]:
    """Union of every team's season schedule, filtered to finished games."""
    ids = set()
    for abbr in team_abbrs():
        path = LANDING / "schedule" / f"season={season}" / f"{abbr}.json.gz"
        if path.exists() and not refresh:
            payload = read_payload(path)
        else:
            payload = fetch_and_land(
                path, {"team": abbr, "season": season},
                client.schedule.team_season_schedule,
                team_abbr=abbr, season=season,
            )
        for g in payload.get("games", []):
            if g.get("gameState") in FINAL_STATES and g.get("gameType") in GAME_TYPES:
                ids.add(g["id"])
    return sorted(ids)


def ingest_season(season: str, limit: int | None = None, refresh_schedule: bool = False):
    ids = final_game_ids(season, refresh_schedule)
    if limit:
        ids = ids[:limit]
    print(f"{season}: {len(ids)} final games")

    landed = failed = 0
    for gid in ids:
        for name, fn in GAME_ENDPOINTS.items():
            path = LANDING / name / f"season={season}" / f"{gid}.json.gz"
            if path.exists():
                continue                             # cache hit, no API call
            try:
                fetch_and_land(path, {"game_id": gid, "season": season,
                                      "endpoint": name}, fn, gid=gid)
                landed += 1
            except Exception as e:
                failed += 1
                print(f"FAILED {name} {gid}: {e}")   # rerun picks up the gaps
    print(f"{season}: landed {landed} new files, {failed} failures")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("seasons", nargs="+", help="e.g. 20242025")
    ap.add_argument("--limit", type=int, help="only the first N games per season")
    ap.add_argument("--refresh-schedule", action="store_true",
                    help="re-fetch schedules (use for the in-progress season)")
    args = ap.parse_args()
    for s in args.seasons:
        ingest_season(s, args.limit, args.refresh_schedule)