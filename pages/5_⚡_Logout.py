import streamlit as st

st.title('🚦Bạn chắc chắn muốn đăng xuất không ?')
if st.button('Đăng xuất'):
    st.session_state['login_state'] = 'false'
    st.success('Đăng xuất thành công')