# Technogym FastAPI Backend

Python backend for the Technogym redesign. It uses FastAPI and SQLite so the project can run locally and deploy on free hosting without paid services.

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

The SQLite database is created and seeded automatically at startup.

## Environment

Copy `.env.example` to `.env` and adjust values:

```env
FRONTEND_URL=http://localhost:5173
DATABASE_URL=sqlite:///./data/technogym.db
```

## Endpoints

- `GET /api/health`
- `GET /api/categories`
- `GET /api/products`
- `POST /api/inquiries`
- `POST /api/orders`

Full docs are available at `/docs` while the server is running.
