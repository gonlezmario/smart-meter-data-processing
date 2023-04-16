import logging

import matplotlib.pyplot as plt


class DataPlot:
    def __init__(self, processed_data) -> None:
        plt.ion()
        self.processed_data = processed_data

        self.fig, self.axs = plt.subplots(2, 2, figsize=(12, 10))

        self.line_voltage_1, = self.axs[0, 0].plot(
            [], [], color='k', label='Voltage 1')
        self.line_voltage_2, = self.axs[0, 0].plot(
            [], [], color='r', label='Voltage 2')
        self.line_voltage_3, = self.axs[0, 0].plot(
            [], [], color='b', label='Voltage 3')
        self.axs[0, 0].set_xlabel('Timestamp')
        self.axs[0, 0].set_ylabel('Voltage [V]')
        self.axs[0, 0].legend()

        self.line_current_1, = self.axs[0, 1].plot(
            [], [], color='k', label='Current 1')
        self.line_current_2, = self.axs[0, 1].plot(
            [], [], color='r', label='Current 2')
        self.line_current_3, = self.axs[0, 1].plot(
            [], [], color='b', label='Current 3')
        self.axs[0, 1].set_xlabel('Timestamp')
        self.axs[0, 1].set_ylabel('Current [A]')
        self.axs[0, 1].legend()

        self.line_active_power, = self.axs[1, 0].plot(
            [], [], color='c', label='Active Power')
        self.line_reactive_power, = self.axs[1, 0].plot(
            [], [], color='m', label='Reactive Power')
        self.line_apparent_power, = self.axs[1, 0].plot(
            [], [], color='y', label='Apparent Power')
        self.axs[1, 0].set_xlabel('Timestamp')
        self.axs[1, 0].set_ylabel('Power [W, VAr, VA]')
        self.axs[1, 0].legend()

        self.line_power_factor, = self.axs[1, 1].plot(
            [], [], color='g', label='Power Factor')
        self.axs[1, 1].set_xlabel('Timestamp')
        self.axs[1, 1].set_ylabel('Power Factor')

    def update_data(self):
        timestamp_points = []
        voltage_1_points = []
        voltage_2_points = []
        voltage_3_points = []
        current_1_points = []
        current_2_points = []
        current_3_points = []
        active_power_points = []
        reactive_power_points = []
        apparent_power_points = []
        power_factor_points = []

        for measurement_point in self.processed_data:
            timestamp_points.append(measurement_point.timestamp)
            voltage_1_points.append(measurement_point.voltage_1)
            voltage_2_points.append(measurement_point.voltage_2)
            voltage_3_points.append(measurement_point.voltage_3)
            current_1_points.append(measurement_point.current_1)
            current_2_points.append(measurement_point.current_2)
            current_3_points.append(measurement_point.current_3)
            active_power_points.append(measurement_point.active_power)
            reactive_power_points.append(measurement_point.reactive_power)
            apparent_power_points.append(measurement_point.apparent_power)
            power_factor_points.append(measurement_point.power_factor)

        self.line_voltage_1.set_data(
            timestamp_points, voltage_1_points)
        self.line_voltage_2.set_data(
            timestamp_points, voltage_2_points)
        self.line_voltage_3.set_data(
            timestamp_points, voltage_3_points)
        self.line_current_1.set_data(
            timestamp_points, current_1_points)
        self.line_current_2.set_data(
            timestamp_points, current_2_points)
        self.line_current_3.set_data(
            timestamp_points, current_3_points)
        self.line_active_power.set_data(
            timestamp_points, active_power_points)
        self.line_reactive_power.set_data(
            timestamp_points, reactive_power_points)
        self.line_apparent_power.set_data(
            timestamp_points, apparent_power_points)
        self.line_power_factor.set_data(
            timestamp_points, power_factor_points)

        # Redraw the plot
        self.fig.canvas.draw()

        # Pause for a short duration to allow the plot to update
        plt.pause(0.01)
