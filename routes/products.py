from fastapi import APIRouter, HTTPException
from bson import ObjectId
from config.database import collection_products
from models.product import Product

router = APIRouter()

def serialize_product(prod) -> dict:
    return {
        "id": str(prod["_id"]),
        "name": prod["name"],
        "price": prod["price"],
        "category_id": prod["category_id"],
        "stock": prod["stock"]
    }

@router.get("/")
async def get_products():
    products = list(collection_products.find())
    return [serialize_product(prod) for prod in products]


@router.post("/")
async def add_product(product: Product):
    new_product = product.dict()
    result = collection_products.insert_one(new_product)
    new_product["_id"] = result.inserted_id
    return serialize_product(new_product)


@router.put("/{product_id}")
async def update_product(product_id: str, product: Product):
    updated = collection_products.update_one(
        {"_id": ObjectId(product_id)},
        {"$set": product.dict()}
    )

    if updated.modified_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    prod = collection_products.find_one({"_id": ObjectId(product_id)})
    return serialize_product(prod)


@router.delete("/{product_id}")
async def delete_product(product_id: str):
    deleted = collection_products.delete_one({"_id": ObjectId(product_id)})

    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"message": "Product deleted"}
