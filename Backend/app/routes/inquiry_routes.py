from fastapi import APIRouter, HTTPException

from app.db import store
from app.schemas.inquiry_schema import InquiryCreate, InquiryStatusUpdate

router = APIRouter(prefix="/inquiries", tags=["Inquiries"])


@router.post("")
def create_inquiry(payload: InquiryCreate):
    data = payload.model_dump()
    inquiry = store.create_inquiry(data)

    return {
        "success": True,
        "message": "Inquiry submitted successfully",
        "data": inquiry
    }


@router.get("")
def get_inquiries():
    data = store.get_inquiries()
    return {"success": True, "count": len(data), "data": data}


@router.patch("/{inquiry_id}/status")
def update_inquiry_status(inquiry_id: str, payload: InquiryStatusUpdate):
    if payload.status not in ["NEW", "IN_PROGRESS", "CLOSED"]:
        raise HTTPException(status_code=400, detail="Invalid inquiry status")

    inquiry = store.update_inquiry_status(inquiry_id, payload.status)
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")

    return {"success": True, "data": inquiry}
