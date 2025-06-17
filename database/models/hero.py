from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database.models import db


class Hero(db.Model):
    __tablename__ = 'hero'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    suit_color = Column(String(255))
    has_cape = Column(Boolean)
    last_mission = Column(DateTime, nullable=False)
    is_retired = Column(Boolean, default=False)
