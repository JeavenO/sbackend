from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config.database import collection_orders
from models.order import Order

router = APIRouter()

def serialize_order(order) -> dict:
    return {
        "id": str(order["_id"]),
        "product_id": order["product_id"],
        "quantity": order["quantity"],
        "total_price": order["total_price"],
        "customer_name": order["customer_name"]
    }

@router.get("/")
async def get_orders():
    orders = list(collection_orders.find())
    return [serialize_order(order) for order in orders]


@router.post("/")
async def add_order(order: Order):
    new_order = order.dict()
    result = collection_orders.insert_one(new_order)
    new_order["_id"] = result.inserted_id
    return serialize_order(new_order)


@router.put("/{order_id}")
async def update_order(order_id: str, order: Order):
    updated = collection_orders.update_one(
        {"_id": ObjectId(order_id)},
        {"$set": order.dict()}
    )

    if updated.modified_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    ord = collection_orders.find_one({"_id": ObjectId(order_id)})
    return serialize_order(ord)


@router.delete("/{order_id}")
async def delete_order(order_id: str):
    deleted = collection_orders.delete_one({"_id": ObjectId(order_id)})

    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Order not found")

    return {"message": "Order deleted"}
