# Worker

The worker is a separate Python process that fetches RSS sources and saves articles in PostgreSQL.

For local development, run it manually from the project root:

```bash
cd fe-brief
source backend/.venv/bin/activate
python worker/run.py
```

To run it continuously every hour:

```bash
python worker/run.py --loop --interval 3600
```

For now the worker reuses the backend dependencies and code. Later it will become its own Docker service.
