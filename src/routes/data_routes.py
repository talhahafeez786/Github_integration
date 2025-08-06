from fastapi import APIRouter, Request
from controllers import data_controller

router = APIRouter(prefix="/data")

@router.get("/{collection}")
async def get_data(collection: str, request: Request):
    return await data_controller.get_collection_data(request, collection)
