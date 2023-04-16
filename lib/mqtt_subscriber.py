import json

import paho.mqtt.client as mqtt

from lib.models import Measurement


class MQTTSubscriber:
    def __init__(self, broker_address: str, port: int, topic: str):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic

    # Callback function to handle incoming messages
    def on_message(self, client, userdata, message):
        """
        Decode the observed published message to utf-8 and then transform it into
        a dictionary to handle it.
        Each dictionary has the following format:
        {
            ts: timestamp,
            v1: voltage_1,
            v2: voltage_2,
            v3: voltage_3,
            i1: current_1,
            i2: current_2,
            i3: current_3,
        }
        """
        msg = message.payload.decode('utf-8')
        data = json.loads(msg)
        Measurement.create_measurement(
            timestamp=data['ts'],
            voltage_1=data['v1'],
            voltage_2=data['v2'],
            voltage_3=data['v3'],
            current_1=data['i1'],
            current_2=data['i2'],
            current_3=data['i3'],
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

    def disconnect(self):
        # Stop MQTT loop and disconnect from MQTT broker
        self.client.loop_stop()
        self.client.disconnect()
