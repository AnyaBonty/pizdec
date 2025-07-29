from pydantic import BaseModel
from datetime import datetime


class NoteOut(BaseModel):
    id: int
    note: str
    date: datetime