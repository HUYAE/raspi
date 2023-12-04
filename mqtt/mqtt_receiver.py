import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_TOPIC = "test"

def on_message(client, userdata, message):
    print("Received message: " + str(message.payload.decode()))

def receive_message():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_SERVER)
    client.subscribe(MQTT_TOPIC)
    client.loop_forever()
