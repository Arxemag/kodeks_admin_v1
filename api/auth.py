from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse
from db.database import get_async_session
from services.auth_service import AuthService
from models.auth import AuthRequest, AuthResponse

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
    responses={404: {"description": "Ресурс не найден"}},
)

@router.post(
    "/authorize",
    response_model=AuthResponse,
    summary="Авторизация по IP или регистрационному номеру",
    description=(
        "Позволяет авторизовать систему Кодекс, передав IP или регистрационный номер. "
        "Сохраняет cookies и заголовок в базе, если авторизация успешна."
    ),
    response_description="Результат авторизации: успешно или нет",
)
async def authorize(
    data: AuthRequest,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Отправляет запрос на авторизацию в систему Кодекс.

    - **ip**: IP-адрес клиента (опционально)
    - **reg_num**: регистрационный номер клиента (опционально, но один из двух обязателен)
    """
    service = AuthService(db)
    result = await service.authorize(data)
    return JSONResponse(content=result.dict())
