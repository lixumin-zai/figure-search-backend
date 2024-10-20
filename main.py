from fastapi import FastAPI, Query
from starlette.responses import StreamingResponse
import time
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import base64
from server import Search
from db_process import Database
from PIL import Image
import io
from datetime import datetime
import uuid
import requests

db = Database('db/test_0928.db')
search = Search()

app = FastAPI(redoc_url=None)

save_image_path = "/root/project/figure_search/public/upload"

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
        return {
            "code": "0",
            "image": "", 
            "times": -1
        }
    else:
        times = db.reduce_usage_count(upload_search_data.verification_code)
        if times < 0:
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
            db.increase_usage_count(verification_code, -5)

        return {"code":0, "verification_code": verification_code, "cost_time": cost_time}
    else:
        return {"code":1, "verification_code": "error", "cost_time": 0}

@app.get("/get_cost_time")
async def get_cost_time(verification_code: str = Query(...)):
    info = db.get_user_info_by_verification_code(verification_code)
    if info:
        return {"code":0, "cost_time": info[3]}
    else:
        return {"code":1, "cost_time": 0}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23333, ssl_keyfile="./lismin.online_other/lismin.online.key", ssl_certfile="./lismin.online_other/lismin.online_bundle.pem")

    # nohup python main.py > main.log &