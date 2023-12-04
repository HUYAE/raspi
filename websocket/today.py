import json
import weather
import weather_grow
import price

weather.weather_csv()
price.price_csv()

prediction_apple = price.price_prediction('price(apple)')
with open('prediction_apple.json', 'w') as f:
    json.dump(prediction_apple, f)
    
prediction_pear = price.price_prediction('price(pear)')
with open('prediction_pear.json', 'w') as f:
    json.dump(prediction_pear, f)

prediction_length = weather_grow.length_grow()
with open('prediction_length.json', 'w') as f:
    json.dump(prediction_length, f)
    
recommended = weather_grow.grow()
with open('recommended.json', 'w') as f:
    json.dump(recommended, f)
