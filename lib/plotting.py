import matplotlib.pyplot as plt
from lib.config import MAXIMUM_PLOT_POINTS, PRICE_PER_KWH, DELTA_T
from matplotlib.animation import FuncAnimation


class Plotter:
    def __init__(self):
        """
        Class constructor. Note that the total energy and the estimated
        price are not stored in the database since both depend on the
        starting time. Therefore, both are class attributes since they
        are only used to be displayed.

        Furthermore, it would not be secure to store this values in the db,
        that way they would be prone for manipulation. They are only displayed
        in the "front-end" for informative purposes, but the billing should
        be handled by the service provider with the raw data received in the
        MQTT server, which is harder to tamper.

        Both consider only the active power since that is what is usually
        billed, the reactive power and power factor are however displayed to
        monitor reactance.

        Matplotlib is not thread-safe and therefore an update function
        is written instead, which is called continuously with the
        computed newest data.
        """

        self.timestamp_points = []
        self.voltage_1_points = []
        self.voltage_2_points = []
        self.voltage_3_points = []
        self.current_1_points = []
        self.current_2_points = []
        self.current_3_points = []
        self.active_power_points = []
        self.reactive_power_points = []
        self.apparent_power_points = []
        self.power_factor_points = []
        self.total_energy = 0
        self.estimated_price = 0
        self.previous_timestamp = 0

        # Enable interactive mode
        plt.ion()

        # Create a 2x2 grid for subplots
        self.fig, self.axs = plt.subplots(2, 2, figsize=(16, 12))

        # Initialize lines on each subplot
        self.voltage_1_line, = self.axs[0, 0].plot(self.timestamp_points, self.voltage_1_points)
        self.voltage_2_line, = self.axs[0, 0].plot(self.timestamp_points, self.voltage_1_points)
        self.voltage_3_line, = self.axs[0, 0].plot(self.timestamp_points, self.voltage_1_points)
        self.current_1_line, = self.axs[0, 1].plot(self.timestamp_points, self.current_1_points)
        self.current_2_line, = self.axs[0, 1].plot(self.timestamp_points, self.current_1_points)
        self.current_3_line, = self.axs[0, 1].plot(self.timestamp_points, self.current_1_points)
        self.active_power_line, = self.axs[1, 0].plot(self.timestamp_points, self.active_power_points)
        self.reactive_power_line, = self.axs[1, 0].plot(self.timestamp_points, self.reactive_power_points)
        self.apparent_power_line, = self.axs[1, 0].plot(self.timestamp_points, self.apparent_power_points)
        self.power_factor_line, = self.axs[1, 1].plot(self.timestamp_points, self.power_factor_points)

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

    def update(self, measurement_point: dict) -> None:
        """
        Function used to update the plot already shown when the instance
        was created. There is a maximum value of data points, declared
        in the config.ini
        """
        new_timestamp = measurement_point["timestamp"]
        new_voltage_1 = measurement_point["voltage_1"]
        new_voltage_2 = measurement_point["voltage_2"]
        new_voltage_3 = measurement_point["voltage_3"]
        new_current_1 = measurement_point["current_1"]
        new_current_2 = measurement_point["current_2"]
        new_current_3 = measurement_point["current_3"]
        new_active_power = measurement_point["active_power"]
        new_reactive_power = measurement_point["reactive_power"]
        new_apparent_power = measurement_point["apparent_power"]
        new_power_factor = measurement_point["power_factor"]

        plot_lines = [
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
        ]

        value_data_points = [
            self.timestamp_points,
            self.voltage_1_points,
            self.voltage_2_points,
            self.voltage_3_points,
            self.current_1_points,
            self.current_2_points,
            self.current_3_points,
            self.active_power_points,
            self.reactive_power_points,
            self.apparent_power_points,
            self.power_factor_points,
        ]

        if len(self.timestamp_points) < MAXIMUM_PLOT_POINTS:
            if new_timestamp != self.previous_timestamp:
                self.timestamp_points.append(new_timestamp)
                self.voltage_1_points.append(new_voltage_1)
                self.voltage_2_points.append(new_voltage_2)
                self.voltage_3_points.append(new_voltage_3)
                self.current_1_points.append(new_current_1)
                self.current_2_points.append(new_current_2)
                self.current_3_points.append(new_current_3)
                self.active_power_points.append(new_active_power)
                self.reactive_power_points.append(new_reactive_power)
                self.apparent_power_points.append(new_apparent_power)
                self.power_factor_points.append(new_power_factor)

        else:
            for data_list in value_data_points:
                data_list.pop(0)
        
        # Update plot lines
        self.voltage_1_line.set_data(self.timestamp_points, self.voltage_1_points)
        self.voltage_2_line.set_data(self.timestamp_points, self.voltage_2_points)
        self.voltage_3_line.set_data(self.timestamp_points, self.voltage_3_points)
        self.current_1_line.set_data(self.timestamp_points, self.current_1_points)
        self.current_2_line.set_data(self.timestamp_points, self.current_2_points)
        self.current_3_line.set_data(self.timestamp_points, self.current_3_points)
        self.active_power_line.set_data(self.timestamp_points, self.active_power_points)
        self.reactive_power_line.set_data(self.timestamp_points, self.reactive_power_points)
        self.apparent_power_line.set_data(self.timestamp_points, self.apparent_power_points)
        self.power_factor_line.set_data(self.timestamp_points, self.power_factor_points)

        joules_to_kWh_factor = 3600000.0
        # Update dynamic text
        self.total_energy += new_active_power * DELTA_T / joules_to_kWh_factor
        self.total_energy_text.set_text(
            f"Total consumed energy: {self.total_energy:.2f} kWh"
        )

        self.estimated_price += new_active_power * DELTA_T / joules_to_kWh_factor * PRICE_PER_KWH
        self.estimated_price_text.set_text(
            f"Estimated price: {self.estimated_price:.2f}€"
        )

        # drawing updated values
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        self.previous_timestamp = new_timestamp
