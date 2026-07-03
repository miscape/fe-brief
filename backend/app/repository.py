from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Article


def _parse_datetime(value: str) -> datetime:
    return datetime.fromisoformat(value)


def save_articles(db: Session, articles: list[dict[str, str]]) -> int:
    saved = 0

    for article in articles:
        article_id = article["id"]
        existing_article = db.get(Article, article_id)

        if existing_article:
            continue

        db.add(
            Article(
                id=article_id,
                title=article["title"],
                source=article["source"],
                published_at=_parse_datetime(article["published_at"]),
                description=article["description"],
                url=article["url"],
            )
        )
        saved += 1

    db.commit()
    return saved


def list_articles(db: Session, limit: int = 100) -> list[Article]:
    statement = (
        select(Article)
        .order_by(Article.published_at.desc())
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def article_to_dict(article: Article) -> dict[str, str]:
    return {
        "id": article.id,
        "title": article.title,
        "source": article.source,
        "published_at": article.published_at.isoformat(),
        "description": article.description,
        "url": article.url,
    }
