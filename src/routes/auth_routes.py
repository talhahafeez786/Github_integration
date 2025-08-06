from fastapi import APIRouter, Request
from controllers import auth_controller

router = APIRouter(prefix="/auth/github")

@router.get("/login")
async def login():
    return await auth_controller.github_login()

@router.get("/callback")
async def callback(request: Request):
    code = request.query_params.get("code")
    return await auth_controller.github_callback(code)
