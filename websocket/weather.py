import requests
import json
import xmltodict
import xmljson
from xmljson import parker
import csv
from datetime import datetime, timedelta
import dotenv
import os

def weather_csv():
	dotenv_path = dotenv.find_dotenv()
	dotenv.load_dotenv(dotenv_path, override=True)

	start_date = datetime.strptime('20230101', '%Y%m%d')
	end_date = datetime.now() - timedelta(days=1)
	page = (end_date - start_date).days + 1
	p_length = 8

	print(start_date, end_date, page)
	with open('weather.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['DATE','TEMPERATURE','HUMIDITY','PRECIPITATION','INSOLATION','LENGTH'])
		
		
		url = 'http://apis.data.go.kr/1360000/AsosDalyInfoService/getWthrDataList'
		params ={'serviceKey' : 'GFjm5eMN9XGX71YaIvHnCvnyJB85umu76m464jqvLYgn8Q9WneadTERa2cBXpeDaLeuuCXvzyry6ohLHXYxeqA==', 'pageNo' : '1', 'numOfRows' : f'{page}', 'dataType' : 'XML', 'dataCd' : 'ASOS', 'dateCd' : 'DAY', 'startDt' : f"{start_date.strftime('%Y%m%d')}", 'endDt' : f"{end_date.strftime('%Y%m%d')}", 'stnIds' : '115' }

		response = requests.get(url, params=params)
		print(response)
		dictionary = xmltodict.parse(response.content)
		data = json.loads(json.dumps(dictionary))
		print(data)
		if data['response']['header']['resultCode'] != '0':
			for item in data['response']['body']['items']['item']:
				c_date = item['tm']
				temperature = item['avgTa']
				if temperature == None:
					temperature = 0
				humidity = item['avgRhm']
				if humidity == None:
					humidity = 0
				precipitation = item['sumRn']
				if precipitation == None:
					precipitation = 0
				insolation = item['sumGsr']
				if insolation == None:
					insolation = 0

				if 20 < float(temperature) < 28:
					p_length += 0.15
				if 60 < float(humidity) < 70:
					p_length += 0.11
				if 0 < float(precipitation):
					p_length += 0.1
				if 10 < float(insolation) < 20:
					p_length += 0.11
										
				dotenv.set_key(dotenv_path, "P_LENGTH", str(p_length))
				writer.writerow([c_date, temperature, humidity, precipitation, insolation, round(p_length, 3)])
