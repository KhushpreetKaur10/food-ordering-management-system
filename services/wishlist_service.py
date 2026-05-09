import os
import csv

from config.settings import WISHLIST_FILE
from models.wishlist import WishlistItem
from services.product_service import ProductService


class WishlistService:

    def __init__(self):
        self.product_service = ProductService()




    def viewWishlist(self, customer):

        if not os.path.exists(WISHLIST_FILE):
            print("📭 Wishlist is empty.")
            return

        print("\n📝 Your Wishlist:\n")
        print(f"{'Product ID':<12} {'Name':<25} {'Price':<10} {'Category':<15}")
        print("-" * 65)

        found = False

        with open(WISHLIST_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:

                if row["CustomerID"].strip() == customer.customer_id.strip():

                    print(
                        f"{row['ProductID']:<12} "
                        f"{row['Name']:<25} "
                        f"₹{row['Price']:<9} "
                        f"{row['Category']:<15}"
                    )

                    found = True

        if not found:
            print("ℹ️ No items in wishlist.")

        print("-" * 65)




    def addToWishlist(self, customer):

        products = self.product_service.readProductFile()

        product_name = input("Enter product name: ").strip().lower()

        product = next(
            (
                p for p in products
                if p.name.strip().lower() == product_name
            ),
            None
        )

        if not product:
            print("❌ Product not found.")
            return

        # duplicate check
        if os.path.exists(WISHLIST_FILE):

            with open(WISHLIST_FILE, "r", newline="") as f:
                reader = csv.DictReader(f)

                for row in reader:
                    if (
                        row["CustomerID"].strip() == customer.customer_id.strip()
                        and row["ProductID"].strip() == product.id.strip()
                    ):
                        print("⚠️ Already in wishlist.")
                        return

        fields = ["CustomerID", "ProductID", "Name", "Price", "Category"]

        file_exists = os.path.exists(WISHLIST_FILE)
        file_not_empty = file_exists and os.path.getsize(WISHLIST_FILE) > 0

        with open(WISHLIST_FILE, "a", newline="") as f:

            writer = csv.DictWriter(f, fieldnames=fields)

            if not file_not_empty:
                writer.writeheader()

            writer.writerow({
                "CustomerID": customer.customer_id,
                "ProductID": product.id,
                "Name": product.name,
                "Price": product.price,
                "Category": product.category
            })

        print(f"✅ {product.name} added to wishlist.")




    def removeFromWishlist(self, customer):
        product_id = input("Enter the Product ID to remove from your wishlist: ").strip()
        if not os.path.exists(WISHLIST_FILE):
            print("📭 Wishlist is empty.")
            return

        updated_rows = []
        removed = False
        customer_id = customer.customer_id.strip()

        with open(WISHLIST_FILE, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if len(row) >= 2:
                    row_customer_id = row["CustomerID"].strip()
                    row_product_id = row["ProductID"].strip()
                    if row_customer_id.lower() == customer_id.lower() and row_product_id.lower() == product_id.lower():
                        removed = True
                        continue
                updated_rows.append(row)

        fields = ["CustomerID", "ProductID", "Name", "Price", "Category"]
        with open(WISHLIST_FILE, "w", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(updated_rows)

        if removed:
            print("✅ Item removed from wishlist.")
        else:
            print("⚠️ No such item found in your wishlist.")