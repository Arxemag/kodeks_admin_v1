from pydantic import BaseModel, Field
from typing import List, Optional

class UserCreateUpdate(BaseModel):
    id: Optional[str] = None  # логин, если передан — редактируем
    uid: str = Field(..., description="Логин пользователя")
    psw: str = Field(..., description="Пароль пользователя")
    name: str = Field(..., description="Имя пользователя")
    org: Optional[str] = ""
    pos: Optional[str] = ""
    mail: Optional[str] = ""
    telephon: Optional[str] = ""
    end: Optional[str] = ""
    set: Optional[str] = ""
    groups: Optional[str] = Field("", description="Список групп через запятую, например '1,4,5'")

class UserResponse(BaseModel):
    id: str
    uid: str
    name: str
    org: Optional[str]
    pos: Optional[str]
    mail: Optional[str]
    telephon: Optional[str]
    end: Optional[str]
    set: Optional[str]
    groups: List[str] = []
