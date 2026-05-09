import csv
import os
from config.settings import CUSTOMERS_FILE, CUSTOMER_PASSWORD_FILE
from utils.validators import is_valid_email, is_valid_phone
from utils.helpers import get_next_id, generatePass
from models.customer import Customer


class CustomerService:

    def __init__(self):
        self.customers = self.readCustomerFile()

   
    def readCustomerFile(self):

        customers = []

        if not os.path.exists(CUSTOMERS_FILE):
            return customers

        with open(CUSTOMERS_FILE, "r", newline="") as f:

            reader = csv.DictReader(f)

            for row in reader:
                customers.append(
                    Customer(
                        name=row["Name"].strip(),
                        password=row["Password"].strip(),
                        customer_id=row["CustomerID"].strip(),
                        city=row["City"].strip(),
                        phone=row["Phone Number"].strip(),
                        email=row["Email"].strip()
                    )
                )

        return customers


    def writeAllCustomers(self):

        fields = [
            "CustomerID",
            "Name",
            "City",
            "Phone Number",
            "Email",
            "Password"
        ]

        with open(CUSTOMERS_FILE, "w", newline="") as f:

            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()

            for c in self.customers:
                writer.writerow({
                    "CustomerID": c.customer_id,
                    "Name": c.name,
                    "City": c.city,
                    "Phone Number": c.phone,
                    "Email": c.email,
                    "Password": c.password
                })

    # =====================================
    # ADD CUSTOMER (INPUT + VALIDATION)
    # =====================================

    def writeCustomersData(self):

        print("\nENTER CUSTOMER DETAILS -\n")

        name = input("Name: ").strip()
        city = input("City: ").strip()

        while True:
            phone = input("Phone number: ").strip()
            if is_valid_phone(phone):
                break
            print("❌ Invalid phone number (must be 10 digits).")

        while True:
            email = input("Email: ").strip()
            if is_valid_email(email):
                break
            print("❌ Invalid email format.")

        existing = next(
            (
                c for c in self.customers
                if c.phone == phone or c.email.lower() == email.lower()
            ),
            None
        )

        if existing:
            print("⚠️ Customer already exists.")
            return -1

        password = generatePass()

        with open(CUSTOMER_PASSWORD_FILE, "w", newline="") as f:
            csv.writer(f).writerow([password])

        print("\n✅ Customer registered successfully.")
        print("🔐 Password saved to local file. Check your system file.")

        new_customer = Customer(
            name=name,
            password=password,
            customer_id=str(get_next_id(CUSTOMERS_FILE)),
            city=city,
            phone=phone,
            email=email
        )

        self.customers.append(new_customer)
        self.writeAllCustomers()

    # =====================================
    # ADD CUSTOMER WRAPPER
    # =====================================

    def addCustomer(self):
        print("\nADD CUSTOMER\n")
        self.writeCustomersData()

    # =====================================
    # REMOVE CUSTOMER
    # =====================================

    def removeCustomer(self):

        if not self.customers:
            print("⚠️ No customers available.")
            return

        c_id = input("\nEnter customer ID: ").strip()

        customer = next(
            (c for c in self.customers if c.customer_id == c_id),
            None
        )

        if not customer:
            print(f"⚠️ No customer found with ID {c_id}.")
            return

        confirm = input(f"Delete {customer.name}? (y/n): ").strip().lower()

        if confirm != "y":
            print("❌ Cancelled.")
            return

        self.customers.remove(customer)
        self.writeAllCustomers()

        print(f"✅ Customer {c_id} removed.")



    def viewCustomers(self):

        if not self.customers:
            print("📭 No customers found.")
            return

        print("\nALL CUSTOMERS\n")
        print("-" * 120)

        print("{:<10} {:<15} {:<20} {:<15} {:<25} {:<15}".format(
            "ID", "Name", "City", "Phone", "Email", "Password"
        ))

        print("-" * 120)

        for c in self.customers:
            print("{:<10} {:<15} {:<20} {:<15} {:<25} {:<15}".format(
                c.customer_id,
                c.name,
                c.city,
                c.phone,
                c.email,
                c.password
            ))

        print("-" * 120)



    def registerCustomer(self):

        print("\n----------- Customer Registration -----------")

        register = self.writeCustomersData()

        if register == -1:
            print("⚠️ Customer already registered. Please login instead.\n")

            wantLogin = input("Do you want to login? (y/n): ").strip().lower()

            if wantLogin == "y":
                from services.auth_service import AuthService
                auth = AuthService()
                auth.loginCustomer()

            return

        self.customers = self.readCustomerFile()