import requests
from pydantic import BaseModel
from typing import List, Optional
from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from typing import List, Optional
from db_process import Database
import uuid
import traceback
app = FastAPI()
db = Database('db/test_0928.db')

def get_access_token():
    # 获取 _access_token
    tenant_token_api = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
    resp = requests.post(
        tenant_token_api, json={
            "app_id": "cli_a621015572aa100c", "app_secret": "iYdkBItcLDdwD90ihVGO5gxjDDpURX3b"
        },
    )
    access_token = resp.json()["tenant_access_token"]
    return access_token

# 定义删除请求的数据模型
class RecordData(BaseModel):
    wechat_id: str
    
# 定义删除记录的路由，使用POST方法
@app.post("/get-code")
async def create_code(record_data: RecordData):
    wechat_id = record_data.wechat_id
    verification_code = str(uuid.uuid4())
    try:
        db.create_user(wechat_id, verification_code)
    except:
        traceback.print_exc()
        verification_code = "1"
    return {"verification_code": verification_code}


# 定义删除请求的数据模型
class CreateData(BaseModel):
    wechat_id: str
    verification_code: str

@app.post("/create-code")
async def create_code(create_data: CreateData):
    wechat_id, verification_code = create_data.wechat_id, create_data.verification_code
    try:
        db.create_user(wechat_id, verification_code)
        status = "true"
    except:
        traceback.print_exc()
        verification_code = "1"
        status = "false"
    return {"status": status}

# 启动FastAPI应用程序
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=23335)

# def create_code(record_data: RecordData):
#     
#     print(wechat_id, create_time)
#     access_token = get_access_token()
#     # https://er063rlq1d.feishu.cn/base/HtywbDgPfaMTWBspXbDcBuTinCb?table=tblbDxj78wOKXrSf&view=vewQx72054
#     app_id = "HtywbDgPfaMTWBspXbDcBuTinCb"
#     app_token = "tblbDxj78wOKXrSf"

#     url = f'https://open.feishu.cn/open-apis/bitable/v1/apps/{app_id}/tables/{app_token}/records/search'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {access_token}'
#     }
#     data = {
#         "view_id": "vewQx72054",
#         "field_names": ["姓名"]
#     }
#     response = requests.post(url, headers=headers, json=data)
#     data = response.json()
#     print(data)


