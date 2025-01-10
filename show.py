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
from datetime import datetime

db = Database('db/test_0928.db')
save_image_path = "/root/project/figure_search/public/upload"


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
    remaining_times = db.reduce_usage_count(verification_code)
    st.markdown(f"**花费时间**:{cost_time:03f}s <br> **剩余次数**:{remaining_times}次", unsafe_allow_html=True)
    st.image(image, width=300)
    # if st.button("重新拍摄", on_click=button_click):
    #     st.rerun()

@st.dialog("搜索结果")
def show_verify_error(verification_code):
    st.write(f"测试码 {verification_code} 无效")
    # st.markdown('<a href="https://t.asczwa.com/taobao?backurl=http://e.tb.cn/h.gGTzWKTFDEO0h4D?tk=gSBI39rUfcz">淘宝</a>')
    st.markdown(r"[由于网站服务器需要维护成本，点击链接自行获取次数](tbopen://m.taobao.com/tbopen/index.html?h5Url=https%3A%2F%2Fh5.m.taobao.com%2Fawp%2Fcore%2Fdetail.htm%3Fapp%3Dchrome%26bxsign%3DscdERnWrms5xgjQzxQqSuuk8no9QGSwt04PvxC-aYh7WvlIz2WDYV85O8XIq82--l1ypaKrgvjnKWtVAaZlgIujkJnST7UIqBq17jV2FIZtlz77570YZdnnZKZQW78EuJ3l%26cpp%3D1%26id%3D841635593499%26price%3D1.99-9.99%26shareUniqueId%3D28600432477%26share_crt_v%3D1%26shareurl%3Dtrue%26short_name%3Dh.gGTzWKTFDEO0h4D%26sourceType%3Ditem%26sp_tk%3DZ1NCSTM5clVmY3o%253D%26spm%3Da2159r.13376460.0.0%26suid%3D003222DE-B2F8-47EC-9ED4-8D5CC01B426E%26tbSocialPopKey%3DshareItem%26un%3D45edcc4dc454c683ad12898721723d67%26un_site%3D0%26ut_sk%3D1.Yh28oag34f8DAOG4GHBDxsuB_21380790_1728311116271.systemSharePanel.1%26wxsign%3DtbwcbXt3qMeTnxvC7ozrjmhIGbwI4_jckhjg_8S8yRPVsJ-HukSPp9ghSsoeDlc3uEJNeJZhkYzJINAMJJo56kEil0PqAB06myg0-AqOG8BycntLJQNqPimRCTWnT6bk4Vz%26slk_gid%3Dgid_er_normal%257Cgid_er_af_pop%257Cgid_er_sidebar_0&action=ali.open.nav&module=h5&bootImage=0&slk_sid=ylV1H8srnVICAQHLYKqS0RrQ_1728312005122&slk_t=1728312005669&slk_gid=gid_er_normal%7Cgid_er_af_pop%7Cgid_er_sidebar_0&afcPromotionOpen=false&bc_fl_src=h5_huanduan&source=slk_dp)")
    # if st.button("重新拍摄", on_click=button_click):
    #     st.rerun()

def post_test(image_base64):
    st = time.time()
    data = {
        "image": image_base64
    }
    resp = requests.post(URL, json=data)
    result = resp.json()
    reasult_image = io.BytesIO(base64.b64decode(result["image"][0]))

    # test
    # reasult_image = io.BytesIO(base64.b64decode(image_base64))

    return reasult_image, time.time()-st

def verify_code(verification_code):
    verification_info = db.get_user_info_by_verification_code(verification_code)
    if not verification_info:
        return False
    else:
        st.session_state.remaining_times = verification_info[3]
        print(st.session_state.remaining_times)
        return True

if "show_result" not in st.session_state and "show_verify_error" not in st.session_state:
    image_base64, verification_code = camera(st.session_state.is_restart)
    # st.markdown(r"[由于网站服务器需要维护成本，点击链接自行获取次数](tbopen://m.taobao.com/tbopen/index.html?h5Url=https%3A%2F%2Fh5.m.taobao.com%2Fawp%2Fcore%2Fdetail.htm%3Fapp%3Dchrome%26bxsign%3DscdERnWrms5xgjQzxQqSuuk8no9QGSwt04PvxC-aYh7WvlIz2WDYV85O8XIq82--l1ypaKrgvjnKWtVAaZlgIujkJnST7UIqBq17jV2FIZtlz77570YZdnnZKZQW78EuJ3l%26cpp%3D1%26id%3D841635593499%26price%3D1.99-9.99%26shareUniqueId%3D28600432477%26share_crt_v%3D1%26shareurl%3Dtrue%26short_name%3Dh.gGTzWKTFDEO0h4D%26sourceType%3Ditem%26sp_tk%3DZ1NCSTM5clVmY3o%253D%26spm%3Da2159r.13376460.0.0%26suid%3D003222DE-B2F8-47EC-9ED4-8D5CC01B426E%26tbSocialPopKey%3DshareItem%26un%3D45edcc4dc454c683ad12898721723d67%26un_site%3D0%26ut_sk%3D1.Yh28oag34f8DAOG4GHBDxsuB_21380790_1728311116271.systemSharePanel.1%26wxsign%3DtbwcbXt3qMeTnxvC7ozrjmhIGbwI4_jckhjg_8S8yRPVsJ-HukSPp9ghSsoeDlc3uEJNeJZhkYzJINAMJJo56kEil0PqAB06myg0-AqOG8BycntLJQNqPimRCTWnT6bk4Vz%26slk_gid%3Dgid_er_normal%257Cgid_er_af_pop%257Cgid_er_sidebar_0&action=ali.open.nav&module=h5&bootImage=0&slk_sid=ylV1H8srnVICAQHLYKqS0RrQ_1728312005122&slk_t=1728312005669&slk_gid=gid_er_normal%7Cgid_er_af_pop%7Cgid_er_sidebar_0&afcPromotionOpen=false&bc_fl_src=h5_huanduan&source=slk_dp)")

    if not verify_code(verification_code):
        if verification_code != " ":
            show_verify_error(verification_code)
    
    else:
        if st.session_state.remaining_times > 0:
            if len(image_base64)>728604:
                image = Image.open(io.BytesIO(base64.b64decode(image_base64))).convert("RGB")
                image.thumbnail((1024, 1024))
                image_bytes = io.BytesIO()
                image.save(image_bytes, format="JPEG")
                image_base64 = base64.b64encode(image_bytes.getvalue()).decode("utf-8")

            if image_base64:
                _image = Image.open(io.BytesIO(base64.b64decode(image_base64))).convert("RGB")
                save_path = f"{save_image_path}/{verification_code}|{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                _image.save(save_path)
                print(save_path)
                image, cost_time = post_test(image_base64)
                image = Image.open(image).convert("RGB")
                show_result(image, cost_time)
        else:
            show_verify_error(verification_code)

# st.markdown("""
# <div style='display: flex;
#     justify-content: center; 
#     align-items: center;   
#     '>
#     <a 
#         href='https://beian.miit.gov.cn/' 
#         target='_blank' 
#         style='
#             color: #666666;
#             text-decoration: none;
#             display: inline-flex;
#             align-items: center;
#             transition: color 0.3s ease;
#             width: fit-content; /* 或指定一个固定宽度 */
#             margin: 0 auto;
#             '>
#         京ICP备2024089598号-2
#         </a><div>""", unsafe_allow_html=True)


# nohup streamlit run show.py > show.log &

# docker run --network host --name nginx -v /root/software/nginx/conf/nginx.conf:/etc/nginx/nginx.conf -v /root/software/nginx/conf/conf.d:/etc/nginx/conf.d -v /root/software/nginx/log:/var/log/nginx -v /root/software/nginx/html:/usr/share/nginx/html -d nginx:latest

