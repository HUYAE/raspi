import requests
import json
import xmltodict
import xmljson
from xmljson import parker
import os
import csv
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller



def price_prediction(file_name):
	start_date = datetime.now() - timedelta(days=1825)
	end_date = datetime.now()
	
	df = pd.read_csv(file_name, header=0, names=['date', 'product', 'area', 'price'])
	df['date'] = pd.to_datetime(df['date'])
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
	
To export both the historical prices and the predicted prices as JSON, you can modify the `price_prediction` function to return a JSON object containing both the historical and predicted data. Here's how you can do it:

```python
import requests
import json
import xmltodict
import xmljson
from xmljson import parker
import os
import csv
from datetime import datetime, timedelta
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

def price_prediction(file_name):
    # (Previous code...)

    # 7일간의 가격 예측
    forecast = model_fit.forecast(steps=7, dynamic=False)
    prediction = df['price'][-1] + forecast

    # Create a dictionary containing both historical and predicted data
    result_dict = {
        'historical_prices': {
            'date': df_month.index.strftime('%Y%m%d').tolist(),
            'price': df_month['price'].tolist()
        },
        'predicted_prices': {
            'date': forecast_dates.strftime('%Y%m%d').tolist(),
            'price': prediction.tolist()
        }
    }

    # Export the combined data as JSON
    return json.dumps(result_dict)

# Call the function to get the JSON data
result_json = price_prediction('your_input_file.csv')

# Save the JSON data to a file if needed
with open('output.json', 'w') as output_file:
	output_file.write(result_json)
