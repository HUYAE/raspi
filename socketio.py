import json
import base64
import growth
import big4
import price_json
import os
import socketio

# create a SocketIO server instance
app = socketio.Client()

@app.on('connect')
async def connect(sid, environ):
    print('Connected:', sid)

@app.on('disconnect')
async def disconnect(sid):
    print('Disconnected:', sid)

@app.on('message')
async def message(sid, data):
    # extract the path from the message
    path = data.get('path')

    if path == '/apple':
        print("apple")
        # file1 처리 로직
        prediction_apple = price_json.price_prediction('price(apple).csv')
        filename1 = 'price(apple).csv.png'
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        response = {'image': encoded_data, 'prediction': prediction_apple}

    elif path == '/pear':
        print("pear")
        # file1 처리 로직
        prediction_pear = price_json.price_prediction('price(pear).csv')
        filename1 = 'price(pear).csv.png'
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        response = {'image': encoded_data, 'prediction': prediction_pear}

    elif path == '/grow':
        print("grow")
        recommended = growth.grow()
        prediction_length = big4.length_grow()
        # file1 처리 로직
        filename1 = 'length.png'
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        response = {'image': encoded_data, 'recommended': recommended, 'prediction':prediction_length}

    else:
        # 예외 처리
        response = 'Invalid request'

    # send the response back to the client
    await app.emit('response', response, room=sid)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='172.21.4.223', port=8002)
