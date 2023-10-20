from flask import render_template, request
from testapp import app
import cv2
import os
# ultralyticsのYOLOモジュールをインポート
from ultralytics import YOLO

# YOLOv8のセグメンテーションモデルをロード
model = YOLO(model="yolov8n-seg.pt")

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
    # 画像を読み込む
    img = cv2.imread('testapp/static/up/' + filename)
    # 画像の加工を行う（ここではYOLOv8でセグメンテーションを行う）
    result = model.predict(source='testapp/static/up/' + filename, save=True, project='testapp/static/', name="down") # projectとnameで保存先を指定
    # 加工後の画像のファイル名を取得（保存先はtestapp/static/up/）
    #processed_filename = result[0]['save_path'].split('/')[-1]
    # 加工後の画像を保存
    #cv2.imwrite('testapp/static/up/processed_' + filename, model.predict(img))
    # 加工後の画像のファイル名を取得（保存先はtestapp/static/up/）
    # processed_filename = result[0]['save_path'].split('/')[-1]
    # processed.htmlを表示し、加工前と加工後の画像を表示
    return render_template('htmls/processed.html', original=filename, processed=filename)
    #return render_template('htmls/processed.html', original=filename, processed='processed_' + filename)
    #return render_template('htmls/processed.html', original=filename, processed=processed_filename)
