from flask import render_template, request
from testapp import app
import cv2
import os
# ultralyticsのYOLOモジュールをインポート
from ultralytics import YOLO

# YOLOv8のセグメンテーションモデルをロード
model = YOLO(model="yolov8n-seg.pt")

# threadingモジュールをインポート
import threading

processing_done = False

# 画像処理を行う関数を定義
def process_image(filename):
    global processing_done
    # 画像を読み込む
    img = cv2.imread('testapp/static/up/' + filename)
    # 画像の加工を行う（ここではYOLOv8でセグメンテーションを行う）
    result = model.predict(source='testapp/static/up/' + filename, save=True, project='testapp/static/', name="down")
    
    processing_done = True

    # カレントディレクトリのファイルとフォルダの一覧を取得
    items = os.listdir("./testapp/static")
    print(items)

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
    file.save('testapp/static/up/' + filename)
    # 画像処理を別のスレッドで実行する（非同期）
    thread = threading.Thread(target=process_image, args=(filename,))
    thread.start()

    # カレントディレクトリのファイルとフォルダの一覧を取得
    items = os.listdir("./testapp/static")
    print(items)
    
    while not processing_done: pass
    
    #processing_done = False

    # processed.htmlを表示し、加工前と加工後の画像を表示（加工後の画像はまだ生成されていない可能性がある）
    return render_template('htmls/processed.html', original=filename, processed=filename)