import streamlit as st
import requests
from streamlit_camera import camera
import io
import base64
import time
from PIL import Image
from exception import UserAlreadyExistsError
from db_process import Database
from streamlit.components.v1 import html

db = Database('db/test_0928.db')

# st.sidebar.image("https://picsum.photos/200")
# with st.container():
#     st.text("This is paragraph :)")
#     html("""
#     <script>
#         // Locate elements
#         var decoration = window.parent.document.querySelectorAll('[data-testid="stDecoration"]')[0];
#         var sidebar = window.parent.document.querySelectorAll('[data-testid="stSidebar"]')[0];
#         // Observe sidebar size
#         function outputsize() {
#             decoration.style.left = `${sidebar.offsetWidth}px`;
#         }
#         new ResizeObserver(outputsize).observe(sidebar);
#         // Adjust sizes
#         outputsize();
#         decoration.style.height = "3.0rem";
#         decoration.style.right = "45px";
#         // Adjust text decorations
#         decoration.innerText = "Welcome, Streamlit App!"; // Replace with your desired text
#         decoration.style.fontWeight = "bold";
#         decoration.style.display = "flex";
#         decoration.style.justifyContent = "center";
#         decoration.style.alignItems = "center";
#     </script>
#     """, width=0, height=0)

URL = "http://117.161.233.78:20007/search"
st.set_page_config(
    page_title="图推搜索",  # 设置页面标题
    page_icon="🔍",  # 设置页面图标
    layout="wide",  # 可以选择"centered" 或 "wide"
    menu_items={
        'About': "[请添加飞书联系托马斯羊](https://www.feishu.cn/invitation/page/add_contact/?token=910q4204-4b5f-43a0-acd6-66cce399e2a3&amp;unique_id=wMk5MKmubTeopGkKkxsglg==)"
    }
)

st.markdown(
    """
    <style>
    .stApp {
        margin-top: -50px;
        padding: 0;
        height: 100vh; /* 使用视口高度 */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.session_state.remaining_times = 0
# 定义按钮点击时的回调函数
if 'is_restart' not in st.session_state:
    st.session_state.is_restart = 0

def button_click():
    st.session_state.is_restart = 1 - st.session_state.is_restart

@st.dialog("搜索结果")
def show_result(image, cost_time):
    st.write(f"花费时间:{cost_time:03f}s  剩余次数:{st.session_state.remaining_times}次")
    st.image(image, width=300)
    # if st.button("重新拍摄", on_click=button_click):
    #     st.rerun()

@st.dialog("搜索结果")
def show_verify_error(verification_code):
    st.write(f"测试码 {verification_code} 无效")
    st.markdown("[请添加飞书联系托马斯羊](https://www.feishu.cn/invitation/page/add_contact/?token=910q4204-4b5f-43a0-acd6-66cce399e2a3&amp;unique_id=wMk5MKmubTeopGkKkxsglg==)")
    # if st.button("重新拍摄", on_click=button_click):
    #     st.rerun()

def post_test(image_base64):
    st = time.time()
    data = {
        "image": image_base64
    }
    resp = requests.post(URL, json=data)
    result = resp.json()
    reasult_image = io.BytesIO(base64.b64decode(result["image"]))

    # test
    # reasult_image = io.BytesIO(base64.b64decode(image_base64))

    return reasult_image, time.time()-st

def verify_code(verification_code):
    verification_info = db.get_user_info_by_verification_code(verification_code)
    if not verification_info:
        return False
    else:
        st.session_state.remaining_times = db.reduce_usage_count(verification_code)
        return True

if "show_result" not in st.session_state and "show_verify_error" not in st.session_state:
    image_base64, verification_code = camera(st.session_state.is_restart)
        
    if not verify_code(verification_code):
        if verification_code != " ":
            show_verify_error(verification_code)
    
    else:
        if len(image_base64)>728604:
            image = Image.open(io.BytesIO(base64.b64decode(image_base64))).convert("RGB")
            image.thumbnail((1024, 1024))
            image_bytes = io.BytesIO()
            image.save(image_bytes, format="JPEG")
            image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

        if image_base64:
            image, cost_time = post_test(image_base64)
            image = Image.open(image).convert("RGB")
            show_result(image, cost_time)



# streamlit run show.py

# docker run --network host --name nginx -v /root/software/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /root/software/nginx/conf/conf.d:/etc/nginx/conf.d -v /root/software/nginx/log:/var/log/nginx -v /root/software/nginx/html:/usr/share/nginx/html -d nginx:latest