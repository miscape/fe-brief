from contextlib import asynccontextmanager
import os

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import create_db_tables, get_db
from app.fetch_service import run_fetch_cycle
from app.repository import article_to_dict, list_articles as list_saved_articles


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_tables()
    yield


app = FastAPI(title="fe-brief API", lifespan=lifespan)

cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:4321,http://127.0.0.1:4321",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
        result = run_fetch_cycle(db)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=500, detail=str(error)) from error

    return {
        "status": "completed",
        "sources": result["sources"],
        "fetched_articles": result["fetched_articles"],
        "saved_articles": result["saved_articles"],
        "errors": result["errors"],
    }
