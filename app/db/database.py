from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from app.core.config import settings

#creating engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo = settings.DEBUG
)

# binding engine
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession 
)