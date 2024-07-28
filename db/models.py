from sqlalchemy import Boolean, String, Integer, Column, ForeignKey, JSON, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship, Mapped
from db.conn import Base
from typing import Dict
import datetime


# PREDICTIONS
class ByVolume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    # stamp = Column(String(255))
    open = Column(String(255))
    high = Column(String(255))
    low = Column(String(255))
    close = Column(String(255))
    volume = Column(String(255))

    # is_expired = Column(Boolean)

    # start_date = Column(DateTime, default=datetime.datetime.utcnow)

    # odds = Column(JSON)


    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}
    

# class Volume(Base):
#     __tablename__ = "newvolumes"
#
#     id = Column(Integer, primary_key=True, index=True)
#     stamp = Column(String(255))
#     open = Column(String(255))
#     high = Column(String(255))
#     low = Column(String(255))
#     close = Column(String(255))
#     volume = Column(String(255))
#
#
#     def as_dict(self):
#        return {c.name: getattr(self, c.name) for c in self.__table__.columns}