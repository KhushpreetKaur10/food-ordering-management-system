import csv
import os
from getpass import getpass
from datetime import datetime

from config.settings import (
    CUSTOMERS_FILE,
    LOGIN_LOGOUT_FILE,
    ADMIN_USERNAME,
    ADMIN_PASSWORD
)

from models.customer import Customer
from models.admin import Admin
from utils.helpers import get_next_id, generatePass
from utils.validators import is_valid_email, is_valid_phone


class AuthService:

    def __init__(self):
        self.admin = Admin(name=ADMIN_USERNAME, password=ADMIN_PASSWORD)
        self.customers = self._load_customers()


    # purpose: read all customer records from a CSV file and store them in a list and create customer objects.
    def _load_customers(self):
        if not os.path.exists(CUSTOMERS_FILE):
            return []
        customers = []
        with open(CUSTOMERS_FILE, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    customers.append(Customer(
                        name=row.get("Name", "").strip(),
                        password=row.get("Password", "").strip(),
                        customer_id=row.get("CustomerID", "").strip(),
                        city=row.get("City", "").strip(),
                        phone=row.get("Phone Number", "").strip(),
                        email=row.get("Email", "").strip()
                    ))
                except:
                    continue
        return customers

    # When _load_customers() reads the CSV and creates Customer objects, _save_customers() takes those Customer objects and writes them back into the file.
    def _save_customers(self):
        fields = ["CustomerID", "Name", "City", "Phone Number", "Email", "Password"]

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



    def loginCustomer(self):
        # Reload customers from disk before each login attempt so newly registered users are recognized.
        self.customers = self._load_customers()

        if not os.path.exists(LOGIN_LOGOUT_FILE):
            with open(LOGIN_LOGOUT_FILE, 'w', newline='') as f:
                pass
        
        print("\nCUSTOMER LOGIN PORTAL:\n")
        while True:
            choice = int(input("How do you want to login?\n1. With phone number\n2. With email\n\nEnter choice: "))
            if choice not in [1, 2]:
                print("⚠️ Invalid choice! Please enter 1 or 2.\n")
            else:
                break

        matched_customer = None
        
        if choice == 1:
            while True:
                phone = input("Enter your phone number: ").strip()
                if is_valid_phone(phone):
                    break
                else:
                    print("❌ Invalid phone number. Must be 10 digits. Please try again.\n")
            
            matched_customer = next((c for c in self.customers if phone == c.phone.strip()), None)
            
            if not matched_customer:
                print("⚠️ Phone number is not registered.")
                wantRegister = input("Do you want to register? (y/n): ")
                if wantRegister.lower() == 'y':
                    name = input("Enter name: ").strip()
                    city = input("Enter city: ").strip()
                    email = input("Enter email: ").strip()
                    self.registerCustomer(name, city, phone, email)
                return -1
            
            while True:
                loginPass = getpass("Enter password: ").strip()
                if loginPass == matched_customer.password.strip():
                    print("✅ Login successful.\n")
                    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return matched_customer, login_time
                else:
                    print("⚠️ Incorrect credentials! Please try again.\n")
        
        elif choice == 2:
            while True:
                email = input("Enter your email: ").strip()
                if is_valid_email(email):
                    break
                else:
                    print("⚠️ Invalid email. Please try again.\n")
            
            matched_customer = next((c for c in self.customers if email.lower() == c.email.lower().strip()), None)
            
            if not matched_customer:
                print("⚠️ Email is not registered.")
                wantRegister = input("Do you want to register? (y/n): ")
                if wantRegister.lower() == 'y':
                    name = input("Enter name: ").strip()
                    city = input("Enter city: ").strip()
                    phone = input("Enter phone: ").strip()
                    self.registerCustomer(name, city, phone, email)
                return -1
            
            while True:
                loginPass = getpass("Enter password: ").strip()
                if loginPass == matched_customer.password.strip():
                    print("✅ Login successful.\n")
                    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    return matched_customer, login_time
                else:
                    print("⚠️ Incorrect credentials! Please try again.\n")



    def adminLogin(self):
        print("\nADMIN LOGIN PORTAL:\n")
        username = input("Admin username: ").strip()
        password = getpass("Admin password: ")

        if username == self.admin.name and password == self.admin.password:
            print("✅ Admin login successful")
            return True
        
        print("❌ Invalid admin credentials")
        return -1



    def registerCustomer(self, name, city, phone, email):

        if not is_valid_phone(phone):
            print("❌ Invalid phone")
            return

        if not is_valid_email(email):
            print("❌ Invalid email")
            return

        exists = next(
            (c for c in self.customers if c.phone == phone or c.email == email),
            None
        )

        if exists:
            print("⚠️ Customer already exists")
            return

        password = generatePass()

        customer = Customer(
            name=name,
            password=password,
            customer_id=str(get_next_id(CUSTOMERS_FILE)),
            city=city,
            phone=phone,
            email=email
        )

        self.customers.append(customer)
        self._save_customers()

        print("✅ Registered successfully")
        print("🔐 Password:", password)



    def changePass(self, customer):
        old = getpass("Old password: ")

        if old != customer.password:
            print("❌ Incorrect password")
            return

        new = getpass("New password: ")

        if new == old:
            print("❌ New password cannot be the same as the old password.")
            return

        customer.password = new
        self._save_customers()

        print("✅ Password updated")



    def AdminChangePass(self):
        password = getpass("\nEnter current password: ").strip()
        if password != self.admin.password.strip():
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
        self.admin.password = new_password
        print("✅ Admin password changed successfully.")
