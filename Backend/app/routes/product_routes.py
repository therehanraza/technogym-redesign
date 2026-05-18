from fastapi import APIRouter, HTTPException

from app.db import store
from app.schemas.product_schema import ProductCreate, ProductUpdate

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("")
def get_products(
    category: str | None = None,
    search: str | None = None,
    featured: bool | None = None
):
    data = store.get_products(category=category, search=search, featured=featured)
    return {"success": True, "count": len(data), "data": data}


@router.get("/{slug}")
def get_product_by_slug(slug: str):
    product = store.get_product_by_slug(slug)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "data": product}


@router.post("")
def create_product(payload: ProductCreate):
    data = payload.model_dump()
    try:
        product = store.create_product(data)
    except Exception as exc:
        if "UNIQUE" in str(exc) or "duplicate" in str(exc).lower():
            raise HTTPException(status_code=409, detail="Product slug already exists")
        raise
    return {"success": True, "data": product}


@router.put("/{product_id}")
def update_product(product_id: str, payload: ProductUpdate):
    update_data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields supplied")
    product = store.update_product(product_id, update_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"success": True, "data": product}


@router.delete("/{product_id}")
def delete_product(product_id: str):
    disabled = store.disable_product(product_id)
    if not disabled:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"success": True, "message": "Product disabled successfully"}
