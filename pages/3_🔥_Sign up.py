import streamlit as st
import requests
import json

def signup():
    st.title('Vui lòng điền thông tin để đăng kí')
    username = st.text_input('Tên đăng nhập')
    password = st.text_input('Mật khẩu')
    full_name = st.text_input('Họ và tên')
    phone = st.text_input('Số điện thoại')

    data = {
        'id': '',
        'user_name': username,
        'password': password,
        'full_name': full_name,
        'phone': phone
    }
    if st.button('Đăng kí'):
        res = requests.post('http://127.0.0.1:8000/signup', data = json.dumps(data))
        print(type(res.text))
        if res.text == '"existed"':
            st.warning('Tên đăng nhập đã tồn tại')
        elif res.text == 'false':
            st.error('Không thể tạo tài khoản. Vui lòng thử lại sau')
        elif res.text == 'true':
            st.success('Tạo tài khoản thành công.')

signup()