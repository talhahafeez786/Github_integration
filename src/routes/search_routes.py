from fastapi import APIRouter, Request
from controllers import search_controller

router = APIRouter()

@router.get("/search")
async def search(request: Request, q: str):
    return await search_controller.global_search(request, q)
