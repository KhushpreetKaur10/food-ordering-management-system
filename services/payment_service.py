def process_payment(amount):

    print("\nChoose payment method:")
    print("1. UPI")
    print("2. Card")
    print("3. COD")

    while True:

        try:
            choice = int(input("\nEnter choice: "))

            if choice in [1, 2, 3]:
                break

            print("❌ Invalid choice")

        except ValueError:
            print("❌ Enter number only")

    if choice == 1:
        input("Enter UPI ID: ")
        print("Processing UPI...")

    elif choice == 2:
        input("Enter card number: ")
        print("Processing card...")

    else:
        print("Cash on Delivery selected")

    print(f"✅ Payment ₹{amount} successful")
    return True