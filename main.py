# order food online portal

import csv
import os
from getpass import getpass
import re
from datetime import datetime
import textwrap
from collections import Counter

adminPass='1234'

products=[]
customers=[]
cart=[]

customerFile = 'C:/Users/hp/Music/PYTHON GATEWAY/csv project food/customers.csv'
customerPassFile = 'C:/Users/hp/Music/PYTHON GATEWAY/csv project food/customerPass.csv'
productsFile='C:/Users/hp/Music/PYTHON GATEWAY/csv project food/products.csv'
ordersFile = 'C:/Users/hp/Music/PYTHON GATEWAY/csv project food/orders.csv'
wishlistFile='C:/Users/hp/Music/PYTHON GATEWAY/csv project food/wishlist.csv'
cartFile='C:/Users/hp/Music/PYTHON GATEWAY/csv project food/cart.csv'
loginLogoutFile='C:/Users/hp/Music/PYTHON GATEWAY/csv project food/login.csv'
searchFile='C:/Users/hp/Music/PYTHON GATEWAY/csv project food/searches.csv'


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) == 10


def get_next_id(filename):
    max_id = 0
    if os.path.exists(filename):
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0].strip().isdigit():
                    current_id = int(row[0].strip())
                    if current_id > max_id:
                        max_id = current_id
    return max_id + 1



def generatePass():
    return str(datetime.now().strftime("%Y%m%d%H%M%S"))
    



def writeCustomersData():
    print("\nENTER FOLLOWING DETAILS -")
    name = input("Name: ")
    city = input("City: ")
    while True:
        phone = input("Phone number: ")
        if is_valid_phone(phone):
            break
        else:
            print("❌ Invalid phone number. Must be 10 digits.")
    while True:
        email = input("Email: ")
        if is_valid_email(email):
            break
        else:
            print("❌ Invalid email format. Please try again.")
    if os.path.exists(customerFile):
        with open(customerFile, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if len(row) >= 5:
                    existing_phone = row['Phone Number']
                    existing_email = row['Email']
                    if phone == existing_phone or email == existing_email:
                        print("⚠️ : Customer is already registered.\n")
                        return -1
    while True:
        password = generatePass()
        with open(customerPassFile, 'w') as f:
            writer=csv.writer(f)
            writer.writerow([password])
        print("✅ Customer registered successfully.\n")
        print("Your password is sent to a file in your PC.\nPlease check it.")
        new_id = get_next_id(customerFile)
        fields=['CustomerID', 'Name', 'City', 'Phone Number', 'Email', 'Password']
        with open(customerFile, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            if not os.path.exists(customerFile) or os.path.getsize(customerFile) == 0:
                writer.writeheader()
            writer.writerow({
                'CustomerID': new_id,
                'Name': name,
                'City': city,
                'Phone Number': phone,
                'Email': email,
                'Password': password
            })
        break
        



def readCustomerFile():
    global customers
    customers = []
    if not os.path.exists(customerFile):
        return customers
    with open(customerFile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers.append(row)
        # for row in reader:
        #     if len(row) >= 6:
        #         customers.append({
        #             'ID': row[0],
        #             'Name': row[1],
        #             'City': row[2],
        #             'Phone Number': row[3],
        #             'Email': row[4],
        #             'Password': row[5]
        #         })
    return customers



def writeProductsData():
    if not os.path.exists(productsFile):
        with open(productsFile, 'w', newline='') as f:
            pass
    print("\nEnter the following details to add a product record-\n")
    name = input("Name: ").strip()
    exists = False
    with open(productsFile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row and len(row) > 1 and row['Name'].strip().lower() == name.lower():
                exists = True
                break
    if not exists:
        new_id = get_next_id(productsFile)
        price = input("Price: ").strip()
        category = input("Category: ").strip()
        description = input("Description: ").strip()
        file_exists = os.path.isfile(productsFile) and os.path.getsize(productsFile) > 0
        with open(productsFile, 'a', newline='') as f:
            fields = ['ID', 'Name', 'Price', 'Category', 'Description']
            writer = csv.DictWriter(f, fieldnames=fields)
            # Write header only if file did NOT exist or is empty
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'ID': new_id,
                'Name': name,
                'Price': price,
                'Category': category,
                'Description': description
            })
        print("✅ Product details added successfully.")
    else:
        print("❗ This product already exists.")




def readProductFile():
    global products
    products = []
    if not os.path.exists(productsFile):
        return products
    with open(productsFile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            products.append({
                'ID': row['ID'].strip(),
                'Name': row['Name'].strip(),
                'Price': row['Price'].strip(),
                'Category': row['Category'].strip(),
                'Description': row['Description'].strip()
            })
    return products




def viewProducts():
    print("\nAll products: \n")
    print("─" * 130)
    print("{:<10} {:<25} {:<15} {:<20} {:<50}".format("Sno.", "Name", "Price", "Category", "Description"))
    print("─" * 130)
    for p in products:
        wrapped_description = textwrap.wrap(p['Description'], width=50)
        print("{:<10} {:<25} ₹{:<15} {:<20} {:<50}".format(
            p['ID'], p['Name'], p['Price'], p['Category'], wrapped_description[0]
        ))
        for line in wrapped_description[1:]:
            print("{:<10} {:<25} {:<15} {:<20} {:<50}".format('', '', '', '', line))
    print("─" * 130)


def viewCustomers():
    if not os.path.exists(customerFile) or os.path.getsize(customerFile) == 0:
        print("📭 No customer data found.")
        return
    
    print("\nAll Customers: \n")
    print("-----------------------------------------------------------------------------------------------------------------------")
    print("{:<10} {:<15} {:<20} {:<25} {:<25} {:<15}".format("🆔", "Name🧑", "City🏙️", "Phone Number📞", "Email📧", "Password🔑"))
    print("-----------------------------------------------------------------------------------------------------------------------")
    for c in customers:
        print("{:<10} {:<15} {:<20} {:<25} {:<25} {:<15}".format(c['CustomerID'], c['Name'], c['City'], c['Phone Number'], c['Email'], c['Password']))
    print("-----------------------------------------------------------------------------------------------------------------------")


def viewByCategory():
    unique_categories = {p['Category'] for p in products}
    if not unique_categories:
        print("⚠️ : No products available.")
        return
    print("\nAvailable product categories:")
    for t in unique_categories:
        print(f"🔸 {t}")
    categoryInput=input("\nEnter the category to search🔍: ").strip().lower()
    categoryFound=[]
    for p in products:
        if categoryInput == p['Category'].strip().lower():
            categoryFound.append(p)
    if categoryFound:
        print(f"{categoryInput} found:\n")
        print("─" * 130)
        print("{:<10} {:<25} {:<15} {:<20} {:<50}".format("Sno", "Name", "Price", "Category", "Description"))
        print("─" * 130)
        for i, product in enumerate(categoryFound, start=1):
            wrapped_description = textwrap.wrap(p['Description'], width=50)
            print("{:<10} {:<25} ₹{:<15} {:<20} {:<50}".format(
                product['ID'], product['Name'], product['Price'], product['Category'], wrapped_description[0]
            ))
            for line in wrapped_description[1:]:
                print("{:<10} {:<25} {:<15} {:<20} {:<50}".format('', '', '', '', line))
        print("─" * 130)
    else:
        print("⚠️ : No such category found.")



def searchProduct():
    if not os.path.exists(searchFile):
        with open(searchFile, 'w', newline='') as f:
            pass
    with open(searchFile, 'r', newline='') as f:
        reader=csv.reader(f)
        searchHistory = [row[0].strip().lower() for row in reader if row]
    if searchHistory:
        counter = Counter(searchHistory)
        top_searches = counter.most_common(3)
        print("\n🔥 Top 3 Most Searched Items:")
        for term, count in top_searches:
            print(f"- {term} ({count} searches)")
    else:
        print("\nℹ️ No previous searches found.")
    search=input("\nEnter the product to search🔍: ").strip().lower()
    with open(searchFile, 'a', newline='') as f:
        writer=csv.writer(f)
        writer.writerow([search])
    searchResults=[]
    for p in products:
        if search == p['Name'].strip().lower():
            searchResults.append(p)
    if searchResults:
        print(f"{search} found:\n")
        print("─" * 130)
        print("{:<10} {:<25} {:<15} {:<20} {:<50}".format("Sno", "Name", "Price", "Category", "Description"))
        print("─" * 130)
        for i, product in enumerate(searchResults, start=1):
            wrapped_description = textwrap.wrap(p['Description'], width=50)
            print("{:<10} {:<25} ₹{:<15} {:<20} {:<50}".format(
                product['ID'], product['Name'], product['Price'], product['Category'], wrapped_description[0]
            ))
            for line in wrapped_description[1:]:
                print("{:<10} {:<25} {:<15} {:<20} {:<50}".format('', '', '', '', line))
        print("─" * 130)
    else:
        print("⚠️ : No such product found.")


def process_payment(amount):
    print("\nChoose a payment method:")
    print("1. UPI")
    print("2. Credit/Debit Card")
    print("3. Cash on Delivery")
    while True:
        choice = int(input("\nEnter payment method: "))
        if choice not in [1, 2, 3]:
            print("❌ Invalid choice. Try again.\n")
        else:
            break
    if choice == 1:
        upi = input("\nEnter your UPI ID: ").strip()
        print("\nProcessing UPI payment...")
    elif choice == 2:
        card = input("\nEnter your card number: ").strip()
        print("\nProcessing card payment...")
    elif choice == 3:
        print("\nCash on Delivery selected.")
    print("✅ Payment of ₹{} successful!".format(amount))
    return True



def viewCart(customer):
    if not os.path.exists(cartFile):
        print("📭 Cart is empty.")
        return
    print(f"\n📝 Your Cart:\n")
    print(f"{'Product ID':<12} {'Name':<25} {'Price':<10} {'Quantity':<15}")
    print("-" * 65)
    found = False
    with open(cartFile, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['Customer ID'].strip() == customer['CustomerID'].strip():
                print(f"{row['Product ID']:<12} {row['Product Name']:<25} ₹{row['Price']:<9} {row['Quantity']:<15}")
                found = True
    if not found:
        print("ℹ️ You have no items in your cart.")
    print("-" * 65)
    if found:
        want_order = input("\nDo you want to order any item from cart? (y/n): ").strip().lower()
        if want_order == 'y':
            order(customer)  
        elif want_order != 'n':
            print("ℹ️ Invalid input!\n")

    



def addToCart(customer):
    global cart
    total_amount = 0
    while True:
        order_input = input("Enter the product name to add to cart: ").strip().lower()
        product = next((p for p in products if p['Name'].strip().lower() == order_input), None)
        already_exists = False
        if os.path.exists(cartFile):
            with open(cartFile, "r", newline='') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if len(row) >= 2 and row['Customer ID'] == customer['CustomerID'] and row['Product ID'] == product['ID']:
                        already_exists = True
                        break
        if already_exists:
            print("⚠️ Product already in your cart.")
            return
        if product and not already_exists:
            try:
                quantity = int(input(f"Enter quantity for '{product['Name']}': "))
                if quantity <= 0:
                    print("⚠️ Quantity must be at least 1.\n")
                    continue
            except ValueError:
                print("⚠️ Invalid quantity. Please enter a number.\n")
                continue
            price = int(product['Price'].strip())
            subtotal = price * quantity
            cart.append({
                'ID': product['ID'],
                'Name': product['Name'],
                'Price': product['Price'],
                'Quantity': quantity,
                'Subtotal': subtotal
            })
            total_amount += subtotal
            fields=['Customer ID', 'Product ID', 'Product Name', 'Price', 'Quantity']
            with open(cartFile, "a", newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                if not os.path.exists(cartFile) or os.path.getsize(cartFile) == 0:
                    writer.writeheader()
                writer.writerow({
                    'Customer ID': customer['CustomerID'],
                   'Product ID' : product['ID'],
                   'Product Name' : product['Name'],
                   'Price' : product['Price'],
                   'Quantity' : quantity
                })
            print(f"🛒 ✅ Added {quantity} x {product['Name']} to cart (Subtotal: ₹{subtotal}).\n")
        else:
            print("⚠️ No such product found. Please try again.\n")
        more = input("Do you want to add anything else to cart? (y/n): ").strip().lower()
        while more not in ['y', 'n']:
            more = input("Invalid input. Please enter 'y' or 'n': ").strip().lower()
        if more == 'n':
            break
    if not cart:
        print("⚠️ No items in cart.")
        return
    


def removeFromCart(customer):
    global cart
    product_id = input("Enter the Product ID to remove from your cart: ").strip()
    if not os.path.exists(cartFile):
        print("📭 Cart is empty.")
        return
    updated_rows = []
    removed = False
    customer_id = customer['CustomerID'].strip()
    with open(cartFile, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(row) >= 2:
                row_customer_id = row['Customer ID'].strip()
                row_product_id = row['Product ID'].strip()
                if row_customer_id.lower() == customer_id.lower() and row_product_id.lower() == product_id.lower():
                    removed = True
                    continue
            updated_rows.append(row)
    fields=['Customer ID','Product ID','Product Name','Price','Quantity']
    with open(cartFile, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(updated_rows)
    if removed:
        print("✅ Item removed from cart.")
        # Remove the product dict from cart list
        cart[:] = [item for item in cart if item['ID'] != product_id]
    else:
        print("⚠️ No such item found in your cart.")



def CartMenu():
    print("\nCart Menu:")
    print("1. View Cart")
    print("2. Add to Cart")
    print("3. Remove from Cart")
    print("4. Back to Main Menu")




def generate_order_id():
    return f"ORD{int(datetime.now().timestamp())}"



def order(customer):
    global cart
    order=[]
    customer_id = customer['CustomerID'].strip()
    total_amount = 0
    want_order = input("\nDo you want to order any item from cart? (y/n): ").strip().lower()
    if want_order == 'y':
        if not os.path.exists(cartFile):
            print("📭 Cart is empty.")
            return
        print(f"\n📝 Your Cart:\n")
        print(f"{'Product ID':<12} {'Name':<25} {'Price':<10} {'Quantity':<15}")
        print("-" * 65)
        found = False
        customer_cart = []
        with open(cartFile, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['Customer ID'].strip() == customer['CustomerID'].strip():
                    print(f"{row['Product ID']:<12} {row['Product Name']:<25} ₹{row['Price']:<9} {row['Quantity']:<15}")
                    customer_cart.append({
                        'ID': row['Product ID'],
                        'Name': row['Product Name'],
                        'Price': row['Price'],
                        'Quantity': int(row['Quantity']),
                        'Subtotal': int(row['Price']) * int(row['Quantity'])
                    })
                    found = True
        if not found:
            print("ℹ️ You have no items in your cart.")
        print("-" * 65) 
        while True:
            order_input = input("Enter the product ID you want to order: ").strip().lower()
            product = next((p for p in customer_cart if p['ID'].strip().lower() == order_input), None)
            if product:
                order.append(product)
                print(f"Product {product['Name']} added to order sequence.")
            else:
                print("⚠️ No such product found. Please try again.\n")
            more = input("Do you want to order anything else? (y/n): ").strip().lower()
            while more not in ['y', 'n']:
                more = input("Invalid input. Please enter 'y' or 'n': ").strip().lower()
            if more == 'n':
                break
        if not order:
            print("⚠️ No items were ordered.")
            return
        print(f"\n🧾 Order Summary - ")
        print("---------------------------------------------------------------")
        print(f"{'Product':<25} {'Qty':<5} {'Price':<8} {'Subtotal':<10}")
        print("-" * 60)
        for item in order:
            print(f"{item['Name']:<25} {item['Quantity']:<5} ₹{item['Price']:<8} ₹{item['Subtotal']:<10}")
            total_amount += item['Subtotal']
        print("-" * 60)
        print(f"{'Total Amount:':<45} ₹{total_amount}")
        print("-" * 60)
        if process_payment(total_amount):
            order_id = generate_order_id()
            print(f"\n✅ Order placed successfully! Order ID: {order_id}")
            fields=['OrderID', 'CustomerID', 'ProductID', 'Name', 'Price', 'Quantity', 'Subtotal', 'OrderTime']
            with open(ordersFile, 'a', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=fields)
                if not os.path.exists(ordersFile) or os.path.getsize(ordersFile) == 0:
                    writer.writeheader()
                for item in order:
                    writer.writerow({
                       'OrderID' : order_id,
                       'CustomerID' : customer_id,
                       'ProductID': item['ID'],
                       'Name' : item['Name'],
                       'Price' : item['Price'],
                       'Quantity' : item['Quantity'],
                       'Subtotal' : item['Subtotal'],
                       'OrderTime':  datetime.now().isoformat()
                    })
                writer.writerow({'OrderID': 'TOTAL_BILL', 'Subtotal': total_amount})
                writer.writerow({})  # Blank line for separation
    elif want_order != 'n':
        print("ℹ️ Invalid input!\n")


    










def cancelOrder(customer):
    customer_id = customer['CustomerID'].strip()
    cancel_id = input("\nEnter Order ID to cancel: ").strip()
    if not os.path.exists(ordersFile):
        print("❌ Order records not found.\n")
        return
    with open(ordersFile, 'r', newline='') as f:
        reader = list(csv.DictReader(f))
    start_index = -1
    end_index = -1
    for i, row in enumerate(reader):
        if row.get('OrderID') == cancel_id and row.get('CustomerID') == customer_id:
            start_index = i
            for j in range(i, len(reader)):
                if reader[j].get('OrderID') == "TOTAL_BILL":
                    end_index = j
                    break
            break
    if start_index == -1 or end_index == -1:
        print("⚠️ No matching order found for this Order ID and customer.\n")
        return
    
    order_block = reader[start_index:end_index+1]  # Include TOTAL_BILL row
    rest_of_file = reader[:start_index] + reader[end_index+1:]  # Skip order block from original
    product_rows = [row for row in order_block if row.get('OrderID') != "TOTAL_BILL"]
    total_row = next((row for row in order_block if row.get('OrderID') == "TOTAL_BILL"), None)
    refund_total = 0
    remaining_items = []
    cancelled_items = []
    print(f"\n🧾 Items in Order ID '{cancel_id}':")
    for i, row in enumerate(product_rows, start=1):
        name = row['Name']
        quantity = row['Quantity']
        price = row['Price']
        print(f"{i}. {name} (Qty: {quantity}, Price: ₹{price})")
    full_cancel = input("\nDo you want to cancel the entire order? (y/n): ").strip().lower()
    while full_cancel not in ['y', 'n']:
        full_cancel = input("Please enter 'y' or 'n': ").strip().lower()
    if full_cancel == 'y':
        refund_total = sum(int(row['Subtotal']) for row in product_rows)
        print(f"\n💸 Refund of ₹{refund_total} has been initiated for the full order.")
        # Write back rest of file 
        with open(ordersFile, 'w', newline='') as f:
            fieldnames = reader[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rest_of_file)
        print(f"✅ Order ID '{cancel_id}' has been fully cancelled.\n")
        return
    for row in product_rows:
        name = row['Name']
        pid = row['ProductID']
        subtotal = int(row['Subtotal'])
        confirm = input(f"Cancel '{name}' (Product ID: {pid}, Refund ₹{subtotal})? (y/n): ").strip().lower()
        while confirm not in ['y', 'n']:
            confirm = input("Please enter 'y' or 'n': ").strip().lower()
        if confirm == 'y':
            cancelled_items.append(row)
            refund_total += subtotal
        else:
            remaining_items.append(row)
    if not cancelled_items:
        print("⚠️ No items were cancelled.\n")
        return
    new_total = sum(int(row['Subtotal']) for row in remaining_items)
    updated_block = remaining_items
    if new_total > 0:
        # Append updated TOTAL_BILL row
        total_row['Subtotal'] = str(new_total)
        updated_block.append(total_row)
    else:
        print("\n🧾 All items were cancelled. Order has been removed.")
    # Merge back all content
    final_content = rest_of_file + updated_block
    with open(ordersFile, 'w', newline='') as f:
        fieldnames = reader[0].keys()
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(final_content)
    print(f"💸 Total refund: ₹{refund_total}")
    print("✅ Cancellation completed.\n")









def viewAllOrders():
    if not os.path.exists(ordersFile) or os.path.getsize(ordersFile) == 0:
        print("❌ Order records not found.")
        return
    print("\n📜 ALL ORDER HISTORY:\n")
    with open(ordersFile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    if not all_rows:
        print("ℹ️ No orders have been placed yet.")
        return
    print(f"\n{'Order ID':<20} {'Customer ID':<12} {'Product ID':<12} {'Name':<25} {'Price':<13} {'Quantity':<10} {'Subtotal':<10} {'Order Time':<30}")
    print("-" * 155)
    for row in all_rows:
        if row.get('OrderID') == 'TOTAL_BILL':
            print(f"{row.get('OrderID'):<20} {'':<12} {'':<12} {'':<25} {'':<13} {'':<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {'':<30}")
            print("-" * 155) 
        elif row.get('OrderID'): 
            print(f"{row.get('OrderID'):<20} {row.get('CustomerID'):<12} {row.get('ProductID'):<12} {row.get('Name'):<25} ₹{float(row.get('Price', 0)):<13.2f} {row.get('Quantity'):<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {row.get('OrderTime'):<30}")
    print("-" * 155)


def viewMyOrders(customer):
    if not os.path.exists(ordersFile) or os.path.getsize(ordersFile) == 0:
        print("❌ No order records found.")
        return
    customer_id = customer['CustomerID'].strip()
    found_orders = False
    print(f"\n🧾 ORDER HISTORY for {customer['Name'].strip()} (ID: {customer_id}):\n")
    with open(ordersFile, 'r', newline='') as f:
        reader = csv.DictReader(f)
        all_rows = list(reader)
    if not all_rows:
        print("ℹ️ You have not placed any orders yet.")
        return
    print(f"{'Order ID':<20} {'Product ID':<12} {'Name':<25} {'Price (Rs)':<12} {'Quantity':<10} {'Subtotal':<10} {'Order Date':<30}")
    print("-" * 125)   
    current_order_id = None
    for row in all_rows:
        if row.get('CustomerID', '').strip() == customer_id and row.get('OrderID') != 'TOTAL_BILL':
            print(f"{row.get('OrderID'):<20} {row.get('ProductID'):<12} {row.get('Name'):<25} ₹{float(row.get('Price', 0)):<12.2f} {row.get('Quantity'):<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {row.get('OrderTime'):<30}")
            found_orders = True
            current_order_id = row.get('OrderID')
        elif row.get('OrderID') == 'TOTAL_BILL' and row.get('CustomerID', '').strip() == current_order_id:
            print(f"{row.get('OrderID'):<20} {'':<12} {'':<25} {'':<12} {'':<10} ₹{float(row.get('Subtotal', 0)):<10.2f} {'':<30}")
            print("-" * 125) 
            current_order_id = None 
    if not found_orders:
        print("ℹ️ You have not placed any orders yet.")
    else:
        if current_order_id is not None:
             print("-" * 125)




def viewWishlist(customer):
    if not os.path.exists(wishlistFile):
        print("📭 Wishlist is empty.")
        return
    print(f"\n📝 Your Wishlist:\n")
    print(f"{'Product ID':<12} {'Name':<25} {'Price':<10} {'Category':<15}")
    print("-" * 65)
    found = False
    with open(wishlistFile, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(row) >= 5 and row['CustomerID'].strip() == customer['CustomerID'].strip():
                print(f"{row['ProductID']:<12} {row['Name']:<25} ₹{row['Price']:<9} {row['Category']:<15}")
                found = True
    if not found:
        print("ℹ️ You have no items in your wishlist.")
    print("-" * 65)
    



def addToWishlist(customer):
    product_name = input("Enter the product name to add to your wishlist: ").strip().lower()
    found_product = next((p for p in products if p['Name'].strip().lower() == product_name), None)
    if not found_product:
        print("❌ Product not found.")
        return
    already_exists = False
    if os.path.exists(wishlistFile):
        with open(wishlistFile, "r", newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if len(row) >= 2 and row['CustomerID'] == customer['CustomerID'] and row['ProductID'] == found_product['ID']:
                    already_exists = True
                    break
    if already_exists:
        print("⚠️ Product already in your wishlist.")
        return
    fields=['CustomerID', 'ProductID', 'Name', 'Price', 'Category']
    with open(wishlistFile, "a", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        if not os.path.exists(wishlistFile) or os.path.getsize(wishlistFile) == 0:
            writer.writeheader()
        writer.writerow({
            'CustomerID': customer['CustomerID'],
            'ProductID': found_product['ID'],
            'Name': found_product['Name'],
            'Price': found_product['Price'],
            'Category': found_product['Category']
        })
    print(f"✅ {found_product['Name']} added to your wishlist.")



def removeFromWishlist(customer):
    product_id = input("Enter the Product ID to remove from your wishlist: ").strip()
    if not os.path.exists(wishlistFile):
        print("📭 Wishlist is empty.")
        return
    updated_rows = []
    removed = False
    customer_id = customer['CustomerID'].strip()
    with open(wishlistFile, "r", newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if len(row) >= 2:
                row_customer_id = row['CustomerID'].strip()
                row_product_id = row['ProductID'].strip()
                if row_customer_id.lower() == customer_id.lower() and row_product_id.lower() == product_id.lower():
                    removed = True
                    continue
            updated_rows.append(row)
    fields=['CustomerID', 'ProductID', 'Name', 'Price', 'Category']
    with open(wishlistFile, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(updated_rows)
    if removed:
        print("✅ Item removed from wishlist.")
    else:
        print("⚠️ No such item found in your wishlist.")



def wishlistMenu():
    print("\nWishlist Menu:")
    print("1. View Wishlist")
    print("2. Add to Wishlist")
    print("3. Remove from Wishlist")
    print("4. Back to Main Menu")



def registerCustomer():
    print("-----------Customer Registeration-----------")
    global customers
    register=writeCustomersData()
    if register== -1:
        print("⚠️ : Customer is already registered. Please login.\n")
        wantLogin = input("Do you want to login? (y/n): ")
        if wantLogin.lower() == 'y':
            loginCustomer() 
        return
    else:
        customers=readCustomerFile()
    

def loginCustomer():
    if not os.path.exists(loginLogoutFile):
        with open(loginLogoutFile, 'w', newline='') as f:
            pass
    print("\nCUSTOMER LOGIN PORTAL:\n")
    while True:
        choice = int(input("How do you want to login?\n1. With phone number\n2. With email\n\nEnter choice: "))
        if choice not in [1, 2]:
            print("⚠️ Invalid choice! Please enter 1 or 2.\n")
        else:
            break
    matched_customer=None
    if choice == 1:
        while True:
            phone = input("Enter your phone number: ").strip()
            if is_valid_phone(phone):
                break
            else:
                print("❌ Invalid phone number. Must be 10 digits. Please try again.\n")
        matched_customer = next((c for c in customers if phone == c['Phone Number'].strip()), None)
        if not matched_customer:
            print("⚠️ Phone number is not registered.")
            wantRegister = input("Do you want to register? (y/n): ")
            if wantRegister.lower() == 'y':
                registerCustomer()
            return -1
        while True:
            loginPass = getpass("Enter password: ").strip()
            if loginPass == matched_customer['Password'].strip():
                print("✅ Login successful.\n")
                login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return matched_customer, login_time
            else:
                print("⚠️ : Incorrect credentials! Customer access denied.❌ \nPlease try again.\n")
    elif choice == 2:
        while True:
            email = input("Enter your email: ").strip()
            if is_valid_email(email):
                break
            else:
                print("⚠️ : Incorrect credentials! Customer access denied.❌ \nPlease try again.\n")
        matched_customer = next((c for c in customers if email.lower() == c['Email'].lower().strip()), None)
        if not matched_customer:
            print("⚠️ Email is not registered.")
            wantRegister = input("Do you want to register? (y/n): ")
            if wantRegister.lower() == 'y':
                registerCustomer()
            return -1
        while True:
            loginPass = getpass("Enter password: ").strip()
            if loginPass == matched_customer['Password'].strip():
                print("✅ Login successful.\n")
                login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                return matched_customer, login_time
            else:
                print("⚠️ : Incorrect credentials! Customer access denied.❌ \nPlease try again.\n")


def adminLogin():
    print("\nADMIN LOGIN PORTAL:\n")
    loginPass = getpass("Enter admin password: ")
    if loginPass==adminPass:
        print("✅ Login successful.\n")
    else:
        print("⚠️ : Incorrect password! \nAdmin access denied❌\n.")
        return -1
    


    
def changePass():
    global customers
    email = input("\nEnter your email: ").strip()
    if not is_valid_email(email):
        print("❌ Invalid email format.")
        return
    password = getpass("Enter your current password: ").strip()
    matched_customer = None
    for c in customers:
        if c['Email'].strip() == email and c['Password'].strip() == password:
            matched_customer = c
            break
    if not matched_customer:
        print("❌ No matching customer found with that email and password.")
        return
    while True:
        new_password = getpass("Enter new password: ").strip()
        confirm_password = getpass("Confirm new password: ").strip()

        if new_password != confirm_password:
            print("❌ Passwords do not match. Try again.")
        elif new_password == password:
            print("❌ New password cannot be the same as the old password.")
        else:
            break
    matched_customer['Password'] = new_password
    fields = ['CustomerID', 'Name', 'City', 'Phone Number', 'Email', 'Password']  # Adjust keys to your data
    with open(customerFile, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(customers)
    print("✅ Password changed successfully.")


def AdminChangePass():
    global ADMINpassword
    password = getpass("\nEnter current password: ").strip()
    if password != ADMINpassword.strip():
        print("❌ Incorrect current password.")
        return
    while True:
        new_password = getpass("Enter new password: ").strip()
        confirm_password = getpass("Confirm new password: ").strip()
        if new_password != confirm_password:
            print("❌ Passwords do not match. Try again.")
        elif new_password == password:
            print("❌ New password cannot be the same as the old password.")
        else:
            break
    ADMINpassword = new_password
    print("✅ Admin password changed successfully.")


def addProduct():
    global products
    while True:
        writeProductsData()
        products = readProductFile()
        print(f"✅ Product record for {products[-1]['Name']} added successfully.\n")
        more = input("Do you want to add more record? (y/n): ").lower()
        if more == 'n':
            break
        elif more != 'y':
            print("⚠️  : Invalid input! Please enter 'y' or 'n'.")


def delProduct():
    while True:
        delID = input("\nEnter product ID you want to delete: ").strip()
        found = False
        for p in products:
            if delID == p['ID'].strip():
                confirm = input(f"Are you sure you want to delete the record for product {delID}? (y/n): ").lower()
                if confirm == 'y':
                    products.remove(p)
                    # update file
                    with open(productsFile, 'w', newline='') as f:
                        fieldnames = ['ID', 'Name', 'Price', 'Category', 'Description']
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        for p in products:
                            writer.writerow({
                                'ID': p['ID'].strip(),
                                'Name': p['Name'].strip(),
                                'Price': p['Price'].strip(),
                                'Category': p['Category'].strip(),
                                'Description': p['Description'].strip()
                            })
                    print(f"✅ Record for product ID {delID} deleted successfully.")
                else:
                    print("❌ Deletion cancelled.")
                found = True
                break 
        if not found:
            print(f"⚠️  No such product with ID {delID} found.\n")
        more = input("Do you want to delete more records? (y/n): ").lower()
        if more == 'n':
            break
        elif more != 'y':
            print("⚠️  Invalid input! Please enter 'y' or 'n'.\n")


def addCustomer():
    global customers
    print("\nADD A CUSTOMER -\n")
    writeCustomersData()
    customers=readCustomerFile()


def removeCustomer():
    if not customers:
        print("⚠️ No customers available to remove.")
        return
    print("\nREMOVE CUSTOMER:\n")
    try:
        cID = input("Enter customer ID to remove: ").strip()
        customer_to_remove = next((c for c in customers if c['CustomerID'].strip() == cID), None)
        if customer_to_remove:
            confirm = input(f"Are you sure you want to remove customer '{customer_to_remove['Name'].strip()}'? (y/n): ").lower()
            if confirm == 'y':
                customers.remove(customer_to_remove)
                with open(customerFile, 'w', newline='') as f:
                    fieldnames = ['CustomerID', 'Name', 'City', 'Phone Number', 'Email', 'Password']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    for customer in customers:
                        writer.writerow({
                            'CustomerID': customer['CustomerID'].strip(),
                            'Name': customer['Name'].strip(),
                            'City': customer['City'].strip(),
                            'Phone Number': customer['Phone Number'].strip(),
                            'Email': customer['Email'].strip(),
                            'Password': customer['Password'].strip()
                        })
                print(f"✅ Customer ID {cID} removed successfully.")
            else:
                print("❌ Removal cancelled.")
        else:
            print(f"⚠️ No customer found with ID {cID}.")
    except ValueError:
        print("❌ Invalid input. Please enter a numeric Customer ID.")










def guestMenu():
    while True:
        print("\n\nMENU -  ")
        print("1. View all products")
        print("2. View by category")
        print("3. Search products")
        print("4. Exit")
        try:
            choice=int(input("\nEnter choice: "))
            if choice==1:
                viewProducts()
            elif choice==2:
                viewByCategory()
            elif choice==3:
                searchProduct()
            elif choice==4:
                print("😊 Thank you for visiting as guest😊")
                break
            else:
                print("⚠️  : Invalid choice!")
        except ValueError:
            print("⚠️  : Input only numeric value.")


def CustomerMenu():
    loginStatus=loginCustomer()
    if loginStatus == -1 or loginStatus is None:
        return
    loginStatus, login_time = loginStatus
    while True:
        print("\n\nMENU -  ")
        print("1. View all products")
        print("2. View by category")
        print("3. Search products")
        print("4. Add to cart")
        print("5. Order online")  
        print("6. Cancel order")  
        print("7. Wishlist")  
        print("8. Order History")  
        print("9. Change Password")
        print("10. Exit")
        try:
            choice=int(input("\nEnter choice: "))
            if choice==1:
                viewProducts()
            elif choice==2:
                viewByCategory()
            elif choice==3:
                searchProduct()
            elif choice==4:
                while True:
                    CartMenu()
                    try:
                        cartChoice = int(input("\nEnter your choice: "))
                        if cartChoice == 1:
                            viewCart(loginStatus)
                        elif cartChoice == 2:
                            addToCart(loginStatus)
                        elif cartChoice == 3:
                            removeFromCart(loginStatus)
                        elif cartChoice == 4:
                            break
                        else:
                            print("⚠️ Invalid choice.")
                    except ValueError:
                        print("⚠️ Enter numeric values only.")
            elif choice==5:
                order(loginStatus)
            elif choice==6:
                cancelOrder(loginStatus)
            elif choice==7:
                while True:
                    wishlistMenu()
                    try:
                        wishchoice = int(input("\nEnter your choice: "))
                        if wishchoice == 1:
                            viewWishlist(loginStatus)
                        elif wishchoice == 2:
                            addToWishlist(loginStatus)
                        elif wishchoice == 3:
                            removeFromWishlist(loginStatus)
                        elif wishchoice == 4:
                            break
                        else:
                            print("⚠️ Invalid choice.")
                    except ValueError:
                        print("⚠️ Enter numeric values only.")
            elif choice==8:
                viewMyOrders(loginStatus)
            elif choice==9:
                changePass()
                input("Press Enter to continue...")  # Pause to let user read the message
            elif choice==10:
                print("😊 Thank you for visiting😊")
                logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fields=['CustomerID', 'Name', 'Login Time', 'LogoutTime']
                with open(loginLogoutFile, 'a', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=fields)
                    if not os.path.exists(loginLogoutFile) or os.path.getsize(loginLogoutFile) == 0:
                        writer.writeheader()
                    writer.writerow({
                        'CustomerID': loginStatus['CustomerID'],
                        'Name': loginStatus['Name'],
                        'Login Time': f"{login_time}",
                        'LogoutTime': f"{logout_time}"
                    })
                break
            else:
                print("⚠️  : Invalid choice!")
        except ValueError:
            print("⚠️  : Input only numeric value.")


def AdminMenu():
    loginStatus=adminLogin()
    if loginStatus != -1:
        while True:
            print("\n\nMENU -  ")
            print("1. View all products")
            print("2. View by category")
            print("3. Search products")
            print("4. View Customers List")
            print("5. Add a product")
            print("6. Remove a product")
            print("7. Add a customer")
            print("8. Remove a customer")
            print("9. Order History of all customers")  
            print("10. Change Password")
            print("11. Exit")
            try:
                choice=int(input("\nEnter choice: "))
                if choice==1:
                    viewProducts()
                elif choice==2:
                    viewByCategory()
                elif choice==3:
                    searchProduct()
                elif choice==4:
                    viewCustomers()
                elif choice==5:
                    addProduct()
                    print(products)
                elif choice==6:
                    delProduct()
                elif choice==7:
                    addCustomer()
                elif choice==8:
                    removeCustomer()
                elif choice==9:
                    viewAllOrders()
                elif choice==10:
                    AdminChangePass()
                elif choice==11:
                    print("😊 Thank you for visiting😊")
                    break
                else:
                    print("⚠️  : Invalid choice!")
            except ValueError:
                print("⚠️  : Input only numeric value.")


def mainMenu():
    print("\nOrder Food Online\n")
    print("1️⃣  Guest user\n2️⃣  Register Customer\n3️⃣  Customer Login\n4️⃣  Admin Login\n5️⃣  Exit")
        
def main():
    readProductFile()
    readCustomerFile()
    print("\n\n----------------😊 Welcome😊 --------------")
    while(True):
        mainMenu()
        try:
            choice=int(input("\nEnter your choice: "))
            if choice==1:
                guestMenu()
            elif choice==2:
                registerCustomer()
            elif choice==3:
                CustomerMenu()
            elif choice==4:
                AdminMenu()
            elif choice==5:
                print("😊 Thank you for using this portal!😊\n")
                break
            else:
                print("⚠️  : Invalid choice!")
        except ValueError:
            print("⚠️  : Input only numeric value.")


main()