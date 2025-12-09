from app.db import SessionLocal
from app.models import Product, Category

def products_menu():
    while True:
        print("\n--- PRODUCTS MENU ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Stock")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ")
        session = SessionLocal()

        if choice == "1":
            name = input("Product name: ")
            price = float(input("Price: "))
            stock = int(input("Stock: "))

            print("Available categories:")
            for c in session.query(Category).all():
                print(f"{c.id}. {c.name}")

            category_id = int(input("Choose category ID: "))

            product = Product(
                name=name,
                price=price,
                stock=stock,
                category_id=category_id
            )
            session.add(product)
            session.commit()
            print("Product added.")

        elif choice == "2":
            products = session.query(Product).all()
            print("\nProducts:")
            for p in products:
                print(f"- {p.id}: {p.name} (${p.price}) Stock: {p.stock}")

        elif choice == "3":
            prod_id = int(input("Product ID: "))
            product = session.query(Product).get(prod_id)

            if product:
                amount = int(input("New stock amount: "))
                product.stock = amount
                session.commit()
                print("Stock updated.")
            else:
                print("Product not found.")

        elif choice == "4":
            session.close()
            break

        else:
            print("Invalid choice.")

        session.close()
