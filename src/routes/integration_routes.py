from fastapi import APIRouter
from controllers import integration_controller

router = APIRouter(prefix="/integration")

@router.get("/status")
async def status():
    return await integration_controller.integration_status(None)

@router.post("/remove")
async def remove():
    return await integration_controller.remove_integration(None)

@router.post("/resync")
async def resync():
    return await integration_controller.resync_integration(None)
