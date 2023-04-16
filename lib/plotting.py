import datetime

import matplotlib.pyplot as plt


def update_plot(processed_data):

    timestamp = processed_data.timestamp,
    voltage_1 = processed_data.voltage_1,
    voltage_2 = processed_data.voltage_2,
    voltage_3 = processed_data.voltage_3,
    current_1 = processed_data.current_1,
    current_2 = processed_data.current_2,
    current_3 = processed_data.current_3,
    active_power = processed_data.active_power,
    reactive_power = processed_data.reactive_power,
    apparent_power = processed_data.apparent_power,
    power_factor = processed_data.power_factor

    timestamp_formatted = datetime.datetime.fromtimestamp(
        timestamp).strftime('%Y-%m-%d %H:%M:%S')

    plt.figure(figsize=(12, 8))
    plt.clf()
    plt.suptitle("Power Metrics", fontsize=16, fontweight='bold')
    plt.subplot(2, 2, 1)
    plt.title("Voltage")
    plt.plot(["Voltage 1", "Voltage 2", "Voltage 3"],
             [voltage_1, voltage_2, voltage_3], 'bo-')
    plt.ylabel("Voltage (V)")
    plt.subplot(2, 2, 2)
    plt.title("Current")
    plt.plot(["Current 1", "Current 2", "Current 3"],
             [current_1, current_2, current_3], 'co-')
    plt.ylabel("Current (A)")
    plt.subplot(2, 2, 3)
    plt.title("Total Apparent/Reactive/Active Power")
    plt.plot(["Apparent Power", "Reactive Power", "Active Power"],
             [apparent_power, reactive_power, active_power], 'ro-')
    plt.ylabel("Power (VA, VAR, W)")
    plt.subplot(2, 2, 4)
    plt.title("Power Factor")
    plt.plot(["Power Factor"], [power_factor], 'go-')
    plt.ylabel("Power Factor")
    plt.tight_layout(rect=[0, 0, 1, 0.95])  # Add some space for the suptitle
    plt.suptitle(f"Timestamp: {timestamp_formatted}",
                 x=0.5, y=1, ha='center', fontsize=14)
    plt.show()
