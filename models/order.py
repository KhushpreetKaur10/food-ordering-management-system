from dataclasses import dataclass, field
from typing import List

@dataclass
class OrderItem:
    product_id: str
    name: str
    price: float
    quantity: int
    subtotal: float

@dataclass
class Order:
    order_id: str
    customer_id: str
    items: List[OrderItem]
    total: float
    created_at: str