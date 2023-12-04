import paho.mqtt.client as mqtt

# MQTT 브로커에 연결하는 함수
def connect_to_broker():
    # MQTT 브로커의 주소와 포트번호
    broker_address = "172.21.4.223"
    broker_port = 1883

    # MQTT 클라이언트 객체 생성
    client = mqtt.Client()

    # 연결에 사용할 사용자 이름과 비밀번호
    username = "evastick"
    password = "evastick!@3"

    # 사용자 이름과 비밀번호 설정
    client.username_pw_set(username, password)

    # MQTT 브로커에 연결
    client.connect(broker_address, broker_port)

    # 연결 유지 및 메시지 처리를 위한 루프 실행
    client.loop_forever()

connect_to_broker()
