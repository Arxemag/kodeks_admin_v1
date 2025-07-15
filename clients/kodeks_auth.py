from typing import Any
import httpx


class KodeksAuthResult:
    def __init__(self, title: str, cookies: dict[str, str]):
        self.title = title
        self.cookies = cookies


class KodeksAuthClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def authorize(self, url: str, ip: str) -> KodeksAuthResult:
        headers = {"X-Forwarded-For": ip}
        async with httpx.AsyncClient(base_url=url, headers=headers) as client:
            response = await client.get("/admin/title")
            response.raise_for_status()

            data = response.json()
            title = data.get("title", "")
            cookies = response.cookies.jar.get_dict()

        return KodeksAuthResult(title=title, cookies=cookies)