from app.db import SessionLocal
from app.models import Category

def categories_menu():
    while True:
        print("\n--- CATEGORY MENU ---")
        print("1. Create Category")
        print("2. View Categories")
        print("3. Delete Category")
        print("4. Back to Main Menu")

        choice = input("Choose an option: ").strip()
        session = SessionLocal()

        if choice == "1":
            name = input("Category name: ").strip()
            description = input("Description: ").strip()

            if not name:
                print("Name cannot be empty.")
                continue

            category = Category(name=name, description=description)
            session.add(category)
            session.commit()
            print("Category added successfully.")

        elif choice == "2":
            categories = session.query(Category).all()
            print("\nCategories:")
            if not categories:
                print("No categories found.")
            for c in categories:
                print(f"- {c.id}: {c.name} ({c.description})")

        elif choice == "3":
            cat_id = input("Enter category ID to delete: ").strip()

            if not cat_id.isdigit():
                print("Invalid ID. Please enter a number.")
                continue

            category = session.query(Category).get(int(cat_id))

            if category:
                session.delete(category)
                session.commit()
                print("Category deleted.")
            else:
                print("Category not found.")

        elif choice == "4":
            session.close()
            break

        else:
            print("Invalid choice.")

        session.close()

