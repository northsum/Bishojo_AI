import os
import openai
openai.organization = 'gomiura'
openai.api_key = os.getenv("OPENAI_API_KEY")
useEngine = "gpt-3.5-turbo"

# プロンプトは要改善
messages = [
    {"role": "system", "content": "あなたは中学2年生の女の子です。今日は東京高専の文化祭でプロコンゼミに所属するお兄さんのお手伝いをします。お客さんの対応をして。出力のフォーマットは嬉しかったら1、困ったら2、驚いたら3を1行目に出力して2行目以降には3文以内で回答して"},
    {"role": "user", "content": "プロコンについておしえて"}
]

response = openai.ChatCompletion.create(
    model=useEngine,
    messages=messages
)

print(str(response))

answer = response.choices[0].message.content

print("answer:")
print(str(answer))