import os
import json
import asyncio
import requests
import websockets
import openai
from whisper_mic.whisper_mic import WhisperMic

# 各環境変数を設定
openai.organization = os.getenv("OPENAI_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")
useEngine = "gpt-3.5-turbo"

websocket_port = 5432
voicevox_url = "http://localhost:50021"
download_file = "../Resource/sounds/tmp.wav"
num = 8

def get_voice(text: str):
    res = requests.post(f"{voicevox_url}/audio_query?text={text}&speaker={num}")
    if res.status_code == 200:
        if os.path.isfile(download_file):
            os.remove(download_file)

        with open(download_file, "xb") as f:
            res = requests.post(
                url=f"{voicevox_url}/synthesis?speaker={num}&enable_interrogative_upspeak=true",
                headers={
                    "accept": "audio/wav",
                    "Content-Type": "application/json"
                },
                json=json.loads(res.text)
            )
            f.write(res.content)


is_test = True
async def bishojo_loop(websocket, path):
    system_prompt = ""
    mic = WhisperMic()

    try:
        while True:
            question = mic.listen()
            send_data = ""
            if not is_test:
                response = openai.ChatCompletion.create(
                    model=useEngine,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": question}
                    ]
                )
                send_data = response.choices[0].message.content
            else:
                send_data = "1\n" + question
            
            print("send_data: ", send_data)
            [a, b] = send_data.split('\n')

            await websocket.send(send_data)

    except websockets.exceptions.ConnectionClosed:
        pass

start_server = websockets.serve(bishojo_loop, "localhost", websocket_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()