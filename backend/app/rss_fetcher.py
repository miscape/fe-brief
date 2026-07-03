from datetime import UTC, datetime
from hashlib import sha256
from typing import Any

import feedparser


def _parse_entry_datetime(entry: Any) -> datetime:
    parsed_date = entry.get("published_parsed") or entry.get("updated_parsed")

    if parsed_date:
        return datetime(*parsed_date[:6], tzinfo=UTC)

    return datetime.now(tz=UTC)


def _article_from_entry(source_name: str, entry: Any) -> dict[str, str]:
    link = entry.get("link", "")
    published_at = _parse_entry_datetime(entry)

    return {
        "id": sha256(link.encode("utf-8")).hexdigest(),
        "title": entry.get("title", "Untitled"),
        "source": source_name,
        "published_at": published_at.isoformat(),
        "description": entry.get("summary", ""),
        "url": link,
    }


def fetch_articles_from_sources(
    sources: list[dict[str, Any]],
) -> dict[str, list[dict[str, str]]]:
    articles_by_url: dict[str, dict[str, str]] = {}
    errors: list[dict[str, str]] = []

    for source in sources:
        source_name = source.get("name", "unknown")
        source_url = source.get("url")

        if not source_url:
            errors.append({"source": source_name, "error": "Missing source URL"})
            continue

        feed = feedparser.parse(source_url)

        if feed.bozo:
            errors.append({"source": source_name, "error": str(feed.bozo_exception)})

        for entry in feed.entries:
            article = _article_from_entry(source_name, entry)

            if article["url"]:
                articles_by_url[article["url"]] = article

    articles = sorted(
        articles_by_url.values(),
        key=lambda article: article["published_at"],
        reverse=True,
    )

    return {
        "articles": articles,
        "errors": errors,
    }
