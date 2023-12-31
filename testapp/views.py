from flask import render_template, request, send_from_directory
from testapp import app
import cv2
import dlib
import os

detector = dlib.get_frontal_face_detector()

@app.route('/')
def index():
    return render_template('htmls/index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if not file:
        return 'ファイルがありません'
    filename = file.filename
    file.save('testapp/static/up/' + filename)
    img = cv2.imread('testapp/static/up/' + filename)
    faces = detector(img)
    option = request.form.get('option')
    if option == 'mosaic':
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            face_img = img[y1:y2, x1:x2]
            face_img = cv2.resize(face_img, (10, 10))
            face_img = cv2.resize(face_img, (x2-x1, y2-y1), interpolation=cv2.INTER_NEAREST)
            img[y1:y2, x1:x2] = face_img # この行をインデントしてfor文の外に出す
    elif option == 'blur':
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            face_img = img[y1:y2, x1:x2]
            face_img = cv2.blur(face_img, (30, 30))
            img[y1:y2, x1:x2] = face_img # この行をインデントしてfor文の外に出す
    elif option == 'stamp':
        stamp_file = request.files['stamp']
        if not stamp_file:
            return 'スタンプ用の画像がありません'
        stamp_filename = stamp_file.filename
        stamp_file.save('testapp/static/stamp/' + stamp_filename)
        stamp = cv2.imread('testapp/static/stamp/' + stamp_filename, cv2.IMREAD_UNCHANGED) # cv2.IMREAD_UNCHANGEDオプションを追加する
        for face in faces:
            x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
            face_img = img[y1:y2, x1:x2]
            stamp_resized = cv2.resize(stamp, (x2-x1, y2-y1))
            stamp_mask = stamp_resized[:, :, 3]
            stamp_mask_inv = cv2.bitwise_not(stamp_mask)
            stamp_resized = stamp_resized[:, :, :3]
            face_bg = cv2.bitwise_and(face_img, face_img, mask=stamp_mask_inv)
            face_fg = cv2.bitwise_and(stamp_resized, stamp_resized, mask=stamp_mask)
            face_img = cv2.add(face_bg, face_fg)
            img[y1:y2, x1:x2] = face_img # この行をインデントしてfor文の外に出す
    cv2.imwrite('testapp/static/down/processed_' + filename, img)
    return render_template('htmls/processed.html', original=filename, processed='processed_' + filename)

@app.route('/download/<filename>')
def download(filename):
    return send_from_directory('testapp/static/down', 'processed_' + filename, as_attachment=True)