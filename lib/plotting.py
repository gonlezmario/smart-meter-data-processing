import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.ion()


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

        self.fig = plt.figure(figsize=(24, 16))
        self.ax1 = plt.subplot(2, 2, 1)
        self.ax2 = plt.subplot(2, 2, 2)
        self.ax3 = plt.subplot(2, 2, 3)
        self.ax4 = plt.subplot(2, 2, 4)

        self.lines = []
        self.lines.append(self.ax1.plot(self.timestamp_points,
                          self.voltage_1_points, label='Voltage 1')[0])
        self.lines.append(self.ax1.plot(self.timestamp_points,
                          self.voltage_2_points, label='Voltage 2')[0])
        self.lines.append(self.ax1.plot(self.timestamp_points,
                          self.voltage_3_points, label='Voltage 3')[0])
        self.ax1.set_xlabel('Timestamp')
        self.ax1.set_ylabel('Voltage [V]')
        self.ax1.legend()

        self.lines.append(self.ax2.plot(self.timestamp_points,
                          self.current_1_points, label='Current 1')[0])
        self.lines.append(self.ax2.plot(self.timestamp_points,
                          self.current_2_points, label='Current 2')[0])
        self.lines.append(self.ax2.plot(self.timestamp_points,
                          self.current_3_points, label='Current 3')[0])
        self.ax2.set_xlabel('Timestamp')
        self.ax2.set_ylabel('Current [A]')
        self.ax2.legend()

        self.lines.append(self.ax3.plot(self.timestamp_points,
                          self.active_power_points, label='Active Power')[0])
        self.lines.append(self.ax3.plot(self.timestamp_points,
                          self.reactive_power_points, label='Reactive Power')[0])
        self.lines.append(self.ax3.plot(self.timestamp_points,
                          self.apparent_power_points, label='Apparent Power')[0])
        self.ax3.set_xlabel('Timestamp')
        self.ax3.set_ylabel('Power [W, var, VA]')
        self.ax3.legend()

        self.lines.append(self.ax4.plot(self.timestamp_points,
                          self.power_factor_points, label='Power Factor')[0])
        self.ax4.set_xlabel('Timestamp')
        self.ax4.set_ylabel('Power Factor []')
        self.ax4.legend()

    def update_plot(self, frame):
        # Clear the axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()

        # Plot voltages
        self.ax1.plot(self.timestamp_points,
                      self.voltage_1_points, label='Voltage 1')
        self.ax1.plot(self.timestamp_points,
                      self.voltage_2_points, label='Voltage 2')
        self.ax1.plot(self.timestamp_points,
                      self.voltage_3_points, label='Voltage 3')
        self.ax1.set_xlabel('Timestamp')
        self.ax1.set_ylabel('Voltage [V]')
        self.ax1.legend()

        # Plot currents
        self.ax2.plot(self.timestamp_points,
                      self.current_1_points, label='Current 1')
        self.ax2.plot(self.timestamp_points,
                      self.current_2_points, label='Current 2')
        self.ax2.plot(self.timestamp_points,
                      self.current_3_points, label='Current 3')
        self.ax2.set_xlabel('Timestamp')
        self.ax2.set_ylabel('Current [A]')
        self.ax2.legend()

        # Plot powers
        self.ax3.plot(self.timestamp_points,
                      self.active_power_points, label='Active Power')
        self.ax3.plot(self.timestamp_points,
                      self.reactive_power_points, label='Reactive Power')
        self.ax3.plot(self.timestamp_points,
                      self.apparent_power_points, label='Apparent Power')
        self.ax3.set_xlabel('Timestamp')
        self.ax3.set_ylabel('Power [W, var, VA]')
        self.ax3.legend()

        # Plot power factor
        self.ax4.plot(self.timestamp_points,
                      self.power_factor_points, label='Power Factor')
        self.ax4.set_xlabel('Timestamp')
        self.ax4.set_ylabel('Power Factor []')
        self.ax4.legend()

        plt.tight_layout()

    def animate(self):
        # Create FuncAnimation to update the plot
        ani = FuncAnimation(self.fig, self.update_plot, frames=len(
            self.processed_data), interval=1000)
        plt.show()
