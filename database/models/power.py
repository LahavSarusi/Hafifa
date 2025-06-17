from sqlalchemy import Column, Integer, String, ForeignKey
from database.models import db


class Power(db.Model):
    __tablename__ = 'power'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    hero_id = Column(Integer, ForeignKey("hero.id"), nullable=False)
