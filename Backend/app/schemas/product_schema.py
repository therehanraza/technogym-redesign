from pydantic import BaseModel, Field
from typing import List, Optional


class ProductCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    slug: str = Field(..., min_length=2, max_length=140)
    category: str = Field(..., min_length=2, max_length=80)
    price: str = "Request price"
    numericPrice: int = Field(default=0, ge=0)
    tag: str = ""
    description: str = Field(..., min_length=10)
    shortDescription: str = ""
    image: str = Field(..., min_length=8)
    gallery: List[str] = Field(default_factory=list)
    specs: List[str] = Field(default_factory=list)
    features: List[str] = Field(default_factory=list)
    stock: int = Field(default=0, ge=0)
    isFeatured: bool = False
    isActive: bool = True


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    category: Optional[str] = None
    price: Optional[str] = None
    numericPrice: Optional[int] = None
    tag: Optional[str] = None
    description: Optional[str] = None
    shortDescription: Optional[str] = None
    image: Optional[str] = None
    gallery: Optional[List[str]] = None
    specs: Optional[List[str]] = None
    features: Optional[List[str]] = None
    stock: Optional[int] = None
    isFeatured: Optional[bool] = None
    isActive: Optional[bool] = None
