import re

def contains_non_japanese_english(text):
    # 正規表現で日本語と英語以外の文字を検出
    pattern = re.compile('[^가-힣]', re.UNICODE)
    return bool(pattern.search(text))

# テスト用の文字列
text1 = "Hello, こんにちは！"
text2 = "안녕하세요, こんにちは！"
text3 = "12345 67890"

# 文字列に非日本語・非英語文字が含まれているかを判定
print(contains_non_japanese_english(text1))  # true
print(contains_non_japanese_english(text2))  # True
print(contains_non_japanese_english(text3))  # true

