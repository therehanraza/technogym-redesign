from fastapi import APIRouter, HTTPException, Query

from app.db import store

router = APIRouter(tags=["Content"])


@router.get("/navigation")
def get_navigation():
    data = store.get_navigation()
    return {"success": True, "count": len(data), "data": data}


@router.get("/site")
def get_site_content():
    pages = store.get_pages()
    categories = store.get_categories()
    products = store.get_products()
    navigation = store.get_navigation()
    return {
        "success": True,
        "data": {
            "navigation": navigation,
            "pages": pages,
            "categories": categories,
            "products": products,
        },
    }


@router.get("/pages")
def get_pages():
    data = store.get_pages()
    return {"success": True, "count": len(data), "data": data}


@router.get("/page")
def get_page_by_query(path: str = Query("/", min_length=1)):
    data = store.get_page_by_path(path)
    if not data:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"success": True, "data": data}


@router.get("/pages/{page_path:path}")
def get_page(page_path: str):
    data = store.get_page_by_path(page_path)
    if not data:
        raise HTTPException(status_code=404, detail="Page not found")
    return {"success": True, "data": data}
