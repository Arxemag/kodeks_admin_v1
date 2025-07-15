from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from models.user import UserCreateUpdate, UserResponse
from services import user_service

router = APIRouter(prefix="", tags=["users"])

@router.post(
    "/users",
    response_model=str,
    summary="Создать или обновить пользователя",
    description=(
        "Создаёт нового пользователя или обновляет существующего, "
        "если передан параметр `id`.\n\n"
        "В теле запроса передаются данные пользователя и список групп "
        "через запятую (например, '1,4,5').\n\n"
        "Возвращает ID (логин) созданного или обновлённого пользователя."
    ),
)
async def create_or_update_user(user: UserCreateUpdate):
    """
    Создать нового пользователя или обновить существующего по id.

    - **id**: (optional) логин пользователя для обновления
    - **uid**: логин пользователя (обязательный)
    - **psw**: пароль (обязательный)
    - **name**: имя (обязательный)
    - **org**: организация (опционально)
    - **pos**: должность (опционально)
    - **mail**: email (опционально)
    - **telephon**: телефон (опционально)
    - **end**: срок действия (опционально)
    - **set**: дополнительные параметры (опционально)
    - **groups**: группы через запятую, например '1,2,5' (опционально)
    """
    try:
        user_id = await user_service.create_or_update_user_service(user)
        return user_id
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/usr",
    response_model=UserResponse,
    summary="Получить данные пользователя по ID",
    description=(
        "Возвращает информацию о пользователе и списке его групп по ID (логину).\n\n"
        "Параметры запроса:\n"
        "- id: ID (логин) пользователя (обязательный)\n\n"
        "В ответе возвращаются все основные поля пользователя и список групп."
    ),
)
async def get_user(
    id: str = Query(..., description="ID (логин) пользователя для получения информации")
):
    """
    Получить информацию о пользователе по ID.

    - **id**: логин пользователя (обязательный)
    """
    try:
        user = await user_service.get_user_service(id)
        return user
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
