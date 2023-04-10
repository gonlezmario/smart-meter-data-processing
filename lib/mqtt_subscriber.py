import paho.mqtt.client as mqtt


class MQTTSubscriber:
    def __init__(self, broker_address, topic):
        self.broker_address = broker_address
        self.topic = topic

    # Callback function to handle incoming messages
    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode('utf-8')}")

    def connect(self):
        # Create MQTT client instance
        self.client = mqtt.Client()

        # Set callback function for incoming messages
        self.client.on_message = self.on_message

        # Connect to MQTT broker
        # Use the appropriate port for your Mosquitto broker
        self.client.connect(self.broker_address, 1883)

        # Subscribe to the topic
        self.client.subscribe(self.topic)

        # Start MQTT loop to receive messages
        self.client.loop_forever()

    def disconnect(self):
        # Stop MQTT loop and disconnect from MQTT broker
        self.client.loop_stop()
        self.client.disconnect()
