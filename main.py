from contextlib import asynccontextmanager
from xmlrpc.client import DateTime

from fastapi import FastAPI, HTTPException,status,Depends,Body,Path
from typing import Annotated


from pydantic import BaseModel
from datetime import datetime
from typing import List

from sqlalchemy import select,insert,delete
from sqlalchemy.ext.asyncio import AsyncSession


from models.db import get_db,engine,Base
from models.note import Note
from shema import NoteOut

"""
Base.metadata	Атрибут metadata содержит сведения обо всех таблицах и моделях, которые унаследованы от Base. Он как "схема всех таблиц" SQLAlchemy.
create_all	Метод create_all() создаёт все таблицы в базе данных, если их ещё нет.
Он берёт информацию из metadata и отправляет CREATE TABLE ... запросы.
"""
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app=FastAPI(lifespan=lifespan)


@app.get("/", response_model=List[NoteOut])
async def get_notes(db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.scalars(select(Note))
    notes = result.all()
    return notes


@app.post('/post_note',status_code=status.HTTP_201_CREATED)
async def post_notes(note:Annotated[str,Body()],db:Annotated[AsyncSession,Depends(get_db)]):
    await db.execute(insert(Note).values(date=datetime.now(),note=note))
    await db.commit()
    return {'Creation':'completed!',
            'note':note}


@app.put('/update_note/{id}')
async def update_note(db:Annotated[AsyncSession,Depends(get_db)], id:Annotated[int,Path()], update_note:Annotated[str,Body()]):
    note=await db.scalar(select(Note).where(Note.id==id))
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='This id not found')
    note.note=update_note
    note.date=datetime.now()
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category update is successful'
    }


@app.delete('/delete/{id}')
async def delete_note(id:Annotated[int,Path()], db:Annotated[AsyncSession,Depends(get_db)]):
    note=await db.scalar(select(Note).where(Note.id==id))
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='This id not found')
    await db.execute(delete(Note).where(Note.id==id))
    await db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'Category delete is successful'
    }