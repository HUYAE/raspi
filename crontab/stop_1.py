import paho.mqtt.publish as publish
import json
import dotenv
import os
import sys

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

host = os.environ['MQTT_BROKER_URL']
port = int(os.environ['MQTT_BROKER_PORT'])
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

device_id = sys.argv[1]

data = {
        "device": device_id,
        "rwtime1":0,
        "rwtime2":0,
        "rcval1":0,
        "rcval2":0,
        "rctime":0
        }
        

publish.single("/valve_control/manual/{}".format(device_id), json.dumps(data), qos=1, hostname=host, port=port, client_id='evastick_manual', auth={'username':username, 'password':password})

