import paho.mqtt.client as mqtt
import json
import time
import random

"""
Independent module to send mock data to the local MQTT server and test
the service.
"""

client = mqtt.Client()
client.connect("localhost", 1883)
last_timestamp = 0

while True:
    timestamp = int(time.time())
    v_1 = 226 + random.uniform(-5, 5)
    v_2 = 220 + random.uniform(-5, 5)
    v_3 = 228 + random.uniform(-5, 5)
    i_1 = 11 + random.uniform(-1, 1)
    i_2 = 8 + random.uniform(-1, 1)
    i_3 = 10 + random.uniform(-1, 1)
    active_power = 6600 + random.uniform(-1000, 1000)
    reactive_power = 1000 + random.uniform(-500, 500)
    apparent_power = 6675 + random.uniform(-1500, 1500)
    power_factor = 0.9 + random.uniform(-0.1, 0.1)

    if last_timestamp < timestamp:
        data = {
            "t": timestamp,
            "V1": round(v_1, 2),
            "V2": round(v_2, 2),
            "V3": round(v_3, 2),
            "I1": round(i_1, 2),
            "I2": round(i_2, 2),
            "I3": round(i_3, 2),
            "P": round(active_power, 2),
            "Q": round(reactive_power, 2),
            "S": round(apparent_power, 2),
            "PF": round(power_factor, 2),
        }

        payload = json.dumps(data)
        client.publish("smart_meter", payload)
        last_timestamp = timestamp
    client.loop()
