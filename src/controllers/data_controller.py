from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from bson import ObjectId, Regex
from helpers.mongodb import db
import json

async def get_collection_by_name(name: str):
    collection_names = await db.list_collection_names()
    if name not in collection_names:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db[name]

def build_filter(filter_str: str):
    try:
        return json.loads(filter_str)
    except:
        raise HTTPException(status_code=400, detail="Invalid filter format")

def build_search_query(search: str, sample_doc: dict):
    if not search:
        return {}
    conditions = []
    for key, value in sample_doc.items():
        if isinstance(value, str):
            conditions.append({key: {"$regex": search, "$options": "i"}})
    return {"$or": conditions} if conditions else {}

async def get_collection_data(request: Request, collection: str):
    query_params = request.query_params

    # Pagination
    page = int(query_params.get("page", 1))
    limit = int(query_params.get("limit", 10))
    skip = (page - 1) * limit

    # Sorting
    sort_by = query_params.get("sort_by", None)
    sort_order = 1 if query_params.get("sort_order", "asc") == "asc" else -1

    # Filter and Search
    filter_obj = build_filter(query_params.get("filter", "{}"))
    search = query_params.get("search", None)

    col = await get_collection_by_name(collection)
    sample_doc = await col.find_one()

    # Merge filter and search
    query = filter_obj or {}
    if search and sample_doc:
        query.update(build_search_query(search, sample_doc))

    cursor = col.find(query).skip(skip).limit(limit)
    if sort_by:
        cursor = cursor.sort(sort_by, sort_order)

    items = []
    async for doc in cursor:
        doc["_id"] = str(doc["_id"])  # Convert ObjectId to str
        items.append(doc)

    total = await col.count_documents(query)

    return JSONResponse(content={
        "page": page,
        "limit": limit,
        "total": total,
        "data": items
    })
