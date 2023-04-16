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
        plt.ioff()
        plt.show()
