from flask import render_template, request
from flask import make_response, after_this_request
from testapp import app
import cv2
import os
import shutil
# ultralyticsのYOLOモジュールをインポート
from ultralytics import YOLO

    # YOLOv8のセグメンテーションモデルをロード
model = YOLO(model="yolov8n-seg.pt")

#画像処理を行う関数を定義
def process_image(filename):
    # 画像の加工を行う（ここではYOLOv8でセグメンテーションを行う）
    model.predict(source='testapp/static/up/' + filename, save=True, project='testapp/static/', name="down", exist_ok=True)
    # 画像ファイルのパスを返す
    return os.path.join('testapp/static/down', filename)

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
    
    # レスポンスオブジェクトを作成
    response = make_response(render_template('htmls/processed.html', original=filename, processed=filename))
    
    # 画像処理を登録
    @after_this_request
    def process_image_after(response):
        # 画像処理を実行し、ファイルパスを取得
        file_path = process_image(filename)
        # ファイルパスからファイル名だけ取り出す
        file_name = os.path.basename(file_path)
        # レスポンスオブジェクトにファイル名を追加する（任意）
        response.headers['X-Processed-File'] = file_name
        # レスポンスオブジェクトを返す
        return response
    
    # レスポンスオブジェクトを返す
    return response