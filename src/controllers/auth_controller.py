from fastapi.responses import RedirectResponse, JSONResponse
from helpers.github_oauth import get_github_login_url, exchange_code_for_token, fetch_github_user
from helpers.mongodb import integration_collection
from datetime import datetime


async def github_login():
    url = get_github_login_url()
    return RedirectResponse(url)


async def github_callback(code: str):
    try:
        token = await exchange_code_for_token(code)
        user_info = await fetch_github_user(token)

        # ✅ Delete previous integration data
        await integration_collection.delete_many({})

        # ✅ Insert the new login
        await integration_collection.insert_one({
            "github_id": user_info["id"],
            "username": user_info["login"],
            "email": user_info.get("email"),
            "token": token,
            "status": "connected",
            "connected_at": datetime.utcnow(),
        })

        return JSONResponse(content={
            "token": token,
            "user": user_info
        })

    except Exception as e:
        return JSONResponse(status_code=400, content={"error": str(e)})
