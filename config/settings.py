import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
CUSTOMER_PASSWORD_FILE = os.path.join(DATA_DIR, "customerPass.csv")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.csv")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.csv")
WISHLIST_FILE = os.path.join(DATA_DIR, "wishlist.csv")
CART_FILE = os.path.join(DATA_DIR, "cart.csv")
LOGIN_LOGOUT_FILE = os.path.join(DATA_DIR, "login.csv")
SEARCH_FILE = os.path.join(DATA_DIR, "searches.csv")
