import asyncio
import websockets

# ５秒に一回websocketで送信
async def send_message(websocket, path):
    inc = 0
    try:
        while True:
            await websocket.send(str(inc))
            inc = (inc + 1) % 9
            await asyncio.sleep(5)
    except websockets.exceptions.ConnectionClosed:
        pass

start_server = websockets.serve(send_message, "localhost", 5432)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()