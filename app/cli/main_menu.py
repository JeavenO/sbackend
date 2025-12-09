from app.db import SessionLocal
from app.models import Category, Product, Order

def main_menu():
    while True:
        print("\n=== SMART AGRO INVENTORY SYSTEM ===")
        print("1. View Categories")
        print("2. Add Category")
        print("3. View Products")
        print("4. Add Product")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            view_categories()

        elif choice == "2":
            add_category()

        elif choice == "3":
            view_products()

        elif choice == "4":
            add_product()

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")


def view_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    print("\n--- Categories ---")
    for c in categories:
        print(f"{c.id}. {c.name} - {c.description}")
    db.close()


def add_category():
    db = SessionLocal()
    name = input("Category name: ")
    desc = input("Description: ")

    new_cat = Category(name=name, description=desc)
    db.add(new_cat)
    db.commit()
    print("Category added successfully!")
    db.close()


def view_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print("\n--- Products ---")
    for p in products:
        print(f"{p.id}. {p.name} | {p.price} | Stock:{p.stock}")
    db.close()


def add_product():
    db = SessionLocal()
    name = input("Product name: ")
    price = float(input("Price: "))
    stock = int(input("Stock: "))
    category_id = int(input("Category ID: "))

    new_product = Product(
        name=name, price=price, stock=stock, category_id=category_id
    )
    db.add(new_product)
    db.commit()
    print("Product added!")
    db.close()

