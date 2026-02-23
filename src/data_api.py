from pathlib import Path
from datetime import datetime
import requests
import json


FPL_BOOTSTRAP_URL = "https://fantasy.premierleague.com/api/bootstrap-static/"


def get_project_root() -> Path:
    """
    Return the project root folder (one level above src/).
    """
    return Path(__file__).resolve().parents[1]


def cache_path(filename: str) -> Path:
    """
    Build a path inside data/cache/ for cached files.
    """
    root = get_project_root()
    cache_dir = root / "data" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / filename


def load_cached_json(path: Path, ttl_seconds: int) -> dict | None:
    """
    Load JSON from cache if file exists and is not older than ttl_seconds.
    """
    if not path.exists():
        return None

    modified_time = datetime.fromtimestamp(path.stat().st_mtime)
    age_seconds = (datetime.now() - modified_time).total_seconds()

    if age_seconds > ttl_seconds:
        return None

    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: dict) -> None:
    """
    Save dictionary as JSON to a file.
    """
    path.write_text(json.dumps(data), encoding="utf-8")


def fetch_bootstrap_static(ttl_seconds: int = 3600) -> dict:
    """
    Fetch FPL bootstrap-static data with caching.

    Args:
        ttl_seconds: how long cached data is considered valid.

    Returns:
        dict: API JSON data
    """
    path = cache_path("bootstrap_static.json")

    cached = load_cached_json(path, ttl_seconds)
    if cached is not None:
        return cached

    response = requests.get(FPL_BOOTSTRAP_URL)
    response.raise_for_status()

    data = response.json()
    save_json(path, data)
    return data