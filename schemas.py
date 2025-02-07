from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True  # Fix incorrect 'from_attribute' typo

# Category Schemas
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        from_attributes = True

# Product Schemas
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int
    category_id: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: int

    class Config:
        from_attributes = True

# Cart Schemas
class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemResponse(BaseModel):
    id: int  # Added missing ID field
    product: ProductResponse
    quantity: int

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    cart_items: List[CartItemResponse]
    total_price: float

    class Config:
        from_attributes = True

# Order Schemas
class OrderItemResponse(BaseModel):
    id: int  # Added missing ID field
    product: ProductResponse
    quantity: int
    unit_price: float

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total_amount: float
    created_at: datetime
    items: List[OrderItemResponse]

    class Config:
        from_attributes = True
