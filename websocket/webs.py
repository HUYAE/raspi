import asyncio
import websockets
import json
import base64
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

async def handle_request(websocket, path):
    if path == '/apple':
        print("apple")
        file_path = os.path.join(dir_path, 'prediction_apple.json')
        with open(file_path, 'rb') as f:
            prediction_apple = json.load(f)
        # file1 처리 로직
        filename1 = os.path.join(dir_path, 'price(apple).png')
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        data = {'image': encoded_data, 'prediction': prediction_apple}
        await websocket.send(json.dumps(data))

    if path == '/pear':
        print("pear")
        file_path = os.path.join(dir_path, 'prediction_pear.json')
        with open(file_path, 'rb') as f:
            prediction_pear = json.load(f)
        # file1 처리 로직
        filename1 = os.path.join(dir_path, 'price(pear).png')
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        data = {'image': encoded_data, 'prediction': prediction_pear}
        await websocket.send(json.dumps(data))
        
    if path == '/apple_json':
        print("apple_json")
        file_path = os.path.join(dir_path, 'price(apple).json')
        with open(file_path, 'rb') as f:
            apple_json = json.load(f)
        await websocket.send(json.dumps(apple_json))

    if path == '/pear_json':
        print("pear_json")
        file_path = os.path.join(dir_path, 'price(pear).json')
        with open(file_path, 'rb') as f:
            pear_json = json.load(f)
        await websocket.send(json.dumps(pear_json))
                
    if path == '/grow':
        print("grow")
        # recommended.json 파일을 불러옵니다.
        file_path1 = os.path.join(dir_path, 'recommended.json')
        with open(file_path1, 'rb') as f:
            recommended = json.load(f)
        # prediction_length.json 파일을 불러옵니다.
        file_path2 = os.path.join(dir_path, 'prediction_length.json')
        with open(file_path2, 'rb') as f:
            prediction_length = json.load(f)
        # file1 처리 로직
        filename1 = os.path.join(dir_path, 'length.png')
        filesize1 = os.path.getsize(filename1)
        with open(filename1, 'rb') as f:
            image = f.read()
        # 이미지 데이터를 base64로 인코딩
        encoded_data = base64.b64encode(image).decode('utf-8')

        # JSON 형태로 만들기
        data = {'image': encoded_data, 'recommended': recommended, 'prediction':prediction_length}
        await websocket.send(json.dumps(data))
    else:
        print(path)
        # 예외 처리
        data = {'message': f'Invalid request /{path}'}
        await websocket.send(json.dumps(data))
    
    
        
        

async def main():
    async with websockets.serve(handle_request, host='172.21.3.47', port=8002):
        await asyncio.Future()  # 무한 루프 실행

asyncio.run(main())
