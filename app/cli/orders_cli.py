from app.db import SessionLocal
from app.models import Product, Order, OrderItem

def orders_menu():
    while True:
        print("\n--- ORDERS MENU ---")
        print("1. Place Order")
        print("2. View Orders")
        print("3. Back to Main Menu")

        choice = input("Choose: ")
        session = SessionLocal()

        if choice == "1":
            customer = input("Customer name: ")
            order = Order(customer_name=customer)
            session.add(order)
            session.commit()

            while True:
                print("\nAvailable products:")
                for p in session.query(Product).all():
                    print(f"{p.id}. {p.name} (${p.price}) Stock: {p.stock}")

                prod_id = input("Enter product ID (or 'done' to finish): ")

                if prod_id.lower() == "done":
                    break

                product = session.query(Product).get(int(prod_id))
                qty = int(input("Quantity: "))

                if qty > product.stock:
                    print("Not enough stock.")
                    continue

                subtotal = qty * product.price
                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    subtotal=subtotal
                )
                product.stock -= qty

                session.add(item)
                session.commit()

            print("Order completed.")

        elif choice == "2":
            orders = session.query(Order).all()
            for o in orders:
                print(f"\nOrder {o.id} - {o.customer_name}")
                for item in o.order_items:
                    print(f"  - {item.product.name} x{item.quantity} = ${item.subtotal}")

        elif choice == "3":
            session.close()
            break

        else:
            print("Invalid choice.")

        session.close()
