from pydantic import BaseModel
from typing import List

class CabinetGroupModel(BaseModel):
    nd: int
    infoboard: str
    groups: List[str]

    class Config:
        orm_mode = True
