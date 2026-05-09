import csv
import os
from datetime import datetime

from config.settings import ORDERS_FILE, CART_FILE
from services.payment_service import process_payment
from models.order import Order, OrderItem


class OrderService:



    def generate_order_id(self):
        return f"ORD{int(datetime.now().timestamp())}"



    def order(self, customer):

        customer_id = customer.customer_id.strip()

        want_order = input("\nDo you want to order items from cart? (y/n): ").strip().lower()

        if want_order != "y":
            if want_order != "n":
                print("ℹ️ Invalid input!")
            return

        if not os.path.exists(CART_FILE) or os.path.getsize(CART_FILE) == 0:
            print("📭 Cart is empty.")
            return

        customer_cart = []

        print("\n📝 Your Cart:\n")
        print(f"{'Product ID':<12} {'Name':<25} {'Price':<10} {'Qty':<10}")
        print("-" * 65)

        with open(CART_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)

            for row in reader:

                if row.get("Customer ID", "").strip() == customer_id:

                    item = OrderItem(
                        product_id=row["Product ID"],
                        name=row["Product Name"],
                        price=float(row["Price"]),
                        quantity=int(row["Quantity"]),
                        subtotal=float(row["Price"]) * int(row["Quantity"])
                    )

                    customer_cart.append(item)

                    print(
                        f"{item.product_id:<12} "
                        f"{item.name:<25} "
                        f"₹{item.price:<10.2f} "
                        f"{item.quantity:<10}"
                    )

        if not customer_cart:
            print("ℹ️ Cart is empty.")
            return

        print("-" * 65)

        order_items = []
        total_amount = 0

        while True:

            product_id = input("Enter product ID: ").strip()

            product = next(
                (p for p in customer_cart if p.product_id.lower() == product_id.lower()),
                None
            )

            if product:
                order_items.append(product)
                print(f"✅ Added {product.name}")
            else:
                print("⚠️ Not found in cart.")

            more = input("Add more? (y/n): ").strip().lower()

            while more not in ["y", "n"]:
                more = input("Enter y or n: ").strip().lower()

            if more == "n":
                break

        if not order_items:
            print("⚠️ No items selected.")
            return

        print("\n🧾 Order Summary\n")
        print(f"{'Product':<25} {'Qty':<5} {'Price':<10} {'Subtotal':<10}")
        print("-" * 60)

        for item in order_items:
            print(
                f"{item.name:<25} "
                f"{item.quantity:<5} "
                f"₹{item.price:<10.2f} "
                f"₹{item.subtotal:<10.2f}"
            )
            total_amount += item.subtotal

        print("-" * 60)
        print(f"{'Total Amount':<42} ₹{total_amount:.2f}")
        print("-" * 60)

        if not process_payment(total_amount):
            return

        order = Order(
            order_id=self.generate_order_id(),
            customer_id=customer_id,
            items=order_items,
            total=total_amount,
            created_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        fields = [
            "OrderID",
            "CustomerID",
            "ProductID",
            "Name",
            "Price",
            "Quantity",
            "Subtotal",
            "OrderTime"
        ]

        file_exists = os.path.exists(ORDERS_FILE)
        file_not_empty = file_exists and os.path.getsize(ORDERS_FILE) > 0

        with open(ORDERS_FILE, "a", newline="") as f:

            writer = csv.DictWriter(f, fieldnames=fields)

            if not file_not_empty:
                writer.writeheader()

            for item in order.items:
                writer.writerow({
                    "OrderID": order.order_id,
                    "CustomerID": order.customer_id,
                    "ProductID": item.product_id,
                    "Name": item.name,
                    "Price": item.price,
                    "Quantity": item.quantity,
                    "Subtotal": item.subtotal,
                    "OrderTime": order.created_at
                })

        # Update grand total at end of file
        self.update_grand_total(order.total)

        print(f"\n✅ Order placed successfully. Order ID: {order.order_id}")

        # Remove ordered items from cart
        self.remove_ordered_items_from_cart(customer_id, order_items)

    def remove_ordered_items_from_cart(self, customer_id, ordered_items):
        """Remove ordered items from customer's cart"""
        if not os.path.exists(CART_FILE):
            return

        updated_rows = []

        with open(CART_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("Customer ID", "").strip() == customer_id:
                    # Check if this cart item was ordered
                    ordered_product_ids = [item.product_id.lower() for item in ordered_items]
                    if row.get("Product ID", "").strip().lower() not in ordered_product_ids:
                        updated_rows.append(row)
                else:
                    updated_rows.append(row)

        # Write back the updated cart
        fields = ["Customer ID", "Product ID", "Product Name", "Price", "Quantity"]
        with open(CART_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(updated_rows)

    def update_grand_total(self, amount_to_add=0):
        """Update the grand total at the end of orders.csv"""
        if not os.path.exists(ORDERS_FILE):
            return

        with open(ORDERS_FILE, "r", newline="") as f:
            rows = list(csv.DictReader(f))

        # Calculate current grand total from all order subtotals
        current_total = sum(float(row.get("Subtotal", 0)) for row in rows if row.get("OrderID") != "TOTAL_BILL")

        # Remove any existing TOTAL_BILL rows
        rows = [row for row in rows if row.get("OrderID") != "TOTAL_BILL"]

        # Add new TOTAL_BILL row with updated total
        total_bill_row = {
            "OrderID": "TOTAL_BILL",
            "CustomerID": "",
            "ProductID": "",
            "Name": "",
            "Price": "",
            "Quantity": "",
            "Subtotal": str(current_total),
            "OrderTime": ""
        }
        rows.append(total_bill_row)

        # Write back to file
        fieldnames = ["OrderID", "CustomerID", "ProductID", "Name", "Price", "Quantity", "Subtotal", "OrderTime"]
        with open(ORDERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def cancelOrder(self, customer):
        customer_id = customer.customer_id.strip()
        cancel_id = input("\nEnter Order ID to cancel: ").strip()

        if not os.path.exists(ORDERS_FILE):
            print("❌ Order file not found.")
            return

        with open(ORDERS_FILE, "r", newline="") as f:
            rows = list(csv.DictReader(f))

        if not rows:
            print("❌ No orders found.")
            return

        order_rows = [row for row in rows if row.get("OrderID") == cancel_id and row.get("CustomerID") == customer_id]

        if not order_rows:
            print("⚠️ Order not found.")
            return

        print(f"\n🧾 Items in Order ID '{cancel_id}':")
        for i, row in enumerate(order_rows, start=1):
            print(f"{i}. {row.get('Name', '')} (Product ID: {row.get('ProductID', '')}, Qty: {row.get('Quantity', '')}, Refund: ₹{row.get('Subtotal', '')})")

        full_cancel = input("\nDo you want to cancel the entire order? (y/n): ").strip().lower()
        while full_cancel not in ["y", "n"]:
            full_cancel = input("Please enter 'y' or 'n': ").strip().lower()

        remaining_rows = [row for row in rows if not (row.get("OrderID") == cancel_id and row.get("CustomerID") == customer_id)]
        refund_total = 0

        if full_cancel == "y":
            refund_total = sum(float(row.get("Subtotal", 0)) for row in order_rows)
            with open(ORDERS_FILE, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(remaining_rows)
            # Update grand total after removing cancelled orders
            self.update_grand_total()
            print(f"\n💸 Refund of ₹{refund_total:.2f} has been initiated for the full order.")
            print(f"✅ Order ID '{cancel_id}' has been fully cancelled.\n")
            return

        cancelled = []
        kept = []
        for row in order_rows:
            confirm = input(f"Cancel '{row.get('Name', '')}' (Product ID: {row.get('ProductID', '')}, Refund ₹{row.get('Subtotal', '')})? (y/n): ").strip().lower()
            while confirm not in ["y", "n"]:
                confirm = input("Please enter 'y' or 'n': ").strip().lower()
            if confirm == "y":
                cancelled.append(row)
                refund_total += float(row.get("Subtotal", 0))
            else:
                kept.append(row)

        if not cancelled:
            print("⚠️ No items were cancelled.\n")
            return

        final_rows = remaining_rows + kept

        with open(ORDERS_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(final_rows)

        # Update grand total after removing cancelled items
        self.update_grand_total()

        print(f"\n💸 Total refund: ₹{refund_total:.2f}")
        print("✅ Cancellation completed.\n")

 
 

    def viewAllOrders(self):

        if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
            print("❌ No orders found.")
            return

        print("\n📜 ALL ORDER HISTORY:\n")

        with open(ORDERS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)

        if not all_rows:
            print("ℹ️ No orders have been placed yet.")
            return

        print(f"{'Order ID':<20} {'Customer ID':<12} {'Product ID':<12} {'Name':<25} {'Price':<13} {'Quantity':<10} {'Subtotal':<10} {'Order Time':<30}")
        print("-" * 155)

        for row in all_rows:
            if row.get("OrderID") == "TOTAL_BILL":
                print(f"{row.get('OrderID'):<20} {'':<12} {'':<12} {'':<25} {'':<13} {'':<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {'':<30}")
                print("-" * 155)
            elif row.get("OrderID"):
                print(f"{row.get('OrderID'):<20} {row.get('CustomerID'):<12} {row.get('ProductID'):<12} {row.get('Name'):<25} ₹{float(row.get('Price', 0)):<13.2f} {row.get('Quantity'):<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {row.get('OrderTime'):<30}")

        print("-" * 155)



    def viewMyOrders(self, customer):

        customer_id = customer.customer_id.strip()

        if not os.path.exists(ORDERS_FILE) or os.path.getsize(ORDERS_FILE) == 0:
            print("❌ No orders found.")
            return

        print(f"\n🧾 Order History for {customer.name} (ID: {customer_id}):\n")

        with open(ORDERS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            all_rows = list(reader)

        if not all_rows:
            print("ℹ️ You have not placed any orders yet.")
            return

        print(f"{'Order ID':<20} {'Product ID':<12} {'Name':<25} {'Price (Rs)':<12} {'Quantity':<10} {'Subtotal':<10} {'Order Date':<30}")
        print("-" * 125)

        found_orders = False

        for row in all_rows:
            if row.get("CustomerID", "").strip() == customer_id and row.get("OrderID") != "TOTAL_BILL":
                print(f"{row.get('OrderID'):<20} {row.get('ProductID'):<12} {row.get('Name'):<25} ₹{float(row.get('Price', 0)):<12.2f} {row.get('Quantity'):<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {row.get('OrderTime'):<30}")
                found_orders = True
            elif row.get("OrderID") == "TOTAL_BILL":
                if found_orders:
                    print("-" * 125)
                    print(f"{row.get('OrderID'):<20} {'':<12} {'':<25} {'':<12} {'':<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {'':<30}")
                    print("-" * 125)

        if not found_orders:
            print("ℹ️ You have not placed any orders yet.")