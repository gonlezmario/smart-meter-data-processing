import json
import math
import random
import time

import paho.mqtt.client as mqtt

frequency = 50  # Hz
sampling_rate = 1000  # Hz
duration = 0.05  # s


t = [i/sampling_rate for i in range(int(duration*sampling_rate))]

amplitude_v = 565.69
amplitude_i = 70

v_1_phase = 0
v_2_phase = 2*math.pi/3
v_3_phase = 4*math.pi/3

i_1_phase = 0
i_2_phase = 2*math.pi/3
i_3_phase = 4*math.pi/3

noise_level = 5

v_1_signal_value = [round(amplitude_v *
                    math.sin(2*math.pi*frequency*time+v_1_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]
v_2_signal_value = [round(amplitude_v *
                    math.sin(2*math.pi*frequency*time+v_2_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]
v_3_signal_value = [round(amplitude_v *
                    math.sin(2*math.pi*frequency*time+v_3_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]

i_1_signal_value = [round(amplitude_i *
                    math.sin(2*math.pi*frequency*time+i_1_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]
i_2_signal_value = [round(amplitude_i *
                    math.sin(2*math.pi*frequency*time+i_2_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]
i_3_signal_value = [round(amplitude_i *
                    math.sin(2*math.pi*frequency*time+i_3_phase) + (random.uniform(-noise_level, noise_level)), 3) for time in t]

# Connect to MQTT broker
client = mqtt.Client()
client.connect("localhost", 1883)  # Update with your MQTT broker details

# Publish the data to MQTT topics
for i in range(len(t)):
    timestamp = int(time.time())
    data = {
        "ts": timestamp,
        "v1": v_1_signal_value[i],
        "v2": v_2_signal_value[i],
        "v3": v_3_signal_value[i],
        "i1": i_1_signal_value[i],
        "i2": i_2_signal_value[i],
        "i3": i_3_signal_value[i]
    }
    payload = json.dumps(data)
    # Update with your MQTT topic
    client.publish("smart_meter", payload)
    client.loop(0.01)  # Adjust loop time if needed

# Disconnect from MQTT broker
client.disconnect()
