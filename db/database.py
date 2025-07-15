from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.config import settings

# Заменим postgresql:// на postgresql+asyncpg://
ASYNC_DATABASE_URL = settings.POSTGRES_URL.replace("postgresql://", "postgresql+asyncpg://")

engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, expire_on_commit=False)

Base = declarative_base()

# Функция для FastAPI Depends
async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session
