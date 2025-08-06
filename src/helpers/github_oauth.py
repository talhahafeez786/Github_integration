from urllib.parse import urlencode
import httpx
from config import settings

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USER_API = "https://api.github.com/user"

def get_github_login_url():
    params = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "redirect_uri": settings.REDIRECT_URI,
        "scope": "read:user user:email repo",
    }
    return f"{GITHUB_AUTH_URL}?{urlencode(params)}"

async def exchange_code_for_token(code: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            GITHUB_TOKEN_URL,
            headers={"Accept": "application/json"},
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.REDIRECT_URI,
            },
        )
        response.raise_for_status()
        return response.json().get("access_token")

async def fetch_github_user(token: str) -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            GITHUB_USER_API,
            headers={"Authorization": f"token {token}"}
        )
        response.raise_for_status()
        return response.json()
