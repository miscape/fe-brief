import os
from pathlib import Path
from typing import Any

import yaml


def resolve_sources_path() -> Path:
    configured_path = Path(os.getenv("SOURCES_FILE", "sources.yaml"))

    if configured_path.is_absolute():
        return configured_path

    candidates = [
        Path.cwd() / configured_path,
        Path.cwd().parent / configured_path,
    ]

    for candidate in candidates:
        if candidate.exists():
            return candidate

    return candidates[0]


def load_sources() -> list[dict[str, Any]]:
    sources_path = resolve_sources_path()

    if not sources_path.exists():
        raise FileNotFoundError(f"Sources file not found: {sources_path}")

    with sources_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}

    sources = data.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("sources.yaml must contain a 'sources' list")

    return [
        source
        for source in sources
        if source.get("enabled", True) and source.get("type") == "rss"
    ]
