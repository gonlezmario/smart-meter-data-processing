import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class MeasurementGraph:
    def __init__(self):
        self.fig, self.axs = plt.subplots(nrows=2, ncols=2, figsize=(15, 12))

        # Create the current subgraph
        self.current_ax = self.axs[0, 0]
        self.current_ax.set_xlabel('Timestamp')
        self.current_ax.set_ylabel('Current (A)')
        self.current_line_1, = self.current_ax.plot([], [], label='Current 1')
        self.current_line_2, = self.current_ax.plot([], [], label='Current 2')
        self.current_line_3, = self.current_ax.plot([], [], label='Current 3')
        self.current_ax.legend()

        # Create the voltage subgraph
        self.voltage_ax = self.axs[0, 1]
        self.voltage_ax.set_xlabel('Timestamp')
        self.voltage_ax.set_ylabel('Voltage (V)')
        self.voltage_line_1, = self.voltage_ax.plot([], [], label='Voltage 1')
        self.voltage_line_2, = self.voltage_ax.plot([], [], label='Voltage 2')
        self.voltage_line_3, = self.voltage_ax.plot([], [], label='Voltage 3')
        self.voltage_ax.legend()

        # Create the power subgraph
        self.power_ax = self.axs[1, 0]
        self.power_ax.set_xlabel('Timestamp')
        self.power_ax.set_ylabel('Power [W]')
        self.active_power_line, = self.power_ax.plot(
            [], [], label='Active Power')
        self.reactive_power_line, = self.power_ax.plot(
            [], [], label='Reactive Power')
        self.apparent_power_line, = self.power_ax.plot(
            [], [], label='Apparent Power')
        self.power_ax.legend()

        # Create the power factor subgraph
        self.power_factor_ax = self.axs[1, 1]
        self.power_factor_ax.set_xlabel('Timestamp')
        self.power_factor_ax.set_ylabel('Power Factor [-]')
        self.power_factor_line, = self.power_factor_ax.plot(
            [], [], label='Power Factor')
        self.power_factor_ax.legend()

        # Set up the FuncAnimation
        self.anim = FuncAnimation(self.fig, self.update_graph, frames=None,
                                  interval=100, save_count=500, cache_frame_data=False)

    def update_graph(self, measurement_point):
        timestamp = measurement_point.timestamp
        current_1 = measurement_point.current_1
        current_2 = measurement_point.current_2
        current_3 = measurement_point.current_3
        voltage_1 = measurement_point.voltage_1
        voltage_2 = measurement_point.voltage_2
        voltage_3 = measurement_point.voltage_3
        active_power = measurement_point.active_power
        reactive_power = measurement_point.reactive_power
        apparent_power = measurement_point.apparent_power
        power_factor = measurement_point.power_factor

        # Update the current subgraph
        self.current_line_1.set_data(timestamp, current_1)
        self.current_line_2.set_data(timestamp, current_2)
        self.current_line_3.set_data(timestamp, current_3)
        self.current_ax.relim()
        self.current_ax.autoscale_view()

        # Update the voltage subgraph
        self.voltage_line_1.set_data(timestamp, voltage_1)
        self.voltage_line_2.set_data(timestamp, voltage_2)
        self.voltage_line_3.set_data(timestamp, voltage_3)
        self.voltage_ax.relim()
        self.voltage_ax.autoscale_view()

        # Update the power subgraph
        self.active_power_line.set_data(timestamp, active_power)
        self.reactive_power_line.set_data(timestamp, reactive_power)
        self.apparent_power_line.set_data(timestamp, apparent_power)
        self.power_ax.relim()
        self.power_ax.autoscale_view()

        # Update the power factor subgraph
        self.power_factor_line.set_data(timestamp, power_factor)
        self.power_factor_ax.relim()
        self.power_factor_ax.autoscale_view()

        # Return all of the lines that were updated
        return [self.current_line_1, self.current_line_2, self.current_line_3,
                self.voltage_line_1, self.voltage_line_2, self.voltage_line_3,
                self.active_power_line, self.reactive_power_line, self.apparent_power_line,
                self.power_factor_line]
