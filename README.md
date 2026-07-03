# fe-brief

`fe-brief` is a small DevOps portfolio project: a local news aggregator that collects articles from configured sources and shows them in chronological order.

![dashboard](/docs/images/dashboard.png)

The goal is not to build a complex product. The goal is to demonstrate an end-to-end DevOps workflow:

1. Build a simple local application.
2. Containerize it with Docker.
3. Publish images to a container registry.
4. Deploy it on a VPS (AWS EC2 Istance).
5. Move the deployment to Kubernetes.
6. Add CI/CD practices.
7. Document the process as a portfolio project.

## MVP

The first version will show local city news only.

Each article will contain:

- title
- source
- publication date
- short description
- link to the original source

The MVP will not include login, favorites, read/unread state, social features, or categories.

## Stack

- Frontend: Astro
- Backend API: Python FastAPI
- Worker: Python
- Database: PostgreSQL
- Cache/job/lock: Redis
- Source configuration: `sources.yaml`
- Local development: Docker Compose
- VPS deployment: Docker Compose and reverse proxy
- Kubernetes deployment: manifests or Helm chart
- CI/CD: GitHub Actions or GitLab CI

## Initial Repository Structure

```text
fe-brief/
├── backend/
├── frontend/
├── worker/
├── deploy/
│   ├── docker/
│   └── kubernetes/
├── docs/
├── .env.example
├── .gitignore
├── README.md
└── sources.example.yaml
```

## Local Configuration

Copy the example files when starting local development:

```bash
cp .env.example .env
cp sources.example.yaml sources.yaml
```

The real `.env` and `sources.yaml` files are ignored by Git because they can contain local configuration or private source details.

## Roadmap

- [x] Fase 0: define repository structure and starter files.
- [x] Fase 1: create FastAPI backend with health, article list, and manual fetch endpoints.
- [x] Fase 2: parse RSS/feed sources, save articles in PostgreSQL, deduplicate by URL hash.
- [x] Fase 3: create Astro frontend with chronological article list.
- [x] Fase 4: create Python worker that fetches sources every hour.
- [x] Fase 5: add Dockerfiles and Docker Compose.
- [x] Fase 6: add CI build/test pipeline.
- [x] Fase 7: publish images to a registry.
- [x] Fase 8: deploy to a VPS with Docker Compose and reverse proxy.
- [ ] Fase 9: add CI/CD deployment to VPS.
- [ ] Fase 10: deploy to Kubernetes.
- [ ] Fase 11: add Kubernetes rollout and rollback workflow.
- [ ] Fase 12: write portfolio documentation.
