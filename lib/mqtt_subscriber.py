import json

import paho.mqtt.client as mqtt

from lib.models import Measurement


class MQTTSubscriber:
    def __init__(self, broker_address: str, port: int, topic: str):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.is_connected = False

    # Callback function to handle incoming messages
    def on_message(self, client, userdata, message):
        """
        Decode the observed published message to utf-8 and then transform it into
        a dictionary to handle it.
        Each dictionary has the following format:
        {
            t: timestamp,
            V1: voltage_1,
            V2: voltage_2,
            V3: voltage_3,
            I1: current_1,
            I2: current_2,
            I3: current_3,
            P: active_power,
            Q: reactive_power,
            S: apparent_power,
            PF: power_factor,
        }
        """
        self.is_connected = True
        msg = message.payload.decode("utf-8")
        data = json.loads(msg)
        Measurement.create_measurement(
            timestamp=data["t"],
            voltage_1=data["V1"],
            voltage_2=data["V2"],
            voltage_3=data["V3"],
            current_1=data["I1"],
            current_2=data["I2"],
            current_3=data["I3"],
            active_power=data["P"],
            reactive_power=data["Q"],
            apparent_power=data["S"],
            power_factor=data["PF"],
        )

    def connect(self):
        # Create MQTT client instance
        self.client = mqtt.Client()

        # Set callback function for incoming messages
        self.client.on_message = self.on_message

        # Connect to MQTT broker
        # Use the appropriate port for your Mosquitto broker
        self.client.connect(self.broker_address, self.port)

        # Subscribe to the topic
        self.client.subscribe(self.topic)

        # Start MQTT loop to receive messages
        self.client.loop_start()

        # Flag confirming it the connection was successful
        

    def disconnect(self):
        self.is_connected = False
        # Stop MQTT loop and disconnect from MQTT broker
        self.client.loop_stop()
        self.client.disconnect()
