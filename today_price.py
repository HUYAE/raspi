import requests
import json
import xmltodict
import xmljson
from xmljson import parker
import csv
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

today_time = datetime.now()

with open('price(apple).csv', 'a', newline='', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile)
	
	url = f"http://211.237.50.150:7080/openapi/b1f84a154ba8827fd105917f96ed5610f1a9c568fd76757208d5eaf7db42fa5d/xml/Grid_20150406000000000217_1/1/5?EXAMIN_DE={int(today_time.strftime('%Y%m%d'))}&PRDLST_CD=411&AREA_CD=2200"
	response = requests.get(url)

	dictionary = xmltodict.parse(response.content)
	data = json.loads(json.dumps(dictionary))
	
	if data['Grid_20150406000000000217_1']['totalCnt'] != '0':
		for item in data['Grid_20150406000000000217_1']['row']:
			grad_nm = item['GRAD_NM']
			if grad_nm == '상품':
				examin_de = item['EXAMIN_DE']
				prdlst_nm = item['PRDLST_NM']
				area_nm = item['AREA_NM']
				examin_unit = item['EXAMIN_UNIT'].replace('kg', '').strip()
				amt = item['AMT']
				writer.writerow([examin_de, prdlst_nm, area_nm, amt])

with open('price(pear).csv', 'a', newline='', encoding='utf-8') as csvfile:
	writer = csv.writer(csvfile)
	
	url = f"http://211.237.50.150:7080/openapi/b1f84a154ba8827fd105917f96ed5610f1a9c568fd76757208d5eaf7db42fa5d/xml/Grid_20150406000000000217_1/1/5?EXAMIN_DE={int(today_time.strftime('%Y%m%d'))}&PRDLST_CD=412&AREA_CD=2200"
	response = requests.get(url)

	dictionary = xmltodict.parse(response.content)
	data = json.loads(json.dumps(dictionary))
	
	if data['Grid_20150406000000000217_1']['totalCnt'] != '0':
		for item in data['Grid_20150406000000000217_1']['row']:
			grad_nm = item['GRAD_NM']
			if grad_nm == '상품':
				examin_de = item['EXAMIN_DE']
				prdlst_nm = item['PRDLST_NM']
				area_nm = item['AREA_NM']
				examin_unit = item['EXAMIN_UNIT'].replace('kg', '').strip()
				amt = item['AMT']
				writer.writerow([examin_de, prdlst_nm, area_nm, amt])



def price_prediction(file_name):
	df = pd.read_csv(file_name, header=0, names=['date', 'product', 'area', 'price'])
	df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
	df.set_index('date', inplace=True)

	def test_stationarity(timeseries):
		rolmean = timeseries.rolling(window=12).mean()
		rolstd = timeseries.rolling(window=12).std()
		
		result = adfuller(timeseries, autolag='AIC')

	# 분해 (seasonal_decompose) 수행
	decomposition = seasonal_decompose(df['price'], model='multiplicative', period=12)

	# trend, seasonal, residual 값을 따로 저장
	trend = decomposition.trend
	seasonal = decomposition.seasonal
	residual = decomposition.resid

	# NaN 값을 가지는 행(row) 삭제
	residual = residual.dropna()

	# 안정성 검정
	test_stationarity(residual)

	# 차분
	diff = residual.diff().dropna()

	# 차분 결과 출력
	#print(diff)

	# 차분 계산
	diff = df['price'].diff().dropna()

	# 1년전부터 한달치 데이터만 선택
	start_date = df.index[-5*52]  # 13주*4주=52주=1년
	end_date = df.index[-1]
	df_month = df.loc[start_date:end_date]

	# ARIMA 모델 학습
	model = ARIMA(diff, order=(1, 1, 1))
	model_fit = model.fit()

	# 7일간의 가격 예측
	forecast = model_fit.forecast(steps=7, dynamic=False)
	prediction = df['price'][-1] + forecast

	# 예측 결과와 기존 데이터 시각화
	plt.figure(figsize=(12,6))
	plt.plot(df_month['price'], label='original')
	plt.plot(pd.date_range(start=df_month.index[-1], periods=7, freq='D'), prediction, label='prediction')
	plt.legend()
	plt.title('Price Forecasting')
	plt.xlabel('Date')
	plt.ylabel('Price')
	plt.savefig(f'{file_name}.png')

price_prediction('price(apple).csv')
price_prediction('price(pear).csv')
