from services.cart_service import CartService
from services.product_service import ProductService


class CartMenu:

    def __init__(self):
        self.cart_service = CartService()
        self.product_service = ProductService()

    def show(self, loginStatus):

        while True:

            print("\nCart Menu:")
            print("1. View Cart")
            print("2. Add to Cart")
            print("3. Remove from Cart")
            print("4. Back to Main Menu")
            try:
                choice = int(input("\nEnter choice: "))
                if choice == 1:
                    self.cart_service.viewCart(loginStatus)

                elif choice == 2:
                    products = self.product_service.readProductFile()
                    self.cart_service.addToCart(loginStatus, products)

                elif choice == 3:
                    self.cart_service.removeFromCart(loginStatus)

                elif choice == 4:
                    break

                else:
                    print("⚠️ Invalid choice!")

            except ValueError:
                print("⚠️ Enter numeric value only.")