# Docker Compose

This setup runs the local MVP as separate services:

- `frontend`: Astro static build served by Nginx
- `backend`: FastAPI API
- `worker`: hourly RSS fetch process
- `postgres`: PostgreSQL database
- `redis`: cache/job/lock service reserved for the next phases

## Run

From the project root:

```bash
cp .env.example .env
cp sources.example.yaml sources.yaml
docker compose up --build
```

Open the frontend:

```text
http://127.0.0.1:4321
```

Check the backend:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/articles
```

Run a manual fetch:

```bash
curl -X POST http://127.0.0.1:8000/api/fetch/run
```

## Stop

```bash
docker compose down
```

To remove the PostgreSQL volume too:

```bash
docker compose down -v
```
