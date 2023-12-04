import pandas as pd
#import weather2
#import big4

def grow():
	#weather2.weather_length()
	#big4.length_grow()

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
