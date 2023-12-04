from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
import json

def length_grow():
    df = pd.read_csv('weather.csv', header=0, names=['date', 'temperature', 'humidity', 'precipitation', 'insolation', 'length'])
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)

    def test_stationarity(timeseries):
        rolmean = timeseries.rolling(window=12).mean()
        rolstd = timeseries.rolling(window=12).std()

        result = adfuller(timeseries, autolag='AIC')

    # 분해 (seasonal_decompose) 수행
    decomposition = seasonal_decompose(df['length'], model='multiplicative', period=12)

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
    diff = df['length'].diff().dropna()


    # ARIMA 모델 학습
    model = ARIMA(diff, order=(1, 1, 1))
    model_fit = model.fit()

    # 7일간의 가격 예측
    forecast = model_fit.forecast(steps=7, dynamic=False)
    prediction = df['length'][-1] + forecast

    # 예측 결과와 기존 데이터 시각화
    plt.figure(figsize=(12,6))
    plt.plot(df['length'], label='original')
    plt.plot(pd.date_range(start=df.index[-1], periods=7, freq='D'), prediction, label='prediction')
    plt.legend()
    plt.title('Length Forecasting')
    plt.xlabel('Date')
    plt.ylabel('Length')
    plt.savefig('length.png')
    
    # 예측 결과와 기존 데이터를 하나의 DataFrame으로 합치기
    forecast_dates = pd.date_range(start=df.index[-1], periods=7, freq='D')
    forecast = pd.DataFrame({'date': forecast_dates, 'length': prediction})
    df_forecast = forecast[['date', 'length']].to_dict('records')

    # 예측 결과를 json 형식으로 변환
    prediction_dict = {'date': forecast_dates.strftime('%Y%m%d').tolist(), 'length': prediction.tolist()}
    return json.dumps(prediction_dict)
    
def grow():
    # 데이터를 불러옵니다.
    df = pd.read_csv('weather.csv')

    # 일자별 길이 증가량을 계산합니다.
    df['Growth'] = df['LENGTH'] - df['LENGTH'].shift(1)

    # 첫 번째 행은 이전 값이 없으므로 NaN이 됩니다. 따라서 이를 0으로 채워줍니다.
    df['Growth'].fillna(0, inplace=True)

    # 일자별 성장률을 계산합니다.
    df['Growth Rate'] = df['Growth'] / df['LENGTH']

    # 온도, 습도, 일사량, 강수량, 성장률의 상관관계를 계산합니다.
    corr = df[['TEMPERATURE', 'HUMIDITY', 'INSOLATION', 'PRECIPITATION', 'Growth Rate']].corr()

    # 성장률과 가장 큰 상관관계를 가진 온도와 습도를 찾습니다.
    max_corr = corr['Growth Rate'].abs().sort_values(ascending=False)[1:3]
    #print(max_corr)

    # 온도와 습도의 평균값을 추천 온습도로 결정합니다.
    recommended_temp = df['TEMPERATURE'].mean()
    recommended_humidity = df['HUMIDITY'].mean()
    #print('Recommended temperature:', recommended_temp + 20)
    #print('Recommended humidity:', recommended_humidity)
    return {'temperature':recommended_temp + 20, 'humidity':recommended_humidity}
