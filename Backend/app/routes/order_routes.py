import json

from fastapi import APIRouter, HTTPException

from app.db.sqlite import get_connection, row_to_dict
from app.schemas.order_schema import OrderCreate, OrderStatusUpdate

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("")
def create_order(payload: OrderCreate):
    data = payload.model_dump()
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO orders (customer, items, notes, status) VALUES (?, ?, ?, 'CREATED')",
            (json.dumps(data["customer"]), json.dumps(data["items"]), data.get("notes", "")),
        )
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (cursor.lastrowid,)).fetchone()
    order = row_to_dict(row)
    order["customer"] = json.loads(order["customer"])
    order["items"] = json.loads(order["items"])

    return {
        "success": True,
        "message": "Order created successfully",
        "data": order
    }


@router.get("")
def get_orders():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM orders ORDER BY createdAt DESC").fetchall()
    data = []
    for row in rows:
        order = row_to_dict(row)
        order["customer"] = json.loads(order["customer"])
        order["items"] = json.loads(order["items"])
        data.append(order)
    return {"success": True, "count": len(data), "data": data}


@router.get("/{order_id}")
def get_order_by_id(order_id: str):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Order not found")
    order = row_to_dict(row)
    order["customer"] = json.loads(order["customer"])
    order["items"] = json.loads(order["items"])
    return {"success": True, "data": order}


@router.patch("/{order_id}/status")
def update_order_status(order_id: str, payload: OrderStatusUpdate):
    allowed = ["CREATED", "CONFIRMED", "DISPATCHED", "DELIVERED", "CANCELLED"]

    if payload.status not in allowed:
        raise HTTPException(status_code=400, detail="Invalid order status")

    with get_connection() as conn:
        result = conn.execute("UPDATE orders SET status = ? WHERE id = ?", (payload.status, order_id))
        row = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Order not found")
    order = row_to_dict(row)
    order["customer"] = json.loads(order["customer"])
    order["items"] = json.loads(order["items"])
    return {"success": True, "data": order}
