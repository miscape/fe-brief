from fastapi import FastAPI, HTTPException

from app.config import load_sources
from app.rss_fetcher import fetch_articles_from_sources

app = FastAPI(title="fe-brief API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/articles")
def list_articles():
    try:
        sources = load_sources()
        result = fetch_articles_from_sources(sources)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "count": len(result["articles"]),
        "articles": result["articles"],
        "errors": result["errors"],
    }


@app.post("/api/fetch/run")
def run_fetch():
    try:
        sources = load_sources()
        result = fetch_articles_from_sources(sources)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "status": "completed",
        "sources": len(sources),
        "articles": len(result["articles"]),
        "errors": result["errors"],
    }
