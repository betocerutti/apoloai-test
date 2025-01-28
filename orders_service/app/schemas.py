from pydantic import BaseModel
from typing import List
from datetime import datetime

class ProductOrderItem(BaseModel):
    id: int  # Product ID
    quantity: int

class OrderCreate(BaseModel):
    products: List[ProductOrderItem]

class OrderUpdate(BaseModel):
    products: List[ProductOrderItem]

class Order(BaseModel):
    id: int # Order ID
    products: List[ProductOrderItem]
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True