from typing import List, Dict
from sqlalchemy.orm import Session
from db.models import CabinetGroup
from clients.kodeks_admin import KodeksAdminClient

class AdminService:
    def __init__(self, db_session: Session, kodeks_client: KodeksAdminClient):
        self.db_session = db_session
        self.kodeks_client = kodeks_client

    def sync_cabinets_and_groups(self):
        # Получаем кабинеты и группы
        cabinets = self.kodeks_client.get_cabinets()
        existing_groups = self.kodeks_client.get_groups()
        existing_group_names = {g["name"]: g["id"] for g in existing_groups}

        for i, cabinet in enumerate(cabinets, start=1):
            title = cabinet["title"]
            infoboard_id = cabinet["id"].lower()

            # Проверяем, есть ли группа с названием кабинета
            if title not in existing_group_names:
                created_group = self.kodeks_client.create_group(title)
                if created_group and "id" in created_group:
                    existing_group_names[title] = created_group["id"]

            group_ids = [existing_group_names.get(title)] if title in existing_group_names else []

            # Сохраняем в БД
            groups_str = ",".join(f'"{gid}"' for gid in group_ids if gid is not None)

            cabinet_group = self.db_session.query(CabinetGroup).filter_by(infoboard=infoboard_id).first()
            if cabinet_group:
                cabinet_group.groups = groups_str
            else:
                cabinet_group = CabinetGroup(nd=i, infoboard=infoboard_id, groups=groups_str)
                self.db_session.add(cabinet_group)

        self.db_session.commit()

    def apply_rights(self):
        # Формируем параметры для /admin/dirs из таблицы cabinet_groups
        cabinet_groups = self.db_session.query(CabinetGroup).all()

        acl_params = {
            "setup2": "",
            "n": str(len(cabinet_groups)),
            "set": "",
            "acl_unstoragero": "",
            "acl_unstorage": "",
            "acl_unstoragefull": "",
            "acl_unprint": "",
            "unprinttext": "Установлен административный запрет на выполнение операции печати.",
            "acl_unsave": "",
            "unsavetext": "Установлен административный запрет на выполнение операции сохранения в файл.",
            "acl_uncopy": "",
            "uncopytext": "Установлен административный запрет на выполнение операции копирования.",
            "uncopylength": "0",
            "acl_inspectactuallinks": "",
            "desiredtab": "-1",
            "desiredtabas": "-1",
        }

        # Добавляем ключи для каждого кабинета
        for cg in cabinet_groups:
            key_acl = f"acl_infoboard_{cg.infoboard}"
            key_on = f"infoboard_{cg.infoboard}"
            acl_params[key_on] = "on"
            acl_params[key_acl] = f'{{"kw":[{cg.groups}]}}' if cg.groups else ""

        return self.kodeks_client.apply_acl(acl_params)
