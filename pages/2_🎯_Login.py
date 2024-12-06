import streamlit as st
import requests
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
            st.session_state['login_state'] = 'true'
        else:
            st.warning('Sai tên đăng nhập hoặc mật khẩu')

login()


