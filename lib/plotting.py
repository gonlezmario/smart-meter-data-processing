import matplotlib.pyplot as plt


class DataPlot:
    def __init__(self, processed_data):
        self.processed_data = processed_data

        self.timestamp_points, \
            self.voltage_1_points, \
            self.voltage_2_points, \
            self.voltage_3_points, \
            self.current_1_points, \
            self.current_2_points, \
            self.current_3_points, \
            self.active_power_points, \
            self.reactive_power_points, \
            self.apparent_power_points, \
            self.power_factor_points \
            = zip(*[
                (
                    measurement_point.timestamp,
                    measurement_point.voltage_1,
                    measurement_point.voltage_2,
                    measurement_point.voltage_3,
                    measurement_point.current_1,
                    measurement_point.current_2,
                    measurement_point.current_3,
                    measurement_point.active_power,
                    measurement_point.reactive_power,
                    measurement_point.apparent_power,
                    measurement_point.power_factor
                )
                for measurement_point in self.processed_data]
            )

    def plot_data(self):
        plt.ion()  # Turn on interactive mode

        plt.figure(figsize=(24, 16))

        # Plot voltages
        plt.subplot(2, 2, 1)
        plt.plot(self.timestamp_points,
                 self.voltage_1_points, label='Voltage 1')
        plt.plot(self.timestamp_points,
                 self.voltage_2_points, label='Voltage 2')
        plt.plot(self.timestamp_points,
                 self.voltage_3_points, label='Voltage 3')
        plt.xlabel('Timestamp')
        plt.ylabel('Voltage [V]')
        plt.legend()

        # Plot currents
        plt.subplot(2, 2, 2)
        plt.plot(self.timestamp_points,
                 self.current_1_points, label='Current 1')
        plt.plot(self.timestamp_points,
                 self.current_2_points, label='Current 2')
        plt.plot(self.timestamp_points,
                 self.current_3_points, label='Current 3')
        plt.xlabel('Timestamp')
        plt.ylabel('Current [A]')
        plt.legend()

        # Plot powers
        plt.subplot(2, 2, 3)
        plt.plot(self.timestamp_points,
                 self.active_power_points, label='Active Power')
        plt.plot(self.timestamp_points, self.reactive_power_points,
                 label='Reactive Power')
        plt.plot(self.timestamp_points, self.apparent_power_points,
                 label='Apparent Power')
        plt.xlabel('Timestamp')
        plt.ylabel('Power [W, var, VA]')
        plt.legend()

        # Plot power factor
        plt.subplot(2, 2, 4)
        plt.plot(self.timestamp_points,
                 self.power_factor_points, label='Power Factor')
        plt.xlabel('Timestamp')
        plt.ylabel('Power Factor []')
        plt.legend()

        plt.clf()
        plt.pause(0.1)  # Pause to allow interaction with the plot
