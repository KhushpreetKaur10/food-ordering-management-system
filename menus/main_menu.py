from menus.guest_menu import GuestMenu
from menus.customer_menu import CustomerMenu
from menus.admin_menu import AdminMenu
from services.customer_service import CustomerService
from services.auth_service import AuthService


class MainMenu:
    
    # Create menu objects once (better OOP practice)
    def __init__(self):
        self.auth_service = AuthService()
        self.customer_service = CustomerService()
        self.guest_menu = GuestMenu()
        self.customer_menu = CustomerMenu()
        self.admin_menu = AdminMenu()


    def show_main_menu(self):
        print("\nOrder Food Online\n")
        print("1️⃣ Guest User")
        print("2️⃣ Register Customer")
        print("3️⃣ Customer Login")
        print("4️⃣ Admin Login")
        print("5️⃣ Exit")


    def start(self):
        print("\n\n---------------- 😊 Welcome 😊 ----------------")
        while True:
            self.show_main_menu()
            try:
                choice = int(input("\nEnter your choice: "))
                if choice == 1:
                    self.guest_menu.show()
                elif choice == 2:
                    self.customer_service.registerCustomer()
                elif choice == 3:
                    self.customer_menu.show()
                elif choice == 4:
                    self.admin_menu.show()
                elif choice == 5:
                    print("😊 Thank you for using this portal! 😊\n\n")
                    break
                else:
                    print("⚠️ Invalid choice!")
            except ValueError:
                print("⚠️ Input only numeric value.")
