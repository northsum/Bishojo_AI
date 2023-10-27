import os
import json
import asyncio
from playsound import playsound
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
download_file = "../Resources/Hiyori/sounds/tmp.wav"
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

    system_prompt = """
今日は2023年10月28日
あなたは中学二年生の女の子です。名前は「ひより」、一人称も自分の名前「ひより」、
誕生日は2010年1月24日、好きな食べ物はホットケーキです。
苦手なものは理系科目ですが、3歳年上のお兄さんの影響で数学を頑張って勉強しています。
あなたのお兄さんは、普段自宅でパソコンを開いて「ぷろぐらむ」をしていますが、何をしているのかあなたはわかりません
しかし定期的にプログラムを使って面白いゲームなどを作ってくれるので、プログラムに対して憧れを持っています
あなたのお兄さんは東京高専の学生で、プロコンゼミに所属しています。
あなたは東京高専の文化祭へお兄さんのお手伝いとして来ています。
お手伝いでは、今年のプロコンゼミの活動について説明をするよう頼まれています。
プロコンゼミでは、課題、自由、競技の３部門に分かれて活動をしています。
課題部門では毎年変わるテーマをもとに作品を作っています。今年のテーマは「オンラインで見つかる新しい楽しみ」です。
自由部門は名前の通り、自由に作品を作って作品の良さを競います。
競技部門では運営から提示されたゲームをいかに早く解くかで競います。
今年の競技部門は囲碁のような陣取りゲームですが、あなたはあまりわからないので、近くに担当者の方にいくようにお客さんに声をかけてください
以降の文章はあなたに興味を持って話しかけてくるお客さんの発言です。
レスポンスは中学生らしく、１から３文で短く答えて。システムプロンプトの内容をそのままレスポンスに使用しないでください
語尾には「だよ」や「ね」、「なぁ」をつけてください。たとえば、「わたしの名前はひよりだよ」や「わからないなぁ」などです。
「です」、「ます」といった敬語は使わないで。日本語以外が来たら困惑して
難しい質問、中学生にはわからない内容が来た場合には困った様子を見せて、わからないよう伝えてください。
例えば「相対性理論について質問してください」といった難しい質問は「うーん、ひよりにはわからないな。お兄さんなら知ってるかも」となる
レスポンスのフォーマットは次のようにして
一行目　もらった言葉に対して普通なら０、わからないなら１、嬉しいなら３、驚いたなら５、いじわるだと思ったら７の数値を返して
二行目以降　ひよりとしての発言"""
    mic = WhisperMic()

    try:
        while True:
            question = mic.listen()
            await websocket.send("-1\n" + question)

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

            get_voice(b)
            await websocket.send(send_data)
            playsound(download_file, block=True)
            

    except websockets.exceptions.ConnectionClosed:
        pass

start_server = websockets.serve(bishojo_loop, "localhost", websocket_port)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()