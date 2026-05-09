from dataclasses import dataclass
from models.user import User

@dataclass
class Customer(User):
    customer_id: str
    city: str
    phone: str
    email: str