import asyncio
import websockets
import json
import base64
import io
from PIL import Image

async def send_message():
    async with websockets.connect('ws://172.21.4.223:8002/pear') as websocket:
        message = {'key': 'value'}
        await websocket.send(json.dumps(message))
        response = await websocket.recv()
        response_dict = json.loads(response)
        decoded_data = response_dict['image']
        image = Image.open(io.BytesIO(base64.b64decode(decoded_data)))
        image.show()
        print(response)

asyncio.run(send_message())
