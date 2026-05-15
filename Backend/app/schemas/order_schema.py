from pydantic import BaseModel, Field
from typing import List, Optional


class OrderItem(BaseModel):
    productId: Optional[str] = None
    name: str = Field(..., min_length=1)
    slug: str = Field(..., min_length=1)
    price: str = Field(..., min_length=1)
    quantity: int = Field(default=1, ge=1, le=25)


class Customer(BaseModel):
    fullName: str = Field(..., min_length=2, max_length=80)
    emailOrPhone: str = Field(..., min_length=5, max_length=120)
    address: Optional[str] = Field(default="", max_length=300)


class OrderCreate(BaseModel):
    customer: Customer
    items: List[OrderItem] = Field(..., min_length=1)
    notes: Optional[str] = Field(default="", max_length=1200)


class OrderStatusUpdate(BaseModel):
    status: str
