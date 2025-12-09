from fastapi import FastAPI
from routes.categories import router as categories_router
from routes.products import router as products_router
from routes.orders import router as orders_router

app = FastAPI()

app.include_router(categories_router, prefix="/categories", tags=["Categories"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])


from app.menus.categories_menu import categories_menu
from app.menus.products_menu import products_menu
from app.menus.orders_menu import orders_menu

def main_menu():
    while True:
        print("\n=== SMART AGRO INVENTORY SYSTEM ===")
        print("1. Manage Categories")
        print("2. Manage Products")
        print("3. Manage Orders")
        print("4. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            categories_menu()
        elif choice == "2":
            products_menu()
        elif choice == "3":
            orders_menu()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()

