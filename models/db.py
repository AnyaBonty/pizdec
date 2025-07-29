from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

from typing import AsyncGenerator

sql_url='postgresql+asyncpg://postgres:qwerty1234@localhost:5432/tutu'
#engine – движок подключения
engine=create_async_engine(sql_url)
#async_sessionmaker(...)?
#Создаёт готовую к использованию фабрику сессий:
#
async_session_maker= async_sessionmaker(engine,expire_on_commit=False,class_=AsyncSession)

class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session