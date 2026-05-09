import csv
from datetime import datetime
from config.settings import LOGIN_LOGOUT_FILE
import os
from models import customer
from services.auth_service import AuthService
from services.product_service import ProductService
from services.cart_service import CartService
from services.order_service import OrderService
from services.wishlist_service import WishlistService
from menus.cart_menu import CartMenu
from menus.wishlist_menu import WishlistMenu


class CustomerMenu:

    def __init__(self):

        self.auth_service = AuthService()
        self.product_service = ProductService()
        self.cart_service = CartService()
        self.order_service = OrderService()
        self.wishlist_service = WishlistService()
        self.wishlist_menu = WishlistMenu()
        self.cart_menu = CartMenu()


    # =====================================
    # MAIN MENU
    # =====================================

    def show(self):
        self.auth_service = AuthService()
        loginStatus = self.auth_service.loginCustomer()
        if loginStatus == -1 or loginStatus is None:
            return
        loginStatus, login_time = loginStatus

        while True:
            print("\n\nMENU - CUSTOMER")
            print("1. View all products")
            print("2. View by category")
            print("3. Search products")
            print("4. Go to Cart")
            print("5. Order online")
            print("6. Cancel order")
            print("7. Wishlist")
            print("8. Order History")
            print("9. Change Password")
            print("10. Exit")

            try:
                choice = int(input("\nEnter choice: "))
                if choice == 1:
                    self.product_service.viewProducts()
                elif choice == 2:
                    self.product_service.viewByCategory()
                elif choice == 3:
                    self.product_service.searchProduct()
                elif choice == 4:
                    self.cart_menu.show(loginStatus)
                elif choice == 5:
                    self.order_service.order(loginStatus)
                elif choice == 6:
                    self.order_service.cancelOrder(loginStatus)
                elif choice == 7:
                    self.wishlist_menu.show(loginStatus)
                elif choice == 8:
                    self.order_service.viewMyOrders(loginStatus)
                elif choice == 9:
                    self.auth_service.changePass(loginStatus)
                    input("Press Enter to continue...")
                elif choice == 10:
                    print("😊 Thank you for visiting 😊")
                    logout_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    fields=['CustomerID', 'Name', 'Login Time', 'LogoutTime']
                    with open(LOGIN_LOGOUT_FILE, 'a', newline='') as f:
                        writer = csv.DictWriter(f, fieldnames=fields)
                        if not os.path.exists(LOGIN_LOGOUT_FILE) or os.path.getsize(LOGIN_LOGOUT_FILE) == 0:
                            writer.writeheader()
                        writer.writerow({
                            'CustomerID': loginStatus.customer_id,
                            'Name': loginStatus.name,
                            'Login Time': f"{login_time}",
                            'LogoutTime': f"{logout_time}"
                        })
                    break

                else:
                    print("⚠️ Invalid choice!")

            except ValueError:
                print("⚠️ Input only numeric value.")

