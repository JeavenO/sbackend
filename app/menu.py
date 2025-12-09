from app.menus.categories_menu import categories_menu
from app.menus.products_menu import products_menu
from app.menus.orders_menu import orders_menu

def main_menu():
    while True:
        print("\n=== Main Menu ===")
        print("1. Categories")
        print("2. Products")
        print("3. Orders")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            categories_menu()
        elif choice == "2":
            products_menu()
        elif choice == "3":
            orders_menu()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main_menu()
