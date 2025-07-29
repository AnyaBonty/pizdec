

from sqlalchemy import Column, Integer, DateTime, String
from models.db import Base

class Note(Base):
    __tablename__ = 'note'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime, nullable=False)
    note = Column(String(500), nullable=True)