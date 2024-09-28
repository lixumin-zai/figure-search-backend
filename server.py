import requests
import base64
import aiohttp
import json

async def fetch(session, url, data):
    # 使用 POST 方法发送请求
    async with session.post(url, data=json.dumps(data), headers={'Content-Type': 'application/json'}) as response:
        # 等待响应并返回结果
        if response.status == 200:
            # 等待响应并返回 JSON 数据
            return await response.json()
        else:
            # 处理其他 HTTP 错误
            return {"error": f"HTTP Error: {response.status}"}

class Search:
    def __init__(self):
        self.url = "http://117.161.233.78:20007/search"

    async def search(self, info):
        data = {
            "image": info.image
        }
        async with aiohttp.ClientSession() as session:
            result = await fetch(session, self.url, data)

        if result.get("image"):
            return result
        else:
            return {"code":500, "msg":"error"}
