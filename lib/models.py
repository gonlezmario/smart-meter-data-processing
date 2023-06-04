from lib.config import MAXIMUM_PLOT_POINTS
import logging

from sqlalchemy import Column, Integer, create_engine, Float
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

from lib.config import DATABASE_URL

"""
This module contains the ORM model of the SQL database where measurements are
stored after being successfully processed.
"""


Base = declarative_base()


class Measurement(Base):
    """
    Object Relational Mapping Class
    """

    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True)
    timestamp = Column(Float)
    voltage_1 = Column(Float)
    voltage_2 = Column(Float)
    voltage_3 = Column(Float)
    current_1 = Column(Float)
    current_2 = Column(Float)
    current_3 = Column(Float)
    active_power = Column(Float)
    reactive_power = Column(Float)
    apparent_power = Column(Float)
    power_factor = Column(Float)

    @staticmethod
    def _session_initialization() -> sessionmaker:
        """
        Method called from other Class methods to follow DRY principles and
        improve maintainability.

        Scoped session to make sure a unique object is handled per thread and
        the session is automatically closed whenever it is no longer used
        """
        engine = create_engine(DATABASE_URL)
        Session = scoped_session(sessionmaker(bind=engine))
        session = Session()
        return session

    @classmethod
    def create_measurement(
        cls,
        timestamp,
        voltage_1,
        voltage_2,
        voltage_3,
        current_1,
        current_2,
        current_3,
        active_power,
        reactive_power,
        apparent_power,
        power_factor,
    ) -> bool:
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
                active_power=active_power,
                reactive_power=reactive_power,
                apparent_power=apparent_power,
                power_factor=power_factor,
            )
            session.add(measurement)
            session.commit()
            return True
        except Exception as e:
            logging.error(
                "Unhandled error creating a measurement row in the database: %s" % e
            )
            return False

    @classmethod
    def query_latest_measurements(
        cls, measurements_limit: int = MAXIMUM_PLOT_POINTS
    ) -> list:
        """
        Function equivalent to the following SQL query:

        SELECT *
        FROM Measurement
        ORDER BY timestamp DESC
        LIMIT measurements_limit;

        To get the latest measurements, the data is ordered from biggest
        to smallest UNIX timestamp. However, it is more practical to order
        them chronologically once the latest measurements have been fetched
        to plot them in an ordered manner. Therefore, the resulting list
        should be reversed.
        """
        session = cls._session_initialization()

        latest_measurements_db = (
            session.query(Measurement)
            .order_by(Measurement.timestamp.desc())
            .limit(measurements_limit)
            .all()
        )

        return latest_measurements_db[::-1]


Base.metadata.create_all(bind=create_engine(DATABASE_URL))
