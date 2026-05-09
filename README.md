# 🍔 Online Food Ordering and Management System

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Architecture](https://img.shields.io/badge/Architecture-OOP%20%7C%20Service%20Layer-2EA44F)
![Storage](https://img.shields.io/badge/Storage-CSV-F39C12)
![Interface](https://img.shields.io/badge/Interface-CLI-6F42C1)
![Status](https://img.shields.io/badge/Status-Stable-2EA44F)
![Maintained](https://img.shields.io/badge/Maintained-Yes-success)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

A modular **command-line food ordering and management system** built using **Python**.

This project follows a **production-style service-oriented architecture** with clear separation of **models**, **services**, **menus**, and **utilities**.

The system allows customers to browse products, manage carts and wishlists, place orders, simulate payments, and view order history. Administrators can manage products, customers, and monitor orders.

---

## 🚀 Highlights

- Modular **OOP architecture** - inheritance, encapsulation, abstraction and polymorphism
- Clean **service-layer design**
- Persistent storage using **CSV files**
- Secure password input with **getpass**
- Search analytics using **Counter**
- Ready for future migration to **database-backed systems**

---

## 👤 Customer Features

- Customer registration with automatic password generation
- Secure login using **phone number** or **email**
- Browse all products
- View products by category
- Search products with search history tracking
- Add products to cart
- Remove products from cart
- View cart contents
- Wishlist management
- Place orders from cart
- Simulated payment processing
- Cancel orders
- View personal order history
- Change account password

---

## 🛠 Admin Features

- Secure admin login
- View all products
- View products by category
- Search products
- Add new products
- Remove products
- View all registered customers
- Add customers
- Remove customers
- View complete order history

---

## 🧱 OOP Design Principles

| OOP Concept | Where Used |
|-------------|------------|
| **Encapsulation** | Business logic is contained inside the `services/` layer, while data structures are defined inside `models/` |
| **Inheritance** | `Customer` and `Admin` inherit common properties from the base `User` model |
| **Abstraction** | Menu classes interact with service methods without needing internal implementation details |
| **Polymorphism** | Different service objects expose different behaviors through consistent method-style interactions |

---

## 🏗 Architecture Diagram

```text
                ┌──────────────────┐
                │     main.py      │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │      Menus       │
                │  (CLI navigation)│
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │    Services      │
                │ (business logic) │
                └────────┬─────────┘
                         │
          ┌──────────────┴──────────────┐
          ▼                             ▼
 ┌──────────────────┐         ┌──────────────────┐
 │      Models      │         │      Utils       │
 │  (data objects)  │         │ helpers/validate │
 └────────┬─────────┘         └────────┬─────────┘
          └──────────────┬─────────────┘
                         ▼
                ┌──────────────────┐
                │    CSV Files      │
                │  persistent data  │
                └──────────────────┘
```

---

## 🔄 Workflow Diagram

```text
Main Menu
   │
   ├── Guest User
   │      └── Browse Products
   │
   ├── Register Customer
   │
   ├── Customer Login
   │      │
   │      ├── Browse Products
   │      ├── Search Products
   │      ├── Cart
   │      ├── Wishlist
   │      ├── Order Placement
   │      └── Order History
   │
   └── Admin Login
          │
          ├── Product Management
          ├── Customer Management
          └── Order Monitoring
```

---

## ⚙️ Technologies Used

- **Python 3**
- **Object-Oriented Programming**
- **CSV file persistence**
- **Regular Expressions**
- **Datetime**
- **Collections (`Counter`)**
- **Text formatting**
- **getpass**

---

## 💾 Data Persistence

The application uses **CSV files** as lightweight persistent storage.

### Stored files

- `customers.csv`
- `customerPass.csv`
- `login.csv`
- `products.csv`
- `orders.csv`
- `cart.csv`
- `wishlist.csv`
- `searches.csv`

This allows the system to preserve data between runs without requiring an external database.

---

## 📂 Project Structure

```text
food_ordering_system/
│
├── main.py
│
├── config/
│   └── settings.py
│
├── models/
│   ├── user.py
│   ├── customer.py
│   ├── admin.py
│   ├── product.py
│   ├── order.py
│   ├── cart.py
│   └── wishlist.py
│
├── services/
│   ├── auth_service.py
│   ├── product_service.py
│   ├── cart_service.py
│   ├── order_service.py
│   ├── wishlist_service.py
│   └── customer_service.py
│
├── utils/
│   ├── validators.py
│   ├── helpers.py
│   └── file_handler.py
│
├── menus/
│   ├── main_menu.py
│   ├── customer_menu.py
│   ├── admin_menu.py
│   ├── guest_menu.py
│   ├── cart_menu.py
│   └── wishlist_menu.py
│
└── data/
    ├── customers.csv
    ├── customerPass.csv
    ├── login.csv
    ├── products.csv
    ├── orders.csv
    ├── cart.csv
    ├── wishlist.csv
    └── searches.csv
```

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/KhushpreetKaur10/food-ordering-management-system.git
```

### 2. Move into the project directory

```bash
cd food-ordering-management-system
```

### 3. Run the application

```bash
python main.py
```

---

## 🧪 Example CLI

```text
---------------- 😊 Welcome 😊 ----------------

1️⃣ Guest User
2️⃣ Register Customer
3️⃣ Customer Login
4️⃣ Admin Login
5️⃣ Exit
```

---

## ✅ Engineering Goals

- Clean modular structure
- Stable service-layer architecture
- Separation of concerns
- Reliable CSV persistence
- Easy future migration to database-backed systems

---

## 🔮 Future Improvements

- Flask / Django web version
- MySQL / PostgreSQL integration
- Password hashing
- Stock management
- Order status tracking
- Admin analytics dashboard
- Recommendation engine
- REST API version

---

## 👩‍💻 Author

**Khushpreet Kaur**

GitHub: **https://github.com/KhushpreetKaur10**
