import csv
import os

from config.settings import CART_FILE
from models.cart import Cart, CartItem
from services.order_service import OrderService


class CartService:

    def __init__(self):
        self.cart = []
        self.order_service = OrderService()

    def viewCart(self, customer):

        if not os.path.exists(CART_FILE):
            print("📭 Cart is empty.")
            return
        customer_cart = Cart(customer_id=customer.customer_id)

        with open(CART_FILE, "r", newline="") as f:

            try:
                reader = csv.DictReader(f)
            except:
                print("📭 Cart is empty.")
                return

            for row in reader:
                if row.get("Customer ID", "").strip() == customer.customer_id.strip():

                    customer_cart.items.append(
                        CartItem(
                            product_id=row.get("Product ID", ""),
                            quantity=int(row.get("Quantity", 0))
                        )
                    )

        print("\n📝 Your Cart:\n")
        print(f"{'Product ID':<12} {'Quantity':<15}")
        print("-" * 35)

        if not customer_cart.items:
            print("ℹ️ You have no items in your cart.")
            return

        for item in customer_cart.items:
            print(f"{item.product_id:<12} {item.quantity:<15}")

        print("-" * 35)

        choice = input("\nDo you want to order any item from cart? (y/n): ").strip().lower()

        if choice == "y":
            self.order_service.order(customer)
        elif choice != "n":
            print("⚠️ Invalid input.")





    def addToCart(self, customer, products):

        while True:

            product_name = input("Enter product name to add to cart: ").strip().lower()

            # SAFE SUPPORT FOR BOTH dict OR object
            product = next(
                (
                    p for p in products
                    if (
                        (isinstance(p, dict) and p["Name"].strip().lower() == product_name)
                        or
                        (hasattr(p, "name") and p.name.strip().lower() == product_name)
                    )
                ),
                None
            )

            if not product:
                print("⚠️ Product not found. Try again.\n")
                continue

            product_id = product["ID"] if isinstance(product, dict) else product.id
            product_name_real = product["Name"] if isinstance(product, dict) else product.name
            product_price = product["Price"] if isinstance(product, dict) else product.price

            if os.path.exists(CART_FILE):
                with open(CART_FILE, "r", newline="") as f:
                    reader = csv.DictReader(f)

                    if any(
                        row.get("Customer ID", "").strip() == customer.customer_id.strip()
                        and row.get("Product ID", "").strip() == str(product_id).strip()
                        for row in reader
                    ):
                        print("⚠️ Product already in cart.")
                        return

            try:
                quantity = int(input(f"Enter quantity for '{product_name_real}': "))

                if quantity <= 0:
                    print("⚠️ Quantity must be greater than 0.\n")
                    continue

            except ValueError:
                print("⚠️ Invalid quantity.\n")
                continue

            self.cart.append(
                CartItem(
                    product_id=str(product_id),
                    quantity=quantity
                )
            )

            fields = [
                "Customer ID",
                "Product ID",
                "Product Name",
                "Price",
                "Quantity"
            ]

            file_exists = os.path.exists(CART_FILE)
            file_not_empty = file_exists and os.path.getsize(CART_FILE) > 0

            with open(CART_FILE, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fields)

                if not file_not_empty:
                    writer.writeheader()

                writer.writerow({
                    "Customer ID": customer.customer_id,
                    "Product ID": product_id,
                    "Product Name": product_name_real,
                    "Price": product_price,
                    "Quantity": quantity
                })

            print(f"🛒 Added {quantity} x {product_name_real} to cart.\n")

            more = input("Add more? (y/n): ").strip().lower()

            if more == "n":
                break




    def removeFromCart(self, customer):

        if not os.path.exists(CART_FILE):
            print("📭 Cart is empty.")
            return

        product_id = input("Enter Product ID to remove: ").strip()

        updated_rows = []
        removed = False

        with open(CART_FILE, "r", newline="") as f:

            try:
                reader = csv.DictReader(f)
            except:
                print("📭 Cart is empty.")
                return

            for row in reader:

                if (
                    row.get("Customer ID", "").strip().lower() ==
                    customer.customer_id.lower()
                    and
                    row.get("Product ID", "").strip().lower() ==
                    product_id.lower()
                ):
                    removed = True
                    continue

                updated_rows.append(row)

        fields = [
            "Customer ID",
            "Product ID",
            "Product Name",
            "Price",
            "Quantity"
        ]

        with open(CART_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(updated_rows)

        if removed:
            print("✅ Item removed from cart.")
        else:
            print("⚠️ Item not found in cart.")