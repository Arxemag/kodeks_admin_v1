from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import AuthServer
from models.auth import AuthRequest, AuthResponse
from clients.kodeks_auth import KodeksAuthClient
from core.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.client = KodeksAuthClient(settings.kodeks_url)

    async def find_by_ip(self, ip: str) -> Optional[AuthServer]:
        result = await self.db.execute(select(AuthServer).where(AuthServer.ip == ip))
        return result.scalars().first()

    async def find_by_reg_num(self, reg_num: str) -> Optional[AuthServer]:
        result = await self.db.execute(select(AuthServer).where(AuthServer.reg_num == reg_num))
        return result.scalars().first()

    async def authorize(self, request: AuthRequest) -> AuthResponse:
        auth_server = None

        if request.ip:
            auth_server = await self.find_by_ip(request.ip)
        elif request.reg_num:
            auth_server = await self.find_by_reg_num(request.reg_num)

        if not auth_server:
            return AuthResponse(success=False)

        ip_to_use = request.ip or auth_server.ip
        if not ip_to_use:
            return AuthResponse(success=False)

        auth_result = await self.client.authorize(auth_server.url, ip_to_use)

        auth_server.title = auth_result.title
        auth_server.cookies = auth_result.cookies
        await self.db.commit()

        return AuthResponse(success=True)
