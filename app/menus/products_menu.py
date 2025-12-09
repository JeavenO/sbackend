from app.db import SessionLocal
from app.models import Product, Category

def products_menu():
    while True:
        print("\n--- PRODUCTS MENU ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Stock")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        session = SessionLocal()

        if choice == "1":
            name = input("Product name: ").strip()

            if not name:
                print("Name cannot be empty.")
                continue

            try:
                price = float(input("Price: ").strip())
                stock = int(input("Stock: ").strip())
            except ValueError:
                print("Price and stock must be numbers.")
                continue

            print("Available categories:")
            categories = session.query(Category).all()

            if not categories:
                print("No categories available! Create a category first.")
                continue

            for c in categories:
                print(f"{c.id}. {c.name}")

            cat_id = input("Choose category ID: ").strip()
            if not cat_id.isdigit():
                print("Invalid category ID.")
                continue

            product = Product(
                name=name,
                price=price,
                stock=stock,
                category_id=int(cat_id)
            )

            session.add(product)
            session.commit()
            print("Product added successfully.")

        elif choice == "2":
            products = session.query(Product).all()
            print("\nProducts:")
            if not products:
                print("No products found.")
            for p in products:
                print(f"- {p.id}: {p.name} (${p.price}) Stock: {p.stock}")

        elif choice == "3":
            prod_id = input("Product ID: ").strip()
            if not prod_id.isdigit():
                print("Invalid ID.")
                continue

            product = session.query(Product).get(int(prod_id))
            if not product:
                print("Product not found.")
                continue

            try:
                amount = int(input("New stock amount: ").strip())
            except ValueError:
                print("Stock must be a number.")
                continue

            product.stock = amount
            session.commit()
            print("Stock updated.")

        elif choice == "4":
            session.close()
            break

        else:
            print("Invalid choice.")

        session.close()

