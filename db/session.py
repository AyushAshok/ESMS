from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

URL_DATABASE='postgresql+asyncpg://postgres:ayush@localhost:5432/ESMS'

engine=create_async_engine(URL_DATABASE)

SessionLocal=sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)