import paho.mqtt.publish as publish
import json
import dotenv
import os
import time

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path, override=True)

host = os.environ['MQTT_BROKER_URL']
port = int(os.environ['MQTT_BROKER_PORT'])
username = os.environ['MQTT_USERNAME']
password = os.environ['MQTT_PASSWORD']

count = 0

while True:
	dotenv_path = dotenv.find_dotenv()
	dotenv.load_dotenv(dotenv_path, override=True)
	if int(os.environ['RWTIME1']) != 0 and int(os.environ['RWTIME2']) != 0:
		time.sleep(1)
		count += 1
		print(count)
		if count >= 60:
			data = {
				"device":os.environ['DEVICE'],
				"rwtime1":str(int(os.environ['RWTIME1']) - 1),
				"rwtime2":str(int(os.environ['RWTIME2']) - 1),
				"rcval1":os.environ['RCVAL1'],
				"rcval2":os.environ['RCVAL2'],
				"rctime":str(int(os.environ['RCTIME']) - 1)
				}
			dotenv.set_key(dotenv_path, "DEVICE", data["device"])
			dotenv.set_key(dotenv_path, "RWTIME1", data["rwtime1"])
			dotenv.set_key(dotenv_path, "RWTIME2", data["rwtime2"])
			dotenv.set_key(dotenv_path, "RCVAL1", data["rcval1"])
			dotenv.set_key(dotenv_path, "RCVAL2", data["rcval2"])
			dotenv.set_key(dotenv_path, "RCTIME", data["rctime"])
			publish.single("/valve_control/log/abcd0001", json.dumps(data), qos=1, hostname=host, port=port, client_id='evastick_manual', auth={'username':username, 'password':password})
			print("send")
			count = 0
	elif int(os.environ['RWTIME1']) == 0 and int(os.environ['RWTIME2']) != 0:
		time.sleep(1)
		count += 1
		print(count)
		if count >= 60:
			data = {
				"device":os.environ['DEVICE'],
				"rwtime1":os.environ['RWTIME1'],
				"rwtime2":str(int(os.environ['RWTIME2']) - 1),
				"rcval1":os.environ['RCVAL1'],
				"rcval2":os.environ['RCVAL2'],
				"rctime":str(int(os.environ['RCTIME']) - 1)
				}
			dotenv.set_key(dotenv_path, "DEVICE", data["device"])
			dotenv.set_key(dotenv_path, "RWTIME1", data["rwtime1"])
			dotenv.set_key(dotenv_path, "RWTIME2", data["rwtime2"])
			dotenv.set_key(dotenv_path, "RCVAL1", data["rcval1"])
			dotenv.set_key(dotenv_path, "RCVAL2", data["rcval2"])
			dotenv.set_key(dotenv_path, "RCTIME", data["rctime"])
			publish.single("/valve_control/log/abcd0001", json.dumps(data), qos=1, hostname=host, port=port, client_id='evastick_manual', auth={'username':username, 'password':password})
			print("send")
			count = 0
	elif int(os.environ['RWTIME1']) != 0 and int(os.environ['RWTIME2']) == 0:
		time.sleep(1)
		count += 1
		print(count)
		if count >= 60:
			data = {
				"device":os.environ['DEVICE'],
				"rwtime1":str(int(os.environ['RWTIME1']) - 1),
				"rwtime2":os.environ['RWTIME2'],
				"rcval1":os.environ['RCVAL1'],
				"rcval2":os.environ['RCVAL2'],
				"rctime":str(int(os.environ['RCTIME']) - 1)
				}
			dotenv.set_key(dotenv_path, "DEVICE", data["device"])
			dotenv.set_key(dotenv_path, "RWTIME1", data["rwtime1"])
			dotenv.set_key(dotenv_path, "RWTIME2", data["rwtime2"])
			dotenv.set_key(dotenv_path, "RCVAL1", data["rcval1"])
			dotenv.set_key(dotenv_path, "RCVAL2", data["rcval2"])
			dotenv.set_key(dotenv_path, "RCTIME", data["rctime"])
			publish.single("/valve_control/log/abcd0001", json.dumps(data), qos=1, hostname=host, port=port, client_id='evastick_manual', auth={'username':username, 'password':password})
			print("send")
			count = 0
	else:
		count = 0
	
