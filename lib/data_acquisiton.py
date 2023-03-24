import paho.mqtt.client as mqtt

# This is the callback function that will be called whenever a message is received
def on_message(client, userdata, message):
    # Extract the topic and payload from the message
    topic = message.topic
    payload = message.payload.decode("utf-8")
    # Print the topic and payload for debugging purposes
    print(topic + ": " + payload)
    # Store the value somewhere (e.g. a database)
    # ...

# Create a new MQTT client instance
client = mqtt.Client()

# Set the callback function to be called whenever a message is received
client.on_message = on_message

# Connect to the MQTT broker
client.connect("localhost", 1883, 60)

# Subscribe to the topics
client.subscribe("voltage/1")
client.subscribe("voltage/2")
client.subscribe("voltage/3")
client.subscribe("current/1")
client.subscribe("current/2")
client.subscribe("current/3")

# Start the MQTT client loop
client.loop_forever()