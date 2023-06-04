import json

import paho.mqtt.client as mqtt

from lib.models import Measurement


class MQTTSubscriber:
    def __init__(self, broker_address: str, port: int, topic: str):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.is_connected = False

    def on_message(self, client, userdata, message):
        """
        Callback function to handle incoming messages.

        Decode the observed published message to utf-8 and then transform it into
        a dictionary to handle it avoiding syntax and formatting errors from
        JSONs to Python.

        Each temporary dictionary should have the following format:
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

        Finally, the dict object is added and committed in the db
        The MQTT connection flag is also written in this function since
        it could also be assigned to true in the connect() function even
        if something is misconfigured. If a message is indeed received,
        however, it is more probable that everything worked out correctly,
        and this flag is used only to update the plot, so there is no
        case scenario or edge case where this could be problematic.
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
        """
        Function establishing initial MQTT connection. The bare minimum
        requirements to do so are:

        -Connect to an address and port
        -Set a callback function to handle incoming messages
        -Subscribe to a given server MQTT topic
        -Keep the connection alive actively
        """
        self.client = mqtt.Client()
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port)
        self.client.subscribe(self.topic)
        self.client.loop_start()

    def disconnect(self):
        """
        Safely terminate MQTT connection
        """
        self.is_connected = False
        self.client.loop_stop()
        self.client.disconnect()
