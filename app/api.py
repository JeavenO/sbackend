from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Category, Product, Order, OrderItem

app = FastAPI(title="Smart Agro API")

# -------------------------
# Database Dependency
# -------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------
# CATEGORY ENDPOINTS
# -------------------------
@app.get("/categories")
def get_categories(db: Session = Depends(get_db)):
    return db.query(Category).all()


@app.post("/categories")
def create_category(name: str, description: str = "", db: Session = Depends(get_db)):
    category = Category(name=name, description=description)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# -------------------------
# PRODUCT ENDPOINTS
# -------------------------
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@app.post("/products")
def create_product(name: str, price: float, stock: int, category_id: int, db: Session = Depends(get_db)):
    category = db.query(Category).get(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=name,
        price=price,
        stock=stock,
        category_id=category_id
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return product


# -------------------------
# ORDER ENDPOINTS
# -------------------------
@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    result = []

    for order in orders:
        items = [
            {
                "product": item.product.name,
                "quantity": item.quantity,
                "subtotal": item.subtotal
            }
            for item in order.order_items
        ]

        result.append({
            "order_id": order.id,
            "customer": order.customer_name,
            "items": items
        })

    return result


@app.post("/orders")
def create_order(customer_name: str, db: Session = Depends(get_db)):
    order = Order(customer_name=customer_name)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@app.get("/")
def home():
    return {"message": "Smart Agro API is running"}
