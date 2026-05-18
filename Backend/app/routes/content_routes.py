from fastapi import APIRouter, HTTPException

from app.db import store

router = APIRouter(tags=["Content"])


@router.get("/navigation")
def get_navigation():
    data = store.get_navigation()
    return {"success": True, "count": len(data), "data": data}


@router.get("/pages")
def get_pages():
    data = store.get_pages()
    return {"success": True, "count": len(data), "data": data}


@router.get("/pages/{page_path:path}")
def get_page(page_path: str):
    data = store.get_page_by_path(page_path)
    if not data:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"success": True, "data": data}
