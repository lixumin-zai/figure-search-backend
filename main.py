from fastapi import FastAPI, Query, Request
from starlette.responses import StreamingResponse
import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
from server import Search
from db_process import Database, RechargeCodeDB, AdViewsDB
from PIL import Image
import io
from datetime import datetime
import uuid
import requests
import  traceback
import re
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse



db = Database('db/test_0928.db')
rechargecode_db = RechargeCodeDB("db/rechargecode.db")
AdViews_db = AdViewsDB('db/test_0928.db')
search = Search()

app = FastAPI(redoc_url=None, docs_url=None)

save_image_path = "/root/project/figure_search/public/upload"

# 封禁的 IP 列表
blocked_ips = {"183.227.29.61"}

class BlockIPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 获取请求的 IP 地址
        client_ip = request.client.host
        print(client_ip)
        # 检查是否在封禁列表中
        if client_ip in blocked_ips:
            return JSONResponse(status_code=403, content={"detail": "死吗东西"})
        return await call_next(request)

# 添加中间件
app.add_middleware(BlockIPMiddleware)


def verify_code(verification_code):
    verification_info = db.get_user_info_by_verification_code(verification_code)
    if not verification_info:
        return False
    else:
        return True

# 定义请求数据的模型
class UploadSearchData(BaseModel):
    image: str
    verification_code: str

@app.post("/search-mini")
async def stream(upload_search_data:UploadSearchData):
    if not verify_code(upload_search_data.verification_code):
        print("验证失败")
        return {
            "code": "0",
            "image": "", 
            "times": -1
        }
    else:
        times = db.reduce_usage_count(upload_search_data.verification_code)
        if times < 0:
            print(f"{upload_search_data.verification_code}: 次数用完")
            return {
                "code": "0",
                "image": "", 
                "times": 0
            }
        _image = Image.open(io.BytesIO(base64.b64decode(upload_search_data.image))).convert("RGB")
        save_path = f"{save_image_path}/{upload_search_data.verification_code}|{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
        _image.save(save_path)
        print(save_path)
        result = await search.search(upload_search_data)
        result["times"] = times
        return result

# 定义请求数据的模型
class UploadFile(BaseModel):
    image: str

@app.post("/search")
async def stream(upload_file:UploadFile):
    result = await search.search(upload_file)
    return result


@app.post("/feedback")
async def feedback(upload_search_data:UploadSearchData):
    image = Image.open(io.BytesIO(base64.b64decode(upload_search_data.image))).convert("RGB")
    image.save(f"feedback/{upload_search_data.verification_code}|{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.jpg", format="JPEG")
    return {"code":0}

class LoginData(BaseModel):
    code: str

@app.get("/login")
async def get_openid(code: str = Query(...)):
    APPID = "wx2a8370452f0677e4"
    SECRET = "4f54e3e098552928014cdbbae56fdabf"
    JSCODE = code
    resp = requests.get(f"https://api.weixin.qq.com/sns/jscode2session?appid={APPID}&secret={SECRET}&js_code={JSCODE}&grant_type=authorization_code")
    open_id = resp.json().get("openid", None)

    if open_id:
        info = db.get_user_info_by_wechat_id(open_id)
        if info:
            verification_code = info[2]
            cost_time = info[3]
        else:
            verification_code = str(uuid.uuid4())
            cost_time = 10
            db.create_user(open_id, verification_code) 
            db.increase_usage_count(verification_code, -13)

        ad_view_info = AdViews_db.get_info_by_verification_code_on_today(verification_code)
        if ad_view_info:
            ad_view_count = ad_view_info[3]
        else:
            AdViews_db.create_view_info(verification_code)
            ad_view_count = 0

        return {"code":0, "verification_code": verification_code, "cost_time": cost_time, "ad_view_count": ad_view_count}
    else:
        return {"code":1, "verification_code": "error", "cost_time": 0, "ad_view_count": 0}

@app.get("/get_cost_time")
async def get_cost_time(verification_code: str = Query(...)):
    info = db.get_user_info_by_verification_code(verification_code)
    if info:
        return {"code":0, "cost_time": info[3]}
    else:
        return {"code":1, "cost_time": 0}

@app.get("/get_view_time")
async def get_cost_time(verification_code: str = Query(...)):
    ad_view_info = AdViews_db.get_info_by_verification_code_on_today(verification_code)
    if ad_view_info:
        return {"code":0, "ad_view_time": ad_view_info[3]}
    else:
        return {"code":1, "ad_view_time": 0}

@app.get("/activateCode")
async def activate_code(openidCode: str = Query(...), recharge_code: str = Query(...)):
    try:
        recharge_code_match = re.search(r'[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', recharge_code)
        if recharge_code_match:
            info = rechargecode_db.get_info_by_recharge_code(recharge_code_match[0])
            if info:
                if info[2]: # user_code
                    return {"code": 1}
                cost_time = rechargecode_db.used_code(recharge_code_match[0], openidCode)
                db.increase_usage_count(openidCode, cost_time)
                return {"code": 0}
            else:
                print(recharge_code, "错误增加码")
                return {"code": 2}
        else:
            print(recharge_code, "错误增加码")
            return {"code": 2}
            
    except:
        traceback.print_exc()
        return {"code": 2}

@app.get("/reward")
async def activate_code(verification_code: str = Query(...)):
    info = AdViews_db.get_info_by_verification_code_on_today(verification_code)
    if info[3] >= 3:
        return {"code": 1, "msg": "超过次数", "add_times":0}
    try:
        times = AdViews_db.watch_one_today(verification_code)
        try:
            print(verification_code, "添加次数：", times)
            db.increase_usage_count_by_verification_code(verification_code, times)
        except:
            return {"code": 3,  "msg": "添加次数失败", "add_times":0}
    except:
        return {"code": 2, "msg": "创建记录失败", "add_times":0}
    return {"code": 0, "add_times":times}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23333, ssl_keyfile="./lismin.online_other/lismin.online.key", ssl_certfile="./lismin.online_other/lismin.online_bundle.pem")

    # nohup python main.py > main.log &