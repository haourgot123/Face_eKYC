import streamlit as st
from PIL import Image
if 'login_state' not in st.session_state:
    st.session_state['login_state'] = 'false'
st.set_page_config(
    page_title = 'Face eKYC',
    page_icon = "🔥",
)

st.title("🚀 Ứng dụng xác thực khuôn mặt kèm căn cước công dân")
st.subheader('🔥 Mô tả ứng dụng')
st.text('''Ứng dụng bao gồm các mô-đun quan trọng, trong đó nổi bật là mô-đun nhận diện khuôn mặt, giúp xác thực danh tính người dùng thông qua dữ liệu từ căn cước công dân (CCCD). Để đảm bảo tính bảo mật và ngăn chặn các hành vi giả mạo, ứng dụng tích hợp kỹ thuật Liveness Detection với phương pháp challenge-response, yêu cầu người dùng thực hiện các thao tác xác minh động để chứng minh sự hiện diện thực tế. Bên cạnh đó, hệ thống cũng hỗ trợ trích xuất thông tin tự động từ CCCD, giúp tối ưu hóa quá trình xử lý dữ liệu và nâng cao trải nghiệm người dùng.
        ''')
image = Image.open('logo.png')
st.image(image)
# st.sidebar.success("Sellect Page")
