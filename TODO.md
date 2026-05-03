# Media Crawler TODO

## Setup Postgres
- [ ] docker compose up -d (start DB)
- [ ] source venv/bin/activate && pip install -r requirements.txt (install SQL deps)
- [ ] alembic upgrade head (run migrations)

## Test
- [ ] python main.py (save to DB)

## Development
- Implement real crawling (YouTube/Twitter/Instagram)
- Add async (aiohttp)
- Scheduler (APScheduler)
- API endpoints (FastAPI)
- Friend collab

## Deploy
- Dockerize app
- Railway/Render for Postgres + app

