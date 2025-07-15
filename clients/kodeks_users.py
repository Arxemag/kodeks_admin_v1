import httpx
from typing import Optional, List
from core.config import settings

BASE_URL = settings.KODEKS_BASE_URL

async def create_or_update_user(params: dict, groups: List[str]) -> str:
    grp_params = [("grp", str(g)) for g in groups]

    async with httpx.AsyncClient() as client:
        multi_data = list(params.items()) + grp_params
        response = await client.post(f"{BASE_URL}/users/users", data=multi_data)
        response.raise_for_status()
        return response.text.strip()

async def get_user_by_id(user_id: str) -> Optional[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/usr", params={"id": user_id})
        response.raise_for_status()
        return response.json()