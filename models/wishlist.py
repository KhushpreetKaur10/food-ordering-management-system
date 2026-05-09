from dataclasses import dataclass

@dataclass
class WishlistItem:
    customer_id: str
    product_id: str
    name: str
    price: float
    category: str