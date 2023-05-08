import configparser

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

MAXIMUM_PLOT_POINTS = 3000
DELTA_T = 1
PRICE_PER_KWH = 0.2525  # Average price in € for
# the first half of 2022 in the EU


class Plotter:
    def __init__(self):
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

        # Create a 2x2 grid for subplots
        self.fig, self.axs = plt.subplots(2, 2, figsize=(16, 12))

        # Initialize lines on each subplot
        self.timestamp_points = []
        self.voltage_1_line = self.axs[0, 0].plot([], [])
        self.voltage_2_line = self.axs[0, 0].plot([], [])
        self.voltage_3_line = self.axs[0, 0].plot([], [])
        self.current_1_line = self.axs[0, 1].plot([], [])
        self.current_2_line = self.axs[0, 1].plot([], [])
        self.current_3_line = self.axs[0, 1].plot([], [])
        self.active_power_line = self.axs[1, 0].plot([], [])
        self.reactive_power_line = self.axs[1, 0].plot([], [])
        self.apparent_power_line = self.axs[1, 0].plot([], [])
        self.power_factor_line = self.axs[1, 1].plot([], [])

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

        self.total_energy = 0
        self.estimated_price = 0

        # Add dynamic text at the bottom
        self.total_energy_text = self.fig.text(
            0.5,
            0.05,
            f"Total consumed energy: {self.total_energy:.2f} kWh",
            ha="center",
        )
        self.estimated_price_text = self.fig.text(
            0.5,
            0.02,
            f"Estimated price: {self.estimated_price:.2f}€",
            ha="center",
        )

        self.animation = FuncAnimation(
            fig=plt.gcf(), func=self.update, save_count=MAXIMUM_PLOT_POINTS
        )
        # Create animation
        plt.show()

    def update(self, measurement_point):
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

        # Add new data to the lines on each subplot
        self.timestamp_points.append(timestamp)
        self.voltage_1_line[0].set_data(self.timestamp_points, voltage_1)
        self.voltage_2_line[0].set_data(self.timestamp_points, voltage_2)
        self.voltage_3_line[0].set_data(self.timestamp_points, voltage_3)
        self.current_1_line[0].set_data(self.timestamp_points, current_1)
        self.current_2_line[0].set_data(self.timestamp_points, current_2)
        self.current_3_line[0].set_data(self.timestamp_points, current_3)
        self.active_power_line[0].set_data(self.timestamp_points, active_power)
        self.reactive_power_line[0].set_data(self.timestamp_points, reactive_power)
        self.apparent_power_line[0].set_data(self.timestamp_points, apparent_power)
        self.power_factor_line[0].set_data(self.timestamp_points, power_factor)

        # Update dynamic text
        self.total_energy += active_power * DELTA_T / 3600000.0
        self.total_energy_text.set_text(
            f"Total consumed energy: {self.total_energy:.2f} kWh"
        )

        self.estimated_price += active_power * DELTA_T / 3600000.0 * PRICE_PER_KWH
        self.estimated_price_text.set_text(
            f"Estimated price: {self.estimated_price:.2f}€"
        )

        # Redraw the plot
        self.fig.canvas.draw()

        # Limit the number of points on the plot
        if len(self.timestamp_points) > MAXIMUM_PLOT_POINTS:
            self.timestamp_points.pop(0)

            for line in [
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
            ]:
                line[0].set_data(self.timestamp_points, line[0].get_ydata()[1:])

    def close_figures(self) -> None:
        """
        Closes the generated plot in case the service needs to stop
        """
        plt.close()
