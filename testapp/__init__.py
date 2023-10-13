# Flaskとopencvをインポート
from flask import Flask, render_template, request
import cv2

# Flaskアプリを作成
app = Flask(__name__)

# ルートディレクトリにアクセスしたときの処理
@app.route('/')
def index():
    # index.htmlを表示
    return render_template('htmls/index.html')

# /uploadにPOSTリクエストが送られたときの処理
@app.route('/upload', methods=['POST'])
def upload():
    # リクエストからファイルを取得
    file = request.files['file']
    # ファイルが存在しない場合はエラーメッセージを表示
    if not file:
        return 'ファイルがありません'
    # ファイル名を取得
    filename = file.filename
    # ファイルを保存
    file.save('static/up/' + filename)
    # 画像を読み込む
    img = cv2.imread('static/up/' + filename)
    # 画像の加工を行う（ここではグレースケールに変換）
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 加工後の画像を保存
    cv2.imwrite('static/up/processed_' + filename, img)
    # processed.htmlを表示し、加工前と加工後の画像を表示
    return render_template('htmls/processed.html', original=filename, processed='processed_' + filename)
