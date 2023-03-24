from sqlalchemy import Column, Integer, JSON, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ElectricalData(Base):
    __tablename__ = 'electrical_data'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    voltage = Column(JSON)
    current = Column(JSON)
    power = Column(JSON)
    error = Column(String)
    processed = Column(Boolean, default=False)