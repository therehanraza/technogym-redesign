from pydantic import BaseModel, Field
from typing import Optional


class InquiryCreate(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=80)
    emailOrPhone: str = Field(..., min_length=5, max_length=120)
    requirementType: str = "Home Gym"
    message: Optional[str] = Field(default="", max_length=1200)


class InquiryStatusUpdate(BaseModel):
    status: str
