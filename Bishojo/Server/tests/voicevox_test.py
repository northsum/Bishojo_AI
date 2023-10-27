import requests
import json
import os
print(os.getcwd())

voicevox_url = "http://localhost:50021"
download_file = "../Resources/Hiyori/sounds/tmp.wav"
num = 8
text = "すごーい。君はヒキニートのフレンズなんだね"

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