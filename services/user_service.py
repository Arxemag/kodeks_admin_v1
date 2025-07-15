from typing import Optional
from clients import kodeks_users
from models.user import UserCreateUpdate, UserResponse

async def create_or_update_user_service(user_data: UserCreateUpdate) -> str:
    groups = user_data.groups.split(",") if user_data.groups else []
    params = {
        "uid": user_data.uid,
        "psw": user_data.psw,
        "name": user_data.name,
        "org": user_data.org or "",
        "pos": user_data.pos or "",
        "mail": user_data.mail or "",
        "telephon": user_data.telephon or "",
        "end": user_data.end or "",
        "set": user_data.set or ""
    }
    if user_data.id:
        params["id"] = user_data.id
    user_id = await kodeks_users.create_or_update_user(params, groups)
    return user_id

async def get_user_service(user_id: str) -> UserResponse:
    data = await kodeks_users.get_user_by_id(user_id)
    groups = data.get("groups", [])
    return UserResponse(
        id=data.get("id", ""),
        uid=data.get("uid", ""),
        name=data.get("name", ""),
        org=data.get("org", ""),
        pos=data.get("pos", ""),
        mail=data.get("mail", ""),
        telephon=data.get("telephon", ""),
        end=data.get("end", ""),
        set=data.get("set", ""),
        groups=groups
    )
