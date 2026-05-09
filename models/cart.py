from dataclasses import dataclass, field
from typing import List

@dataclass
class CartItem:
    product_id: str
    quantity: int

@dataclass
class Cart:
    customer_id: str
    items: List[CartItem] = field(default_factory=list)