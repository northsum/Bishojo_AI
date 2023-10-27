from PIL import Image, ImageDraw, ImageFont
import datetime
while True:
  print("Input text...")  
  text = input()
  if text == "":
      text = "無いぞ知名度SCSK"
  text += "\n_______________________________"
  # RGB, 画像サイズ, 背景色を設定
  im = Image.new("RGBA", (2120, 140), (0, 0, 0, 120))  # (x,y),(R,G,B,A)
  draw = ImageDraw.Draw(im)

  # PCローカルのフォントへのパスと、フォントサイズを指定
  fontsize = 100  # 140
  font = ImageFont.truetype("/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc", fontsize)

  # 描画位置、描画する文字、文字色、フォントを指定
  # 改行は\n
  draw.multiline_text((0, 0), text, fill=(255, 255, 0),
                      font=font, align='center')  # Yellow

  # ファイルに出力
  time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
  im.save("./"+time+".png")