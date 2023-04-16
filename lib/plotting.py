import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DataPlot:
    def __init__(self, processed_data):
        self.processed_data = processed_data

    def plot_data(self):
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

        # Create a Tkinter window
        root = tk.Tk()
        root.title('Data Plot')

        # Create a Matplotlib figure
        fig = plt.figure(figsize=(12, 8))

        # Plot voltages
        ax1 = fig.add_subplot(2, 2, 1)
        ax1.plot(timestamp_points, voltage_1_points, label='Voltage 1')
        ax1.plot(timestamp_points, voltage_2_points, label='Voltage 2')
        ax1.plot(timestamp_points, voltage_3_points, label='Voltage 3')
        ax1.set_xlabel('Timestamp')
        ax1.set_ylabel('Voltage')
        ax1.set_title('Voltage')
        ax1.legend()

        # Plot currents
        ax2 = fig.add_subplot(2, 2, 2)
        ax2.plot(timestamp_points, current_1_points, label='Current 1')
        ax2.plot(timestamp_points, current_2_points, label='Current 2')
        ax2.plot(timestamp_points, current_3_points, label='Current 3')
        ax2.set_xlabel('Timestamp')
        ax2.set_ylabel('Current')
        ax2.set_title('Current')
        ax2.legend()

        # Plot powers
        ax3 = fig.add_subplot(2, 2, 3)
        ax3.plot(timestamp_points, active_power_points, label='Active Power')
        ax3.plot(timestamp_points, reactive_power_points,
                 label='Reactive Power')
        ax3.plot(timestamp_points, apparent_power_points,
                 label='Apparent Power')
        ax3.set_xlabel('Timestamp')
        ax3.set_ylabel('Power')
        ax3.set_title('Power')
        ax3.legend()

        # Plot power factor
        ax4 = fig.add_subplot(2, 2, 4)
        ax4.plot(timestamp_points, power_factor_points, label='Power Factor')
        ax4.set_xlabel('Timestamp')
        ax4.set_ylabel('Power Factor')
        ax4.set_title('Power Factor')
        ax4.legend()

        # Create a FigureCanvasTkAgg object and add it to the Tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.get_tk_widget().pack()

        # Start the Tkinter event loop
        tk.mainloop()
