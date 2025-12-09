from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .db import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String)

    # 1-to-Many
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category id={self.id} name={self.name}>"

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

    category_id = Column(Integer, ForeignKey("categories.id"))

    # Relations
    category = relationship("Category", back_populates="products")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product id={self.id} name={self.name} stock={self.stock}>"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")

    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order id={self.id} customer={self.customer_name}>"

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)

    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    quantity = Column(Integer, nullable=False)
    subtotal = Column(Float, nullable=False)

    # Relations
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")

    def __repr__(self):
        return f"<OrderItem order={self.order_id} product={self.product_id}>"
