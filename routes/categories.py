from fastapi import APIRouter, HTTPException
from config.database import collection_categories
from models.category import Category
from bson import ObjectId

router = APIRouter()

# Convert MongoDB item to JSON
def serialize_category(cat) -> dict:
    return {
        "id": str(cat["_id"]),
        "name": cat["name"],
        "description": cat.get("description", "")
    }

@router.get("/")
async def get_categories():
    categories = list(collection_categories.find())
    return [serialize_category(cat) for cat in categories]


@router.post("/")
async def add_category(category: Category):
    new_category = category.dict()
    result = collection_categories.insert_one(new_category)
    new_category["_id"] = result.inserted_id
    return serialize_category(new_category)


@router.put("/{category_id}")
async def update_category(category_id: str, category: Category):
    updated = collection_categories.update_one(
        {"_id": ObjectId(category_id)},
        {"$set": category.dict()}
    )

    if updated.modified_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    cat = collection_categories.find_one({"_id": ObjectId(category_id)})
    return serialize_category(cat)


@router.delete("/{category_id}")
async def delete_category(category_id: str):
    deleted = collection_categories.delete_one({"_id": ObjectId(category_id)})

    if deleted.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Category not found")

    return {"message": "Category deleted"}
