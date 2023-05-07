import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class Plotter:
    def __init__(self, fig=None, axs=None):
        """
        Class constructor. Note that the total energy and the estimated price
        are not stored in the database since both depend on the starting time.
        Therefore, both are class attributes since they are only used to be
        displayed.

        Furthermore, it would not be secure to store this values in the db,
        that way they would be prone for manipulation. They are only displayed
        in the "front-end" for informative purposes, but the billing should
        be handled by the service provider with the raw data received in the
        MQTT server, which is harder to tamper.

        Both consider only the active power since that is what is usually
        billed, the reactive power and power factor are however displayed to
        monitor reactance.

        """
        if fig is None:
            self.fig, self.axs = plt.subplots(2, 2, figsize=(16, 12))
            self.total_energy = 0
            self.estimated_price = 0
        else:
            self.fig = fig
            self.axs = axs

        # Initialize lines on each subplot
        (self.voltage_1_line,) = self.axs[0, 0].plot([], [])
        (self.voltage_2_line,) = self.axs[0, 0].plot([], [])
        (self.voltage_3_line,) = self.axs[0, 0].plot([], [])
        (self.current_1_line,) = self.axs[0, 1].plot([], [])
        (self.current_2_line,) = self.axs[0, 1].plot([], [])
        (self.current_3_line,) = self.axs[0, 1].plot([], [])
        (self.active_power_line,) = self.axs[1, 0].plot([], [])
        (self.reactive_power_line,) = self.axs[1, 0].plot([], [])
        (self.apparent_power_line,) = self.axs[1, 0].plot([], [])
        (self.power_factor_line,) = self.axs[1, 1].plot([], [])

        # Set titles for each subplot
        self.axs[0, 0].set_title("Voltage")
        self.axs[0, 1].set_title("Current")
        self.axs[1, 0].set_title("Power")
        self.axs[1, 1].set_title("Power Factor")

        # Set y-labels for each subplot
        self.axs[0, 0].set_ylabel("[V]")
        self.axs[0, 1].set_ylabel("[A]")
        self.axs[1, 0].set_ylabel("[W], [VAr], [VA]")

        # Set x-labels for bottom subplots
        self.axs[1, 0].set_xlabel("Time")
        self.axs[1, 1].set_xlabel("Time")

        # Set shared x-limits for all subplots
        self.axs[0, 0].set_xlim(0, 3000)
        self.axs[0, 1].set_xlim(0, 3000)
        self.axs[1, 0].set_xlim(0, 3000)
        self.axs[1, 1].set_xlim(0, 3000)

        # Set shared y-limits for each subplot
        self.axs[0, 0].set_ylim(-575, 575)
        self.axs[0, 1].set_ylim(-80, 80)
        self.axs[1, 0].set_ylim(-46000, 46000)
        self.axs[1, 1].set_ylim(0, 1)

        # Add text at the bottom of each plot
        self.total_energy_text = self.fig.text(
            0.5,
            0.05,
            f"Total consumed energy: {self.total_energy:.2f} kWh",
            ha="center",
        )
        self.estimated_price_text = self.fig.text(
            0.5,
            0.02,
            f"Estimated price: ${self.estimated_price:.2f}",
            ha="center",
        )

        # Create animation
        self.animation = FuncAnimation(fig=plt.gcf(), func=self.update, save_count=3000)
        plt.show()

    def update(self, measurement_point: dict):
        # Update lines on each subplot
        timestamp = measurement_point["timestamp"]
        voltage_1 = measurement_point["voltage_1"]
        voltage_2 = measurement_point["voltage_2"]
        voltage_3 = measurement_point["voltage_3"]
        current_1 = measurement_point["current_1"]
        current_2 = measurement_point["current_2"]
        current_3 = measurement_point["current_3"]
        active_power = measurement_point["active_power"]
        reactive_power = measurement_point["reactive_power"]
        apparent_power = measurement_point["apparent_power"]
        power_factor = measurement_point["power_factor"]
        total_energy = 0
        estimated_price = 0

        self.voltage_1_line.set_data(timestamp, voltage_1)
        self.voltage_2_line.set_data(timestamp, voltage_2)
        self.voltage_3_line.set_data(timestamp, voltage_3)
        self.current_1_line.set_data(timestamp, current_1)
        self.current_2_line.set_data(timestamp, current_2)
        self.current_3_line.set_data(timestamp, current_3)
        self.active_power_line.set_data(timestamp, active_power)
        self.reactive_power_line.set_data(timestamp, reactive_power)
        self.apparent_power_line.set_data(timestamp, apparent_power)
        self.pf_line.set_data(timestamp, power_factor)

        return (
            self.voltage_1_line,
            self.voltage_2_line,
            self.voltage_3_line,
            self.current_1_line,
            self.current_2_line,
            self.current_3_line,
            self.active_power_line,
            self.reactive_power_line,
            self.apparent_power_line,
            self.power_factor_line,
        )


Plotter()
