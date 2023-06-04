import matplotlib.pyplot as plt
from lib.config import PRICE_PER_KWH
from matplotlib.animation import FuncAnimation
from lib.models import Measurement
import logging
import matplotlib.pyplot as plt
import datetime
import matplotlib.dates as mdates


class Plotter:
    def __init__(self):
        """
        The class is always initialized only once at the start of the
        main script. However, since new data processed from the other
        thread might be received, it is necessary to refresh the latest
        values with matplotlib's interactive mode.

        Matplotlib is not thread-safe and therefore an update function
        is written instead, which is called periodically to refresh the
        old single figure.

        Note that the price estimation and energy consumption is computed
        dynamically, and is not stored in the database explicitly. This
        provides more security against tampering, but once the program is
        closed, all the values are restarted.
        """

        self.last_timestamp = 0
        self.total_energy = 0
        self.estimated_price = 0
        self.measurements_date = datetime.date.today()

        plt.ion()
        self.fig, self.axs = plt.subplots(2, 2, figsize=(16, 12))

        (self.voltage_1_line,) = self.axs[0, 0].plot(
            [], [], color="blue", label="Voltage 1"
        )
        (self.voltage_2_line,) = self.axs[0, 0].plot(
            [], [], color="sienna", label="Voltage 2"
        )
        (self.voltage_3_line,) = self.axs[0, 0].plot(
            [], [], color="black", label="Voltage 3"
        )
        (self.current_1_line,) = self.axs[0, 1].plot(
            [], [], color="blue", label="Current 1"
        )
        (self.current_2_line,) = self.axs[0, 1].plot(
            [], [], color="sienna", label="Current 2"
        )
        (self.current_3_line,) = self.axs[0, 1].plot(
            [], [], color="black", label="Current 3"
        )
        (self.active_power_line,) = self.axs[1, 0].plot(
            [], [], color="crimson", label="Active Power"
        )
        (self.reactive_power_line,) = self.axs[1, 0].plot(
            [], [], color="orange", label="Reactive Power"
        )
        (self.apparent_power_line,) = self.axs[1, 0].plot(
            [], [], color="green", label="Apparent Power"
        )
        (self.power_factor_line,) = self.axs[1, 1].plot(
            [], [], color="magenta", label="Power Factor"
        )

        self.axs[0, 0].set_title("Voltage")
        self.axs[0, 1].set_title("Current")
        self.axs[1, 0].set_title("Power")
        self.axs[1, 1].set_title("Power Factor")

        self.axs[0, 0].legend()
        self.axs[0, 1].legend()
        self.axs[1, 0].legend()
        self.axs[1, 1].legend()

        self.axs[0, 0].set_ylabel("[V]")
        self.axs[0, 1].set_ylabel("[A]")
        self.axs[1, 0].set_ylabel("[W], [VAr], [VA]")

        self.axs[1, 0].set_xlabel("Time")
        self.axs[1, 1].set_xlabel("Time")

        self.total_energy_text = self.fig.text(
            0.5,
            0.98,
            f"Total consumed energy: {self.total_energy:.2f} kWh",
            ha="center",
        )
        self.estimated_price_text = self.fig.text(
            0.5,
            0.95,
            f"Estimated price: {self.estimated_price:.2f}€",
            ha="center",
        )
        self.measurements_date_text = self.fig.text(
            0.5,
            0.92,
            f"Year: {self.measurements_date.year}, "
            + f"Month: {self.measurements_date.month}, "
            + f"Day: {self.measurements_date.day}",
            ha="center",
        )

    def update(self, latest_measurements: list[Measurement]) -> None:
        """
        Function used to update the plot already shown when the instance
        was created. There is a maximum value of data points, declared
        in the config.ini
        """
        try:
            timestamp_points = [
                measurement.timestamp for measurement in latest_measurements
            ]
            voltage_1_points = [
                measurement.voltage_1 for measurement in latest_measurements
            ]
            voltage_2_points = [
                measurement.voltage_2 for measurement in latest_measurements
            ]
            voltage_3_points = [
                measurement.voltage_3 for measurement in latest_measurements
            ]
            current_1_points = [
                measurement.current_1 for measurement in latest_measurements
            ]
            current_2_points = [
                measurement.current_2 for measurement in latest_measurements
            ]
            current_3_points = [
                measurement.current_3 for measurement in latest_measurements
            ]
            active_power_points = [
                measurement.active_power for measurement in latest_measurements
            ]
            reactive_power_points = [
                measurement.reactive_power for measurement in latest_measurements
            ]
            apparent_power_points = [
                measurement.apparent_power for measurement in latest_measurements
            ]
            power_factor_points = [
                measurement.power_factor for measurement in latest_measurements
            ]

            if timestamp_points[-1] > self.last_timestamp:
                time_step = timestamp_points[-1] - timestamp_points[-2]

                joules_to_kWh_factor = 3600000.0
                self.total_energy += (
                    active_power_points[-1] * time_step / joules_to_kWh_factor
                )
                self.total_energy_text.set_text(
                    f"Total consumed energy: {self.total_energy:.2f} kWh"
                )

                self.estimated_price += (
                    active_power_points[-1]
                    * time_step
                    / joules_to_kWh_factor
                    * PRICE_PER_KWH
                )
                self.estimated_price_text.set_text(
                    f"Estimated price: {self.estimated_price:.2f}€"
                )
                self.measurements_date = datetime.datetime.fromtimestamp(
                    timestamp_points[-1]
                )
                self.last_timestamp = timestamp_points[-1]

            timestamp_dates = [
                datetime.datetime.fromtimestamp(timestamp)
                for timestamp in timestamp_points
            ]

            self.axs[0, 0].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

            self.axs[0, 0].set_xlim(min(timestamp_dates), max(timestamp_dates))
            self.axs[0, 1].set_xlim(min(timestamp_dates), max(timestamp_dates))
            self.axs[1, 0].set_xlim(min(timestamp_dates), max(timestamp_dates))
            self.axs[1, 1].set_xlim(min(timestamp_dates), max(timestamp_dates))

            self.axs[0, 0].set_ylim(
                min(voltage_1_points + voltage_2_points + voltage_3_points) - 10,
                max(voltage_1_points + voltage_2_points + voltage_3_points) + 10,
            )
            self.axs[0, 1].set_ylim(
                min(current_1_points + current_2_points + current_3_points) - 10,
                max(current_1_points + current_2_points + current_3_points) + 10,
            )
            self.axs[1, 0].set_ylim(
                min(active_power_points + reactive_power_points + apparent_power_points)
                - 1000,
                max(active_power_points + reactive_power_points + apparent_power_points)
                + 1000,
            )
            self.axs[1, 1].set_ylim(
                min(power_factor_points) - 0.1, max(power_factor_points) + 0.1
            )

            self.voltage_1_line.set_data(timestamp_dates, voltage_1_points)
            self.voltage_2_line.set_data(timestamp_dates, voltage_2_points)
            self.voltage_3_line.set_data(timestamp_dates, voltage_3_points)
            self.current_1_line.set_data(timestamp_dates, current_1_points)
            self.current_2_line.set_data(timestamp_dates, current_2_points)
            self.current_3_line.set_data(timestamp_dates, current_3_points)
            self.active_power_line.set_data(timestamp_dates, active_power_points)
            self.reactive_power_line.set_data(timestamp_dates, reactive_power_points)
            self.apparent_power_line.set_data(timestamp_dates, apparent_power_points)
            self.power_factor_line.set_data(timestamp_dates, power_factor_points)

            self.fig.canvas.draw()
            self.fig.canvas.flush_events()

        except Exception as e:
            logging.error(e)
