from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app.config import load_sources
from app.database import create_db_tables, get_db
from app.repository import article_to_dict, list_articles as list_saved_articles
from app.repository import save_articles
from app.rss_fetcher import fetch_articles_from_sources


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(title="fe-brief API", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/articles")
def list_articles(db: Session = Depends(get_db)):
    articles = list_saved_articles(db)

    return {
        "count": len(articles),
        "articles": [article_to_dict(article) for article in articles],
    }


@app.post("/api/fetch/run")
def run_fetch(db: Session = Depends(get_db)):
    try:
        sources = load_sources()
        result = fetch_articles_from_sources(sources)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    saved = save_articles(db, result["articles"])

    return {
        "status": "completed",
        "sources": len(sources),
        "fetched_articles": len(result["articles"]),
        "saved_articles": saved,
        "errors": result["errors"],
    }
