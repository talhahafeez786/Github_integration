from fastapi import Request
from fastapi.responses import JSONResponse
from helpers.mongodb import integration_collection
from helpers.github_sync import sync_github_data
from datetime import datetime

# GET /integration/status
async def integration_status(request: Request):
    data = await integration_collection.find_one()
    if data:
        return JSONResponse(content={
            "status": data.get("status"),
            "connected_at": data.get("connected_at").isoformat() if data.get("connected_at") else None,
            "username": data.get("username")
        })
    return JSONResponse(status_code=404, content={"message": "No integration found"})

# POST /integration/remove
async def remove_integration(request: Request):
    result = await integration_collection.delete_many({})
    return JSONResponse(content={"message": f"{result.deleted_count} integration(s) removed"})

# POST /integration/resync
async def resync_integration(request: Request):
    result = await sync_github_data()
    return JSONResponse(content=result)
