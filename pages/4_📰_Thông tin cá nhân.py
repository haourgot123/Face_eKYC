import streamlit as st
import requests
import json



if 'login_state' not in st.session_state:
    st.session_state['login_state'] = 'false'

if st.session_state['login_state']  != 'false':
    username = st.session_state['login_state']
    res = requests.get(f'http://127.0.0.1:8000/cards/{username}')
    print(res.json())
    infor = res.json()
    so_cccd = infor['so_cccd']
    ho_ten = infor['ho_ten']
    ngay_sinh = infor['ngay_sinh']
    gioi_tinh = infor['gioi_tinh']
    quoc_tich = infor['quoc_tich']
    que_quan = infor['que_quan']
    thuong_tru = infor['thuong_tru']
    st.title(f'🎈Xin chào {ho_ten}')
    with st.expander('Xem thông tin cá nhân'):
        st.write(f'⚡Họ và tên:   {ho_ten}')
        st.write(f'⚡Số CCCD:     {so_cccd}')
        st.write(f'⚡Ngày sinh:   {ngay_sinh}')
        st.write(f'⚡Giới tính:   {gioi_tinh}')
        st.write(f'⚡Quốc tịch:   {quoc_tich}')
        st.write(f'⚡Quê Quán:    {que_quan}')
        st.write(f'⚡Thường trú:  {thuong_tru}')

    

else:
    st.title('🔥 Ban vui lòng đăng nhập trước khi xem thông tin cá nhân')
    st.text('Trong phần thông tin cá nhân, nếu bạn muốn xem các thông tin trên căn cước công dân, bạn có thể thực hiện việc này thông qua một hộp thoại hoặc giao diện người dùng trong ứng dụng. Các thông tin trên căn cước công dân thường bao gồm họ và tên, ngày tháng năm sinh, giới tính, địa chỉ, số chứng minh thư hoặc số căn cước, và ngày cấp. Các thông tin này được trích xuất từ ảnh căn cước công dân của bạn.')