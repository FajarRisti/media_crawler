# Media Crawler

Media content crawler/scraper project.

## Setup
1. `cd /Users/mac/Desktop/users/media_crawler`
2. `pip install -r requirements.txt` (create venv first: `python -m venv venv && source venv/bin/activate`)

## Run with Postgres
1. Start DB: `docker compose up -d`
2. Install new deps: `source venv/bin/activate && pip install -r requirements.txt`
3. Run migrations: `alembic upgrade head`
python main.py

**Web UI:**
pip install flask
python app.py
open http://localhost:5000
- Run crawler from UI
- View results live
- Clear data

Note: Edit alembic.ini sqlalchemy.url to match your .env

## Collaboration
1. Create GitHub repo: https://github.com/new - name 'media-crawler' (public/private)
2. Add remote: `git remote add origin https://github.com/YOUR_USERNAME/media-crawler.git`
3. First commit/push: `git add . && git commit -m "Initial commit" && git push -u origin main`
4. Invite friend as collaborator in GitHub repo settings.
5. Friend clones: `git clone https://github.com/YOUR_USERNAME/media-crawler.git`

Rename branch to main if needed: `git branch -m master main`

