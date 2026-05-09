import csv
import os
import textwrap
from collections import Counter

from config.settings import PRODUCTS_FILE, SEARCH_FILE
from models.product import Product
from utils.helpers import get_next_id


class ProductService:

    def __init__(self):
        self.products = self.readProductFile()

    def _refresh(self):
        self.products = self.readProductFile()

    def readProductFile(self):

        products = []

        if not os.path.exists(PRODUCTS_FILE):
            return products

        with open(PRODUCTS_FILE, "r", newline="", encoding="utf-8") as f:

            reader = csv.DictReader(f)

            for row in reader:

                if not row:
                    continue

                try:
                    products.append(
                        Product(
                            id=row["ID"].strip(),
                            name=row["Name"].strip(),
                            price=float(row["Price"]),
                            category=row["Category"].strip(),
                            description=row["Description"].strip()
                        )
                    )
                except:
                    continue

        return products

    def writeAllProducts(self):

        fields = ["ID", "Name", "Price", "Category", "Description"]

        with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:

            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for product in self.products:
                writer.writerow({
                    "ID": product.id,
                    "Name": product.name,
                    "Price": f"{product.price:.2f}",
                    "Category": product.category,
                    "Description": product.description
                })

    def _print_products(self, products_list):

        if not products_list:
            print("⚠️ No products to display.")
            return

        print("\n─" * 130)
        print("{:<10} {:<25} {:<15} {:<20} {:<50}".format(
            "ID", "Name", "Price", "Category", "Description"
        ))
        print("─" * 130)

        for product in products_list:

            wrapped = textwrap.wrap(product.description, width=50)
            first_line = wrapped[0] if wrapped else ""

            print("{:<10} {:<25} ₹{:<15} {:<20} {:<50}".format(
                product.id,
                product.name,
                product.price,
                product.category,
                first_line
            ))

            for line in wrapped[1:]:
                print("{:<10} {:<25} {:<15} {:<20} {:<50}".format(
                    "", "", "", "", line
                ))

        print("─" * 130)

    def addProduct(self):

        while True:

            self._refresh()

            print("\nEnter product details:\n")

            name = input("Name: ").strip()

            exists = next(
                (p for p in self.products if p.name.lower() == name.lower()),
                None
            )

            if exists:
                print("❗ Product already exists.")
            else:

                try:
                    price = float(input("Price: ").strip())
                except ValueError:
                    print("❌ Invalid price.")
                    continue

                category = input("Category: ").strip()
                description = input("Description: ").strip()

                new_product = Product(
                    id=str(get_next_id(PRODUCTS_FILE)),
                    name=name,
                    price=price,
                    category=category,
                    description=description
                )

                self.products.append(new_product)
                self.writeAllProducts()

                print(f"✅ Product '{name}' added successfully.")

            more = input("Add more? (y/n): ").strip().lower()

            if more == "n":
                break
            elif more != "y":
                print("⚠️ Invalid input.")



    def delProduct(self):
        while True:

            self._refresh()

            del_id = input("\nEnter product ID: ").strip()

            product = next(
                (p for p in self.products if p.id == del_id),
                None
            )

            if product:

                confirm = input(f"Delete {del_id}? (y/n): ").strip().lower()

                if confirm == "y":
                    self.products.remove(product)
                    self.writeAllProducts()
                    print(f"✅ Deleted product {del_id}")
                else:
                    print("❌ Cancelled")
            else:
                print("⚠️ Product not found")

            more = input("Delete more? (y/n): ").strip().lower()
            if more == "n":
                break


    def viewProducts(self):
        self._refresh()

        if not self.products:
            print("⚠️ No products available.")
            return

        self._print_products(self.products)



    def viewByCategory(self):
        self._refresh()

        categories = {p.category for p in self.products}

        if not categories:
            print("⚠️ No products available.")
            return

        print("\nCategories:")
        for c in categories:
            print("🔸", c)

        cat = input("\nEnter category: ").strip().lower()

        filtered = [
            p for p in self.products
            if p.category.lower().strip() == cat
        ]

        if not filtered:
            print("⚠️ No products found.")
            return

        self._print_products(filtered)




    def searchProduct(self):

        self._refresh()

        if not os.path.exists(SEARCH_FILE):
            open(SEARCH_FILE, "w").close()

        with open(SEARCH_FILE, "r", newline="") as f:
            reader = csv.reader(f)

            history = [
                row[0].strip().lower()
                for row in reader
                if row and row[0].strip()
            ]

        if history:
            counter = Counter(history)
            print("\n🔥 Top searches:")
            for term, count in counter.most_common(3):
                print(f"- {term} ({count})")
        else:
            print("\nℹ️ No search history.")

        search = input("\nSearch product: ").strip().lower()

        with open(SEARCH_FILE, "a", newline="") as f:
            csv.writer(f).writerow([search])

        results = [
            p for p in self.products
            if search in p.name.lower()
        ]

        if not results:
            print("⚠️ No product found.")
            return

        self._print_products(results)