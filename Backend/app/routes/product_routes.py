import json

from fastapi import APIRouter, HTTPException

from app.db.sqlite import get_connection, row_to_dict
from app.schemas.product_schema import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
def get_products(
    category: str | None = None,
    search: str | None = None,
    featured: bool | None = None
):
    clauses = ["isActive = 1"]
    params = []
    if category:
        clauses.append("LOWER(category) LIKE ?")
        params.append(f"%{category.lower()}%")
    if featured is not None:
        clauses.append("isFeatured = ?")
        params.append(int(featured))
    if search:
        clauses.append("(LOWER(name) LIKE ? OR LOWER(category) LIKE ? OR LOWER(description) LIKE ?)")
        value = f"%{search.lower()}%"
        params.extend([value, value, value])
    sql = f"SELECT * FROM products WHERE {' AND '.join(clauses)} ORDER BY createdAt DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    data = [row_to_dict(row) for row in rows]
    return {"success": True, "count": len(data), "data": data}


@router.get("/{slug}")
def get_product_by_slug(slug: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM products WHERE slug = ? AND isActive = 1", (slug,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "data": row_to_dict(row)}


@router.post("")
def create_product(payload: ProductCreate):
    data = payload.model_dump()
    try:
        with get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO products
                (name, slug, category, price, numericPrice, tag, description, shortDescription, image, specs, isFeatured, isActive)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data["name"], data["slug"], data["category"], data["price"], data["numericPrice"],
                    data["tag"], data["description"], data["shortDescription"], data["image"],
                    json.dumps(data["specs"]), int(data["isFeatured"]), int(data["isActive"]),
                ),
            )
            row = conn.execute("SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)).fetchone()
    except Exception as exc:
        if "UNIQUE" in str(exc):
            raise HTTPException(status_code=409, detail="Product slug already exists")
        raise
    return {"success": True, "data": row_to_dict(row)}


@router.put("/{product_id}")
def update_product(product_id: str, payload: ProductUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields supplied")
    if "specs" in update_data:
        update_data["specs"] = json.dumps(update_data["specs"])
    fields = ", ".join([f"{key} = ?" for key in update_data])
    with get_connection() as conn:
        result = conn.execute(f"UPDATE products SET {fields} WHERE id = ?", [*update_data.values(), product_id])
        row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "data": row_to_dict(row)}


@router.delete("/{product_id}")
def delete_product(product_id: str):
    with get_connection() as conn:
        result = conn.execute("UPDATE products SET isActive = 0 WHERE id = ?", (product_id,))
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"success": True, "message": "Product disabled successfully"}
