from fastapi import APIRouter, HTTPException

from app.db.sqlite import get_connection, row_to_dict
from app.schemas.inquiry_schema import InquiryCreate, InquiryStatusUpdate

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("")
def create_inquiry(payload: InquiryCreate):
    data = payload.model_dump()
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO inquiries (fullName, emailOrPhone, requirementType, message, status)
            VALUES (?, ?, ?, ?, 'NEW')
            """,
            (data["fullName"], data["emailOrPhone"], data["requirementType"], data.get("message", "")),
        )
        row = conn.execute("SELECT * FROM inquiries WHERE id = ?", (cursor.lastrowid,)).fetchone()

    return {
        "success": True,
        "message": "Inquiry submitted successfully",
        "data": row_to_dict(row)
    }


@router.get("")
def get_inquiries():
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM inquiries ORDER BY createdAt DESC").fetchall()
    data = [row_to_dict(row) for row in rows]
    return {"success": True, "count": len(data), "data": data}


@router.patch("/{inquiry_id}/status")
def update_inquiry_status(inquiry_id: str, payload: InquiryStatusUpdate):
    if payload.status not in ["NEW", "IN_PROGRESS", "CLOSED"]:
        raise HTTPException(status_code=400, detail="Invalid inquiry status")

    with get_connection() as conn:
        result = conn.execute("UPDATE inquiries SET status = ? WHERE id = ?", (payload.status, inquiry_id))
        row = conn.execute("SELECT * FROM inquiries WHERE id = ?", (inquiry_id,)).fetchone()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    return {"success": True, "data": row_to_dict(row)}
