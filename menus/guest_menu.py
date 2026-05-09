from services.product_service import ProductService

class GuestMenu:
    def __init__(self):
        self.product_service = ProductService()

    def show(self):
        while True:
            print("\n\nGUEST MENU")
            print("1. View all products")
            print("2. View by category")
            print("3. Search products")
            print("4. Exit")
            try:
                choice = int(input("\nEnter choice: "))
                if choice == 1:
                    self.product_service.viewProducts()
                elif choice == 2:
                    self.product_service.viewByCategory()
                elif choice == 3:
                    self.product_service.searchProduct()
                elif choice == 4:
                    print("😊 Thank you for visiting 😊")
                    break
                else:
                    print("⚠️ Invalid choice!")
            except ValueError:
                print("⚠️ Please enter numeric value only.")