from fastapi import APIRouter, HTTPException

from app.db import store
from app.schemas.order_schema import OrderCreate, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("")
def create_order(payload: OrderCreate):
    data = payload.model_dump()
    order = store.create_order(data)

    return {
        "success": True,
        "message": "Order created successfully",
        "data": order
    }


@router.get("")
def get_orders():
    data = store.get_orders()
    return {"success": True, "count": len(data), "data": data}


@router.get("/{order_id}")
def get_order_by_id(order_id: str):
    order = store.get_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"success": True, "data": order}


@router.patch("/{order_id}/status")
def update_order_status(order_id: str, payload: OrderStatusUpdate):
    allowed = ["CREATED", "CONFIRMED", "DISPATCHED", "DELIVERED", "CANCELLED"]

    if payload.status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid order status")

    order = store.update_order_status(order_id, payload.status)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"success": True, "data": order}
