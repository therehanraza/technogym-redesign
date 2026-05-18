from fastapi import APIRouter, HTTPException

from app.db import store
from app.schemas.category_schema import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
def get_categories():
    data = store.get_categories()
    return {"success": True, "count": len(data), "data": data}


@router.get("/{slug}")
def get_category_by_slug(slug: str):
    category = store.get_category_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "data": category}


@router.post("")
def create_category(payload: CategoryCreate):
    data = payload.model_dump()
    try:
        category = store.create_category(data)
    except Exception as exc:
        if "UNIQUE" in str(exc) or "duplicate" in str(exc).lower():
            raise HTTPException(status_code=409, detail="Category slug already exists")
        raise
    return {"success": True, "data": category}
