import configparser
import logging
from typing import TypeVar

from sqlalchemy import JSON, Boolean, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from lib.config import DATABASE_URL

"""
This module contains the ORM model of the SQL database where measurements are
stored after being successfully processed.
"""


Base = declarative_base()


class Measurement(Base):
    __tablename__ = 'measurements'

    id = Column(Integer, primary_key=True)
    timestamp = Column(Integer)
    voltage_1 = Column(Integer)
    voltage_2 = Column(Integer)
    voltage_3 = Column(Integer)
    current_1 = Column(Integer)
    current_2 = Column(Integer)
    current_3 = Column(Integer)

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
    def create_measurement(cls, timestamp, voltage_1, voltage_2, voltage_3, current_1, current_2, current_3) -> bool:
        """
        Initializes a session, creates a class instance with the given parameters and commits them
        to the database.
        """
        try:
            session = cls._session_initialization()
            measurement = cls(
                timestamp=timestamp,
                voltage_1=voltage_1,
                voltage_2=voltage_2,
                voltage_3=voltage_3,
                current_1=current_1,
                current_2=current_2,
                current_3=current_3,
            )
            session.add(measurement)
            session.commit()
            return True
        except Exception as e:
            logging.error(
                "Unhandled error creating a measurement row in the database: %s" % e)
            return False


# Create the model table if it does not exist
Base.metadata.create_all(bind=create_engine(DATABASE_URL))
