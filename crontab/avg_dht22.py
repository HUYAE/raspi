import pymysql.cursors
import datetime

# MySQL 연결 설정
connection = pymysql.connect(host='localhost',
                             user='demo',
                             password='maco',
                             db='demo',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

try:
    with connection.cursor() as cursor:
        # 현재 시간 기준으로 하루 전 시간 계산
        now = datetime.datetime.now()
        one_day_ago = (now - datetime.timedelta(days=1)).strftime('%y%m%d')
        print(one_day_ago)
        
        
        # 하루 전부터 현재까지의 데이터 가져오기
        sql = "SELECT * FROM `data` WHERE `date` LIKE %s"
        # cursor.execute(sql, (one_day_ago))
        cursor.execute(sql, (one_day_ago))
        data = cursor.fetchall()
        
        # 온도와 습도 평균값 계산
        temperature_sum = 0
        humidity_sum = 0
        count = 0
        for row in data:
            temperature_sum += row['temperature']
            humidity_sum += row['humidity']
            count += 1
            
        if count > 0:
            temperature_avg = temperature_sum / count
            humidity_avg = humidity_sum / count
            
            # 평균값을 데이터베이스에 저장
            sql = "INSERT INTO `avg_data` (`avg_date`, `avg_temperature`, `avg_humidity`) VALUES (%s, %s, %s)"
            cursor.execute(sql, (datetime.datetime.now().strftime('%y%m%d'), round(temperature_avg, 1), round(humidity_avg, 1)))
            
            # 변경사항 커밋
            connection.commit()

finally:
    connection.close()
