import logging
from typing import List

import numpy as np

from lib.models import Measurement


class ProcessedMeasurement:
    def __init__(self, measurements: List[Measurement]) -> None:
        """
        Class calculating the correspondent powers given a list
        containing fetched measurements from the database.

        The timestamp should be constant through all the measurements
        objects since the SQL query fetches all the measurements with
        the maximum timestamp.
        """
        try:
            self.timestamp = measurements[0].timestamp

            self.voltage_1_data_points = []
            self.voltage_2_data_points = []
            self.voltage_3_data_points = []
            self.current_1_data_points = []
            self.current_2_data_points = []
            self.current_3_data_points = []

            for measurement in measurements:
                self.voltage_1_data_points.append(measurement.voltage_1)
                self.voltage_2_data_points.append(measurement.voltage_2)
                self.voltage_3_data_points.append(measurement.voltage_3)
                self.current_1_data_points.append(measurement.current_1)
                self.current_2_data_points.append(measurement.current_2)
                self.current_3_data_points.append(measurement.current_3)

        except TypeError:
            logging.error(
                "Could not initialize ProcessedMeasurements. \
                    Non-iterable object"
            )

        except AttributeError:
            logging.error(
                "Could not initialize ProcessedMeasurements. \
                    Object with unexpected attributes"
            )

        except IndexError:
            logging.error(
                "Could not initialize ProcessedMeasurements. \
                          Empty list"
            )

    def get_mean_voltage_1(self) -> float:
        return np.mean(self.voltage_1_data_points)

    def get_mean_voltage_2(self) -> float:
        return np.mean(self.voltage_2_data_points)

    def get_mean_voltage_3(self) -> float:
        return np.mean(self.voltage_3_data_points)

    def get_mean_current_1(self) -> float:
        return np.mean(self.current_1_data_points)

    def get_mean_current_2(self) -> float:
        return np.mean(self.current_2_data_points)

    def get_mean_current_3(self) -> float:
        return np.mean(self.current_3_data_points)

    def get_total_active_power(self) -> float:
        """
        Getter computing the scalar product of each phase's voltage and
        current vectors since:

        P = sum(V_n * I_n)
        """
        active_power_1 = np.dot(self.current_1_data_points, self.voltage_1_data_points)
        active_power_2 = np.dot(self.current_2_data_points, self.voltage_2_data_points)
        active_power_3 = np.dot(self.current_3_data_points, self.voltage_3_data_points)

        total_active_power = active_power_1 + active_power_2 + active_power_3

        return total_active_power

    def get_total_apparent_power(self) -> float:
        """
        Getter computing the RMS value of all data points since:

        S = U_rms * I_rms

        And then add phase apparent powers to obtain the total
        apparent power.
        """

        def get_root_mean_square(data_points: list) -> float:
            squared_measurements = np.square(data_points)
            mean = np.mean(squared_measurements)
            rms_value = np.sqrt(mean)
            return rms_value

        voltage_1_rms = get_root_mean_square(self.voltage_1_data_points)
        voltage_2_rms = get_root_mean_square(self.voltage_2_data_points)
        voltage_3_rms = get_root_mean_square(self.voltage_3_data_points)

        current_1_rms = get_root_mean_square(self.current_1_data_points)
        current_2_rms = get_root_mean_square(self.current_2_data_points)
        current_3_rms = get_root_mean_square(self.current_3_data_points)

        total_apparent_power = voltage_1_rms * current_1_rms
        +voltage_2_rms * current_2_rms
        +voltage_3_rms * current_3_rms

        return total_apparent_power

    def get_total_reactive_power(self) -> float:
        """
        The getter uses the following formula

        Q = sqrt((S + P) * (S - P))

        Note that however, some problems might arise if the product
        is a negative number. This situation is handled with a factor
        of -1 applied in this case.
        """
        total_active_power = self.get_total_active_power()
        total_apparent_power = self.get_total_apparent_power()

        if total_apparent_power - total_apparent_power > 0:
            total_reactive_power = np.sqrt(
                (total_apparent_power + total_active_power)
                * (total_apparent_power - total_active_power)
            )
            return total_reactive_power

        total_reactive_power = -1 * np.sqrt(
            np.abs(
                (total_apparent_power + total_active_power)
                * (total_apparent_power - total_active_power)
            )
        )
        return total_reactive_power

    def get_power_factor(self) -> float:
        """
        PF = P/S
        """
        active_power = self.get_total_active_power()
        apparent_power = self.get_total_apparent_power()
        power_factor = active_power / apparent_power

        return power_factor

    def get_all_measurement_attributes(self) -> dict:
        """
        Getter of all computer variables inside this class. Returning
        a dictionary to increase readability from the main module.

        Includes:

        "timestamp": int
        "voltage_1": float
        "voltage_2": float
        "voltage_3": float
        "current_1": float
        "current_2": float
        "current_3": float
        "active_power": float
        "apparent_power": float
        "reactive_power": float
        "power_factor": float
        """
        try:
            return {
                "timestamp": self.timestamp,
                "voltage_1": self.get_mean_voltage_1(),
                "voltage_2": self.get_mean_voltage_2(),
                "voltage_3": self.get_mean_voltage_3(),
                "current_1": self.get_mean_current_1(),
                "current_2": self.get_mean_current_2(),
                "current_3": self.get_mean_current_3(),
                "active_power": self.get_total_active_power(),
                "apparent_power": self.get_total_apparent_power(),
                "reactive_power": self.get_total_reactive_power(),
                "power_factor": self.get_power_factor(),
            }

        except Exception as e:
            logging.error("Uncaught exception: %s" % e)
