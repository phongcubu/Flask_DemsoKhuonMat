from flask import Flask
from flask_cors import CORS, cross_origin
from flask import request

import numpy as np
import cv2
import base64

app = Flask(__name__)
# Apply Flask CORS
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def dem_so_mat(face):
    # Khởi tạo bộ phát hiện khuôn mặt
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Chuyen gray
    gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    # Phát hiện khuôn mặt trong ảnh
    faces = face_cascade.detectMultiScale(gray, 1.2, 10)

    so_mat = len(faces)

    return so_mat



#  hàm chuyển chuyển base64 sang anh
def chuyen_base64_sang_anh(anh_base64):
    try:
        anh_base64 = np.fromstring(base64.b64decode(anh_base64), dtype=np.uint8)
        anh_base64 = cv2.imdecode(anh_base64, cv2.IMREAD_ANYCOLOR)

    except:
        return None
    return anh_base64


@app.route("/phathienkhuonmat", methods=['POST'])
@cross_origin(origin='*')
def phathienkhuonmat():
    face_number = 0  # khai báo biến đếm số khuôn mặt
    # đọc ảnh từ client gửi lên
    facebase64 = request.form.get('filefacebase64')

    # chuyển base 64 về Opencv format
    face = chuyen_base64_sang_anh(facebase64)

    # Đêm số mặt trong ảnh
    face_number = dem_so_mat(face)

    return "Số Khuôn Mặt Thấy được là : " + str(face_number)


# Start Backend
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6868')

