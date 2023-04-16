import matplotlib.pyplot as plt

# Interactive mode
plt.ion()

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
line_voltage_1, = axs[0, 0].plot([], [], color='k', label='Voltage 1')
line_voltage_2, = axs[0, 0].plot([], [], color='r', label='Voltage 2')
line_voltage_3, = axs[0, 0].plot([], [], color='b', label='Voltage 3')
axs[0, 0].set_xlabel('Timestamp')
axs[0, 0].set_ylabel('Voltage')
axs[0, 0].set_title('Voltages')
axs[0, 0].legend()

line_current_1, = axs[0, 1].plot([], [], color='k', label='Current 1')
line_current_2, = axs[0, 1].plot([], [], color='r', label='Current 2')
line_current_3, = axs[0, 1].plot([], [], color='b', label='Current 3')
axs[0, 1].set_xlabel('Timestamp')
axs[0, 1].set_ylabel('Current')
axs[0, 1].set_title('Currents')
axs[0, 1].legend()

line_active_power, = axs[1, 0].plot([], [], color='c', label='Active Power')
line_reactive_power, = axs[1, 0].plot(
    [], [], color='m', label='Reactive Power')
line_apparent_power, = axs[1, 0].plot(
    [], [], color='y', label='Apparent Power')
axs[1, 0].set_xlabel('Timestamp')
axs[1, 0].set_ylabel('Power')
axs[1, 0].set_title('Powers')
axs[1, 0].legend()

line_power_factor, = axs[1, 1].plot([], [], color='g', label='Power Factor')
axs[1, 1].set_xlabel('Timestamp')
axs[1, 1].set_ylabel('Power Factor')
axs[1, 1].set_title('Power Factor')


def update_plot(processed_data):
    line_voltage_1.set_data(
        processed_data[0].timestamp, processed_data[0].voltage_1)
    line_voltage_2.set_data(
        processed_data[0].timestamp, processed_data[0].voltage_2)
    line_voltage_3.set_data(
        processed_data[0].timestamp, processed_data[0].voltage_3)
    axs[0, 0].relim()
    axs[0, 0].autoscale_view()

    line_current_1.set_data(
        processed_data[0].timestamp, processed_data[0].current_1)
    line_current_2.set_data(
        processed_data[0].timestamp, processed_data[0].current_2)
    line_current_3.set_data(
        processed_data[0].timestamp, processed_data[0].current_3)
    axs[0, 1].relim()
    axs[0, 1].autoscale_view()

    line_active_power.set_data(
        processed_data[0].timestamp, processed_data[0].active_power)
    line_reactive_power.set_data(
        processed_data[0].timestamp, processed_data[0].reactive_power)
    line_apparent_power.set_data(
        processed_data[0].timestamp, processed_data[0].apparent_power)
    axs[1, 0].relim()
    axs[1, 0].autoscale_view()

    line_power_factor.set_data(
        processed_data[0].timestamp, processed_data[0].power_factor)
    axs[1, 1].relim()
    axs[1, 1].autoscale_view()

    # Redraw the plot
    plt.draw()
    plt.pause(0.5)
