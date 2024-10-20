import time
import requests
import json
from db_process import Database
import traceback

# https://pcnqlkzb5ai3.feishu.cn/base/KQvib0tHdakoOts4BzpcAMzSnPg?table=tbl18pkdZSZwSznM&view=vewhGxAd7b
db = Database('db/test_0928.db')


def filter_record(resp_data):
    for item in resp_data["data"]["items"]:
        record_id = item["record_id"]
        name = item["fields"]["姓名"][0]["text"]
        print(name, record_id)
        if name == "oneworkonewife":
            continue
        try:
            db.create_user(name, name)
            updata_record(record_id)
        except:
            traceback.print_exc()
            continue

def updata_record(record_id):
    access_token = get_access_token()
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/KQvib0tHdakoOts4BzpcAMzSnPg/tables/tbl18pkdZSZwSznM/records/{record_id}"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "fields": {
            "状态": "true"
        }
    }
    response = requests.put(url, headers=headers, json=data)
    if response.status_code == 200:
        print("添加成功")

def process():
    access_token = get_access_token()
    url = 'https://open.feishu.cn/open-apis/bitable/v1/apps/KQvib0tHdakoOts4BzpcAMzSnPg/tables/tbl18pkdZSZwSznM/records/search'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "view_id": "vewhGxAd7b",
        "field_names": [
            "姓名"
        ],
        "filter": {
            "conjunction": "and",
            "conditions": [
            {
                "field_name": "状态",
                "operator": "isEmpty",
                "value": []
            }
            ]
        },
        "automatic_fields": False
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    filter_record(response.json())
    print("执行函数!")

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

if __name__ == "__main__":
    # 每10秒执行一次
    while True:
        print("******************")
        print("开始执行")
        process()
        print("执行结束")
        print("******************")
        time.sleep(20)  # 等待10秒

    
