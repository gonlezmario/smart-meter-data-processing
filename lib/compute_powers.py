
import logging
from typing import Type

import numpy as np

from lib.models import Measurement


class ProcessedMeasurement:
    def __init__(
            self,
            measurements: Type[Measurement]
    ) -> None:
        """
        Class calculating the correspondent powers in the initialization
        already. All the methods are use the standard python protected
        notation instead of private in case it is extended in the
        future.

        Note there are also protected object attributes, since some
        parameters use the RMS value instead, which requires to access
        all the data points instead of their arithmetic mean. However, the timestamp should be constant through all
        the measurements since that is how the SQL is defined.
        """
        try:
            self.timestamp = measurements[0].timestamp

            _voltage_1 = []
            _voltage_2 = []
            _voltage_3 = []
            _current_1 = []
            _current_2 = []
            _current_3 = []

            for measurement in measurements:
                _voltage_1.append(measurement.voltage_1)
                _voltage_2.append(measurement.voltage_2)
                _voltage_3.append(measurement.voltage_3)
                _current_1.append(measurement.current_1)
                _current_2.append(measurement.current_2)
                _current_3.append(measurement.current_3)

            self.voltage_1 = np.mean(_voltage_1)
            self.voltage_2 = np.mean(_voltage_2)
            self.voltage_3 = np.mean(_voltage_3)
            self.current_1 = np.mean(_current_1)
            self.current_2 = np.mean(_current_2)
            self.current_3 = np.mean(_current_3)

            self.active_power = 100
            self.reactive_power = 200
            self.apparent_power = 300
            self.power_factor = 0.95

        except Exception as e:
            logging.error("Could not initialize ProcessedMeasurements: %s" % e)

    def get_total_active_power(self) -> float:
        """
        Getter using the already computed mean values instead of the more
        computationally expensive scalar product of arrays (protected attrs)
        """
        try:
            active_power_1 = self.voltage_1 * self.current_1
            active_power_2 = self.voltage_2 * self.current_2
            active_power_3 = self.voltage_3 * self.current_3
            total_active_power = active_power_1 + active_power_2 + active_power_3
            return total_active_power
        except Exception as e:
            logging.error(
                "Unhandled error while computing active power: %s" % e)

    def get_total_apparent_power(self) -> float:
        try:
            def get_root_mean_square(data_points: list) -> float:
                squared_measurements = np.square(data_points)
                mean = np.mean(squared_measurements)
                rms_value = np.sqrt(mean)
                return rms_value

            voltage_1_rms = get_root_mean_square(self._voltage_1)
            voltage_2_rms = get_root_mean_square(self._voltage_2)
            voltage_3_rms = get_root_mean_square(self._voltage_3)
            current_1_rms = get_root_mean_square(self._current_1)
            current_2_rms = get_root_mean_square(self._current_2)
            current_3_rms = get_root_mean_square(self._current_3)

            total_apparent_power = voltage_1_rms * current_1_rms
            + voltage_2_rms * current_2_rms
            + voltage_3_rms * current_3_rms

            return total_apparent_power

        except Exception as e:
            logging.error(
                "Unhandled error while computing apparent power: %s" % e)

    def get_power_factor(self) -> float:
        try:
            active_power = self.get_total_active_power()
            apparent_power = self.get_total_apparent_power()
            power_factor = active_power / apparent_power

            return power_factor

        except Exception as e:
            logging.error(
                "Unhandled error while computing power factor: %s" % e)

    def get_total_reactive_power(self):
        """
        S = sqrt(P**2 + Q**2)
        """
        try:
            squared_total_active_power = np.square(
                self.get_total_active_power())
            squared_total_apparent_power = np.square(
                self.get_total_apparent_power())

            reactive_power = np.sqrt(
                squared_total_apparent_power-squared_total_active_power)
            return reactive_power
        except Exception as e:
            logging.error(
                "Unhandled error while computing reactive power: %s" % e)
