import requests
import xmltodict
import json
import pymysql

# 데이터베이스 연결 설정
connection = pymysql.connect(
    host='210.223.152.45',
    user='evastick',
    password='evastick!@3',
    db='evastick_db',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

url = 'http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList'
params = {
    "serviceKey": "GFjm5eMN9XGX71YaIvHnCvnyJB85umu76m464jqvLYgn8Q9WneadTERa2cBXpeDaLeuuCXvzyry6ohLHXYxeqA==",
    "pageNo": "1",
    "numOfRows": "999",
    "dataType": "XML",
    "dataCd": "ASOS",
    "dateCd": "HR",
    "startDt": "20231108",
    "startHh": "00",
    "endDt": "20231108",
    "endHh": "23",
    "stnIds": "143"
}

response = requests.get(url, params=params)
print(response)

if response.status_code == 200:
    print(1)
    dictionary = xmltodict.parse(response.text)
    print(2)
    data = json.loads(json.dumps(dictionary))
    print(3)
    grow = 0
    
    for item in data['response']['body']['items']['item']:
        sql = "INSERT INTO `envir_entity` (`temperature`, `humidity`, `soil_humid`, `grow`, `created_at`, `userId`, `precipitaion`, `insolation`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = connection.cursor()
        cursor.execute(sql, (item['ta'], item['hm'], 0, grow, item['tm'] + ":00.815114", 1, 0, 0))
        cursor.close()
        connection.commit()

connection.close()
