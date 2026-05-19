from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.store import init_storage, using_mongo
from app.routes.category_routes import router as category_router
from app.routes.content_routes import router as content_router
from app.routes.product_routes import router as product_router
from app.routes.inquiry_routes import router as inquiry_router
from app.routes.order_routes import router as order_router

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Python FastAPI backend for the Technogym website redesign"
)

allowed_origins = [
    settings.FRONTEND_URL,
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:4173",
    "http://127.0.0.1:4173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup_event():
    init_storage()


@app.get("/api/health", tags=["Health"])
def health_check():
    return {
        "success": True,
        "message": "Technogym Python backend is running",
        "database": "mongodb" if using_mongo() else "sqlite"
    }


app.include_router(category_router, prefix="/api")
app.include_router(content_router, prefix="/api")
app.include_router(product_router, prefix="/api")
app.include_router(inquiry_router, prefix="/api")
app.include_router(order_router, prefix="/api")
