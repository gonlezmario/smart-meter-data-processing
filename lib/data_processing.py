from typing import TypeVar

from lib.config import EXPECTED_FREQUENCY

processed_measurements = TypeVar(
    'processed_measurements', bound='ProcessedMeasurements')
raw_measurements = TypeVar('raw_measurements', bound='RawMeasurements')


class RawMeasurements:
    """
    This class should be initialized once for every measurement
    """

    def __init__(self, timestamp: int, voltage_1: float, current_1: float,
                 voltage_2: float = 0, current_2: float = 0, voltage_3: float = 0,
                 current_3: float = 0) -> None:
        """
        Stores the measurements received over MQTT into objects for easier manipulation
        """
        self.timestamp = timestamp
        self.voltage_1 = voltage_1
        self.voltage_2 = voltage_2
        self.voltage_3 = voltage_3
        self.current_1 = current_1
        self.current_2 = current_2
        self.current_3 = current_3


class ProcessedMeasurements(RawMeasurements):

    def separate_timestamps(self) -> list:
        """
        Set timestamps together 
        """
        last_timestamp = self.timestamp
        measurements = []
        while self.timestamp - last_timestamp < 3:
            measurements.append(self)
            self.timestamp
