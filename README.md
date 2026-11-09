# StudyDeck

Local study todo and attendance app using Python 3.12, FastAPI, SQLite, and static HTML/CSS/JavaScript. Users are distinguished by a nickname stored in browser localStorage. There is no login or signup.

## Install and run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Open http://127.0.0.1:8080.

## Test

```powershell
python -m pytest -p no:cacheprovider -q
```

## Docker

```powershell
docker build -t studydeck .
docker run --rm -p 8080:8080 studydeck
```

The SQLite database is stored at `/app/data/studydeck.db` inside the container. It is ephemeral: deleting the container deletes the data. Mount `/app/data` to persist it.

No AI or large model is used, so no model preparation is required.

## GitHub Actions and Docker Hub

Pull requests run pytest, build the image, and start the container for endpoint checks. Pushes to `main` publish `DOCKERHUB_USERNAME/studydeck:latest` and `DOCKERHUB_USERNAME/studydeck:<commit-sha>` after all checks pass. Configure the GitHub Actions secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`.
