import time
import Adafruit_DHT
import pymysql.cursors
import datetime
import size_roi

# MySQL 연결 설정
connection = pymysql.connect(host='210.223.152.45',
                             user='evastick',
                             password='evastick!@3',
                             db='evastick_db',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

sensor = Adafruit_DHT.DHT22
pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

print(time)
try:
	if humidity is not None and temperature is not None:
		
		with connection.cursor() as cursor:
			# SQL 쿼리 실행
			grow = size_roi.size()
			sql = "INSERT INTO `envir_entity` (`userId`, `temperature`, `humidity`, `soil_humid`, `grow`) VALUES ( %s, %s, %s, %s, %s)"
			cursor.execute(sql, (1, round(temperature, 1), round(humidity, 1), 0, grow))
			# 변경사항 커밋
			connection.commit()
			print('온도={0:0.1f}*C  습도={1:0.1f}%	길이={2:0.1f}cm'.format(temperature, humidity, grow))
	else:
		print('DHT22 에러 발생')
finally:
	connection.close()

