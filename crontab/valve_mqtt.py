import paho.mqtt.client as mqtt
import json
import dotenv
import os
import RPi.GPIO as GPIO
import time
import datetime
from crontab import CronTab

cron = CronTab(user='pi')

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path, override=True)

mqtt_broker = os.environ['MQTT_BROKER_URL']
mqtt_port = int(os.environ['MQTT_BROKER_PORT'])
mqtt_username = os.environ['MQTT_USERNAME']
mqtt_password = os.environ['MQTT_PASSWORD']

# GPIO 핀 설정
# 솔레노이드 밸브
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings (False)
valve_pin = 18
GPIO.setup(valve_pin, GPIO.IN)
GPIO.setup(valve_pin, GPIO.OUT)
# 워터펌프
A1A = 5
A1B = 6
GPIO.setmode(GPIO.BCM)
GPIO.setup(A1A, GPIO.OUT)
GPIO.output(A1A, GPIO.LOW)
GPIO.setup(A1B, GPIO.OUT)
GPIO.output(A1B, GPIO.LOW)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe([("/valve_control/manual/abcd0001", 1), ("/valve_control/check/abcd0001", 1)])

# 수신한 메시지를 처리
def on_message(client, userdata, message):
    try:
        data = json.loads(message.payload.decode("utf-8"))
        
        device_id = 'abcd0001'
        rwval1 = 0
        rwval2 = 0
        
        # 관수밸브 2 
        if int(data["rwtime1"]) == 0:
            rwval1 = 0
        else:
            rwval1 = 1

        if int(data["rwtime2"]) == 0:
            rwval2 = 0
        else:
            rwval2 = 1
        
        # 수동 조작 데이터 처리
        if message.topic == "/valve_control/manual/{}".format(device_id):
            response_topic = "/valve_control/stay/{}".format(device_id)
            # 수동 조작 데이터 처리 코드 작성
            if int(data["rwtime1"]) != 0 and GPIO.input(valve_pin) == 0:
                GPIO.output(valve_pin, GPIO.HIGH)
                time.sleep(7)
                GPIO.output(A1B, GPIO.HIGH)  #워터펌프 가동
                GPIO.output(A1A, GPIO.LOW)
                time.sleep(1)
                response_topic = "/valve_control/start/{}".format(device_id)
            elif int(data["rwtime1"]) == 0 and GPIO.input(valve_pin) == 1:
                GPIO.output(A1B, GPIO.LOW)
                time.sleep(1)
                GPIO.output(valve_pin, GPIO.LOW)
                time.sleep(7)
                response_topic = "/valve_control/end/{}".format(device_id)
            
            dotenv.set_key(dotenv_path, "DEVICE", data["device"])
            dotenv.set_key(dotenv_path, "RWTIME1", data["rwtime1"])
            dotenv.set_key(dotenv_path, "RWTIME2", data["rwtime2"])
            dotenv.set_key(dotenv_path, "RCVAL1", data["rcval1"])
            dotenv.set_key(dotenv_path, "RCVAL2", data["rcval2"])
            dotenv.set_key(dotenv_path, "RCTIME", data["rctime"])
            
            # 웹서버로 전송할 데이터 생성
            response_data = {
                "device": data["device"],
                "epump":1,
                "etime":1,
                "wpump":GPIO.input(A1B),
                "wval1": GPIO.input(valve_pin),
                "wtime1": data["rwtime1"],
                "wval2": rwval2,
                "wtime2": data["rwtime2"],
                "cval1": data["rcval1"],
                "cval2": data["rcval2"],
                "ctime": data["rctime"]
            }
            client.publish(response_topic, json.dumps(response_data), 1)
        elif message.topic == "/valve_control/check/{}".format(device_id):
            if data["rwtime1"] == '0' and GPIO.input(valve_pin) == 1:
                GPIO.output(A1B, GPIO.LOW)
                time.sleep(1)
                GPIO.output(valve_pin, GPIO.LOW)
                time.sleep(7)
            if data["rwtime1"] == '0' and data["rwtime1"] == '0':
                response_data = {
                    "device": data["device"],
                    "epump":1,
                    "etime":1,
                    "wpump":GPIO.input(A1B),
                    "wval1": GPIO.input(valve_pin),
                    "wtime1": data["rwtime1"],
                    "wval2": 0,
                    "wtime2": data["rwtime2"],
                    "cval1": data["rcval1"],
                    "cval2": data["rcval2"],
                    "ctime": data["rctime"]
                }
                response_topic = "/valve_control/end/{}".format(device_id)
                client.publish(response_topic, json.dumps(response_data), 1)
        else:
            print(message.topic)
    # 예외처
    except json.decoder.JSONDecodeError:
        error = {"error": "Invalid JSON data: {}".format(message.payload)}
        response_topic = "/valve_control/error/{}".format(device_id)
        client.publish(response_topic, json.dumps(error), 1)
    except KeyError as e:
        error = {"error": "Missing key in JSON data: {}".format(str(e))}
        response_topic = "/valve_control/error/{}".format(device_id)
        client.publish(response_topic, json.dumps(error), 1)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected MQTT disconnection. Will auto-reconnect")

# 클라이언트 ID 설정
client_id = "evastick"

# MQTT 클라이언트 생성
client = mqtt.Client(client_id, clean_session=False)

# MQTT 브로커 연결 후 메시지 대기
client.username_pw_set(mqtt_username, mqtt_password)
client.on_connect = on_connect
client.on_message = on_message
mqtt.on_disconnect = on_disconnect
client.connect(mqtt_broker, mqtt_port, 60)
client.loop_forever()
