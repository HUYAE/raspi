from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import json
import time
import RPi.GPIO as GPIO
from flask_cors import CORS
import dotenv
import os

dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_path)

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = os.environ['MQTT_BROKER_URL']  # MQTT 브로커의 주소
app.config['MQTT_BROKER_PORT'] = int(os.environ['MQTT_BROKER_PORT'])  # MQTT 브로커의 포트번호
app.config['MQTT_USERNAME'] = os.environ['MQTT_USERNAME']  # MQTT 브로커에 연결할 사용자 이름
app.config['MQTT_PASSWORD'] = os.environ['MQTT_PASSWORD']  # MQTT 브로커에 연결할 사용자 비밀번호
app.config['MQTT_REFRESH_TIME'] = float(os.environ['MQTT_REFRESH_TIME'])  # MQTT 브로커와 연결을 유지할 시간(초)
mqtt = Mqtt(app)

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

@mqtt.on_connect()
def handle_connect(client, userdata, flags, rc):
    mqtt.subscribe('/test')  # 'test_topic' 주제를 구독합니다.
    mqtt.publish('test_topic', 'Hello, MQTT!')  # 'test_topic' 주제로 메시지를 보냅니다.

@mqtt.on_message()
def handle_message(client, userdata, message):
    print('Received message on topic {}: {}'.format(message.topic, message.payload.decode()))

# JSON 데이터를 받아 처리하는 API
@app.route('/test', methods=['POST'])
def control_valve():
    datas = request.get_json()
    print(datas)
    if GPIO.input(valve_pin) == datas["wval1"]:
		mqtt.publish('/test', json.dumps({"device": datas["device"], "rwtime1":datas["wtime1"]})) 
	elif GPIO.input(valve_pin) != datas["wval1"]:
		
    return ""

if __name__ == '__main__':
    mqtt.subscribe('/test')  # 'test_topic' 주제를 구독합니다.
    app.run(debug=True, host='0.0.0.0',  port=8080)  # Flask 애플리케이션을 실행합니다.
