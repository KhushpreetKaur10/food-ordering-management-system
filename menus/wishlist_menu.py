from services.wishlist_service import WishlistService


class WishlistMenu:

    def __init__(self):
        self.wishlist_service = WishlistService()

    def show(self, loginStatus):
        while True:
            print("\nWishlist Menu:")
            print("1. View Wishlist")
            print("2. Add to Wishlist")
            print("3. Remove from Wishlist")
            print("4. Back to Main Menu")
            try:
                choice = int(input("\nEnter choice: "))
                if choice == 1:
                    self.wishlist_service.viewWishlist(loginStatus)
                elif choice == 2:
                    self.wishlist_service.addToWishlist(loginStatus)
                elif choice == 3:
                    self.wishlist_service.removeFromWishlist(loginStatus)
                elif choice == 4:
                    break
                else:
                    print("⚠️ Invalid choice!")
            except ValueError:
                print("⚠️ Enter numeric value only.")