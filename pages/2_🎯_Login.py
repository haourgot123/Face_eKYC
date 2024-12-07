import streamlit as st
import numpy as np
import requests
import cv2
import json

if 'login_state' not in st.session_state:
    st.session_state['login_state'] = 'false'


def login():
    st.title(':orange[Wellcome to Face eKYC] 🤖')
    username = st.text_input('Tên đăng nhập')
    password = st.text_input('Mật khẩu')
    data = {
        'id' : '',
        'user_name': username,
        'password': password,
        'full_name': '',
        'phone': ''
    }
    if st.button('Đăng nhập'):
        res = requests.post('http://127.0.0.1:8000/login', data = json.dumps(data))
        print(res.text)
        if res.text == 'true':
            st.success('Đăng nhập thành công')
            st.session_state['login_state'] = username
        else:
            st.warning('Sai tên đăng nhập hoặc mật khẩu')

def login_video():
    
    st.title('📷 :orange[Đăng nhập bằng khuôn mặt]')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        st.error('Không thể mở webcam. Vui lòng kiểm tra lại bằng thiết bị ❌')
    stframe = st.empty()
    try:
        while True:
            success, frame = cap.read()
            if not success:
                st.warning('Không nhận được khung hình từ Webcam')
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, _ = frame.shape
            mask = np.zeros((height, width), dtype=np.uint8)
            center = (width // 2, height // 2)
            radius = min(height, width) // 2
            cv2.circle(mask, center, radius, 255, -1)

            # Áp dụng mặt nạ hình tròn lên khung hình
            circular_frame = cv2.bitwise_and(frame, frame, mask=mask)

            # Chuyển phần nền xung quanh thành màu đen
            background = np.zeros_like(frame)
            circular_frame = np.where(mask[..., None] == 255, circular_frame, background)
            stframe.image(circular_frame, channels="RGB", caption="Webcam Video")
    except Exception as e:
        st.error(f'Có lỗi xảy ra: {e}')

    cap.release()
if st.session_state['login_state'] == 'false':
    choose = st.selectbox('Hãy chọn phương thức đăng nhâp: ', options=['None','Đăng nhập bằng tài khoản', 'Đăng nhập bằng khuôn mặt'])

    if choose == 'None':
        st.title('Trang chủ Đăng Nhập 💌')
        st.text('Bạn có thể đăng nhập bằng 2 phương thức. 🎯 Vui lòng chọn phương thức đăng nhập')
        st.text('📌 Đăng nhập bằng tài khoản và mật khẩu')
        st.text('📌 Đăng nhập bằng khuôn mặt')
    elif choose == 'Đăng nhập bằng tài khoản':
        login()
    elif choose == 'Đăng nhập bằng khuôn mặt':
        login_video()
else:
    st.title(f'Chúc mừng bạn đã đăng nhập thành công 🎉')


