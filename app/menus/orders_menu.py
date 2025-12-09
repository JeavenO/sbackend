from app.db import SessionLocal
from app.models import Product, Order, OrderItem

def orders_menu():
    while True:
        print("\n--- ORDERS MENU ---")
        print("1. Place Order")
        print("2. View Orders")
        print("3. Back to Main Menu")

        choice = input("Choose: ").strip()
        session = SessionLocal()

        if choice == "1":
            customer = input("Customer name: ").strip()

            if not customer:
                print("Customer name required.")
                continue

            order = Order(customer_name=customer)
            session.add(order)
            session.commit()

            while True:
                print("\nAvailable products:")
                products = session.query(Product).all()

                if not products:
                    print("No products available.")
                    break

                for p in products:
                    print(f"{p.id}. {p.name} (${p.price}) Stock: {p.stock}")

                prod_id = input("Enter product ID (or 'done' to finish): ").strip()

                if prod_id.lower() == "done":
                    break

                if not prod_id.isdigit():
                    print("Invalid ID.")
                    continue

                product = session.query(Product).get(int(prod_id))

                if not product:
                    print("Product not found.")
                    continue

                try:
                    qty = int(input("Quantity: ").strip())
                except ValueError:
                    print("Quantity must be a number.")
                    continue

                if qty <= 0:
                    print("Quantity must be positive.")
                    continue

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
            if not orders:
                print("No orders found.")

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

