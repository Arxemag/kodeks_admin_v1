from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_async_session
from clients.kodeks_admin import KodeksAdminClient
from services.admin_service import AdminService
from core.config import settings

router = APIRouter()

def get_kodeks_client():
    """
    Создает экземпляр клиента для взаимодействия с Kodeks Admin API.
    """
    return KodeksAdminClient(base_url=settings.kodeks_base_url, session_cookie=settings.kodeks_session_cookie)

@router.post(
    "/sync",
    summary="Синхронизация кабинетов и групп",
    description=(
        "Парсит список кабинетов через GraphQL, проверяет и создает группы, если их нет, "
        "сохраняет данные в базе данных."
    ),
    response_description="Статус выполнения операции синхронизации"
)
def sync_admin(db: Session = Depends(get_async_session), kodeks_client: KodeksAdminClient = Depends(get_kodeks_client)):
    """
    Эндпоинт для запуска синхронизации кабинетов и групп.
    """
    service = AdminService(db_session=db, kodeks_client=kodeks_client)
    try:
        service.sync_cabinets_and_groups()
        return {"status": "ok", "message": "Кабинеты и группы синхронизированы"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка синхронизации: {str(e)}")

@router.post(
    "/apply-acl",
    summary="Применение прав доступа к кабинетам",
    description=(
        "Формирует и отправляет запрос для назначения прав (ACL) на кабинеты согласно данным из базы."
    ),
    response_description="Результат применения прав доступа"
)
def apply_acl(db: Session = Depends(get_async_session), kodeks_client: KodeksAdminClient = Depends(get_kodeks_client)):
    """
    Эндпоинт для применения прав доступа (ACL) на кабинеты.
    """
    service = AdminService(db_session=db, kodeks_client=kodeks_client)
    try:
        result = service.apply_rights()
        if result:
            return {"status": "ok", "message": "Права успешно применены"}
        else:
            raise HTTPException(status_code=400, detail="Не удалось применить права")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка применения прав: {str(e)}")
