from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, JSON, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from db.conn import Base
from typing import Dict
import datetime


# PREDICTIONS
class ByVolume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(255))
    volume = Column(Integer)
    smvol = Column(Integer)
  
    # is_expired = Column(Boolean)
    
    # start_date = Column(DateTime, default=datetime.datetime.utcnow)
  
    # odds = Column(JSON)
   

    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}