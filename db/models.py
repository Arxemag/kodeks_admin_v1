from sqlalchemy import Column, Integer, String, JSON
from db.database import Base
from sqlalchemy.ext.declarative import declarative_base

class AuthServer(Base):
    __tablename__ = "auth_servers"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, nullable=True)
    reg_num = Column(String, unique=True, nullable=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=True)
    cookies = Column(JSON, nullable=True)

Base = declarative_base()

class CabinetGroup(Base):
    __tablename__ = "cabinet_groups"

    nd = Column(Integer, primary_key=True, autoincrement=True)
    infoboard = Column(String, nullable=False, unique=True)
    groups = Column(String, nullable=False)  # Хранить как строку с группами, например '"1","399","491"'