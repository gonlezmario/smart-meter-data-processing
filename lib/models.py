import configparser
from typing import TypeVar

from sqlalchemy import Column, Integer, JSON, String, Boolean, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


measurements = TypeVar('measurements', bound='Measurements')


Base = declarative_base()


class Measurements(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    voltage = Column(JSON)
    current = Column(JSON)
    power = Column(JSON)
    error = Column(String)
    processed = Column(Boolean, default=False)

    @staticmethod
    def _session_initialization() -> sessionmaker:
        config = configparser.ConfigParser()
        config.read('config.ini')

        engine = create_engine(config.get('database', 'url'))
        Session = sessionmaker(bind=engine)
        session = Session()
        return session

    @classmethod
    def get_pending_measurements(cls) -> measurements:
        session = cls._session_initialization()
        measurements = session.query(cls).filter_by(pending=True, error='').all()
        session.close()
        return measurements

    @classmethod
    def set_not_pending(cls, measurement_id: int) -> None:
        session = cls._session_initialization()
        measurement = session.query(cls).filter_by(id=measurement_id).one_or_none()
        if measurement:
            measurement.pending = False
            session.commit()
        session.close()
