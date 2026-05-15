from pydantic import BaseModel, Field
from typing import Optional


class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: Optional[str] = ""
    image: Optional[str] = ""
    isActive: bool = True


class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    image: Optional[str] = None
    isActive: Optional[bool] = None
