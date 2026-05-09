from services.auth_service import AuthService
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.order_service import OrderService


class AdminMenu:

    def __init__(self):

        self.auth_service = AuthService()
        self.product_service = ProductService()
        self.customer_service = CustomerService()
        self.order_service = OrderService()

    def show(self):

        loginStatus=self.auth_service.adminLogin() 
        if loginStatus != -1:

            while True:

                print("\n\nADMIN MENU")
                print("1. View all products")
                print("2. View by category")
                print("3. Search products")
                print("4. View customers")
                print("5. Add product")
                print("6. Remove product")
                print("7. Add customer")
                print("8. Remove customer")
                print("9. Order history of all customers")
                print("10. Change admin password")
                print("11. Exit")

                try:
                    choice = int(input("\nEnter choice: "))
                    if choice == 1:
                        self.product_service.viewProducts()
                    elif choice == 2:
                        self.product_service.viewByCategory()
                    elif choice == 3:
                        self.product_service.searchProduct()
                    elif choice == 4:
                        self.customer_service.viewCustomers()
                    elif choice == 5:
                        self.product_service.addProduct()
                    elif choice == 6:
                        self.product_service.delProduct()
                    elif choice == 7:
                        self.customer_service.addCustomer()
                    elif choice == 8:
                        self.customer_service.removeCustomer()
                    elif choice == 9:
                        self.order_service.viewAllOrders()
                    elif choice == 10:
                        self.auth_service.AdminChangePass()
                    elif choice == 11:
                        print("😊 Thank you Admin 😊")
                        break
                    else:
                        print("⚠️ Invalid choice!")
                except ValueError:
                    print("⚠️ Input only numeric value.")