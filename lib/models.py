import configparser
import logging
from typing import TypeVar

from sqlalchemy import JSON, Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from lib.config import DATABASE_URL

"""
This module contains the ORM model of the SQL database where measurements are
stored after being succesfully processed.
"""

measurements = TypeVar('measurements', bound='Measurement')


Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    voltage = Column(JSON)
    current = Column(JSON)
    power = Column(JSON)
    error = Column(String)

    @staticmethod
    def _session_initialization() -> sessionmaker:
        """
        Method called from other Class methods to follow DRY principles and
        improve sustainability.

        Scoped session to make sure a unique object is handled per thread and
        the session is automatically closed whenever it is no longer used

        """
        engine = create_engine(DATABASE_URL)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        return session

    @classmethod
    def create_measurement(cls, timestamp, voltage, current, power, error='') -> bool:
        """
        Initializes a session, creates a class instance with the given parameters and commits them
        to the database.
        """
        try:
            session = cls._session_initialization()
            measurement = cls(timestamp=timestamp, voltage=voltage,
                              current=current, power=power, error=error)
            session.add(measurement)
            session.commit()
            return True
        except Exception as e:
            logging.error(
                "Unhandled error creating a measurement row in the database: %s" % e)
            return False
