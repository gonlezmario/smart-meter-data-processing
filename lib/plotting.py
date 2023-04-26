import matplotlib.pyplot as plt

# create empty lists to store the data
voltage_list = []
current_list = []
power_list = []
pf_list = []

# create an empty figure with 2x2 subplots
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(14, 8))

# create a subplot for voltages
axs[0, 0].set_xlabel('Time')
axs[0, 0].set_ylabel('Voltage (V)')
axs[0, 0].plot([], [], label='Voltage 1')
axs[0, 0].plot([], [], label='Voltage 2')
axs[0, 0].plot([], [], label='Voltage 3')
axs[0, 0].legend()

# create a subplot for currents
axs[0, 1].set_xlabel('Time')
axs[0, 1].set_ylabel('Current (A)')
axs[0, 1].plot([], [], label='Current 1')
axs[0, 1].plot([], [], label='Current 2')
axs[0, 1].plot([], [], label='Current 3')
axs[0, 1].legend()

# create a subplot for powers
axs[1, 0].set_xlabel('Time')
axs[1, 0].set_ylabel('Power (W, var, VA)')
axs[1, 0].plot([], [], label='Active Power')
axs[1, 0].plot([], [], label='Reactive Power')
axs[1, 0].plot([], [], label='Apparent Power')
axs[1, 0].legend()

# create a subplot for power factor
axs[1, 1].set_xlabel('Time')
axs[1, 1].set_ylabel('Power Factor')
axs[1, 1].plot([], [], label='Power Factor')
axs[1, 1].legend()

# adjust the layout and padding of the subplots
fig.tight_layout(pad=3.0)

plt.show()
