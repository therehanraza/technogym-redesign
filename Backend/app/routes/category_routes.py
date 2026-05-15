from fastapi import APIRouter, HTTPException

from app.db.sqlite import get_connection, row_to_dict
from app.schemas.category_schema import CategoryCreate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("")
def get_categories():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM categories WHERE isActive = 1 ORDER BY name").fetchall()
    data = [row_to_dict(row) for row in rows]
    return {"success": True, "count": len(data), "data": data}


@router.get("/{slug}")
def get_category_by_slug(slug: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM categories WHERE slug = ? AND isActive = 1", (slug,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "data": row_to_dict(row)}


@router.post("")
def create_category(payload: CategoryCreate):
    data = payload.model_dump()
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                "INSERT INTO categories (name, slug, description, image, isActive) VALUES (?, ?, ?, ?, ?)",
                (data["name"], data["slug"], data.get("description", ""), data.get("image", ""), int(data.get("isActive", True))),
            )
            row = conn.execute("SELECT * FROM categories WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except Exception as exc:
        if "UNIQUE" in str(exc):
            raise HTTPException(status_code=409, detail="Category slug already exists")
        raise
    return {"success": True, "data": row_to_dict(row)}
