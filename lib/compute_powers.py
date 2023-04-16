from typing import Type

import numpy as np

from lib.models import Measurement


class ComputePowers:
    def __init__(
            self,
            measurements: list[Type[Measurement]]
    ) -> None:

        timestamp, voltage_1_data_points, voltage_2_data_points, \
            voltage_3_data_points, current_1_data_points, \
            current_2_data_points, \
            current_3_data_points = self._get_data_points(
                measurements=measurements)

        self.timestamp = measurements[0].timestamp
        self.voltage_1 = np.mean(voltage_1_data_points)
        self.voltage_2 = np.mean(voltage_2_data_points)
        self.voltage_3 = np.mean(voltage_3_data_points)
        self.current_1 = np.mean(current_1_data_points)
        self.current_2 = np.mean(current_2_data_points)
        self.current_3 = np.mean(current_3_data_points)

        self.active_power = self.get_total_active_power()
        self.reactive_power = self.get_total_reactive_power()
        self.apparent_power = self.get_total_apparent_power()
        self.power_factor = self.get_power_factor()

    def _get_data_points(self, measurements: list[Type[Measurement]]):

        voltage_1_data_points = [
            measurement.voltage_1 for measurement in measurements]
        voltage_2_data_points = [
            measurement.voltage_2 for measurement in measurements]
        voltage_3_data_points = [
            measurement.voltage_3 for measurement in measurements]
        current_1_data_points = [
            measurement.current_1 for measurement in measurements]
        current_2_data_points = [
            measurement.current_2 for measurement in measurements]
        current_3_data_points = [
            measurement.current_3 for measurement in measurements]

        return voltage_1_data_points, voltage_2_data_points, \
            voltage_3_data_points, current_1_data_points, \
            current_2_data_points, current_3_data_points

    def get_total_active_power(self) -> float:
        active_power_1 = np.sum([voltage_1 * current_1
                                 for voltage_1, current_1 in zip(
                                     self.voltage_1_data_points,
                                     self.current_1_data_points
                                 )])

        active_power_2 = np.sum([voltage_2 * current_2
                                 for voltage_2, current_2 in zip(
                                     self.voltage_2_data_points,
                                     self.current_2_data_points
                                 )])
        active_power_3 = np.sum([voltage_3 * current_3
                                 for voltage_3, current_3 in zip(
                                     self.voltage_3_data_points,
                                     self.current_3_data_points
                                 )])
        total_active_power = active_power_1 + active_power_2 + active_power_3
        return total_active_power

    def get_rms_values(self) -> tuple[
            float, float, float, float, float, float,
    ]:

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

        return voltage_1_rms, voltage_2_rms, voltage_3_rms, current_1_rms, current_2_rms, current_3_rms

    def get_total_apparent_power(self) -> float:
        voltage_1_rms, voltage_2_rms, voltage_3_rms, current_1_rms, current_2_rms, current_3_rms = self.get_rms_values()

        total_apparent_power = voltage_1_rms * current_1_rms + \
            voltage_2_rms * current_2_rms + voltage_3_rms * current_3_rms

        return total_apparent_power

    def get_power_factor(self) -> float:
        active_power = self.get_total_active_power()
        apparent_power = self.get_total_apparent_power()
        power_factor = round(active_power / apparent_power, 3)
        return power_factor

    def get_total_reactive_power(self):
        squared_total_active_power = np.square(self.get_total_active_power())
        squared_total_apparent_power = np.square(
            self.get_total_apparent_power())

        reactive_power = np.sqrt(
            squared_total_apparent_power-squared_total_active_power
        )
        return reactive_power
