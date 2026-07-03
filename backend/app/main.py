from fastapi import FastAPI

app = FastAPI(title="fe-brief API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/articles")
def list_articles():
    return {
        "articles": []
    }


@app.post("/api/fetch/run")
def run_fetch():
    return {
        "status": "accepted",
        "message": "Manual fetch will be implemented in the next phase"
    }
