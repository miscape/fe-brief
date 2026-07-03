from sqlalchemy.orm import Session

from app.config import load_sources
from app.repository import save_articles
from app.rss_fetcher import fetch_articles_from_sources


def run_fetch_cycle(db: Session) -> dict[str, object]:
    sources = load_sources()
    result = fetch_articles_from_sources(sources)
    saved = save_articles(db, result["articles"])

    return {
        "sources": len(sources),
        "fetched_articles": len(result["articles"]),
        "saved_articles": saved,
        "errors": result["errors"],
    }
