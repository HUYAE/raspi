import paho.mqtt.client as mqtt

MQTT_SERVER = "localhost"
MQTT_TOPIC = "test"

def send_message(message):
    client = mqtt.Client()
    client.connect(MQTT_SERVER)
    client.publish(MQTT_TOPIC, message)
    client.disconnect()
