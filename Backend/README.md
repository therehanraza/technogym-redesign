# Technogym FastAPI Backend

Python backend for the Technogym redesign. It uses FastAPI with MongoDB Atlas for deployed persistent data, while keeping SQLite as a local fallback when `MONGODB_URI` is not configured.

## Run Locally

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## Environment

Copy `.env.example` to `.env` and adjust values:

```env
FRONTEND_URL=http://localhost:5173
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/technogym_redesign?retryWrites=true&w=majority
MONGODB_DB_NAME=technogym_redesign
```

If `MONGODB_URI` is empty, the backend uses local SQLite at `data/technogym.db`.

## Endpoints

- `GET /api/health`
- `GET /api/site`
- `GET /api/navigation`
- `GET /api/page?path=/`
- `GET /api/pages`
- `GET /api/pages/{path}`
- `GET /api/categories`
- `GET /api/categories/{slug}`
- `GET /api/products`
- `GET /api/products/{slug}`
- `POST /api/inquiries`
- `POST /api/orders`

Full docs are available at `/docs` while the server is running.
