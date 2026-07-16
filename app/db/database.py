from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession
)
from app.core.config import Settings

#creating engine
engine = create_async_engine(
    Settings.DATABASE_URL,
    echo = Settings.DEBUG
)

# binding engine
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession 
)