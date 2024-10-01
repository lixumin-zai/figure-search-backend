from fastapi import FastAPI
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

db = Database('db/test_0928.db')
search = Search()

app = FastAPI()

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23333, ssl_keyfile="./lismin.online_other/lismin.online.key", ssl_certfile="./lismin.online_other/lismin.online_bundle.pem")

    # nohup python main.py > main.log &